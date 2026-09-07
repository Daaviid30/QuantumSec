from dataclasses import replace

import pytest
from cryptography.exceptions import InvalidTag

from core.rng import SeededRNG
from data_protection import DataPlaneDirection
from orchestration import (
    QKDProfile,
    SessionConfig,
    SessionExecutionContext,
    SessionProfile,
    SessionStatus,
    open_data_plane,
    run_session,
)
from orchestration.authentication import (
    MLDSAAuthenticationContext,
    WegmanCarterAuthenticationContext,
)
from pqc import MLDSAIdentity, PQCFinishedMessage, PQCParty, TrustedIdentityStore
from qkd.channel import IdentityChannel
from qkd.protocols import BB84Protocol


def _parties() -> tuple[PQCParty, PQCParty]:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    bob.trust_peer(alice.public_identity)
    return alice, bob


def _establish(profile: SessionProfile, *, seed: int = 901):
    alice, bob = _parties()
    if profile in (SessionProfile.HYBRID, SessionProfile.HYBRID_DIVERSE):
        return run_session(
            SessionConfig(
                profile,
                qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
                qkd_signal_count=512,
            ),
            SessionExecutionContext(
                qkd_protocol=BB84Protocol(IdentityChannel(), SeededRNG(seed)),
                pqc_initiator=alice,
                pqc_responder=bob,
            ),
        )
    return run_session(
        SessionConfig(profile),
        SessionExecutionContext(pqc_initiator=alice, pqc_responder=bob),
    )


@pytest.mark.parametrize(
    "profile",
    [
        SessionProfile.PQC_BASE,
        SessionProfile.PQC_DIVERSE,
        SessionProfile.HYBRID,
        SessionProfile.HYBRID_DIVERSE,
    ],
)
def test_all_256_bit_session_key_profiles_open_data_plane(profile: SessionProfile) -> None:
    result = _establish(profile)
    assert result.status is SessionStatus.ESTABLISHED
    metadata_before = result.to_public_dict()
    with open_data_plane(result) as protected:
        record = protected.encrypt(
            b"profile payload",
            direction=DataPlaneDirection.ALICE_TO_BOB,
        )
        assert protected.decrypt(record) == b"profile payload"
    assert result.is_closed
    with pytest.raises(RuntimeError, match="closed"):
        result.export_session_key()
    assert result.to_public_dict() == metadata_before


def test_end_to_end_protected_hybrid_session() -> None:
    result = _establish(SessionProfile.HYBRID, seed=902)
    with open_data_plane(result) as protected:
        plaintext = b"QuantumSec protected application payload"
        aad = b"quantumsec/application/v1/message-1"
        record = protected.encrypt(
            plaintext,
            direction=DataPlaneDirection.ALICE_TO_BOB,
            aad=aad,
        )
        assert protected.decrypt(record, aad=aad) == plaintext

        tampered_ciphertext = replace(
            record,
            ciphertext=bytes((record.ciphertext[0] ^ 1,)) + record.ciphertext[1:],
        )
        tampered_tag = replace(
            record,
            tag=bytes((record.tag[0] ^ 1,)) + record.tag[1:],
        )
        with pytest.raises(InvalidTag):
            protected.decrypt(tampered_ciphertext, aad=aad)
        with pytest.raises(InvalidTag):
            protected.decrypt(tampered_tag, aad=aad)
        with pytest.raises(InvalidTag):
            protected.decrypt(record, aad=b"quantumsec/application/v1/message-2")


def _qkd_authentication(profile: QKDProfile):
    if profile is QKDProfile.QKD_ASSUMED:
        return None
    if profile is QKDProfile.QKD_CLASSICAL_AUTH:
        return WegmanCarterAuthenticationContext.from_shared_secrets(
            alice_to_bob_secret=b"a" * 65_536,
            bob_to_alice_secret=b"b" * 65_536,
        )
    alice = MLDSAIdentity.generate("qkd-alice")
    bob = MLDSAIdentity.generate("qkd-bob")
    alice_trust = TrustedIdentityStore()
    bob_trust = TrustedIdentityStore()
    alice_trust.trust(bob.public_identity)
    bob_trust.trust(alice.public_identity)
    return MLDSAAuthenticationContext(alice, bob, alice_trust, bob_trust)


@pytest.mark.parametrize(
    ("profile", "qkd_profile"),
    [
        (SessionProfile.QKD_ASSUMED, QKDProfile.QKD_ASSUMED),
        (SessionProfile.QKD_CLASSICAL_AUTH, QKDProfile.QKD_CLASSICAL_AUTH),
        (SessionProfile.QKD_PQC_AUTH, QKDProfile.QKD_PQC_AUTH),
    ],
)
def test_qkd_only_profiles_require_an_explicit_application_key_schedule(
    profile: SessionProfile,
    qkd_profile: QKDProfile,
) -> None:
    result = run_session(
        SessionConfig(profile, qkd_signal_count=512),
        SessionExecutionContext(
            qkd_protocol=BB84Protocol(IdentityChannel(), SeededRNG(903)),
            qkd_authentication=_qkd_authentication(qkd_profile),
        ),
    )
    assert result.status is SessionStatus.ESTABLISHED
    with pytest.raises(ValueError, match="QKD_BITSTRING.*application-key schedule"):
        open_data_plane(result)
    assert not result.is_closed
    result.close()


def test_aborted_session_cannot_open_data_plane() -> None:
    alice, bob = _parties()

    def tamper(message: PQCFinishedMessage) -> PQCFinishedMessage:
        return replace(
            message,
            verify_data=bytes((message.verify_data[0] ^ 1,)) + message.verify_data[1:],
        )

    result = run_session(
        SessionConfig(SessionProfile.PQC_BASE),
        SessionExecutionContext(
            pqc_initiator=alice,
            pqc_responder=bob,
            pqc_finished_transport_hook=tamper,
        ),
    )
    assert result.status is SessionStatus.ABORTED
    with pytest.raises(RuntimeError, match="established session"):
        open_data_plane(result)
