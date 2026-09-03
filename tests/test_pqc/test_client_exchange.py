"""Tests for authenticated Alice responses and Bob-side KEM decapsulation."""

import base64
from dataclasses import dataclass, fields, replace
from hashlib import sha384
from unittest.mock import patch

import pytest

from pqc import (
    HQC3,
    MLKEM768,
    ClientKeyExchange,
    ClientKeyExchangeFactory,
    ClientKeyExchangeProcessingStatus,
    ClientKeyExchangeProcessor,
    PQCParty,
    PQCProfile,
    ProcessedServerOffer,
    PublicIdentity,
    ServerKeyOfferFactory,
    ServerKeyOfferProcessor,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
)
from pqc.errors import BackendOperationError
from pqc.protocol import InitiatorKEMState, ResponderKEMState, ResponderSharedSecretState
from pqc.protocol.messages import (
    CLIENT_KEY_EXCHANGE_DOMAIN_SEPARATOR,
    CLIENT_KEY_EXCHANGE_NONCE_LENGTH,
    CLIENT_KEY_EXCHANGE_SERVER_OFFER_HASH_LENGTH,
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
)


@dataclass(slots=True)
class _Phase4Flow:
    alice: PQCParty
    bob: PQCParty
    responder_kem_state: ResponderKEMState
    server_offer: SignedServerKeyOffer
    processed_offer: ProcessedServerOffer
    signed_exchange: SignedClientKeyExchange


def _prepare_phase3(
    profile: PQCProfile,
    *,
    bob_trusts_alice: bool = True,
) -> tuple[PQCParty, PQCParty, ResponderKEMState, SignedServerKeyOffer, ProcessedServerOffer]:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    if bob_trusts_alice:
        bob.trust_peer(alice.public_identity)
    responder_state, server_offer = ServerKeyOfferFactory().create(
        responder=bob,
        profile=profile,
    )
    processed_offer = ServerKeyOfferProcessor().process(
        initiator=alice,
        signed_offer=server_offer,
    )
    assert processed_offer.authenticated
    return alice, bob, responder_state, server_offer, processed_offer


def _create_flow(profile: PQCProfile, *, bob_trusts_alice: bool = True) -> _Phase4Flow:
    alice, bob, responder_state, server_offer, processed_offer = _prepare_phase3(
        profile,
        bob_trusts_alice=bob_trusts_alice,
    )
    signed_exchange = ClientKeyExchangeFactory().create(
        initiator=alice,
        signed_server_offer=server_offer,
        processed_offer=processed_offer,
    )
    return _Phase4Flow(
        alice=alice,
        bob=bob,
        responder_kem_state=responder_state,
        server_offer=server_offer,
        processed_offer=processed_offer,
        signed_exchange=signed_exchange,
    )


def _private_initiator_state(flow: _Phase4Flow) -> InitiatorKEMState:
    state = flow.processed_offer.initiator_state
    assert state is not None
    return state


def _process(flow: _Phase4Flow):  # type: ignore[no-untyped-def]
    return ClientKeyExchangeProcessor().process(
        responder=flow.bob,
        responder_state=flow.responder_kem_state,
        server_offer=flow.server_offer,
        signed_exchange=flow.signed_exchange,
    )


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_valid_phase4_flow_recovers_matching_independent_kem_secrets(profile: PQCProfile) -> None:
    flow = _create_flow(profile)
    result = _process(flow)

    assert result.authenticated
    assert result.status is ClientKeyExchangeProcessingStatus.AUTHENTICATED_AND_DECAPSULATED
    assert result.failure_reason is None
    assert result.responder_state is not None
    assert result.signer == "Alice"
    assert flow.responder_kem_state.is_closed

    alice_state = _private_initiator_state(flow)
    bob_state = result.responder_state
    assert object.__getattribute__(alice_state, "_ml_kem_shared_secret") == object.__getattribute__(
        bob_state,
        "_ml_kem_shared_secret",
    )
    assert object.__getattribute__(alice_state, "_hqc_shared_secret") == object.__getattribute__(
        bob_state,
        "_hqc_shared_secret",
    )


