"""Private and public identities for PQC authentication."""

import base64
import binascii
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Self

from pqc.signatures import ML_DSA_65_METADATA, MLDSA65, SignatureMetadata
from pqc.signatures.registry import _metadata_for_algorithm, verify_signature


def _validated_identity_name(value: object) -> str:
    """Validate that the given identity name is a non-empty string and return its trimmed form."""
    if not isinstance(value, str):
        raise TypeError(f"identity name must be a string. Got {type(value).__name__}.")
    clean = value.strip()
    if not clean:
        raise ValueError("identity name must not be empty.")
    return clean


@dataclass(frozen=True, slots=True)
class PublicIdentity:
    """Immutable public verification identity associating an owner name with public key bytes."""

    owner: str
    algorithm: str
    public_key: bytes = field(repr=False)

    def __post_init__(self) -> None:
        """Validate owner, algorithm, and public key buffer dimensions, storing an immutable copy."""
        owner = _validated_identity_name(self.owner)
        if not isinstance(self.algorithm, str):
            raise TypeError(f"algorithm must be a string. Got {type(self.algorithm).__name__}.")
        algorithm = self.algorithm.strip()
        if not algorithm:
            raise ValueError("algorithm must not be empty.")
        if not isinstance(self.public_key, bytes):
            raise TypeError(f"public_key must be bytes. Got {type(self.public_key).__name__}.")
        if not self.public_key:
            raise ValueError("public_key must not be empty.")
        metadata = _metadata_for_algorithm(algorithm)
        if metadata is not None and len(self.public_key) != metadata.public_key_length:
            raise ValueError(
                f"{algorithm} public_key must contain {metadata.public_key_length} bytes. "
                f"Got {len(self.public_key)}."
            )
        object.__setattr__(self, "owner", owner)
        object.__setattr__(self, "algorithm", algorithm)
        object.__setattr__(self, "public_key", bytes(self.public_key))

    def verify(self, message: bytes, signature: bytes) -> bool:
        """Verify a signature against the message using this public identity's algorithm and key."""

        return verify_signature(self.algorithm, message, signature, self.public_key)

    def to_dict(self) -> dict[str, str]:
        """Serialize this public identity into a JSON-compatible dictionary with Base64-encoded key bytes."""

        return {
            "owner": self.owner,
            "algorithm": self.algorithm,
            "public_key": base64.b64encode(self.public_key).decode("ascii"),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize and validate a public identity from a JSON-compatible dictionary payload."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        missing = {"owner", "algorithm", "public_key"}.difference(payload)
        if missing:
            raise ValueError(f"Public identity payload is missing fields: {', '.join(sorted(missing))}.")
        owner = payload["owner"]
        algorithm = payload["algorithm"]
        encoded_key = payload["public_key"]
        if not isinstance(owner, str) or not isinstance(algorithm, str) or not isinstance(encoded_key, str):
            raise TypeError("Public identity fields owner, algorithm, and public_key must be strings.")
        try:
            public_key = base64.b64decode(encoded_key, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Public identity public_key must be valid Base64.") from exc
        return cls(owner=owner, algorithm=algorithm, public_key=public_key)


@dataclass(frozen=True, slots=True, repr=False)
class MLDSAIdentity:
    """Named private identity holding an ML-DSA-65 signing capability and associated owner name."""

    owner: str
    _signer: MLDSA65 = field(repr=False)

    def __post_init__(self) -> None:
        """Validate the owner name and ensure the internal signer is an MLDSA65 instance."""
        object.__setattr__(self, "owner", _validated_identity_name(self.owner))
        if not isinstance(self._signer, MLDSA65):
            raise TypeError(f"signer must be MLDSA65. Got {type(self._signer).__name__}.")

    @classmethod
    def generate(cls, owner: str) -> Self:
        """Generate a new named private ML-DSA-65 signing identity with fresh cryptographic keys."""

        clean_owner = _validated_identity_name(owner)
        return cls(owner=clean_owner, _signer=MLDSA65.generate())

    @property
    def metadata(self) -> SignatureMetadata:
        """Return public algorithm metadata and key lengths for this identity's ML-DSA-65 signer."""

        return ML_DSA_65_METADATA

    @property
    def public_identity(self) -> PublicIdentity:
        """Export the non-secret public identity suitable for peer trust stores."""

        return PublicIdentity(
            owner=self.owner,
            algorithm=self.metadata.name,
            public_key=self._signer.public_key,
        )

    def sign(self, message: bytes) -> bytes:
        """Generate an ML-DSA-65 signature over message bytes using this identity's private key."""

        return self._signer.sign(message)

    def verify(self, message: bytes, signature: bytes, identity: PublicIdentity) -> bool:
        """Verify a message signature against an explicitly provided public identity."""

        if not isinstance(identity, PublicIdentity):
            raise TypeError(f"identity must be a PublicIdentity. Got {type(identity).__name__}.")
        return identity.verify(message, signature)

    def __repr__(self) -> str:
        """Return a safe string representation showing owner and algorithm without exposing secret keys."""
        return f"MLDSAIdentity(owner={self.owner!r}, algorithm={self.metadata.name!r})"
