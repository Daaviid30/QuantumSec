"""Bilateral authentication of a completed canonical QKD public transcript."""

import platform
import sys
from collections.abc import Callable
from time import perf_counter_ns

from orchestration.authentication.base import (
    TRANSCRIPT_CHECKPOINT_TYPE,
    AuthenticationEvidence,
    AuthenticationFrame,
    AuthenticationMetrics,
    AuthenticationState,
    ClassicalAuthenticationResult,
    DirectionalAuthenticator,
)
from orchestration.authentication.wegman_carter import AuthenticationMaterialError
from orchestration.profiles import ClassicalAuthenticationMode
from orchestration.qkd.transcript import QKDClassicalDirection, QKDClassicalTranscript
from pqc.backends.oqs_backend import oqs_runtime_versions
from pqc.errors import PQCError

type AuthenticationTransportHook = Callable[
    [AuthenticationFrame, AuthenticationEvidence],
    tuple[AuthenticationFrame, AuthenticationEvidence | None],
]


def _validate_authenticator_pair(
    authenticators: tuple[DirectionalAuthenticator, DirectionalAuthenticator],
) -> None:
    if len(authenticators) != 2 or not all(
        isinstance(authenticator, DirectionalAuthenticator) for authenticator in authenticators
    ):
        raise TypeError("authenticators must contain exactly two DirectionalAuthenticator values.")
    first, second = authenticators
    if first.metadata.mechanism is not second.metadata.mechanism:
        raise ValueError("Both directions must use the same authentication mechanism.")
    if first.metadata.algorithm != second.metadata.algorithm:
        raise ValueError("Both directions must use the same authentication algorithm.")


def authenticate_transcript_checkpoints(
    transcript: QKDClassicalTranscript,
    authenticators: tuple[DirectionalAuthenticator, DirectionalAuthenticator],
    *,
    transport_hook: AuthenticationTransportHook | None = None,
) -> ClassicalAuthenticationResult:
    """Authenticate both directional views before any final key can be released.

    This is an end-of-transcript batching strategy. It detects manipulation
    before orchestration releases key material, but does not prevent an attacker
    from causing unauthenticated protocol computation and denial of service.
    """

    if not isinstance(transcript, QKDClassicalTranscript):
        raise TypeError("transcript must be a QKDClassicalTranscript.")
    _validate_authenticator_pair(authenticators)
    if transport_hook is not None and not callable(transport_hook):
        raise TypeError("transport_hook must be callable or None.")

    directions = (
        QKDClassicalDirection.ALICE_TO_BOB,
        QKDClassicalDirection.BOB_TO_ALICE,
    )
    payload = transcript.canonical_bytes()
    metadata = authenticators[0].metadata
    environment = [
        ("python", platform.python_version()),
        ("implementation", sys.implementation.name),
        ("platform", platform.platform()),
        ("processor", platform.processor() or platform.machine() or "unknown"),
    ]
    if metadata.mechanism is ClassicalAuthenticationMode.ML_DSA_65:
        versions = oqs_runtime_versions()
        environment.extend((("liboqs", versions.liboqs), ("liboqs-python", versions.liboqs_python)))
    evidence_items: list[AuthenticationEvidence] = []
    authenticated_bytes = 0
    evidence_bytes = 0
    secret_bits_consumed = 0
    generation_operations = 0
    verification_operations = 0
    generation_time_ns = 0
    verification_time_ns = 0
    failure_reason: str | None = None

    for offset, (direction, authenticator) in enumerate(zip(directions, authenticators, strict=True)):
        frame = AuthenticationFrame(
            session_id=transcript.session_id,
            direction=direction,
            sequence_number=transcript.message_count + offset,
            message_type=TRANSCRIPT_CHECKPOINT_TYPE,
            payload=payload,
        )
        authenticated_bytes += len(frame.canonical_bytes())
        generation_started = perf_counter_ns()
        generation_operations += 1
        try:
            evidence = authenticator.generate_evidence(frame)
        except (AuthenticationMaterialError, PQCError, TypeError, ValueError) as exc:
            generation_time_ns += perf_counter_ns() - generation_started
            failure_reason = f"Authentication evidence generation failed: {exc}"
            break
        generation_time_ns += perf_counter_ns() - generation_started
        evidence_items.append(evidence)
        evidence_bytes += evidence.evidence_bytes
        if evidence.secret_bits_consumed is not None:
            secret_bits_consumed += evidence.secret_bits_consumed

        received_frame = frame
        received_evidence: AuthenticationEvidence | None = evidence
        if transport_hook is not None:
            transported = transport_hook(frame, evidence)
            if (
                not isinstance(transported, tuple)
                or len(transported) != 2
                or not isinstance(transported[0], AuthenticationFrame)
                or (transported[1] is not None and not isinstance(transported[1], AuthenticationEvidence))
            ):
                raise TypeError(
                    "transport_hook must return (AuthenticationFrame, AuthenticationEvidence | None)."
                )
            received_frame, received_evidence = transported

        verification_started = perf_counter_ns()
        verification_operations += 1
        verification = authenticator.verify_evidence(received_frame, received_evidence)
        verification_time_ns += perf_counter_ns() - verification_started
        if not verification.verified:
            failure_reason = verification.failure_reason
            break

    executed_all = failure_reason is None and verification_operations == len(authenticators)
    provisioning_values = tuple(
        authenticator.metadata.public_key_provisioning_bytes for authenticator in authenticators
    )
    public_key_provisioning_bytes = (
        None
        if any(value is None for value in provisioning_values)
        else sum(value for value in provisioning_values if value is not None)
    )
    metrics = AuthenticationMetrics(
        mechanism=metadata.mechanism,
        algorithm=metadata.algorithm,
        family=metadata.family,
        authenticated_bytes=authenticated_bytes,
        evidence_bytes=evidence_bytes,
        checkpoints=generation_operations,
        generation_operations=generation_operations,
        verification_operations=verification_operations,
        generation_time_ns=generation_time_ns,
        verification_time_ns=verification_time_ns,
        total_time_ns=generation_time_ns + verification_time_ns,
        trust_assumption=metadata.trust_assumption,
        secret_bits_consumed=(
            secret_bits_consumed if metadata.mechanism is ClassicalAuthenticationMode.WEGMAN_CARTER else None
        ),
        public_key_provisioning_bytes=public_key_provisioning_bytes,
        forgery_bound=metadata.forgery_bound,
        runtime_environment=tuple(environment),
    )
    if executed_all:
        return ClassicalAuthenticationResult(
            state=AuthenticationState.EXECUTED_VERIFIED,
            executed=True,
            verified=True,
            metrics=metrics,
            evidence=tuple(evidence_items),
        )
    return ClassicalAuthenticationResult(
        state=AuthenticationState.EXECUTED_FAILED,
        executed=True,
        verified=False,
        metrics=metrics,
        failure_reason=failure_reason or "Classical authentication did not complete.",
        evidence=tuple(evidence_items),
    )
