"""Domain errors for post-quantum cryptographic operations."""


class PQCError(Exception):
    """Base exception class for all post-quantum cryptography domain errors in QuantumSec."""


class BackendUnavailableError(PQCError):
    """Raised when the post-quantum cryptography backend (liboqs) cannot be loaded or initialized."""


class BackendOperationError(PQCError):
    """Raised when an active post-quantum cryptography backend fails during execution."""


class UnsupportedAlgorithmError(PQCError):
    """Raised when a requested post-quantum algorithm is unsupported or disabled in the backend."""


class UnknownTrustedPeerError(PQCError):
    """Raised when an operation requires an identity from a peer not found in the local trust store."""


class TrustedIdentityConflictError(PQCError):
    """Raised when adding an identity for an existing peer without overwrite permission."""
