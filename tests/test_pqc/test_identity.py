"""Tests for private and public ML-DSA identity boundaries."""

from dataclasses import FrozenInstanceError, fields

import pytest

from pqc.errors import UnsupportedAlgorithmError
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


def test_public_identity_verifies_without_private_identity(alice_identity: MLDSAIdentity) -> None:
    public_identity = alice_identity.public_identity
    message = b"passive verifier"

    assert public_identity.verify(message, alice_identity.sign(message))


def test_public_identity_validates_known_algorithm_key_length() -> None:
    with pytest.raises(ValueError, match="must contain 1952 bytes"):
        PublicIdentity(owner="Alice", algorithm="ML-DSA-65", public_key=b"truncated")


def test_public_identity_serialization_round_trip(alice_identity: MLDSAIdentity) -> None:
    public_identity = alice_identity.public_identity

    restored = PublicIdentity.from_dict(public_identity.to_dict())

    assert restored == public_identity
    assert restored.public_key == public_identity.public_key


def test_public_identity_rejects_invalid_base64() -> None:
    with pytest.raises(ValueError, match="valid Base64"):
        PublicIdentity.from_dict({"owner": "Alice", "algorithm": "ML-DSA-65", "public_key": "not base64!"})


def test_unicode_identity_name_is_preserved() -> None:
    identity = MLDSAIdentity.generate("  Álvaro  ")

    assert identity.owner == "Álvaro"
    assert identity.public_identity.owner == "Álvaro"


def test_unknown_public_algorithm_fails_only_when_verification_is_requested() -> None:
    identity = PublicIdentity(owner="Future", algorithm="FUTURE-SIG", public_key=b"public")

    with pytest.raises(UnsupportedAlgorithmError, match="No signature verifier"):
        identity.verify(b"message", b"signature")
