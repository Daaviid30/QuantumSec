"""Tests for Alice-side authenticated processing of server KEM offers."""

from dataclasses import fields, replace
from unittest.mock import patch

import pytest

from pqc import (
    HQC3,
    MLKEM768,
    EncapsulationResponse,
    PQCParty,
    PQCProfile,
    ProcessedServerOffer,
    PublicIdentity,
    ServerKeyOfferFactory,
    ServerKeyOfferProcessor,
    ServerOfferProcessingStatus,
    SignedServerKeyOffer,
)
from pqc.backends.oqs_kem_backend import OQSKEMBackend
from pqc.kem import hqc_3_metadata, ml_kem_768_metadata
from pqc.profiles import profile_definition
from pqc.protocol import InitiatorKEMState
from pqc.protocol.messages import SERVER_KEY_OFFER_NONCE_LENGTH


@pytest.fixture(scope="module")
def bob() -> PQCParty:
    return PQCParty.create("Bob")


@pytest.fixture(scope="module")
def alice(bob: PQCParty) -> PQCParty:
    initiator = PQCParty.create("Alice")
    initiator.trust_peer(bob.public_identity)
    return initiator


@pytest.fixture(scope="module")
def low_offer(bob: PQCParty) -> SignedServerKeyOffer:
    return ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.LOW)[1]


@pytest.fixture(scope="module")
def high_offer(bob: PQCParty) -> SignedServerKeyOffer:
    return ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.HIGH)[1]


def _require_success(
    result: ProcessedServerOffer,
) -> tuple[InitiatorKEMState, EncapsulationResponse]:
    assert result.authenticated
    assert result.status is ServerOfferProcessingStatus.AUTHENTICATED
    assert result.failure_reason is None
    assert result.initiator_state is not None
    assert result.public_encapsulation is not None
    return result.initiator_state, result.public_encapsulation


def test_valid_low_offer_authenticates_before_ml_kem_encapsulation(
    alice: PQCParty,
    low_offer: SignedServerKeyOffer,
) -> None:
    result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=low_offer)
    state, public = _require_success(result)
    ml_secret = object.__getattribute__(state, "_ml_kem_shared_secret")

    assert result.signer == "Bob"
    assert result.profile is PQCProfile.LOW
    assert state.session_id == low_offer.offer.session_id == public.session_id
    assert state.profile is public.profile is PQCProfile.LOW
    assert len(ml_secret) == ml_kem_768_metadata().shared_secret_length
    assert len(public.ml_kem_ciphertext) == ml_kem_768_metadata().ciphertext_length
    assert object.__getattribute__(state, "_hqc_shared_secret") is None
    assert public.hqc_algorithm is None
    assert public.hqc_ciphertext is None