def test_client_exchange_binds_existing_phase3_response_without_reencapsulation() -> None:
    alice, _, _, server_offer, processed_offer = _prepare_phase3(PQCProfile.HIGH)
    public_response = processed_offer.public_encapsulation
    assert public_response is not None

    with (
        patch.object(MLKEM768, "encapsulate") as ml_encapsulate,
        patch.object(HQC3, "encapsulate") as hqc_encapsulate,
    ):
        signed_exchange = ClientKeyExchangeFactory().create(
            initiator=alice,
            signed_server_offer=server_offer,
            processed_offer=processed_offer,
        )
        second_signed_exchange = ClientKeyExchangeFactory().create(
            initiator=alice,
            signed_server_offer=server_offer,
            processed_offer=processed_offer,
        )

    exchange = signed_exchange.exchange
    assert exchange.ml_kem_ciphertext == public_response.ml_kem_ciphertext
    assert exchange.hqc_ciphertext == public_response.hqc_ciphertext
    assert len(exchange.client_nonce) == CLIENT_KEY_EXCHANGE_NONCE_LENGTH
    assert exchange.client_nonce != second_signed_exchange.exchange.client_nonce
    assert exchange.server_offer_hash == sha384(server_offer.offer.canonical_bytes()).digest()
    assert alice.public_identity.verify(exchange.canonical_bytes(), signed_exchange.signature)
    ml_encapsulate.assert_not_called()
    hqc_encapsulate.assert_not_called()


def test_factory_rejects_failed_phase3_result() -> None:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    responder_state, server_offer = ServerKeyOfferFactory().create(
        responder=bob,
        profile=PQCProfile.LOW,
    )
    rejected = ServerKeyOfferProcessor().process(initiator=alice, signed_offer=server_offer)

    with pytest.raises(ValueError, match="authenticated Phase 3"):
        ClientKeyExchangeFactory().create(
            initiator=alice,
            signed_server_offer=server_offer,
            processed_offer=rejected,
        )

    assert not responder_state.is_closed


def test_untrusted_alice_is_rejected_before_decapsulation() -> None:
    flow = _create_flow(PQCProfile.HIGH, bob_trusts_alice=False)

    with (
        patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate,
        patch.object(ResponderKEMState, "decapsulate_hqc") as hqc_decapsulate,
    ):
        result = _process(flow)

    assert result.status is ClientKeyExchangeProcessingStatus.UNTRUSTED_SIGNER
    assert result.responder_state is None
    assert result.failure_reason is not None
    assert not flow.responder_kem_state.is_closed
    ml_decapsulate.assert_not_called()
    hqc_decapsulate.assert_not_called()


def test_tampered_client_exchange_is_rejected_before_decapsulation() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    ciphertext = flow.signed_exchange.exchange.ml_kem_ciphertext
    tampered_exchange = replace(
        flow.signed_exchange.exchange,
        ml_kem_ciphertext=bytes([ciphertext[0] ^ 1]) + ciphertext[1:],
    )
    flow.signed_exchange = replace(flow.signed_exchange, exchange=tampered_exchange)

    with (
        patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate,
        patch.object(ResponderKEMState, "decapsulate_hqc") as hqc_decapsulate,
    ):
        result = _process(flow)

    assert result.status is ClientKeyExchangeProcessingStatus.INVALID_SIGNATURE
    assert result.responder_state is None
    ml_decapsulate.assert_not_called()
    hqc_decapsulate.assert_not_called()


def test_wrong_trusted_alice_key_is_rejected_before_decapsulation() -> None:
    flow = _create_flow(PQCProfile.LOW)
    mallory = PQCParty.create("Mallory")
    wrong_alice_identity = PublicIdentity(
        owner=flow.alice.name,
        algorithm=mallory.public_identity.algorithm,
        public_key=mallory.public_identity.public_key,
    )
    wrong_bob = PQCParty.create("Bob")
    wrong_bob.trust_peer(wrong_alice_identity)
    flow.bob = wrong_bob

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        result = _process(flow)

    assert result.status is ClientKeyExchangeProcessingStatus.INVALID_SIGNATURE
    assert result.responder_state is None
    ml_decapsulate.assert_not_called()


def test_response_from_another_session_is_rejected_before_decapsulation() -> None:
    flow_a = _create_flow(PQCProfile.LOW)
    flow_b = _create_flow(PQCProfile.LOW)
    flow_b.signed_exchange = flow_a.signed_exchange

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        result = _process(flow_b)

    assert result.status is ClientKeyExchangeProcessingStatus.SESSION_MISMATCH
    assert result.responder_state is None
    ml_decapsulate.assert_not_called()


