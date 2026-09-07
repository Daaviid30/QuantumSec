import ast
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from core.rng import SeededRNG
from orchestration import QKDOrchestrationStatus, QKDProfile, run_qkd_profile
from orchestration.authentication import (
    AuthenticationFrame,
    AuthenticationSessionReplayError,
    MLDSAAuthenticationContext,
    WegmanCarterAuthenticationContext,
)
from orchestration.qkd import QKDClassicalDirection, QKDClassicalMessageType
from pqc.protocol import MLDSAIdentity, TrustedIdentityStore
from qkd.channel import DepolarizingChannel, IdentityChannel, InterceptResendAttack
from qkd.protocols import BB84Protocol, BB84SessionStatus


@pytest.fixture(scope="module")
def ml_dsa_context() -> MLDSAAuthenticationContext:
    alice = MLDSAIdentity.generate("alice")
    bob = MLDSAIdentity.generate("bob")
    alice_trust = TrustedIdentityStore()
    bob_trust = TrustedIdentityStore()
    alice_trust.trust(bob.public_identity)
    bob_trust.trust(alice.public_identity)
    return MLDSAAuthenticationContext(alice, bob, alice_trust, bob_trust)


def _wc_context(size: int = 65_536) -> WegmanCarterAuthenticationContext:
    return WegmanCarterAuthenticationContext.from_shared_secrets(
        alice_to_bob_secret=b"a" * size,
        bob_to_alice_secret=b"b" * size,
    )


def _session_id(label: str) -> bytes:
    return label.encode("ascii").ljust(16, b"_")[:16]


def test_qkd_assumed_is_explicitly_not_executed_and_has_no_evidence() -> None:
    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_ASSUMED,
        session_id=_session_id("assumed"),
    )

    assert result.status is QKDOrchestrationStatus.ACCEPTED
    assert not result.authentication.executed
    assert result.authentication.verified is None
    assert not result.authentication.evidence
    assert result.authentication.metrics.evidence_bytes == 0
    alice, bob = result.release_final_keys()
    assert np.array_equal(alice, bob)
    assert not alice.flags.writeable


@pytest.mark.parametrize("profile", [QKDProfile.QKD_CLASSICAL_AUTH, QKDProfile.QKD_PQC_AUTH])
def test_authenticated_ideal_bb84_completes(profile, ml_dsa_context) -> None:
    context = _wc_context() if profile is QKDProfile.QKD_CLASSICAL_AUTH else ml_dsa_context

    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        profile,
        authentication_context=context,
        session_id=_session_id(profile.value),
    )

    assert result.status is QKDOrchestrationStatus.ACCEPTED
    assert result.authentication.executed
    assert result.authentication.verified
    assert result.authentication.metrics.checkpoints == 2
    assert result.authentication.metrics.generation_operations == 2
    assert result.authentication.metrics.verification_operations == 2
    assert result.authentication.metrics.authenticated_bytes > 0
    assert result.authentication.metrics.evidence_bytes > 0


def test_ml_dsa_metrics_separate_preprovisioned_keys_from_session_bytes(ml_dsa_context) -> None:
    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=_session_id("pqc-metrics"),
    )

    metrics = result.authentication.metrics
    assert metrics.evidence_bytes == 2 * 3309
    assert metrics.public_key_provisioning_bytes == 2 * 1952
    assert metrics.secret_bits_consumed is None
    assert {key for key, _ in metrics.runtime_environment} >= {
        "python",
        "platform",
        "processor",
        "liboqs",
        "liboqs-python",
    }


def test_authenticated_noisy_bb84_can_complete(ml_dsa_context) -> None:
    result = run_qkd_profile(
        BB84Protocol(DepolarizingChannel(0.04), SeededRNG(91)),
        4_000,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=_session_id("pqc-noisy"),
    )

    assert result.status is QKDOrchestrationStatus.ACCEPTED
    assert result.qkd.status is BB84SessionStatus.COMPLETED
    assert result.authentication.verified


def test_eve_full_interception_aborts_quantum_decision_despite_valid_authentication(
    ml_dsa_context,
) -> None:
    protocol = BB84Protocol(
        InterceptResendAttack(1.0, SeededRNG(900)),
        SeededRNG(901),
    )

    result = run_qkd_profile(
        protocol,
        4_000,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=_session_id("pqc-eve"),
    )

    assert result.status is QKDOrchestrationStatus.ABORTED
    assert result.qkd.status is BB84SessionStatus.ABORTED
    assert result.authentication.verified
    assert "BB84 security abort" in (result.abort_reason or "")
    assert result.qkd.phase_error_bound is not None
    assert result.qkd.phase_error_bound > 0.11
    with pytest.raises(RuntimeError, match="withheld"):
        result.release_final_keys()


