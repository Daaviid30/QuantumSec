"""Tests for parties and explicit pre-provisioned trust."""

import pytest

from pqc import PQCParty
from pqc.errors import UnknownTrustedPeerError, UnsupportedAlgorithmError
from pqc.protocol import PublicIdentity


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


def test_trust_store_rejects_non_ml_dsa_identity(alice: PQCParty) -> None:
    unsupported = PublicIdentity(owner="Legacy", algorithm="ECDSA", public_key=b"public")

    with pytest.raises(UnsupportedAlgorithmError, match="unsupported algorithm"):
        alice.trust_peer(unsupported)


def test_party_representation_contains_no_key_material(alice: PQCParty) -> None:
    public_key = alice.public_identity.public_key

    assert repr(public_key) not in repr(alice)
    assert "Alice" in repr(alice)
