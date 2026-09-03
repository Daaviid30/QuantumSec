"""Tests for ephemeral responder state and authenticated ServerKeyOffer messages."""

from dataclasses import fields, replace

import pytest

from pqc import (
    HQC3,
    MLKEM768,
    PQCParty,
    PQCProfile,
    ServerKeyOffer,
    ServerKeyOfferFactory,
    SignedServerKeyOffer,
)
from pqc.kem import HQC_3_ALGORITHM, ML_KEM_768_ALGORITHM
from pqc.protocol import ResponderKEMState
from pqc.protocol.messages import (
    SERVER_KEY_OFFER_DOMAIN_SEPARATOR,
    SERVER_KEY_OFFER_NONCE_LENGTH,
    SERVER_KEY_OFFER_PROTOCOL_VERSION,
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
)

OfferCreation = tuple[ResponderKEMState, SignedServerKeyOffer]


@pytest.fixture(scope="module")
def bob() -> PQCParty:
    return PQCParty.create("Bob")


@pytest.fixture(scope="module")
def low_creation(bob: PQCParty) -> OfferCreation:
    return ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.LOW)


@pytest.fixture(scope="module")
def high_creation(bob: PQCParty) -> OfferCreation:
    return ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.HIGH)


def test_low_offer_contains_only_ml_kem(low_creation: OfferCreation) -> None:
    state, signed_offer = low_creation
    offer = signed_offer.offer

    assert state.profile is PQCProfile.LOW
    assert offer.protocol_version == SERVER_KEY_OFFER_PROTOCOL_VERSION
    assert offer.profile is PQCProfile.LOW
    assert len(offer.session_id) == SERVER_KEY_OFFER_SESSION_ID_LENGTH
    assert state.session_id == offer.session_id
    assert len(offer.nonce) == SERVER_KEY_OFFER_NONCE_LENGTH
    assert offer.ml_kem_algorithm == ML_KEM_768_ALGORITHM
    assert offer.ml_kem_public_key == state.ml_kem_public_key
    assert offer.hqc_algorithm is None
    assert offer.hqc_public_key is None
    assert state.hqc_public_key is None


def test_high_offer_contains_ml_kem_and_hqc(high_creation: OfferCreation) -> None:
    state, signed_offer = high_creation
    offer = signed_offer.offer

    assert state.profile is PQCProfile.HIGH
    assert offer.profile is PQCProfile.HIGH
    assert offer.ml_kem_algorithm == ML_KEM_768_ALGORITHM
    assert offer.ml_kem_public_key == state.ml_kem_public_key
    assert offer.hqc_algorithm == HQC_3_ALGORITHM
    assert offer.hqc_public_key == state.hqc_public_key
    assert offer.hqc_public_key


def test_server_offer_rejects_profile_inconsistencies(
    low_creation: OfferCreation,
    high_creation: OfferCreation,
) -> None:
    low = low_creation[1].offer
    high = high_creation[1].offer

    with pytest.raises(ValueError, match="LOW ServerKeyOffer must not contain HQC"):
        replace(low, hqc_algorithm=HQC_3_ALGORITHM, hqc_public_key=high.hqc_public_key)
    with pytest.raises(ValueError, match="HIGH ServerKeyOffer must contain"):
        replace(high, hqc_algorithm=None, hqc_public_key=None)
    with pytest.raises(ValueError, match="ml_kem_algorithm"):
        replace(low, ml_kem_algorithm="ML-KEM-512")
    with pytest.raises(ValueError, match="HIGH ServerKeyOffer must contain"):
        replace(high, hqc_algorithm="HQC-5")


def test_server_offer_rejects_malformed_public_key(low_creation: OfferCreation) -> None:
    with pytest.raises(ValueError, match="ml_kem_public_key must contain 1184 bytes"):
        replace(low_creation[1].offer, ml_kem_public_key=b"truncated")


def test_kem_material_is_ephemeral_between_offers(bob: PQCParty) -> None:
    factory = ServerKeyOfferFactory()
    low_one = factory.create(responder=bob, profile=PQCProfile.LOW)[1].offer
    low_two = factory.create(responder=bob, profile=PQCProfile.LOW)[1].offer
    high_one = factory.create(responder=bob, profile=PQCProfile.HIGH)[1].offer
    high_two = factory.create(responder=bob, profile=PQCProfile.HIGH)[1].offer

    assert low_one.ml_kem_public_key != low_two.ml_kem_public_key
    assert high_one.ml_kem_public_key != high_two.ml_kem_public_key
    assert high_one.hqc_public_key != high_two.hqc_public_key
    assert low_one.session_id != low_two.session_id
    assert low_one.nonce != low_two.nonce


