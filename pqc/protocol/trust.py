"""Explicit pre-provisioned trust for public PQC identities."""

from collections.abc import Iterator

from pqc.errors import TrustedIdentityConflictError, UnknownTrustedPeerError
from pqc.protocol.identity import PublicIdentity, _validated_identity_name


class TrustedIdentityStore:
    """Map peer names to public identities trusted out of band."""

    __slots__ = ("_identities",)

    def __init__(self) -> None:
        self._identities: dict[str, PublicIdentity] = {}

    def trust(self, identity: PublicIdentity, *, overwrite: bool = False) -> None:
        """Explicitly provision a peer, rejecting silent key replacement."""

        if not isinstance(identity, PublicIdentity):
            raise TypeError(f"identity must be a PublicIdentity. Got {type(identity).__name__}.")
        if not isinstance(overwrite, bool):
            raise TypeError(f"overwrite must be a bool. Got {type(overwrite).__name__}.")
        if identity.owner in self._identities and not overwrite:
            raise TrustedIdentityConflictError(
                f"Identity for {identity.owner!r} is already trusted; pass overwrite=True to replace it."
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
