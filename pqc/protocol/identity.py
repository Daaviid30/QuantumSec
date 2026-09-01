"""Private and public identities for PQC authentication."""

from dataclasses import dataclass, field
from typing import Self

from pqc.errors import UnsupportedAlgorithmError
from pqc.signatures import ML_DSA_65_METADATA, MLDSA65, SignatureMetadata


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
        object.__setattr__(self, "owner", owner)
        object.__setattr__(self, "algorithm", algorithm)
        object.__setattr__(self, "public_key", bytes(self.public_key))


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
        if identity.algorithm != self.metadata.name:
            raise UnsupportedAlgorithmError(
                f"Trusted identity {identity.owner!r} uses unsupported algorithm {identity.algorithm!r}."
            )
        return self._signer.verify(message, signature, identity.public_key)

    def __repr__(self) -> str:
        return f"MLDSAIdentity(owner={self.owner!r}, algorithm={self.metadata.name!r})"