def test_canonical_serialization_is_deterministic_and_domain_separated(
    low_creation: OfferCreation,
) -> None:
    offer = low_creation[1].offer

    assert offer.canonical_bytes() == replace(offer).canonical_bytes()
    assert SERVER_KEY_OFFER_DOMAIN_SEPARATOR in offer.canonical_bytes()
    assert b"ML-KEM-768" in offer.canonical_bytes()


@pytest.mark.parametrize("creation_fixture", ["low_creation", "high_creation"])
def test_signed_offer_transport_serialization_round_trip(
    creation_fixture: str,
    request: pytest.FixtureRequest,
) -> None:
    signed_offer = request.getfixturevalue(creation_fixture)[1]

    restored = SignedServerKeyOffer.from_dict(signed_offer.to_dict())

    assert restored == signed_offer
    assert restored.offer.canonical_bytes() == signed_offer.offer.canonical_bytes()


def test_offer_transport_parser_rejects_invalid_base64(low_creation: OfferCreation) -> None:
    payload = low_creation[1].offer.to_dict()
    payload["ml_kem_public_key"] = "not Base64!"

    with pytest.raises(ValueError, match="ml_kem_public_key must be valid Base64"):
        ServerKeyOffer.from_dict(payload)


def test_changing_any_offer_field_changes_canonical_bytes(
    low_creation: OfferCreation,
    high_creation: OfferCreation,
) -> None:
    low = low_creation[1].offer
    high = high_creation[1].offer
    baseline = low.canonical_bytes()
    other_ml_kem = MLKEM768.generate()
    other_hqc = HQC3.generate()

    assert replace(low, session_id=b"S" * SERVER_KEY_OFFER_SESSION_ID_LENGTH).canonical_bytes() != baseline
    assert replace(low, nonce=b"N" * SERVER_KEY_OFFER_NONCE_LENGTH).canonical_bytes() != baseline
    assert replace(low, ml_kem_public_key=other_ml_kem.public_key).canonical_bytes() != baseline
    assert high.canonical_bytes() != baseline
    assert replace(high, hqc_public_key=other_hqc.public_key).canonical_bytes() != high.canonical_bytes()
    assert baseline.replace(b"ML-KEM-768", b"ML-KEM-769") != baseline


def test_private_kem_keys_never_enter_offer_or_repr(low_creation: OfferCreation) -> None:
    state, signed_offer = low_creation
    ml_kem = object.__getattribute__(state, "_ml_kem")
    secret_key = object.__getattribute__(ml_kem, "_secret_key")
    canonical = signed_offer.offer.canonical_bytes()

    assert secret_key not in canonical
    assert repr(secret_key) not in repr(state)
    assert "secret" not in repr(state).lower()


def test_responder_state_close_releases_private_capabilities(bob: PQCParty) -> None:
    state, _ = ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.HIGH)

    state.close()
    state.close()

    assert state.is_closed
    assert object.__getattribute__(state, "_ml_kem") is None
    assert object.__getattribute__(state, "_hqc") is None
    with pytest.raises(RuntimeError, match="state is closed"):
        _ = state.ml_kem_public_key
    with pytest.raises(RuntimeError, match="state is closed"):
        _ = state.hqc_public_key


def test_responder_state_context_manager_closes_on_exit(bob: PQCParty) -> None:
    state, signed_offer = ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.HIGH)

    with state as managed_state:
        assert managed_state is state
        assert state.ml_kem_public_key == signed_offer.offer.ml_kem_public_key
        assert state.hqc_public_key == signed_offer.offer.hqc_public_key

    assert state.is_closed
    assert object.__getattribute__(state, "_ml_kem") is None
    assert object.__getattribute__(state, "_hqc") is None


def test_bob_signs_canonical_offer_with_existing_identity(
    bob: PQCParty,
    high_creation: OfferCreation,
) -> None:
    _, signed_offer = high_creation

    assert signed_offer.signer == "Bob"
    assert signed_offer.signature_algorithm == "ML-DSA-65"
    assert bob.public_identity.verify(signed_offer.offer.canonical_bytes(), signed_offer.signature)
    assert {item.name for item in fields(signed_offer)} == {
        "offer",
        "signer",
        "signature_algorithm",
        "signature",
    }


def test_tampered_offer_does_not_verify(
    bob: PQCParty,
    low_creation: OfferCreation,
) -> None:
    _, signed_offer = low_creation
    tampered = replace(signed_offer.offer, nonce=b"T" * SERVER_KEY_OFFER_NONCE_LENGTH)

    assert not bob.public_identity.verify(tampered.canonical_bytes(), signed_offer.signature)
