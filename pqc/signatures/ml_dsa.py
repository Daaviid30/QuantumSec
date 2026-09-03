"""ML-DSA-65 signatures executed by the configured PQC backend."""

from dataclasses import dataclass, field
from typing import Final, Self

from pqc.backends.oqs_backend import OQSSignatureBackend
from pqc.signatures.base import SignatureMetadata, SignatureProvider

_ML_DSA_65_PUBLIC_KEY_LENGTH: Final = 1952
_ML_DSA_65_SECRET_KEY_LENGTH: Final = 4032
_ML_DSA_65_SIGNATURE_LENGTH: Final = 3309
ML_DSA_65_METADATA: Final = SignatureMetadata(
    name="ML-DSA-65",
    algorithm_type="digital signature",
    family="module-lattice based",
    nist_security_category=3,
    standardization="NIST FIPS 204",
    public_key_length=_ML_DSA_65_PUBLIC_KEY_LENGTH,
    secret_key_length=_ML_DSA_65_SECRET_KEY_LENGTH,
    signature_length=_ML_DSA_65_SIGNATURE_LENGTH,
)


def _require_bytes(value: object, *, name: str) -> bytes:
    """Validate that the input value is a byte string, raising a TypeError if it is not."""
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    return value


@dataclass(frozen=True, slots=True, repr=False)
class MLDSA65(SignatureProvider):
    """ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs."""

    _public_key: bytes = field(repr=False)
    _secret_key: bytes = field(repr=False)
    _backend: OQSSignatureBackend = field(default_factory=OQSSignatureBackend, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the keys."""
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
        """Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider instance."""

        key_pair = OQSSignatureBackend().generate_keypair(ML_DSA_65_METADATA.name)
        return cls(_public_key=key_pair.public_key, _secret_key=key_pair.secret_key)

    @property
    def metadata(self) -> SignatureMetadata:
        """Return standardized FIPS 204 metadata and key/signature lengths for ML-DSA-65."""

        return ML_DSA_65_METADATA

    @property
    def public_key(self) -> bytes:
        """Return the immutable ML-DSA-65 public key."""

        return self._public_key

    def sign(self, message: bytes) -> bytes:
        """Generate an ML-DSA-65 signature over message bytes using the private signing key."""

        clean_message = _require_bytes(message, name="message")
        return self._backend.sign(self.metadata.name, clean_message, self._secret_key)

    @staticmethod
    def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify an ML-DSA-65 signature against the message and public verification key."""

        clean_message = _require_bytes(message, name="message")
        clean_signature = _require_bytes(signature, name="signature")
        clean_public_key = _require_bytes(public_key, name="public_key")
        if len(clean_public_key) != _ML_DSA_65_PUBLIC_KEY_LENGTH:
            raise ValueError(
                f"ML-DSA-65 public_key must contain {_ML_DSA_65_PUBLIC_KEY_LENGTH} bytes. "
                f"Got {len(clean_public_key)}."
            )
        return OQSSignatureBackend().verify(
            ML_DSA_65_METADATA.name,
            clean_message,
            clean_signature,
            clean_public_key,
        )

    def __repr__(self) -> str:
        """Return a safe string representation with public key length without leaking secret bytes."""
        return f"MLDSA65(algorithm={self.metadata.name!r}, public_key_length={len(self._public_key)})"
