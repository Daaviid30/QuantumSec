"""Thin public dispatcher for all session profiles."""

from orchestration.config import SessionConfig
from orchestration.context import SessionExecutionContext
from orchestration.hybrid.runner import run_hybrid_session
from orchestration.pqc.runner import run_pqc_session
from orchestration.profiles import session_profile_definition
from orchestration.qkd.session_runner import run_qkd_session
from orchestration.result import SessionResult


def run_session(config: SessionConfig, context: SessionExecutionContext) -> SessionResult:
    """Dispatch a normalized session config to its domain-specific adapter."""

    if not isinstance(config, SessionConfig):
        raise TypeError("config must be a SessionConfig.")
    if not isinstance(context, SessionExecutionContext):
        raise TypeError("context must be a SessionExecutionContext.")
    definition = session_profile_definition(config.profile)
    if definition.hybrid:
        return run_hybrid_session(config, context)
    if definition.qkd_profile is not None:
        return run_qkd_session(config, context)
    return run_pqc_session(config, context)
