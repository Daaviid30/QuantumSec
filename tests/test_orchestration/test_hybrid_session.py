from dataclasses import replace

import pytest

from core.rng import SeededRNG
from orchestration import (
    QKDProfile,
    SessionConfig,
    SessionExecutionContext,
    SessionProfile,
    SessionStatus,
    run_session,
)
from orchestration.authentication import WegmanCarterAuthenticationContext
from orchestration.hybrid.encoding import HYBRID_SECRET_INPUT_DOMAIN
from orchestration.hybrid.finished import HybridFinishedMessage
from orchestration.hybrid.key_schedule import (
    HYBRID_CONFIRMATION_KEY_DOMAIN,
    HYBRID_SESSION_KEY_DOMAIN,
)
from pqc import ClientKeyExchangeProcessor, PQCParty, SignedServerKeyOffer
from pqc.errors import BackendOperationError
from qkd.channel import ChannelPipeline, IdentityChannel, InterceptResendAttack
from qkd.protocols import BB84Protocol


def _context(seed: int = 41) -> SessionExecutionContext:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    bob.trust_peer(alice.public_identity)
    return SessionExecutionContext(
        qkd_protocol=BB84Protocol(IdentityChannel(), SeededRNG(seed)),
        pqc_initiator=alice,
        pqc_responder=bob,
    )


@pytest.mark.parametrize(
    ("profile", "component_count"),
    [(SessionProfile.HYBRID, 2), (SessionProfile.HYBRID_DIVERSE, 3)],
)
def test_hybrid_profiles_establish_a_confirmed_256_bit_key(profile, component_count) -> None:
    result = run_session(
        SessionConfig(
            profile,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        _context(),
    )
    assert result.status is SessionStatus.ESTABLISHED
    assert len(result.export_session_key()) == 32
    assert len(result.provenance) == component_count
    assert result.provenance[0].source == "qkd"
    assert [item.algorithm for item in result.provenance][1] == "ML-KEM-768"
    assert result.metrics.hybrid is not None
    assert result.metrics.hybrid.component_count == component_count
    assert result.metrics.qkd is not None and result.metrics.pqc is not None
    assert dict(result.public_context)["hybrid_context_hash_sha384"]
    result.close()


def test_role_local_component_mismatch_fails_hybrid_finished_and_withholds_key() -> None:
    context = _context()

    def mismatch(role: str, values: tuple[tuple[str, bytes], ...]):
        if role != "responder":
            return values
        algorithm, secret = values[0]
        changed = bytes((secret[0] ^ 1,)) + secret[1:]
        return ((algorithm, changed),) + values[1:]

    context.hybrid_contribution_hook = mismatch
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert "Finished verification failed" in (result.abort_reason or "")
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()


def test_tampered_hybrid_finished_aborts() -> None:
    context = _context()

    def tamper(message: object) -> object:
        assert isinstance(message, HybridFinishedMessage)
        changed = bytes((message.verify_data[0] ^ 1,)) + message.verify_data[1:]
        return replace(message, verify_data=changed)

    context.hybrid_finished_transport_hook = tamper
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert result.metrics.hybrid is not None
    assert result.metrics.hybrid.hkdf_session_time_ns >= 0
    assert result.metrics.hybrid.finished_responder_bytes > 0
    public_context = dict(result.public_context)
    assert public_context["hybrid_context_hash_sha384"]
    assert public_context["qkd_transcript_hash_sha384"]
    assert public_context["pqc_transcript_hash_sha384"]
    with pytest.raises(RuntimeError):
        result.export_session_key()


def test_hybrid_operational_failure_returns_failed_result(monkeypatch) -> None:
    def fail_finished(*_args, **_kwargs):
        raise BackendOperationError("injected Finished backend failure")

    monkeypatch.setattr("orchestration.hybrid.runner.create_finished", fail_finished)
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        _context(),
    )
    assert result.status is SessionStatus.FAILED
    assert result.metrics.hybrid is not None
    assert dict(result.public_context)["hybrid_context_hash_sha384"]
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()


