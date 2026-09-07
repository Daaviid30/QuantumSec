"""Profile-aware QKD runner that gates final-key release on authentication."""

import numpy as np

from orchestration.authentication import (
    AuthenticationTransportHook,
    MLDSAAuthenticationContext,
    WegmanCarterAuthenticationContext,
    assumed_authentication_result,
    authenticate_transcript_checkpoints,
)
from orchestration.profiles import QKDProfile
from orchestration.qkd.result import (
    AuthenticatedQKDSessionResult,
    QKDOrchestrationStatus,
    QKDSessionSummary,
    QKDTraceEvent,
)
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH, build_qkd_classical_transcript
from qkd.protocols import BB84PostprocessingConfig, BB84Protocol, BB84SessionStatus

type AuthenticationContext = MLDSAAuthenticationContext | WegmanCarterAuthenticationContext


def _session_identifier(protocol: BB84Protocol, supplied: bytes | None) -> bytes:
    if supplied is not None:
        if not isinstance(supplied, bytes) or len(supplied) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        return bytes(supplied)
    values = protocol.rng.gen.integers(
        0,
        256,
        size=QKD_CLASSICAL_SESSION_ID_LENGTH,
        dtype=np.uint8,
    )
    return np.asarray(values, dtype=np.uint8).tobytes()


def validate_qkd_authentication_context(
    profile: QKDProfile,
    context: AuthenticationContext | None,
    *,
    transport_hook: AuthenticationTransportHook | None = None,
) -> None:
    """Validate runtime authentication capabilities before starting QKD work."""

    if profile is QKDProfile.QKD_ASSUMED:
        if context is not None:
            raise ValueError("QKD-ASSUMED does not execute or accept an authentication context.")
        if transport_hook is not None:
            raise ValueError("QKD-ASSUMED has no authentication transport boundary to mutate.")
    elif profile is QKDProfile.QKD_CLASSICAL_AUTH:
        if not isinstance(context, WegmanCarterAuthenticationContext):
            raise TypeError("QKD-CLASSICAL-AUTH requires a WegmanCarterAuthenticationContext.")
    elif not isinstance(context, MLDSAAuthenticationContext):
        raise TypeError("QKD-PQC-AUTH requires an MLDSAAuthenticationContext.")


def run_qkd_profile(
    protocol: BB84Protocol,
    n_signals: int,
    profile: QKDProfile,
    *,
    config: BB84PostprocessingConfig | None = None,
    authentication_context: AuthenticationContext | None = None,
    session_id: bytes | None = None,
    transport_hook: AuthenticationTransportHook | None = None,
) -> AuthenticatedQKDSessionResult:
    """Run BB84 and authenticate its public transcript according to ``profile``."""

    if not isinstance(protocol, BB84Protocol):
        raise TypeError("protocol must be a BB84Protocol.")
    if not isinstance(profile, QKDProfile):
        raise TypeError("profile must be a QKDProfile.")
    validate_qkd_authentication_context(
        profile,
        authentication_context,
        transport_hook=transport_hook,
    )

    clean_session_id = _session_identifier(protocol, session_id)
    if authentication_context is not None:
        authentication_context.reserve_session_id(clean_session_id)
    bb84 = protocol.run_session(n_signals, config)
    transcript = build_qkd_classical_transcript(bb84, clean_session_id)
    if profile is QKDProfile.QKD_ASSUMED:
        authentication = assumed_authentication_result()
    else:
        assert authentication_context is not None
        authentication = authenticate_transcript_checkpoints(
            transcript,
            authentication_context.authenticators(),
            transport_hook=transport_hook,
        )

    trace = [
        QKDTraceEvent(
            stage="bb84",
            state=bb84.status.value,
            detail=bb84.abort_reason or "BB84 post-processing completed.",
        ),
        QKDTraceEvent(
            stage="classical_authentication",
            state=authentication.state.value,
            detail=(authentication.failure_reason or authentication.metrics.trust_assumption),
        ),
    ]
    if authentication.executed and authentication.verified is not True:
        status = QKDOrchestrationStatus.ABORTED
        abort_reason = f"Classical authentication failed: {authentication.failure_reason}"
    elif bb84.status is BB84SessionStatus.ABORTED:
        status = QKDOrchestrationStatus.ABORTED
        abort_reason = f"BB84 security abort: {bb84.abort_reason}"
    else:
        status = QKDOrchestrationStatus.ACCEPTED
        abort_reason = None
    released = status is QKDOrchestrationStatus.ACCEPTED
    trace.append(
        QKDTraceEvent(
            stage="key_release",
            state="released" if released else "withheld",
            detail=(
                "Final key released after all profile checks."
                if released
                else "No final key material is exposed by the orchestration result."
            ),
        )
    )
    return AuthenticatedQKDSessionResult(
        profile=profile,
        session_id=clean_session_id,
        status=status,
        qkd=QKDSessionSummary.from_session(bb84),
        authentication=authentication,
        transcript=transcript,
        abort_reason=abort_reason,
        trace=tuple(trace),
        _alice_final_key=bb84.alice_final_key if released else None,
        _bob_final_key=bb84.bob_final_key if released else None,
    )
