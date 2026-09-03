"""Adapter isolating the liboqs-python key-encapsulation API."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cache, lru_cache
from importlib import import_module
from types import ModuleType, TracebackType
from typing import Protocol, Self, cast

from pqc.errors import BackendOperationError, BackendUnavailableError, UnsupportedAlgorithmError


class _OQSKEM(Protocol):
    """Protocol defining the interface for a liboqs KeyEncapsulation context manager."""

    details: Mapping[str, object]

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def generate_keypair(self) -> bytes: ...

    def export_secret_key(self) -> bytes: ...

    def encap_secret(self, public_key: bytes) -> tuple[bytes, bytes]: ...

    def decap_secret(self, ciphertext: bytes) -> bytes: ...


class _KEMFactory(Protocol):
    """Protocol for the liboqs KeyEncapsulation constructor callable."""

    def __call__(self, alg_name: str, secret_key: bytes | None = None) -> _OQSKEM: ...


class _OQSModule(Protocol):
    """Protocol describing the exported interface of the imported oqs module."""

    KeyEncapsulation: _KEMFactory
    MechanismNotEnabledError: type[Exception]
    MechanismNotSupportedError: type[Exception]

    def is_kem_enabled(self, alg_name: str) -> int: ...


@dataclass(frozen=True, slots=True)
class OQSKEMKeyPair:
    """Immutable container transferring generated key pairs across the liboqs adapter boundary."""

    public_key: bytes = field(repr=False)
    secret_key: bytes = field(repr=False)


@dataclass(frozen=True, slots=True)
class OQSKEMEncapsulation:
    """Immutable container holding ciphertext and shared secret produced by liboqs encapsulation."""

    ciphertext: bytes = field(repr=False)
    shared_secret: bytes = field(repr=False)


@dataclass(frozen=True, slots=True)
class OQSKEMDetails:
    """Immutable data structure storing algorithm parameters and buffer dimensions from liboqs."""

    name: str
    version: str
    claimed_nist_level: int
    public_key_length: int
    secret_key_length: int
    ciphertext_length: int
    shared_secret_length: int


@lru_cache(maxsize=1)
def _load_oqs() -> _OQSModule:
    """Dynamically import and cache the liboqs Python module, raising BackendUnavailableError on failure."""
    try:
        module: ModuleType = import_module("oqs")
    except (ImportError, OSError, RuntimeError) as exc:
        raise BackendUnavailableError("The liboqs-python backend could not be loaded.") from exc
    return cast(_OQSModule, module)


@cache
def _ensure_kem_algorithm_enabled(algorithm: str) -> None:
    """Verify that the requested KEM algorithm is enabled in the liboqs library."""
    module = _load_oqs()
    try:
        algorithm_enabled = bool(module.is_kem_enabled(algorithm))
    except Exception as exc:
        raise BackendUnavailableError("The liboqs backend could not query enabled KEMs.") from exc
    if not algorithm_enabled:
        raise UnsupportedAlgorithmError(f"KEM algorithm {algorithm!r} is not enabled by liboqs.")


def _new_kem(algorithm: str, *, secret_key: bytes | None = None) -> _OQSKEM:
    """Initialize and return a new liboqs KeyEncapsulation instance for the specified algorithm."""
    module = _load_oqs()
    _ensure_kem_algorithm_enabled(algorithm)
    try:
        return module.KeyEncapsulation(algorithm, secret_key=secret_key)
    except (module.MechanismNotEnabledError, module.MechanismNotSupportedError) as exc:
        raise UnsupportedAlgorithmError(f"KEM algorithm {algorithm!r} is unavailable.") from exc
    except Exception as exc:
        raise BackendUnavailableError(f"The liboqs backend could not initialize {algorithm!r}.") from exc


def _required_detail(
    details: Mapping[str, object],
    name: str,
    expected_type: type[str] | type[int],
) -> str | int:
    """Extract and validate a required metadata field from the liboqs algorithm details mapping."""
    value = details.get(name)
    if expected_type is int:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise BackendOperationError(f"liboqs returned invalid KEM metadata field {name!r}.")
        return value
    if not isinstance(value, str) or not value:
        raise BackendOperationError(f"liboqs returned invalid KEM metadata field {name!r}.")
    return value


class OQSKEMBackend:
    """Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic operations."""

    def details(self, algorithm: str) -> OQSKEMDetails:
        """Query and return validated metadata and buffer dimensions for a KEM algorithm from liboqs."""
        kem = _new_kem(algorithm)
        try:
            with kem:
                details = dict(kem.details)
        except Exception as exc:
            raise BackendOperationError(f"liboqs metadata retrieval failed for {algorithm!r}.") from exc
        return OQSKEMDetails(
            name=cast(str, _required_detail(details, "name", str)),
            version=cast(str, _required_detail(details, "version", str)),
            claimed_nist_level=cast(int, _required_detail(details, "claimed_nist_level", int)),
            public_key_length=cast(int, _required_detail(details, "length_public_key", int)),
            secret_key_length=cast(int, _required_detail(details, "length_secret_key", int)),
            ciphertext_length=cast(int, _required_detail(details, "length_ciphertext", int)),
            shared_secret_length=cast(int, _required_detail(details, "length_shared_secret", int)),
        )

    def generate_keypair(self, algorithm: str) -> OQSKEMKeyPair:
        """Generate a fresh key pair for the specified KEM algorithm using liboqs."""
        kem = _new_kem(algorithm)
        try:
            with kem:
                public_key = bytes(kem.generate_keypair())
                secret_key = bytes(kem.export_secret_key())
        except Exception as exc:
            raise BackendOperationError(f"liboqs KEM key generation failed for {algorithm!r}.") from exc
        return OQSKEMKeyPair(public_key=public_key, secret_key=secret_key)

    def encapsulate(self, algorithm: str, public_key: bytes) -> OQSKEMEncapsulation:
        """Encapsulate a secret against the public key via liboqs, returning ciphertext and shared secret."""
        kem = _new_kem(algorithm)
        try:
            with kem:
                ciphertext, shared_secret = kem.encap_secret(public_key)
        except Exception as exc:
            raise BackendOperationError(f"liboqs encapsulation failed for {algorithm!r}.") from exc
        return OQSKEMEncapsulation(ciphertext=bytes(ciphertext), shared_secret=bytes(shared_secret))

    def decapsulate(self, algorithm: str, ciphertext: bytes, secret_key: bytes) -> bytes:
        """Decapsulate a ciphertext using the provided secret key via liboqs to recover the shared secret."""
        kem = _new_kem(algorithm, secret_key=secret_key)
        try:
            with kem:
                return bytes(kem.decap_secret(ciphertext))
        except Exception as exc:
            raise BackendOperationError(f"liboqs decapsulation failed for {algorithm!r}.") from exc