def test_hybrid_domains_are_explicit_and_purpose_separated() -> None:
    assert HYBRID_SECRET_INPUT_DOMAIN == b"QuantumSec/HybridSession/v1/SecretInput"
    assert HYBRID_SESSION_KEY_DOMAIN != HYBRID_CONFIRMATION_KEY_DOMAIN


def test_intercept_resend_qkd_abort_prevents_hybrid_establishment() -> None:
    context = _context(seed=44)
    context.qkd_protocol = BB84Protocol(
        ChannelPipeline((InterceptResendAttack(1.0, SeededRNG(1_000_044)),)),
        SeededRNG(44),
    )
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=12_000,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert result.metrics.hybrid is None
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()


def test_qkd_authentication_failure_prevents_hybrid_establishment() -> None:
    context = _context()
    context.qkd_authentication = WegmanCarterAuthenticationContext.from_shared_secrets(
        alice_to_bob_secret=b"a" * 65_536,
        bob_to_alice_secret=b"b" * 65_536,
    )

    def tamper(frame, evidence):
        return replace(frame, payload=frame.payload + b"tampered"), evidence

    context.qkd_transport_hook = tamper
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_CLASSICAL_AUTH,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert result.authentication.qkd_classical is not None
    assert result.authentication.qkd_classical.verified is False
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()


def test_pqc_authentication_failure_prevents_hybrid_establishment() -> None:
    context = _context()

    def tamper(message: SignedServerKeyOffer) -> SignedServerKeyOffer:
        changed = bytes((message.signature[0] ^ 1,)) + message.signature[1:]
        return replace(message, signature=changed)

    context.server_offer_transport_hook = tamper
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert result.authentication.pqc_exchange is not None
    assert result.authentication.pqc_exchange.verified is False


def test_pqc_state_and_signed_offer_session_mismatch_is_rejected() -> None:
    context = _context()
    assert context.pqc_responder is not None
    responder = context.pqc_responder

    def substitute_session(message: SignedServerKeyOffer) -> SignedServerKeyOffer:
        new_offer = replace(message.offer, session_id=b"other-session-id")
        return replace(
            message,
            offer=new_offer,
            signature=responder.sign(new_offer.canonical_bytes()),
        )

    context.server_offer_transport_hook = substitute_session
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert "session" in (result.abort_reason or "").lower()


def test_qkd_role_local_mismatch_fails_finished() -> None:
    context = _context()

    def mismatch(role: str, secret: bytes, _bit_length: int) -> bytes:
        if role == "initiator":
            return secret
        return bytes((secret[0] ^ 1,)) + secret[1:]

    context.hybrid_qkd_contribution_hook = mismatch
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert "Finished verification failed" in (result.abort_reason or "")


def test_hqc_role_local_mismatch_fails_diverse_finished() -> None:
    context = _context()

    def mismatch(role: str, values: tuple[tuple[str, bytes], ...]):
        if role == "initiator":
            return values
        algorithm, secret = values[1]
        changed = bytes((secret[0] ^ 1,)) + secret[1:]
        return (values[0], (algorithm, changed))

    context.hybrid_contribution_hook = mismatch
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID_DIVERSE,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        context,
    )
    assert result.status is SessionStatus.ABORTED
    assert "Finished verification failed" in (result.abort_reason or "")


def test_kem_processing_failure_aborts_and_withholds_key(monkeypatch) -> None:
    def fail_processing(*_args, **_kwargs):
        raise BackendOperationError("injected decapsulation failure")

    monkeypatch.setattr(ClientKeyExchangeProcessor, "process", fail_processing)
    result = run_session(
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        _context(),
    )
    assert result.status is SessionStatus.ABORTED
    assert "processing failed" in (result.abort_reason or "")
    with pytest.raises(RuntimeError, match="withheld"):
        result.export_session_key()
