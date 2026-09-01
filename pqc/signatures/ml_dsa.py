"""ML-DSA-65 signatures executed by the configured PQC backend."""

from dataclasses import dataclass, field
from typing import Final, Self

from pqc.backends.oqs_backend import OQSSignatureBackend
from pqc.signatures.base import SignatureMetadata, SignatureProvider

ML_DSA_65_METADATA: Final = SignatureMetadata(
    name="ML-DSA-65",
    algorithm_type="digital signature",
    family="module-lattice based",
    nist_security_category=3,
    standardization="NIST FIPS 204",
)
_ML_DSA_65_PUBLIC_KEY_LENGTH: Final = 1952
_ML_DSA_65_SECRET_KEY_LENGTH: Final = 4032


def _require_bytes(value: object, *, name: str) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    return value


@dataclass(frozen=True, slots=True, repr=False)
class MLDSA65(SignatureProvider):
    """Private ML-DSA-65 signing capability backed by liboqs."""

    _public_key: bytes = field(repr=False)
    _secret_key: bytes = field(repr=False)
    _backend: OQSSignatureBackend = field(default_factory=OQSSignatureBackend, repr=False, compare=False)

    def __post_init__(self) -> None:
        public_key = _require_bytes(self._public_key, name="public_key")
        secret_key = _require_bytes(self._secret_key, name="secret_key")
        if not public_key:
            raise ValueError("public_key must not be empty.")
        if not secret_key:
            raise ValueError("secret_key must not be empty.")
        if len(public_key) != _ML_DSA_65_PUBLIC_KEY_LENGTH:
            raise ValueError(
                f"ML-DSA-65 public_key must contain {_ML_DSA_65_PUBLIC_KEY_LENGTH} bytes. "
                f"Got {len(public_key)}."
            )
        if len(secret_key) != _ML_DSA_65_SECRET_KEY_LENGTH:
            raise ValueError(
                f"ML-DSA-65 secret_key must contain {_ML_DSA_65_SECRET_KEY_LENGTH} bytes. "
                f"Got {len(secret_key)}."
            )
        object.__setattr__(self, "_public_key", bytes(public_key))
        object.__setattr__(self, "_secret_key", bytes(secret_key))

    @classmethod
    def generate(cls) -> Self:
        """Generate a real ML-DSA-65 key pair using liboqs CSPRNG state."""

        key_pair = OQSSignatureBackend().generate_keypair(ML_DSA_65_METADATA.name)
        return cls(_public_key=key_pair.public_key, _secret_key=key_pair.secret_key)

    @property
    def metadata(self) -> SignatureMetadata:
        """Return standardized ML-DSA-65 metadata."""

        return ML_DSA_65_METADATA

    @property
    def public_key(self) -> bytes:
        """Return the immutable ML-DSA-65 public key."""

        return self._public_key

    def sign(self, message: bytes) -> bytes:
        """Sign a message using the private ML-DSA-65 key."""

        clean_message = _require_bytes(message, name="message")
        return self._backend.sign(self.metadata.name, clean_message, self._secret_key)

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Return whether a signature is valid for a message and public key."""

        clean_message = _require_bytes(message, name="message")
        clean_signature = _require_bytes(signature, name="signature")
        clean_public_key = _require_bytes(public_key, name="public_key")
        if len(clean_public_key) != _ML_DSA_65_PUBLIC_KEY_LENGTH:
            raise ValueError(
                f"ML-DSA-65 public_key must contain {_ML_DSA_65_PUBLIC_KEY_LENGTH} bytes. "
                f"Got {len(clean_public_key)}."
            )
        return self._backend.verify(self.metadata.name, clean_message, clean_signature, clean_public_key)

    def __repr__(self) -> str:
        return f"MLDSA65(algorithm={self.metadata.name!r}, public_key_length={len(self._public_key)})"
