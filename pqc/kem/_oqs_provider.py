"""Shared private implementation for liboqs-backed KEM providers."""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Self

from pqc.backends.oqs_kem_backend import OQSKEMBackend
from pqc.errors import BackendOperationError
from pqc.kem.base import KEMEncapsulation, KEMMetadata, KEMProvider


def _require_bytes(value: object, *, name: str) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    return value


@dataclass(frozen=True, slots=True, repr=False)
class OQSKEMProvider(KEMProvider):
    """Private base for KEMs sharing the same liboqs lifecycle."""

    ALGORITHM: ClassVar[str]

    _public_key: bytes = field(repr=False)
    _secret_key: bytes = field(repr=False)
    _backend: OQSKEMBackend = field(default_factory=OQSKEMBackend, repr=False, compare=False)

    def __post_init__(self) -> None:
        public_key = _require_bytes(self._public_key, name="public_key")
        secret_key = _require_bytes(self._secret_key, name="secret_key")
        metadata = self.algorithm_metadata()
        if len(public_key) != metadata.public_key_length:
            raise ValueError(
                f"{metadata.name} public_key must contain {metadata.public_key_length} bytes. "
                f"Got {len(public_key)}."
            )
        if len(secret_key) != metadata.secret_key_length:
            raise ValueError(
                f"{metadata.name} secret_key must contain {metadata.secret_key_length} bytes. "
                f"Got {len(secret_key)}."
            )
        object.__setattr__(self, "_public_key", bytes(public_key))
        object.__setattr__(self, "_secret_key", bytes(secret_key))

    @classmethod
    @abstractmethod
    def algorithm_metadata(cls) -> KEMMetadata:
        """Return cached metadata for the concrete OQS mechanism."""

        raise NotImplementedError

    @classmethod
    def generate(cls) -> Self:
        """Generate an ephemeral key pair through liboqs."""

        key_pair = OQSKEMBackend().generate_keypair(cls.ALGORITHM)
        return cls(_public_key=key_pair.public_key, _secret_key=key_pair.secret_key)

    @property
    def metadata(self) -> KEMMetadata:
        """Return cached backend-derived metadata."""

        return self.algorithm_metadata()

    @property
    def public_key(self) -> bytes:
        """Return the immutable public encapsulation key."""

        return self._public_key

    @classmethod
    def encapsulate(cls, public_key: bytes) -> KEMEncapsulation:
        """Encapsulate to a public key through liboqs."""

        clean_public_key = _require_bytes(public_key, name="public_key")
        metadata = cls.algorithm_metadata()
        if len(clean_public_key) != metadata.public_key_length:
            raise ValueError(
                f"{metadata.name} public_key must contain {metadata.public_key_length} bytes. "
                f"Got {len(clean_public_key)}."
            )
        result = OQSKEMBackend().encapsulate(cls.ALGORITHM, clean_public_key)
        if len(result.ciphertext) != metadata.ciphertext_length:
            raise BackendOperationError(f"liboqs returned an invalid {metadata.name} ciphertext length.")
        if len(result.shared_secret) != metadata.shared_secret_length:
            raise BackendOperationError(f"liboqs returned an invalid {metadata.name} shared-secret length.")
        return KEMEncapsulation(ciphertext=result.ciphertext, shared_secret=result.shared_secret)

    def decapsulate(self, ciphertext: bytes) -> bytes:
        """Decapsulate a ciphertext through liboqs."""

        clean_ciphertext = _require_bytes(ciphertext, name="ciphertext")
        metadata = self.metadata
        if len(clean_ciphertext) != metadata.ciphertext_length:
            raise ValueError(
                f"{metadata.name} ciphertext must contain {metadata.ciphertext_length} bytes. "
                f"Got {len(clean_ciphertext)}."
            )
        shared_secret = self._backend.decapsulate(self.ALGORITHM, clean_ciphertext, self._secret_key)
        if len(shared_secret) != metadata.shared_secret_length:
            raise BackendOperationError(f"liboqs returned an invalid {metadata.name} shared-secret length.")
        return shared_secret

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(algorithm={self.ALGORITHM!r}, public_key_length={len(self._public_key)})"
        )
