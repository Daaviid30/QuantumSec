"""Named PQC parties with signing and pre-provisioned verification trust."""

from dataclasses import dataclass, field
from typing import Self

from pqc.protocol.identity import MLDSAIdentity, PublicIdentity
from pqc.protocol.trust import TrustedIdentityStore


@dataclass(slots=True, repr=False)
class PQCParty:
    """Protocol participant holding a private signing identity and a trusted peer store."""

    _identity: MLDSAIdentity = field(repr=False)
    _trusted_peers: TrustedIdentityStore = field(default_factory=TrustedIdentityStore, repr=False)

    def __post_init__(self) -> None:
        """Validate that the party identity and trusted peer store instances are valid."""
        if not isinstance(self._identity, MLDSAIdentity):
            raise TypeError(f"identity must be MLDSAIdentity. Got {type(self._identity).__name__}.")
        if not isinstance(self._trusted_peers, TrustedIdentityStore):
            raise TypeError(
                f"trusted_peers must be TrustedIdentityStore. Got {type(self._trusted_peers).__name__}."
            )

    @classmethod
    def create(cls, name: str) -> Self:
        """Create a new party instance initialized with a fresh ML-DSA-65 signing identity."""

        identity = MLDSAIdentity.generate(name)
        return cls(_identity=identity)

    @property
    def name(self) -> str:
        """Return the owner name of this party's private identity."""

        return self._identity.owner

    @property
    def public_identity(self) -> PublicIdentity:
        """Return this party's public identity for distribution and registration in peer trust stores."""

        return self._identity.public_identity

    @property
    def trusted_peers(self) -> TrustedIdentityStore:
        """Return the explicit store of trusted peer identities configured for this party."""

        return self._trusted_peers

    def trust_peer(self, identity: PublicIdentity, *, overwrite: bool = False) -> None:
        """Add a peer's public identity to this party's trusted store with optional overwrite."""

        self._trusted_peers.trust(identity, overwrite=overwrite)

    def sign(self, message: bytes) -> bytes:
        """Sign message bytes using this party's private ML-DSA signing identity."""

        return self._identity.sign(message)

    def verify(self, peer_name: str, message: bytes, signature: bytes) -> bool:
        """Verify a signature against a trusted peer's pre-provisioned public identity."""

        trusted_identity = self._trusted_peers.lookup(peer_name)
        return trusted_identity.verify(message, signature)

    def __repr__(self) -> str:
        """Return a safe string representation showing party name and trusted peer owners."""
        return f"PQCParty(name={self.name!r}, trusted_peers={self._trusted_peers.owners!r})"
