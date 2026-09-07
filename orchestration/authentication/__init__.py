"""Classical-authentication mechanisms used by upper QKD session orchestration."""

from orchestration.authentication.assumed import (
    ASSUMED_AUTHENTICATION_TRUST,
    assumed_authentication_result,
)
from orchestration.authentication.base import (
    TRANSCRIPT_CHECKPOINT_TYPE,
    AuthenticationEvidence,
    AuthenticationFrame,
    AuthenticationMetrics,
    AuthenticationSessionRegistry,
    AuthenticationSessionReplayError,
    AuthenticationState,
    AuthenticationVerification,
    AuthenticatorMetadata,
    ClassicalAuthenticationResult,
    DirectionalAuthenticator,
)
from orchestration.authentication.execution import (
    AuthenticationTransportHook,
    authenticate_transcript_checkpoints,
)
from orchestration.authentication.ml_dsa import (
    ML_DSA_TRUST_ASSUMPTION,
    MLDSAAuthenticationContext,
    MLDSADirectionalAuthenticator,
)
from orchestration.authentication.wegman_carter import (
    WEGMAN_CARTER_DEFAULT_TAG_BITS,
    WEGMAN_CARTER_TRUST_ASSUMPTION,
    AuthenticationMaterialError,
    AuthenticationMaterialExhaustedError,
    AuthenticationMaterialReuseError,
    PreSharedAuthenticationMaterial,
    WegmanCarterAuthenticationContext,
    WegmanCarterDirectionalAuthenticator,
)

__all__ = [
    "ASSUMED_AUTHENTICATION_TRUST",
    "TRANSCRIPT_CHECKPOINT_TYPE",
    "AuthenticationEvidence",
    "AuthenticationFrame",
    "AuthenticationMetrics",
    "AuthenticationSessionRegistry",
    "AuthenticationSessionReplayError",
    "AuthenticationState",
    "AuthenticationTransportHook",
    "AuthenticationVerification",
    "AuthenticatorMetadata",
    "ClassicalAuthenticationResult",
    "DirectionalAuthenticator",
    "MLDSAAuthenticationContext",
    "MLDSADirectionalAuthenticator",
    "ML_DSA_TRUST_ASSUMPTION",
    "WEGMAN_CARTER_DEFAULT_TAG_BITS",
    "WEGMAN_CARTER_TRUST_ASSUMPTION",
    "AuthenticationMaterialError",
    "AuthenticationMaterialExhaustedError",
    "AuthenticationMaterialReuseError",
    "PreSharedAuthenticationMaterial",
    "WegmanCarterAuthenticationContext",
    "WegmanCarterDirectionalAuthenticator",
    "assumed_authentication_result",
    "authenticate_transcript_checkpoints",
]