def test_classical_transport_tampering_aborts_and_withholds_key(ml_dsa_context) -> None:
    mutated = False

    def tamper(frame, evidence):
        nonlocal mutated
        if not mutated:
            mutated = True
            return replace(frame, payload=frame.payload + b"tampered"), evidence
        return frame, evidence

    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=_session_id("pqc-tamper"),
        transport_hook=tamper,
    )

    assert result.status is QKDOrchestrationStatus.ABORTED
    assert result.authentication.verified is False
    assert result.final_key_length == 0
    with pytest.raises(RuntimeError, match="withheld"):
        result.release_final_keys()


def test_wc_depletion_becomes_an_authentication_abort() -> None:
    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_CLASSICAL_AUTH,
        authentication_context=_wc_context(size=8),
        session_id=_session_id("wc-depleted"),
    )

    assert result.status is QKDOrchestrationStatus.ABORTED
    assert result.authentication.verified is False
    assert "Insufficient fresh" in (result.authentication.failure_reason or "")
    assert result.final_key_length == 0


def test_transcript_contains_every_security_relevant_public_event_family() -> None:
    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_ASSUMED,
        session_id=_session_id("transcript"),
    )
    message_types = {event.message_type for event in result.transcript.events}

    assert {
        QKDClassicalMessageType.ALICE_BASIS_ANNOUNCEMENT,
        QKDClassicalMessageType.BOB_BASIS_ANNOUNCEMENT,
        QKDClassicalMessageType.SIFTING_SELECTION,
        QKDClassicalMessageType.PARAMETER_ESTIMATION_DISCLOSURE,
        QKDClassicalMessageType.CASCADE_PERMUTATION,
        QKDClassicalMessageType.CASCADE_ROOT_PARITY,
        QKDClassicalMessageType.KEY_VERIFICATION_SEED,
        QKDClassicalMessageType.KEY_VERIFICATION_TAG,
        QKDClassicalMessageType.PRIVACY_AMPLIFICATION_SEED,
    }.issubset(message_types)
    assert tuple(event.sequence_number for event in result.transcript.events) == tuple(
        range(result.transcript.message_count)
    )


def test_canonical_frame_binds_all_replay_relevant_fields() -> None:
    frame = AuthenticationFrame(
        session_id=b"a" * 16,
        direction=QKDClassicalDirection.ALICE_TO_BOB,
        sequence_number=3,
        message_type="cascade_binary_parity",
        payload=b"payload",
    )
    encodings = {
        frame.canonical_bytes(),
        replace(frame, session_id=b"b" * 16).canonical_bytes(),
        replace(frame, direction=QKDClassicalDirection.BOB_TO_ALICE).canonical_bytes(),
        replace(frame, sequence_number=4).canonical_bytes(),
        replace(frame, message_type="cascade_root_parity").canonical_bytes(),
        replace(frame, payload=b"payload-2").canonical_bytes(),
    }

    assert len(encodings) == 6


def _imports_top_level(path: Path, module_name: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] == module_name for alias in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] == module_name:
            return True
    return False


def test_qkd_and_pqc_remain_independent_sibling_domains() -> None:
    qkd_files = tuple(Path("qkd").rglob("*.py"))
    pqc_files = tuple(Path("pqc").rglob("*.py"))
    orchestration_files = tuple(Path("orchestration").rglob("*.py"))

    assert not any(_imports_top_level(path, "pqc") for path in qkd_files)
    assert not any(_imports_top_level(path, "qkd") for path in pqc_files)
    assert any(_imports_top_level(path, "qkd") for path in orchestration_files)
    assert any(_imports_top_level(path, "pqc") for path in orchestration_files)


def test_safe_result_repr_has_no_final_or_private_material(ml_dsa_context) -> None:
    result = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(2026)),
        512,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=_session_id("safe-result"),
    )

    rendered = repr(result).lower()
    assert "alice_final_key" not in rendered
    assert "bob_final_key" not in rendered
    assert "secret_key" not in rendered
    assert "private" not in rendered
    assert "_signer" not in rendered

    serialized = json.dumps(result.to_public_dict()).lower()
    assert "alice_final_key" not in serialized
    assert "bob_final_key" not in serialized
    assert "secret_key" not in serialized
    assert "public_seed" not in serialized
    assert "payload" not in serialized


def test_persistent_authentication_context_rejects_reused_session_id(ml_dsa_context) -> None:
    session_id = _session_id("unique-replay")
    first = run_qkd_profile(
        BB84Protocol(IdentityChannel(), SeededRNG(111)),
        512,
        QKDProfile.QKD_PQC_AUTH,
        authentication_context=ml_dsa_context,
        session_id=session_id,
    )
    assert first.authentication.verified

    with pytest.raises(AuthenticationSessionReplayError, match="already used"):
        run_qkd_profile(
            BB84Protocol(IdentityChannel(), SeededRNG(112)),
            512,
            QKDProfile.QKD_PQC_AUTH,
            authentication_context=ml_dsa_context,
            session_id=session_id,
        )
