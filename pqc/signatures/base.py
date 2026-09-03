"""Backend-independent signature contracts and metadata."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class SignatureMetadata:
    """Immutable specification and buffer dimensions for a post-quantum digital signature algorithm."""

    name: str
    algorithm_type: str
    family: str
    nist_security_category: int
    standardization: str
    public_key_length: int
    secret_key_length: int
    signature_length: int

    def __post_init__(self) -> None:
        """Validate metadata text fields and ensure category and buffer sizes are positive integers."""
        for field_name in ("name", "algorithm_type", "family", "standardization"):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string. Got {type(value).__name__}.")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty.")
        category = self.nist_security_category
        if isinstance(category, bool) or not isinstance(category, int) or category <= 0:
            raise ValueError("nist_security_category must be a positive integer.")
        for field_name in ("public_key_length", "secret_key_length", "signature_length"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{field_name} must be a positive integer.")


class SignatureProvider(ABC):
    """Abstract base contract defining post-quantum digital signature operations."""

    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        """Generate a fresh signing key pair using secure cryptographic backend randomness."""

        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> SignatureMetadata:
        """Return the public algorithm metadata and key/signature buffer dimensions."""

        raise NotImplementedError

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """Return the immutable public verification key bytes."""

        raise NotImplementedError

    @abstractmethod
    def sign(self, message: bytes) -> bytes:
        """Generate a digital signature over the provided message bytes using the private key."""

        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify whether a signature is authentic for the message and explicit public verification key."""

        raise NotImplementedError
