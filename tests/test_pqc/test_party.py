"""Tests for parties and explicit pre-provisioned trust."""

import pytest

from pqc import PQCParty
from pqc.errors import (
    TrustedIdentityConflictError,
    UnknownTrustedPeerError,
    UnsupportedAlgorithmError,
)
from pqc.protocol import MLDSAIdentity, PublicIdentity, TrustedIdentityStore


@pytest.fixture(scope="module")
def alice() -> PQCParty:
    return PQCParty.create("Alice")


@pytest.fixture(scope="module")
def bob() -> PQCParty:
    return PQCParty.create("Bob")


def test_trusted_alice_to_bob_signing_flow(alice: PQCParty, bob: PQCParty) -> None:
    bob.trust_peer(alice.public_identity)
    message = b"authenticated message"

    assert bob.verify("Alice", message, alice.sign(message))
    assert "Alice" in bob.trusted_peers


def test_untrusted_peer_fails_explicitly(alice: PQCParty) -> None:
    charlie = PQCParty.create("Charlie")
    message = b"trust must be provisioned out of band"

    with pytest.raises(UnknownTrustedPeerError, match="not trusted"):
        charlie.verify("Alice", message, alice.sign(message))


def test_received_public_data_does_not_create_trust(alice: PQCParty) -> None:
    recipient = PQCParty.create("Recipient")
    received_identity = alice.public_identity

    assert received_identity.owner == "Alice"
    assert len(recipient.trusted_peers) == 0
    with pytest.raises(UnknownTrustedPeerError):
        recipient.verify("Alice", b"message", alice.sign(b"message"))


def test_trust_store_is_not_coupled_to_ml_dsa(alice: PQCParty) -> None:
    unsupported = PublicIdentity(owner="Legacy", algorithm="ECDSA", public_key=b"public")

    alice.trust_peer(unsupported)

    assert alice.trusted_peers.lookup("Legacy") is unsupported
    with pytest.raises(UnsupportedAlgorithmError, match="No signature verifier"):
        alice.verify("Legacy", b"message", b"signature")


def test_trust_store_rejects_silent_key_replacement(alice: PQCParty) -> None:
    store = TrustedIdentityStore()
    original = alice.public_identity
    replacement = MLDSAIdentity.generate("Alice").public_identity
    store.trust(original)

    with pytest.raises(TrustedIdentityConflictError, match="already trusted"):
        store.trust(replacement)

    assert store.lookup("Alice") == original
    store.trust(replacement, overwrite=True)
    assert store.lookup("Alice") == replacement


def test_trust_store_collection_protocol(alice: PQCParty) -> None:
    store = TrustedIdentityStore()
    future = PublicIdentity(owner="Zoë", algorithm="FUTURE-SIG", public_key=b"public")
    store.trust(future)
    store.trust(alice.public_identity)

    assert len(store) == 2
    assert store.owners == ("Alice", "Zoë")
    assert tuple(identity.owner for identity in store) == store.owners
    assert " Zoë " in store


def test_party_representation_contains_no_key_material(alice: PQCParty) -> None:
    public_key = alice.public_identity.public_key

    assert repr(public_key) not in repr(alice)
    assert "Alice" in repr(alice)


def test_party_name_remains_bound_to_immutable_private_identity(alice: PQCParty) -> None:
    assert alice.name == alice.public_identity.owner

    with pytest.raises(AttributeError):
        alice.name = "Mallory"  # type: ignore[misc]
