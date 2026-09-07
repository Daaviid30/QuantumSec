"""Upper-layer composition of independent QKD and PQC domain modules."""

from orchestration.config import SESSION_CONFIG_VERSION, SessionConfig
from orchestration.context import SessionExecutionContext
from orchestration.data_plane import open_data_plane
from orchestration.hybrid import (
    HybridPublicContext,
    HybridSecretComponent,
    canonical_hybrid_secret_input,
    run_hybrid_session,
)
from orchestration.metrics import (
    HybridSessionMetrics,
    PQCAuthenticationMetrics,
    PQCSessionMetrics,
    QKDSessionMetrics,
    SessionMetrics,
)
from orchestration.profiles import (
    CapabilityStatus,
    ClassicalAuthenticationMode,
    EstablishmentSource,
    QKDProfile,
    QKDProfileDefinition,
    SessionProfile,
    SessionProfileDefinition,
    qkd_profile_definition,
    session_capabilities,
    session_profile_definition,
)
from orchestration.qkd import (
    AuthenticatedQKDSessionResult,
    QKDOrchestrationStatus,
    QKDSessionSummary,
    QKDTraceEvent,
    run_qkd_profile,
)
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
from orchestration.runner import run_session
from orchestration.trace import (
    SESSION_TRACE_VERSION,
    SessionTrace,
    SessionTraceEvent,
    SessionTraceSource,
)

__all__ = [
    "AuthenticatedQKDSessionResult",
    "AuthenticationOutcome",
    "CapabilityStatus",
    "ClassicalAuthenticationMode",
    "EstablishmentSource",
    "EstablishedKeyCapability",
    "EstablishedKeyType",
    "HybridSessionMetrics",
    "HybridPublicContext",
    "HybridSecretComponent",
    "PQCAuthenticationMetrics",
    "PQCSessionMetrics",
    "QKDOrchestrationStatus",
    "QKDProfile",
    "QKDProfileDefinition",
    "QKDSessionMetrics",
    "QKDSessionSummary",
    "QKDTraceEvent",
    "SESSION_CONFIG_VERSION",
    "SESSION_RESULT_VERSION",
    "SESSION_TRACE_VERSION",
    "SecretProvenance",
    "SessionAuthentication",
    "SessionConfig",
    "SessionExecutionContext",
    "SessionMetrics",
    "SessionProfile",
    "SessionProfileDefinition",
    "SessionResult",
    "SessionStatus",
    "SessionTrace",
    "SessionTraceEvent",
    "SessionTraceSource",
    "qkd_profile_definition",
    "canonical_hybrid_secret_input",
    "open_data_plane",
    "run_hybrid_session",
    "run_qkd_profile",
    "run_session",
    "session_capabilities",
    "session_profile_definition",
]
