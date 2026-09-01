"""Backend-independent signature contracts and metadata."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class SignatureMetadata:
    """Non-secret description of a digital-signature algorithm."""

    name: str
    algorithm_type: str
    family: str
    nist_security_category: int
    standardization: str
    public_key_length: int
    secret_key_length: int
    signature_length: int

    def __post_init__(self) -> None:
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
    """Minimal backend-independent signing capability used by QuantumSec."""

    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        """Generate a new signing identity using backend cryptographic randomness."""

        raise NotImplementedError

    @property
    @abstractmethod
    def metadata(self) -> SignatureMetadata:
        """Return public algorithm metadata."""

        raise NotImplementedError

    @property
    @abstractmethod
    def public_key(self) -> bytes:
        """Return the immutable public verification key."""

        raise NotImplementedError

    @abstractmethod
    def sign(self, message: bytes) -> bytes:
        """Sign a byte string with this provider's private identity."""

        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify a signature against an explicitly supplied public key."""

        raise NotImplementedError
