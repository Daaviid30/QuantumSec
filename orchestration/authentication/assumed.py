"""Explicit non-executed authentication result for the QKD baseline profile."""

import platform
import sys

from orchestration.authentication.base import (
    AuthenticationMetrics,
    AuthenticationState,
    ClassicalAuthenticationResult,
)
from orchestration.profiles import ClassicalAuthenticationMode

ASSUMED_AUTHENTICATION_TRUST = "The classical BB84 channel is assumed authenticated externally."


def assumed_authentication_result() -> ClassicalAuthenticationResult:
    return ClassicalAuthenticationResult(
        state=AuthenticationState.ASSUMED_NOT_EXECUTED,
        executed=False,
        verified=None,
        metrics=AuthenticationMetrics(
            mechanism=ClassicalAuthenticationMode.ASSUMED,
            algorithm="none",
            family="none",
            authenticated_bytes=0,
            evidence_bytes=0,
            checkpoints=0,
            generation_operations=0,
            verification_operations=0,
            generation_time_ns=0,
            verification_time_ns=0,
            total_time_ns=0,
            trust_assumption=ASSUMED_AUTHENTICATION_TRUST,
            secret_bits_consumed=None,
            public_key_provisioning_bytes=None,
            forgery_bound=None,
            runtime_environment=(
                ("python", platform.python_version()),
                ("implementation", sys.implementation.name),
                ("platform", platform.platform()),
                ("processor", platform.processor() or platform.machine() or "unknown"),
            ),
        ),
    )
