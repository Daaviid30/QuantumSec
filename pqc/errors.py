"""Domain errors for post-quantum cryptographic operations."""


class PQCError(Exception):
    """Base class for PQC domain errors."""


class BackendUnavailableError(PQCError):
    """Raised when the configured PQC backend cannot be loaded or initialized."""


class BackendOperationError(PQCError):
    """Raised when an available PQC backend fails during an operation."""


class UnsupportedAlgorithmError(PQCError):
    """Raised when the backend cannot provide a requested algorithm."""


class UnknownTrustedPeerError(PQCError):
    """Raised when a peer is absent from the pre-provisioned trust store."""