def test_wrong_offer_hash_is_rejected_even_with_valid_alice_signature() -> None:
    flow = _create_flow(PQCProfile.LOW)
    _, other_offer = ServerKeyOfferFactory().create(
        responder=flow.bob,
        profile=PQCProfile.LOW,
    )
    exchange = replace(
        flow.signed_exchange.exchange,
        server_offer_hash=sha384(other_offer.offer.canonical_bytes()).digest(),
    )
    flow.signed_exchange = SignedClientKeyExchange(
        exchange=exchange,
        signer=flow.alice.name,
        signature_algorithm=flow.signed_exchange.signature_algorithm,
        signature=flow.alice.sign(exchange.canonical_bytes()),
    )

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        result = _process(flow)

    assert result.status is ClientKeyExchangeProcessingStatus.OFFER_BINDING_MISMATCH
    assert result.responder_state is None
    ml_decapsulate.assert_not_called()


def test_profile_and_algorithm_mismatches_are_rejected_before_decapsulation() -> None:
    low = _create_flow(PQCProfile.LOW)
    high = _create_flow(PQCProfile.HIGH)
    high_exchange = replace(
        high.signed_exchange.exchange,
        session_id=low.responder_kem_state.session_id,
        server_offer_hash=sha384(low.server_offer.offer.canonical_bytes()).digest(),
    )
    low.signed_exchange = SignedClientKeyExchange(
        exchange=high_exchange,
        signer=low.alice.name,
        signature_algorithm=high.signed_exchange.signature_algorithm,
        signature=low.alice.sign(high_exchange.canonical_bytes()),
    )

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        profile_result = _process(low)

    assert profile_result.status is ClientKeyExchangeProcessingStatus.PROFILE_MISMATCH
    assert profile_result.responder_state is None
    ml_decapsulate.assert_not_called()

    algorithm_flow = _create_flow(PQCProfile.LOW)
    inconsistent_exchange = replace(algorithm_flow.signed_exchange.exchange)
    object.__setattr__(inconsistent_exchange, "ml_kem_algorithm", "ML-KEM-512")
    algorithm_flow.signed_exchange = SignedClientKeyExchange(
        exchange=inconsistent_exchange,
        signer=algorithm_flow.alice.name,
        signature_algorithm=algorithm_flow.signed_exchange.signature_algorithm,
        signature=algorithm_flow.alice.sign(inconsistent_exchange.canonical_bytes()),
    )

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        algorithm_result = _process(algorithm_flow)

    assert algorithm_result.status is ClientKeyExchangeProcessingStatus.ALGORITHM_MISMATCH
    assert algorithm_result.responder_state is None
    ml_decapsulate.assert_not_called()


def test_bob_decapsulates_but_never_encapsulates() -> None:
    flow = _create_flow(PQCProfile.HIGH)

    with (
        patch.object(MLKEM768, "encapsulate") as ml_encapsulate,
        patch.object(HQC3, "encapsulate") as hqc_encapsulate,
    ):
        result = _process(flow)

    assert result.authenticated
    ml_encapsulate.assert_not_called()
    hqc_encapsulate.assert_not_called()


def test_responder_kem_state_closes_only_after_all_decapsulations_succeed() -> None:
    flow = _create_flow(PQCProfile.HIGH)

    with patch.object(HQC3, "decapsulate", side_effect=BackendOperationError("HQC failure")):
        with pytest.raises(BackendOperationError, match="HQC failure"):
            _process(flow)

    assert not flow.responder_kem_state.is_closed
    assert flow.responder_kem_state.ml_kem_public_key == flow.server_offer.offer.ml_kem_public_key


def test_closed_responder_state_cannot_be_reused_after_success() -> None:
    flow = _create_flow(PQCProfile.LOW)
    assert _process(flow).authenticated

    with patch.object(ResponderKEMState, "decapsulate_ml_kem") as ml_decapsulate:
        replay = _process(flow)

    assert replay.status is ClientKeyExchangeProcessingStatus.RESPONDER_STATE_CLOSED
    assert replay.responder_state is None
    ml_decapsulate.assert_not_called()


def test_low_responder_state_rejects_hqc_decapsulation() -> None:
    flow = _create_flow(PQCProfile.LOW)

    with pytest.raises(RuntimeError, match="does not contain an HQC key pair"):
        flow.responder_kem_state.decapsulate_hqc(b"not-an-hqc-ciphertext")

    assert not flow.responder_kem_state.is_closed


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_signed_client_exchange_transport_round_trip(profile: PQCProfile) -> None:
    signed_exchange = _create_flow(profile).signed_exchange

    payload = signed_exchange.to_dict()
    restored = SignedClientKeyExchange.from_dict(payload)

    exchange_payload = payload["exchange"]
    assert isinstance(exchange_payload, dict)
    assert restored == signed_exchange
    assert restored.exchange.canonical_bytes() == signed_exchange.exchange.canonical_bytes()
    assert isinstance(exchange_payload["session_id"], str)
    assert isinstance(exchange_payload["client_nonce"], str)
    assert isinstance(exchange_payload["server_offer_hash"], str)
    assert isinstance(exchange_payload["ml_kem_ciphertext"], str)
    assert isinstance(payload["signature"], str)


