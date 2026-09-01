"""Named PQC parties with signing and pre-provisioned verification trust."""

from dataclasses import dataclass, field
from typing import Self

from pqc.protocol.identity import MLDSAIdentity, PublicIdentity
from pqc.protocol.trust import TrustedIdentityStore


@dataclass(slots=True, repr=False)
class PQCParty:
    """Mutable trust-bearing party with an immutable private ML-DSA identity."""

    _identity: MLDSAIdentity = field(repr=False)
    _trusted_peers: TrustedIdentityStore = field(default_factory=TrustedIdentityStore, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self._identity, MLDSAIdentity):
            raise TypeError(f"identity must be MLDSAIdentity. Got {type(self._identity).__name__}.")
        if not isinstance(self._trusted_peers, TrustedIdentityStore):
            raise TypeError(
                f"trusted_peers must be TrustedIdentityStore. Got {type(self._trusted_peers).__name__}."
            )

    @classmethod
    def create(cls, name: str) -> Self:
        """Create a party with a new real ML-DSA-65 identity."""

        identity = MLDSAIdentity.generate(name)
        return cls(_identity=identity)

    @property
    def name(self) -> str:
        """Return the immutable owner name of this party's private identity."""

        return self._identity.owner

    @property
    def public_identity(self) -> PublicIdentity:
        """Return the non-secret identity that peers may provision as trusted."""

        return self._identity.public_identity

    @property
    def trusted_peers(self) -> TrustedIdentityStore:
        """Return this party's explicit trust store."""

        return self._trusted_peers

    def trust_peer(self, identity: PublicIdentity, *, overwrite: bool = False) -> None:
        """Explicitly provision a peer's public identity as trusted."""

        self._trusted_peers.trust(identity, overwrite=overwrite)

    def sign(self, message: bytes) -> bytes:
        """Sign data using this party's private identity."""

        return self._identity.sign(message)

    def verify(self, peer_name: str, message: bytes, signature: bytes) -> bool:
        """Verify data using only the peer key already present in the trust store."""

        trusted_identity = self._trusted_peers.lookup(peer_name)
        return trusted_identity.verify(message, signature)

    def __repr__(self) -> str:
        return f"PQCParty(name={self.name!r}, trusted_peers={self._trusted_peers.owners!r})"
