import json
from dataclasses import replace

import pytest

from core.rng import SeededRNG
from orchestration import (
    CapabilityStatus,
    QKDProfile,
    SessionConfig,
    SessionExecutionContext,
    SessionProfile,
    SessionStatus,
    run_session,
    session_capabilities,
)
from orchestration.authentication import (
    MLDSAAuthenticationContext,
    WegmanCarterAuthenticationContext,
)
from pqc import (
    MLDSAIdentity,
    PQCFinishedMessage,
    PQCParty,
    PQCSessionKeyDeriver,
    TrustedIdentityStore,
)
from pqc.errors import BackendOperationError
from qkd.channel import IdentityChannel
from qkd.protocols import BB84Protocol


def _parties() -> tuple[PQCParty, PQCParty]:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    bob.trust_peer(alice.public_identity)
    return alice, bob


def _qkd_context(
    profile: QKDProfile,
) -> MLDSAAuthenticationContext | WegmanCarterAuthenticationContext | None:
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


def test_all_seven_public_capabilities_are_current_and_stably_ordered() -> None:
    capabilities = session_capabilities()
    assert tuple(item.profile for item in capabilities) == tuple(SessionProfile)
    assert len(capabilities) == 7
    assert all(item.status is CapabilityStatus.CURRENT for item in capabilities)
    assert all(item.authentication_policy for item in capabilities)
    assert all(item.supported and json.dumps(item.to_public_dict()) for item in capabilities)


def test_session_config_normalizes_internal_profiles_and_rejects_mixed_options() -> None:
    pqc = SessionConfig(SessionProfile.PQC_BASE)
    assert pqc.internal_pqc_profile is not None
    with pytest.raises(ValueError, match="explicit qkd_authentication_profile"):
        SessionConfig(SessionProfile.HYBRID, qkd_signal_count=512)
    with pytest.raises(ValueError, match="PQC-only"):
        SessionConfig(SessionProfile.PQC_BASE, qkd_signal_count=512)
    assert json.dumps(pqc.to_public_dict())


@pytest.mark.parametrize(
    ("session_profile", "qkd_profile"),
    [
        (SessionProfile.QKD_ASSUMED, QKDProfile.QKD_ASSUMED),
        (SessionProfile.QKD_CLASSICAL_AUTH, QKDProfile.QKD_CLASSICAL_AUTH),
        (SessionProfile.QKD_PQC_AUTH, QKDProfile.QKD_PQC_AUTH),
    ],
)
def test_common_runner_executes_all_qkd_profiles(session_profile, qkd_profile) -> None:
    result = run_session(
        SessionConfig(session_profile, qkd_signal_count=512),
        SessionExecutionContext(
            qkd_protocol=BB84Protocol(IdentityChannel(), SeededRNG(812)),
            qkd_authentication=_qkd_context(qkd_profile),
        ),
    )
    assert result.status is SessionStatus.ESTABLISHED
    assert result.established_key_bits > 0
    exported = result.export_session_key()
    assert len(exported) == (result.established_key_bits + 7) // 8
    assert result.metrics.qkd is not None
    assert result.metrics.pqc is None
    public_json = json.dumps(result.to_public_dict())
    assert exported.hex() not in repr(result)
    assert exported.hex() not in public_json
    result.close()
    with pytest.raises(RuntimeError, match="closed"):
        result.export_session_key()


def test_session_result_context_manager_closes_established_key() -> None:
    result = run_session(
        SessionConfig(SessionProfile.QKD_ASSUMED, qkd_signal_count=512),
        SessionExecutionContext(
            qkd_protocol=BB84Protocol(IdentityChannel(), SeededRNG(813)),
        ),
    )
    assert not result.is_closed
    with result as managed:
        assert managed.export_session_key()
    assert result.is_closed
    with pytest.raises(RuntimeError, match="closed"):
        result.export_session_key()


@pytest.mark.parametrize("profile", [SessionProfile.PQC_BASE, SessionProfile.PQC_DIVERSE])
def test_common_runner_executes_both_pqc_profiles(profile: SessionProfile) -> None:
    alice, bob = _parties()
    result = run_session(
        SessionConfig(profile),
        SessionExecutionContext(pqc_initiator=alice, pqc_responder=bob),
    )
    assert result.status is SessionStatus.ESTABLISHED
    assert len(result.export_session_key()) == 32
    assert result.metrics.qkd is None
    assert result.metrics.pqc is not None
    assert result.metrics.pqc_authentication is not None
    assert result.metrics.pqc_authentication.verified
    assert [event.sequence for event in result.trace.events] == list(range(len(result.trace.events)))
    result.close()


def test_pqc_finished_failure_withholds_the_key() -> None:
    alice, bob = _parties()

    def tamper(message: PQCFinishedMessage) -> PQCFinishedMessage:
        changed = bytes((message.verify_data[0] ^ 1,)) + message.verify_data[1:]
        return replace(message, verify_data=changed)

    result = run_session(
        SessionConfig(SessionProfile.PQC_BASE),
        SessionExecutionContext(
            pqc_initiator=alice,
            pqc_responder=bob,
            pqc_finished_transport_hook=tamper,
        ),
    )
    assert result.status is SessionStatus.ABORTED
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()


def test_pqc_operational_failure_returns_failed_result(monkeypatch) -> None:
    alice, bob = _parties()

    def fail_derivation(*_args, **_kwargs):
        raise BackendOperationError("injected key-schedule failure")

    monkeypatch.setattr(PQCSessionKeyDeriver, "derive_initiator", fail_derivation)
    result = run_session(
        SessionConfig(SessionProfile.PQC_BASE),
        SessionExecutionContext(pqc_initiator=alice, pqc_responder=bob),
    )
    assert result.status is SessionStatus.FAILED
    assert "Operational execution failure" in (result.abort_reason or "")
    assert result.authentication.pqc_exchange is not None
    assert result.authentication.pqc_exchange.verified is True
    assert dict(result.public_context)["pqc_transcript_hash_sha384"]
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()