def test_client_exchange_transport_rejects_invalid_base64() -> None:
    payload = _create_flow(PQCProfile.LOW).signed_exchange.to_dict()
    exchange_payload = payload["exchange"]
    assert isinstance(exchange_payload, dict)
    exchange_payload["server_offer_hash"] = "not Base64!"

    with pytest.raises(ValueError, match="server_offer_hash must be valid Base64"):
        SignedClientKeyExchange.from_dict(payload)


def test_client_exchange_transport_rejects_wrong_offer_hash_length() -> None:
    payload = _create_flow(PQCProfile.LOW).signed_exchange.to_dict()
    exchange_payload = payload["exchange"]
    assert isinstance(exchange_payload, dict)
    exchange_payload["server_offer_hash"] = base64.b64encode(b"short digest").decode("ascii")

    with pytest.raises(ValueError, match="server_offer_hash must contain 48 bytes"):
        SignedClientKeyExchange.from_dict(payload)


def test_client_canonical_serialization_authenticates_every_field() -> None:
    low = _create_flow(PQCProfile.LOW).signed_exchange.exchange
    high = _create_flow(PQCProfile.HIGH).signed_exchange.exchange
    baseline = low.canonical_bytes()
    changed_algorithm = replace(low)
    object.__setattr__(changed_algorithm, "ml_kem_algorithm", "ML-KEM-769")
    ciphertext = low.ml_kem_ciphertext
    high_ciphertext = high.hqc_ciphertext
    assert high_ciphertext is not None
    changed_nonce = bytes([low.client_nonce[0] ^ 1]) + low.client_nonce[1:]

    assert baseline == replace(low).canonical_bytes()
    assert CLIENT_KEY_EXCHANGE_DOMAIN_SEPARATOR in baseline
    assert replace(low, session_id=b"S" * SERVER_KEY_OFFER_SESSION_ID_LENGTH).canonical_bytes() != baseline
    assert replace(low, client_nonce=changed_nonce).canonical_bytes() != baseline
    assert (
        replace(low, server_offer_hash=b"H" * CLIENT_KEY_EXCHANGE_SERVER_OFFER_HASH_LENGTH).canonical_bytes()
        != baseline
    )
    assert (
        replace(
            low,
            ml_kem_ciphertext=bytes([ciphertext[0] ^ 1]) + ciphertext[1:],
        ).canonical_bytes()
        != baseline
    )
    assert changed_algorithm.canonical_bytes() != baseline
    assert high.canonical_bytes() != baseline
    assert (
        replace(
            high,
            hqc_ciphertext=bytes([high_ciphertext[0] ^ 1]) + high_ciphertext[1:],
        ).canonical_bytes()
        != high.canonical_bytes()
    )


def test_public_messages_and_reprs_never_expose_shared_secrets() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    result = _process(flow)
    assert result.responder_state is not None
    alice_state = _private_initiator_state(flow)
    alice_ml_secret = object.__getattribute__(alice_state, "_ml_kem_shared_secret")
    alice_hqc_secret = object.__getattribute__(alice_state, "_hqc_shared_secret")
    bob_ml_secret = object.__getattribute__(result.responder_state, "_ml_kem_shared_secret")
    bob_hqc_secret = object.__getattribute__(result.responder_state, "_hqc_shared_secret")
    public_bytes = flow.signed_exchange.exchange.canonical_bytes()
    public_repr = repr(flow.signed_exchange) + repr(result)

    assert all("secret" not in item.name for item in fields(ClientKeyExchange))
    assert all("secret" not in key for key in flow.signed_exchange.to_dict())
    for secret in (alice_ml_secret, alice_hqc_secret, bob_ml_secret, bob_hqc_secret):
        assert secret is not None
        assert secret not in public_bytes
        assert repr(secret) not in public_repr


def test_responder_shared_secret_state_close_releases_secret_references() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    result = _process(flow)
    state = result.responder_state
    assert isinstance(state, ResponderSharedSecretState)
    ml_secret = object.__getattribute__(state, "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(state, "_hqc_shared_secret")

    with state as managed_state:
        assert managed_state is state
        assert not state.is_closed

    state.close()

    assert state.is_closed
    assert object.__getattribute__(state, "_ml_kem_shared_secret") is None
    assert object.__getattribute__(state, "_hqc_shared_secret") is None
    assert repr(ml_secret) not in repr(state)
    assert repr(hqc_secret) not in repr(state)
