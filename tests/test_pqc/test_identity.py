"""Tests for private and public ML-DSA identity boundaries."""

from dataclasses import FrozenInstanceError, fields

import pytest

from pqc.protocol import MLDSAIdentity, PublicIdentity


@pytest.fixture(scope="module")
def alice_identity() -> MLDSAIdentity:
    return MLDSAIdentity.generate("Alice")


def test_public_identity_is_immutable_and_contains_only_public_material(
    alice_identity: MLDSAIdentity,
) -> None:
    public_identity = alice_identity.public_identity

    assert isinstance(public_identity, PublicIdentity)
    assert public_identity.owner == "Alice"
    assert public_identity.algorithm == "ML-DSA-65"
    assert isinstance(public_identity.public_key, bytes)
    assert public_identity.public_key
    assert {item.name for item in fields(public_identity)} == {"owner", "algorithm", "public_key"}
    assert not hasattr(public_identity, "secret_key")
    assert not hasattr(public_identity, "sign")

    with pytest.raises(FrozenInstanceError):
        public_identity.owner = "Mallory"  # type: ignore[misc]


def test_private_identity_signs_without_revealing_private_material(
    alice_identity: MLDSAIdentity,
) -> None:
    signature = alice_identity.sign(b"identity proof")

    assert signature
    assert "secret" not in repr(alice_identity).lower()
    assert "private" not in repr(alice_identity).lower()
    assert "ML-DSA-65" in repr(alice_identity)
