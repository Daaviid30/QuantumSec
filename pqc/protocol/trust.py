"""Explicit pre-provisioned trust for public PQC identities."""

from collections.abc import Iterator

from pqc.errors import UnknownTrustedPeerError, UnsupportedAlgorithmError
from pqc.protocol.identity import PublicIdentity, _validated_identity_name
from pqc.signatures import ML_DSA_65_METADATA


class TrustedIdentityStore:
    """Map peer names to public identities trusted out of band."""

    __slots__ = ("_identities",)

    def __init__(self) -> None:
        self._identities: dict[str, PublicIdentity] = {}

    def trust(self, identity: PublicIdentity) -> None:
        """Explicitly provision or replace a peer's trusted public identity."""

        if not isinstance(identity, PublicIdentity):
            raise TypeError(f"identity must be a PublicIdentity. Got {type(identity).__name__}.")
        if identity.algorithm != ML_DSA_65_METADATA.name:
            raise UnsupportedAlgorithmError(
                f"Trusted identity {identity.owner!r} uses unsupported algorithm {identity.algorithm!r}."
            )
        self._identities[identity.owner] = identity

    def lookup(self, owner: str) -> PublicIdentity:
        """Return a pre-provisioned identity or raise an explicit trust error."""

        clean_owner = _validated_identity_name(owner)
        try:
            return self._identities[clean_owner]
        except KeyError as exc:
            raise UnknownTrustedPeerError(f"Peer {clean_owner!r} is not trusted.") from exc

    @property
    def owners(self) -> tuple[str, ...]:
        """Return trusted owner names in deterministic order."""

        return tuple(sorted(self._identities))

    def __contains__(self, owner: object) -> bool:
        return isinstance(owner, str) and owner.strip() in self._identities

    def __iter__(self) -> Iterator[PublicIdentity]:
        for owner in self.owners:
            yield self._identities[owner]

    def __len__(self) -> int:
        return len(self._identities)

    def __repr__(self) -> str:
        return f"TrustedIdentityStore(owners={self.owners!r})"
