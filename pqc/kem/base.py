"""Backend-independent key-encapsulation contracts and metadata."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True, slots=True)
class KEMMetadata:
    """Non-secret description and sizes of a key-encapsulation mechanism."""

    name: str
    algorithm_type: str
    family: str
    nist_security_category: int
    standardization: str
    implementation_version: str
    public_key_length: int
    secret_key_length: int
    ciphertext_length: int
    shared_secret_length: int

    def __post_init__(self) -> None:
        for field_name in (
            "name",
            "algorithm_type",
            "family",
            "standardization",
            "implementation_version",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string. Got {type(value).__name__}.")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty.")
        for field_name in (
            "nist_security_category",
            "public_key_length",
            "secret_key_length",
            "ciphertext_length",
            "shared_secret_length",
        ):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{field_name} must be a positive integer.")


@dataclass(frozen=True, slots=True, repr=False)
class KEMEncapsulation:
    """Primitive KEM output; its shared secret is never shown in representations."""

    ciphertext: bytes = field(repr=False)
    shared_secret: bytes = field(repr=False)

    def __post_init__(self) -> None:
        for field_name in ("ciphertext", "shared_secret"):
            value = getattr(self, field_name)
            if not isinstance(value, bytes):
                raise TypeError(f"{field_name} must be bytes. Got {type(value).__name__}.")
            if not value:
                raise ValueError(f"{field_name} must not be empty.")
            object.__setattr__(self, field_name, bytes(value))

    def __repr__(self) -> str:
        return (
            f"KEMEncapsulation(ciphertext_length={len(self.ciphertext)}, "
            f"shared_secret_length={len(self.shared_secret)})"
        )


class KEMProvider(ABC):
    """Minimal KEM capability independent of a concrete cryptographic backend."""

    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        """Generate a new KEM key pair using backend cryptographic randomness."""

        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> KEMMetadata:
        """Return public KEM metadata."""

        raise NotImplementedError

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """Return the immutable public encapsulation key."""

        raise NotImplementedError

    @classmethod
    @abstractmethod
    def encapsulate(cls, public_key: bytes) -> KEMEncapsulation:
        """Encapsulate to a public key as a standalone primitive operation."""

        raise NotImplementedError

    @abstractmethod
    def decapsulate(self, ciphertext: bytes) -> bytes:
        """Decapsulate using this provider's private key."""

        raise NotImplementedError
