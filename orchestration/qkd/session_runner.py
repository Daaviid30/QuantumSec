"""Adapter from authenticated QKD execution to the common session contract."""

from hashlib import sha384
from time import perf_counter_ns

import numpy as np

from orchestration.config import SessionConfig
from orchestration.context import SessionExecutionContext
from orchestration.metrics import QKDSessionMetrics, SessionMetrics
from orchestration.profiles import session_profile_definition
from orchestration.qkd.result import QKDOrchestrationStatus
from orchestration.qkd.runner import run_qkd_profile
from orchestration.result import (
    SESSION_RESULT_VERSION,
    AuthenticationOutcome,
    EstablishedKeyCapability,
    EstablishedKeyType,
    SecretProvenance,
    SessionAuthentication,
    SessionResult,
    SessionStatus,
)
from orchestration.trace import SessionTraceBuilder, SessionTraceSource


def run_qkd_session(config: SessionConfig, context: SessionExecutionContext) -> SessionResult:
    """Execute one QKD-only public profile and expose a key only after acceptance."""

    definition = session_profile_definition(config.profile)
    if definition.qkd_profile is None or definition.hybrid:
        raise ValueError("run_qkd_session requires a QKD-only session profile.")
    if context.qkd_protocol is None:
        raise ValueError("QKD execution requires context.qkd_protocol.")
    assert config.qkd_signal_count is not None

    trace = SessionTraceBuilder()
    trace.append(SessionTraceSource.SESSION, "session", "started", config.profile.value)
    started = perf_counter_ns()
    result = run_qkd_profile(
        context.qkd_protocol,
        config.qkd_signal_count,
        definition.qkd_profile,
        config=config.qkd_postprocessing,
        authentication_context=context.qkd_authentication,
        transport_hook=context.qkd_transport_hook,
    )
    elapsed = perf_counter_ns() - started
    for event in result.trace:
        trace.append(SessionTraceSource.QKD, event.stage, event.state, event.detail)

    auth = result.authentication
    auth_outcome = AuthenticationOutcome(
        purpose="QKD classical transcript authentication",
        mechanism=auth.metrics.mechanism.value,
        algorithm=auth.metrics.algorithm,
        executed=auth.executed,
        verified=auth.verified,
        trust_assumption=auth.metrics.trust_assumption,
    )
    transcript_bytes = result.transcript.canonical_bytes()
    qkd_metrics = QKDSessionMetrics(
        simulation_time_ns=max(0, elapsed - auth.metrics.total_time_ns),
        n_raw=result.qkd.n_raw,
        n_sifted=result.qkd.n_sifted,
        n_disclosed=result.qkd.n_disclosed,
        n_candidate=result.qkd.n_candidate,
        n_reconciled=result.qkd.n_reconciled,
        n_final=result.qkd.n_final,
        sifting_efficiency=result.qkd.sifting_efficiency,
        final_secret_fraction=result.qkd.final_secret_fraction,
        estimated_qber_z=result.qkd.estimated_qber_z,
        estimated_qber_x=result.qkd.estimated_qber_x,
        estimated_qber_aggregated=result.qkd.estimated_qber_aggregated,
        estimated_z_errors=result.qkd.estimated_z_errors,
        estimated_z_trials=result.qkd.estimated_z_trials,
        estimated_x_errors=result.qkd.estimated_x_errors,
        estimated_x_trials=result.qkd.estimated_x_trials,
        estimated_aggregate_errors=result.qkd.estimated_aggregate_errors,
        estimated_aggregate_trials=result.qkd.estimated_aggregate_trials,
        phase_error_bound=result.qkd.phase_error_bound,
        diagnostic_full_sifted_qber=result.qkd.diagnostic_full_sifted_qber,
        diagnostic_qber_z=result.qkd.diagnostic_qber_z,
        diagnostic_qber_x=result.qkd.diagnostic_qber_x,
        diagnostic_qber_aggregated=result.qkd.diagnostic_qber_aggregated,
        transcript_bytes=len(transcript_bytes),
    )
    metrics = SessionMetrics(
        qkd=qkd_metrics,
        qkd_authentication=auth.metrics,
        orchestration_software_wall_time_ns=elapsed,
    )
    public_context = (
        ("qkd_transcript_version", result.transcript.version),
        ("qkd_transcript_hash_sha384", sha384(transcript_bytes).hexdigest()),
    )
    if result.status is QKDOrchestrationStatus.ABORTED:
        trace.append(SessionTraceSource.SESSION, "session", "aborted", result.abort_reason or "QKD aborted.")
        return SessionResult(
            version=SESSION_RESULT_VERSION,
            session_id=result.session_id,
            profile=config.profile,
            status=SessionStatus.ABORTED,
            abort_reason=result.abort_reason or "QKD session aborted.",
            provenance=(),
            authentication=SessionAuthentication(qkd_classical=auth_outcome),
            trace=trace.freeze(),
            metrics=metrics,
            public_context=public_context,
        )

    alice, _bob = result.release_final_keys()
    bit_length = int(alice.size)
    packed = np.packbits(alice, bitorder="big").tobytes()
    trace.append(SessionTraceSource.SESSION, "session", "established", "Authenticated QKD key released.")
    return SessionResult(
        version=SESSION_RESULT_VERSION,
        session_id=result.session_id,
        profile=config.profile,
        status=SessionStatus.ESTABLISHED,
        abort_reason=None,
        provenance=(
            SecretProvenance(
                position=1,
                source="qkd",
                protocol="BB84",
                algorithm="privacy-amplified-bitstring",
                encoding="big-endian packed bits with explicit bit length",
                bit_length=bit_length,
                byte_length=len(packed),
            ),
        ),
        authentication=SessionAuthentication(qkd_classical=auth_outcome),
        trace=trace.freeze(),
        metrics=metrics,
        public_context=public_context,
        _key_capability=EstablishedKeyCapability(
            packed,
            bit_length=bit_length,
            key_type=EstablishedKeyType.QKD_BITSTRING,
        ),
    )