def test_valid_high_offer_authenticates_before_dual_kem_encapsulation(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    state, public = _require_success(result)
    ml_secret = object.__getattribute__(state, "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(state, "_hqc_shared_secret")

    assert state.session_id == high_offer.offer.session_id == public.session_id
    assert state.profile is public.profile is PQCProfile.HIGH
    assert len(ml_secret) == ml_kem_768_metadata().shared_secret_length
    assert len(public.ml_kem_ciphertext) == ml_kem_768_metadata().ciphertext_length
    assert hqc_secret is not None
    assert len(hqc_secret) == hqc_3_metadata().shared_secret_length
    assert public.hqc_algorithm == "HQC-3"
    assert public.hqc_ciphertext is not None
    assert len(public.hqc_ciphertext) == hqc_3_metadata().ciphertext_length


def test_untrusted_bob_aborts_without_encapsulation(
    low_offer: SignedServerKeyOffer,
) -> None:
    unprovisioned_alice = PQCParty.create("Unprovisioned Alice")

    with (
        patch.object(MLKEM768, "encapsulate") as ml_encapsulate,
        patch.object(HQC3, "encapsulate") as hqc_encapsulate,
    ):
        result = ServerKeyOfferProcessor().process(
            initiator=unprovisioned_alice,
            signed_offer=low_offer,
        )

    assert not result.authenticated
    assert result.status is ServerOfferProcessingStatus.UNTRUSTED_SIGNER
    assert result.initiator_state is None
    assert result.public_encapsulation is None
    assert result.failure_reason is not None and "trust store" in result.failure_reason
    ml_encapsulate.assert_not_called()
    hqc_encapsulate.assert_not_called()


def test_tampered_offer_aborts_before_any_encapsulation(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    tampered_offer = replace(
        high_offer.offer,
        nonce=b"T" * SERVER_KEY_OFFER_NONCE_LENGTH,
    )
    tampered = replace(high_offer, offer=tampered_offer)

    with (
        patch.object(MLKEM768, "encapsulate") as ml_encapsulate,
        patch.object(HQC3, "encapsulate") as hqc_encapsulate,
    ):
        result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=tampered)

    assert not result.authenticated
    assert result.status is ServerOfferProcessingStatus.INVALID_SIGNATURE
    assert result.initiator_state is None
    assert result.public_encapsulation is None
    ml_encapsulate.assert_not_called()
    hqc_encapsulate.assert_not_called()


def test_wrong_trusted_bob_key_aborts_without_encapsulation(
    bob: PQCParty,
    low_offer: SignedServerKeyOffer,
) -> None:
    mallory = PQCParty.create("Mallory")
    wrong_bob_identity = PublicIdentity(
        owner=bob.name,
        algorithm=mallory.public_identity.algorithm,
        public_key=mallory.public_identity.public_key,
    )
    alice_with_wrong_key = PQCParty.create("Alice with wrong key")
    alice_with_wrong_key.trust_peer(wrong_bob_identity)

    with patch.object(MLKEM768, "encapsulate") as ml_encapsulate:
        result = ServerKeyOfferProcessor().process(
            initiator=alice_with_wrong_key,
            signed_offer=low_offer,
        )

    assert result.status is ServerOfferProcessingStatus.INVALID_SIGNATURE
    assert result.initiator_state is None
    assert result.public_encapsulation is None
    ml_encapsulate.assert_not_called()


def test_signature_algorithm_mismatch_aborts_before_verification_or_encapsulation(
    alice: PQCParty,
    low_offer: SignedServerKeyOffer,
) -> None:
    inconsistent = replace(low_offer)
    object.__setattr__(inconsistent, "signature_algorithm", "ML-DSA-44")

    with (
        patch.object(PublicIdentity, "verify") as verify,
        patch.object(MLKEM768, "encapsulate") as ml_encapsulate,
    ):
        result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=inconsistent)

    assert result.status is ServerOfferProcessingStatus.ALGORITHM_MISMATCH
    verify.assert_not_called()
    ml_encapsulate.assert_not_called()


def test_shared_secrets_exist_only_in_private_initiator_state(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    state, public = _require_success(result)
    ml_secret = object.__getattribute__(state, "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(state, "_hqc_shared_secret")

    assert hqc_secret is not None
    assert all("secret" not in item.name for item in fields(public))
    assert ml_secret != public.ml_kem_ciphertext
    assert hqc_secret != public.hqc_ciphertext
    assert repr(ml_secret) not in repr(state)
    assert repr(hqc_secret) not in repr(state)
    assert repr(ml_secret) not in repr(result)
    assert repr(hqc_secret) not in repr(result)
    assert ml_secret not in high_offer.offer.canonical_bytes()
    assert hqc_secret not in high_offer.offer.canonical_bytes()
    assert ml_secret not in high_offer.signature
    assert hqc_secret not in high_offer.signature


def test_repeated_processing_uses_fresh_kem_randomness(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    first = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    second = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    _, first_public = _require_success(first)
    _, second_public = _require_success(second)

    assert first_public.ml_kem_ciphertext != second_public.ml_kem_ciphertext
    assert first_public.hqc_ciphertext != second_public.hqc_ciphertext


def test_alice_processing_never_decapsulates(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    with patch.object(OQSKEMBackend, "decapsulate") as decapsulate:
        result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)

    assert result.authenticated
    decapsulate.assert_not_called()


def test_public_response_rejects_profile_inconsistencies(
    alice: PQCParty,
    low_offer: SignedServerKeyOffer,
    high_offer: SignedServerKeyOffer,
) -> None:
    _, low_public = _require_success(
        ServerKeyOfferProcessor().process(initiator=alice, signed_offer=low_offer)
    )
    _, high_public = _require_success(
        ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    )

    with pytest.raises(ValueError, match="LOW encapsulation response must not contain HQC"):
        replace(
            low_public,
            hqc_algorithm=high_public.hqc_algorithm,
            hqc_ciphertext=high_public.hqc_ciphertext,
        )
    with pytest.raises(ValueError, match="HIGH encapsulation response must contain"):
        replace(high_public, hqc_algorithm=None, hqc_ciphertext=None)


@pytest.mark.parametrize("offer_fixture", ["low_offer", "high_offer"])
def test_encapsulation_response_transport_round_trip(
    alice: PQCParty,
    offer_fixture: str,
    request: pytest.FixtureRequest,
) -> None:
    signed_offer = request.getfixturevalue(offer_fixture)
    _, public = _require_success(
        ServerKeyOfferProcessor().process(initiator=alice, signed_offer=signed_offer)
    )

    payload = public.to_dict()
    restored = EncapsulationResponse.from_dict(payload)

    assert restored == public
    assert restored.__class__.__module__ == "pqc.protocol.messages"
    assert isinstance(payload["session_id"], str)
    assert isinstance(payload["ml_kem_ciphertext"], str)
    assert all("secret" not in field_name for field_name in payload)


def test_encapsulation_response_transport_rejects_invalid_base64(
    alice: PQCParty,
    low_offer: SignedServerKeyOffer,
) -> None:
    _, public = _require_success(ServerKeyOfferProcessor().process(initiator=alice, signed_offer=low_offer))
    payload = public.to_dict()
    payload["ml_kem_ciphertext"] = "not Base64!"

    with pytest.raises(ValueError, match="ml_kem_ciphertext must be valid Base64"):
        EncapsulationResponse.from_dict(payload)


def test_initiator_state_close_releases_secret_references(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    state, _ = _require_success(result)
    ml_secret = object.__getattribute__(state, "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(state, "_hqc_shared_secret")

    state.close()
    state.close()

    assert state.is_closed
    assert object.__getattribute__(state, "_ml_kem_shared_secret") is None
    assert object.__getattribute__(state, "_hqc_shared_secret") is None
    assert repr(ml_secret) not in repr(state)
    assert repr(hqc_secret) not in repr(state)


def test_initiator_state_context_manager_closes_on_exception(
    alice: PQCParty,
    high_offer: SignedServerKeyOffer,
) -> None:
    result = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=high_offer)
    state, _ = _require_success(result)

    with pytest.raises(RuntimeError, match="abort handshake"):
        with state as managed_state:
            assert managed_state is state
            raise RuntimeError("abort handshake")

    assert state.is_closed
    assert object.__getattribute__(state, "_ml_kem_shared_secret") is None
    assert object.__getattribute__(state, "_hqc_shared_secret") is None


def test_profile_algorithm_matching_uses_semantic_profile_fields(
    high_offer: SignedServerKeyOffer,
) -> None:
    definition = profile_definition(PQCProfile.HIGH)
    swapped = replace(
        definition,
        ml_kem_algorithm=definition.hqc_algorithm or "",
        hqc_algorithm=definition.ml_kem_algorithm,
    )

    with patch("pqc.protocol.initiator.profile_definition", return_value=swapped):
        assert not ServerKeyOfferProcessor._offer_algorithms_match_profile(high_offer.offer)
