"""Explicit pre-provisioned trust for public PQC identities."""

from collections.abc import Iterator

from pqc.errors import TrustedIdentityConflictError, UnknownTrustedPeerError
from pqc.protocol.identity import PublicIdentity, _validated_identity_name


class TrustedIdentityStore:
    """Thread-safe in-memory registry mapping peer names to pre-provisioned trusted PublicIdentity objects."""

    __slots__ = ("_identities",)

    def __init__(self) -> None:
        """Initialize an empty trusted identity store."""
        self._identities: dict[str, PublicIdentity] = {}

    def trust(self, identity: PublicIdentity, *, overwrite: bool = False) -> None:
        """Register a public identity as trusted, raising an error if already present unless overwrite."""

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
        """Return the trusted public identity for an owner, raising UnknownTrustedPeerError if absent."""

        clean_owner = _validated_identity_name(owner)
        try:
            return self._identities[clean_owner]
        except KeyError as exc:
            raise UnknownTrustedPeerError(f"Peer {clean_owner!r} is not trusted.") from exc

    @property
    def owners(self) -> tuple[str, ...]:
        """Return a sorted tuple of all trusted owner names registered in the store."""

        return tuple(sorted(self._identities))

    def __contains__(self, owner: object) -> bool:
        """Check whether an owner name is registered in the trusted identity store."""
        return isinstance(owner, str) and owner.strip() in self._identities

    def __iter__(self) -> Iterator[PublicIdentity]:
        """Iterate over all trusted public identities in deterministic owner order."""
        for owner in self.owners:
            yield self._identities[owner]

    def __len__(self) -> int:
        """Return the total number of trusted peer identities in the store."""
        return len(self._identities)

    def __repr__(self) -> str:
        """Return a string representation listing registered trusted owner names."""
        return f"TrustedIdentityStore(owners={self.owners!r})"
