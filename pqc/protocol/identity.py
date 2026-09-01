"""Private and public identities for PQC authentication."""

import base64
import binascii
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Self

from pqc.signatures import ML_DSA_65_METADATA, MLDSA65, SignatureMetadata
from pqc.signatures.registry import _metadata_for_algorithm, verify_signature


def _validated_identity_name(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError(f"identity name must be a string. Got {type(value).__name__}.")
    clean = value.strip()
    if not clean:
        raise ValueError("identity name must not be empty.")
    return clean


@dataclass(frozen=True, slots=True)
class PublicIdentity:
    """Immutable public verification identity with no signing material."""

    owner: str
    algorithm: str
    public_key: bytes = field(repr=False)

    def __post_init__(self) -> None:
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
        """Verify a signature using only this public identity."""

        return verify_signature(self.algorithm, message, signature, self.public_key)

    def to_dict(self) -> dict[str, str]:
        """Serialize this non-secret identity to a JSON-compatible mapping."""

        return {
            "owner": self.owner,
            "algorithm": self.algorithm,
            "public_key": base64.b64encode(self.public_key).decode("ascii"),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Restore a public identity from its JSON-compatible mapping."""

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
    """Named private identity with ML-DSA-65 signing capability."""

    owner: str
    _signer: MLDSA65 = field(repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "owner", _validated_identity_name(self.owner))
        if not isinstance(self._signer, MLDSA65):
            raise TypeError(f"signer must be MLDSA65. Got {type(self._signer).__name__}.")

    @classmethod
    def generate(cls, owner: str) -> Self:
        """Generate a named ML-DSA-65 identity using secure backend randomness."""

        clean_owner = _validated_identity_name(owner)
        return cls(owner=clean_owner, _signer=MLDSA65.generate())

    @property
    def metadata(self) -> SignatureMetadata:
        """Return public ML-DSA-65 metadata."""

        return ML_DSA_65_METADATA

    @property
    def public_identity(self) -> PublicIdentity:
        """Export the non-secret form suitable for trust provisioning."""

        return PublicIdentity(
            owner=self.owner,
            algorithm=self.metadata.name,
            public_key=self._signer.public_key,
        )

    def sign(self, message: bytes) -> bytes:
        """Sign a message with this identity's private capability."""

        return self._signer.sign(message)

    def verify(self, message: bytes, signature: bytes, identity: PublicIdentity) -> bool:
        """Verify against an explicitly selected public identity."""

        if not isinstance(identity, PublicIdentity):
            raise TypeError(f"identity must be a PublicIdentity. Got {type(identity).__name__}.")
        return identity.verify(message, signature)

    def __repr__(self) -> str:
        return f"MLDSAIdentity(owner={self.owner!r}, algorithm={self.metadata.name!r})"
