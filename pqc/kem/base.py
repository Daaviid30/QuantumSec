"""Backend-independent key-encapsulation contracts and metadata."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True, slots=True)
class KEMMetadata:
    """Immutable specification and buffer dimensions for a Key Encapsulation Mechanism."""

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
        """Validate that descriptive strings are non-empty and buffer sizes are positive integers."""
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
    """Immutable container holding the ciphertext and shared secret produced during encapsulation."""

    ciphertext: bytes = field(repr=False)
    shared_secret: bytes = field(repr=False)

    def __post_init__(self) -> None:
        """Validate that ciphertext and shared secret are non-empty bytes and store immutable copies."""
        for field_name in ("ciphertext", "shared_secret"):
            value = getattr(self, field_name)
            if not isinstance(value, bytes):
                raise TypeError(f"{field_name} must be bytes. Got {type(value).__name__}.")
            if not value:
                raise ValueError(f"{field_name} must not be empty.")
            object.__setattr__(self, field_name, bytes(value))

    def __repr__(self) -> str:
        """Return a safe string representation showing buffer lengths without exposing secret bytes."""
        return (
            f"KEMEncapsulation(ciphertext_length={len(self.ciphertext)}, "
            f"shared_secret_length={len(self.shared_secret)})"
        )


class KEMProvider(ABC):
    """Abstract base contract defining core Key Encapsulation Mechanism (KEM) operations."""

    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        """Generate a fresh ephemeral KEM key pair using secure cryptographic backend randomness."""

        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> KEMMetadata:
        """Return the public algorithm metadata and key/ciphertext buffer dimensions."""

        raise NotImplementedError

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """Return the immutable public encapsulation key bytes."""

        raise NotImplementedError

    @classmethod
    @abstractmethod
    def encapsulate(cls, public_key: bytes) -> KEMEncapsulation:
        """Generate and encapsulate a fresh shared secret against the target public key."""

        raise NotImplementedError

    @abstractmethod
    def decapsulate(self, ciphertext: bytes) -> bytes:
        """Decapsulate an incoming ciphertext using this provider instance's private key."""

        raise NotImplementedError
