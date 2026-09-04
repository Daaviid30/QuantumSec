"""Tests for canonical Phase 5 transcripts, KEM combination, and session-key derivation."""

from dataclasses import dataclass, replace
from unittest.mock import patch

import pytest

from pqc import (
    PQC_SESSION_KEY_LENGTH,
    ClientKeyExchangeFactory,
    ClientKeyExchangeProcessor,
    DerivedSessionKeyState,
    PQCHandshakeTranscript,
    PQCParty,
    PQCProfile,
    PQCSessionKeyDeriver,
    ProcessedClientKeyExchange,
    ProcessedServerOffer,
    ServerKeyOfferFactory,
    ServerKeyOfferProcessor,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
)
from pqc._encoding import _length_prefixed
from pqc.kdf import KEM_SECRET_INPUT_DOMAIN, canonical_kem_secret_input, derive_hkdf_sha384
from pqc.kem import hqc_3_metadata, ml_kem_768_metadata
from pqc.protocol import InitiatorKEMState, ResponderKEMState, ResponderSharedSecretState
from pqc.protocol.key_schedule import PQC_SESSION_KEY_INFO_DOMAIN, _session_key_info
from pqc.protocol.transcript import (
    PQC_HANDSHAKE_TRANSCRIPT_DOMAIN,
    PQC_TRANSCRIPT_HASH_LENGTH,
)


@dataclass(slots=True)
class _Phase5Flow:
    alice: PQCParty
    bob: PQCParty
    responder_kem_state: ResponderKEMState
    signed_server_offer: SignedServerKeyOffer
    processed_server_offer: ProcessedServerOffer
    signed_client_exchange: SignedClientKeyExchange
    processed_client_exchange: ProcessedClientKeyExchange


def _create_flow(profile: PQCProfile) -> _Phase5Flow:
    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    bob.trust_peer(alice.public_identity)

    responder_kem_state, signed_server_offer = ServerKeyOfferFactory().create(
        responder=bob,
        profile=profile,
    )
    processed_server_offer = ServerKeyOfferProcessor().process(
        initiator=alice,
        signed_offer=signed_server_offer,
    )
    signed_client_exchange = ClientKeyExchangeFactory().create(
        initiator=alice,
        signed_server_offer=signed_server_offer,
        processed_offer=processed_server_offer,
    )
    processed_client_exchange = ClientKeyExchangeProcessor().process(
        responder=bob,
        responder_state=responder_kem_state,
        server_offer=signed_server_offer,
        signed_exchange=signed_client_exchange,
    )
    assert processed_server_offer.authenticated
    assert processed_client_exchange.authenticated
    return _Phase5Flow(
        alice=alice,
        bob=bob,
        responder_kem_state=responder_kem_state,
        signed_server_offer=signed_server_offer,
        processed_server_offer=processed_server_offer,
        signed_client_exchange=signed_client_exchange,
        processed_client_exchange=processed_client_exchange,
    )


def _initiator_state(flow: _Phase5Flow) -> InitiatorKEMState:
    state = flow.processed_server_offer.initiator_state
    assert state is not None
    return state


def _responder_state(flow: _Phase5Flow) -> ResponderSharedSecretState:
    state = flow.processed_client_exchange.responder_state
    assert state is not None
    return state


def _derive_both(flow: _Phase5Flow) -> tuple[DerivedSessionKeyState, DerivedSessionKeyState]:
    deriver = PQCSessionKeyDeriver()
    alice_key = deriver.derive_initiator(
        processed_server_offer=flow.processed_server_offer,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    bob_key = deriver.derive_responder(
        processed_client_exchange=flow.processed_client_exchange,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    return alice_key, bob_key


def _flipped(value: bytes) -> bytes:
    return bytes([value[0] ^ 1]) + value[1:]


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_valid_phase5_flow_derives_matching_transcript_bound_session_keys(
    profile: PQCProfile,
) -> None:
    flow = _create_flow(profile)
    alice_key_state, bob_key_state = _derive_both(flow)
    alice_session_key = object.__getattribute__(alice_key_state, "_session_key")
    bob_session_key = object.__getattribute__(bob_key_state, "_session_key")
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )

    assert alice_session_key == bob_session_key
    assert alice_session_key is not None
    assert len(alice_session_key) == PQC_SESSION_KEY_LENGTH
    assert alice_key_state.transcript_hash == bob_key_state.transcript_hash == transcript.transcript_hash
    assert len(transcript.transcript_hash) == PQC_TRANSCRIPT_HASH_LENGTH
    assert not _initiator_state(flow).is_closed
    assert not _responder_state(flow).is_closed
    assert flow.responder_kem_state.is_closed

    alice_ml_secret = object.__getattribute__(_initiator_state(flow), "_ml_kem_shared_secret")
    bob_ml_secret = object.__getattribute__(_responder_state(flow), "_ml_kem_shared_secret")
    assert alice_ml_secret == bob_ml_secret
    if profile is PQCProfile.HIGH:
        alice_hqc_secret = object.__getattribute__(_initiator_state(flow), "_hqc_shared_secret")
        bob_hqc_secret = object.__getattribute__(_responder_state(flow), "_hqc_shared_secret")
        assert alice_hqc_secret == bob_hqc_secret


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_independent_sessions_derive_different_keys(profile: PQCProfile) -> None:
    first_alice_key, _ = _derive_both(_create_flow(profile))
    second_alice_key, _ = _derive_both(_create_flow(profile))

    assert first_alice_key.transcript_hash != second_alice_key.transcript_hash
    assert object.__getattribute__(first_alice_key, "_session_key") != object.__getattribute__(
        second_alice_key,
        "_session_key",
    )


def test_hkdf_sha384_is_deterministic_and_domain_separated() -> None:
    key_material = b"controlled KEM input"
    transcript_hash = b"T" * PQC_TRANSCRIPT_HASH_LENGTH
    session_info = b"QuantumSec test session purpose"
    finished_info = b"QuantumSec test finished purpose"

    first = derive_hkdf_sha384(
        key_material=key_material,
        salt=transcript_hash,
        info=session_info,
        length=PQC_SESSION_KEY_LENGTH,
    )
    second = derive_hkdf_sha384(
        key_material=key_material,
        salt=transcript_hash,
        info=session_info,
        length=PQC_SESSION_KEY_LENGTH,
    )
    different_purpose = derive_hkdf_sha384(
        key_material=key_material,
        salt=transcript_hash,
        info=finished_info,
        length=PQC_SESSION_KEY_LENGTH,
    )

    assert first == second
    assert first != different_purpose
    assert len(first) == PQC_SESSION_KEY_LENGTH


def test_session_key_info_binds_domain_version_and_profile() -> None:
    low_info = _session_key_info(protocol_version=1, profile=PQCProfile.LOW)
    high_info = _session_key_info(protocol_version=1, profile=PQCProfile.HIGH)

    assert _length_prefixed(PQC_SESSION_KEY_INFO_DOMAIN) in low_info
    assert b"\x00\x01" in low_info
    assert _length_prefixed(b"low") in low_info
    assert _length_prefixed(b"high") in high_info
    assert low_info != high_info


def test_transcript_canonicalization_includes_both_exact_signed_messages() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    canonical = transcript.canonical_bytes()

    assert canonical == replace(transcript).canonical_bytes()
    assert transcript.transcript_hash == replace(transcript).transcript_hash
    assert _length_prefixed(PQC_HANDSHAKE_TRANSCRIPT_DOMAIN) in canonical
    assert _length_prefixed(flow.signed_server_offer.offer.canonical_bytes()) in canonical
    assert _length_prefixed(flow.signed_server_offer.signature) in canonical
    assert _length_prefixed(flow.signed_client_exchange.exchange.canonical_bytes()) in canonical
    assert _length_prefixed(flow.signed_client_exchange.signature) in canonical


def test_each_signature_changes_the_transcript_hash() -> None:
    flow = _create_flow(PQCProfile.LOW)
    baseline = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    changed_server_signature = replace(
        flow.signed_server_offer,
        signature=_flipped(flow.signed_server_offer.signature),
    )
    changed_client_signature = replace(
        flow.signed_client_exchange,
        signature=_flipped(flow.signed_client_exchange.signature),
    )

    assert (
        PQCHandshakeTranscript.from_messages(
            changed_server_signature,
            flow.signed_client_exchange,
        ).transcript_hash
        != baseline.transcript_hash
    )
    assert (
        PQCHandshakeTranscript.from_messages(
            flow.signed_server_offer,
            changed_client_signature,
        ).transcript_hash
        != baseline.transcript_hash
    )


def test_client_nonce_changes_transcript_hash_and_hkdf_output() -> None:
    flow = _create_flow(PQCProfile.LOW)
    baseline = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    changed_exchange = replace(
        flow.signed_client_exchange.exchange,
        client_nonce=_flipped(flow.signed_client_exchange.exchange.client_nonce),
    )
    changed_signed_exchange = replace(flow.signed_client_exchange, exchange=changed_exchange)
    changed = PQCHandshakeTranscript.from_messages(flow.signed_server_offer, changed_signed_exchange)
    kem_input = _initiator_state(flow)._build_kdf_input()
    info = _session_key_info(protocol_version=baseline.protocol_version, profile=baseline.profile)

    baseline_key = derive_hkdf_sha384(
        key_material=kem_input,
        salt=baseline.transcript_hash,
        info=info,
        length=PQC_SESSION_KEY_LENGTH,
    )
    changed_key = derive_hkdf_sha384(
        key_material=kem_input,
        salt=changed.transcript_hash,
        info=info,
        length=PQC_SESSION_KEY_LENGTH,
    )

    assert changed.transcript_hash != baseline.transcript_hash
    assert changed_key != baseline_key


def test_transcript_rejects_unrelated_or_role_confused_messages() -> None:
    first = _create_flow(PQCProfile.LOW)
    second = _create_flow(PQCProfile.LOW)

    with pytest.raises(ValueError, match="session IDs do not match"):
        PQCHandshakeTranscript.from_messages(
            first.signed_server_offer,
            second.signed_client_exchange,
        )

    wrong_hash_exchange = replace(
        first.signed_client_exchange.exchange,
        server_offer_hash=b"W" * PQC_TRANSCRIPT_HASH_LENGTH,
    )
    with pytest.raises(ValueError, match="not bound"):
        PQCHandshakeTranscript.from_messages(
            first.signed_server_offer,
            replace(first.signed_client_exchange, exchange=wrong_hash_exchange),
        )

    confused_signer = replace(first.signed_client_exchange, signer=first.signed_server_offer.signer)
    with pytest.raises(ValueError, match="distinct initiator and responder"):
        PQCHandshakeTranscript.from_messages(first.signed_server_offer, confused_signer)


def test_low_kem_input_is_explicit_and_rejects_hqc_material() -> None:
    ml_secret = b"M" * ml_kem_768_metadata().shared_secret_length
    encoded = canonical_kem_secret_input(
        profile=PQCProfile.LOW,
        ml_kem_shared_secret=ml_secret,
    )
    expected = b"".join(
        (
            _length_prefixed(KEM_SECRET_INPUT_DOMAIN),
            b"\x01",
            _length_prefixed(b"ML-KEM-768"),
            _length_prefixed(ml_secret),
        )
    )

    assert encoded == expected
    with pytest.raises(ValueError, match="LOW KEM secret input must not contain an HQC"):
        canonical_kem_secret_input(
            profile=PQCProfile.LOW,
            ml_kem_shared_secret=ml_secret,
            hqc_shared_secret=b"H" * hqc_3_metadata().shared_secret_length,
        )


def test_high_kem_input_has_fixed_order_boundaries_and_component_sensitivity() -> None:
    ml_secret = b"M" * ml_kem_768_metadata().shared_secret_length
    hqc_secret = b"H" * hqc_3_metadata().shared_secret_length
    encoded = canonical_kem_secret_input(
        profile=PQCProfile.HIGH,
        ml_kem_shared_secret=ml_secret,
        hqc_shared_secret=hqc_secret,
    )
    expected = b"".join(
        (
            _length_prefixed(KEM_SECRET_INPUT_DOMAIN),
            b"\x02",
            _length_prefixed(b"ML-KEM-768"),
            _length_prefixed(ml_secret),
            _length_prefixed(b"HQC-3"),
            _length_prefixed(hqc_secret),
        )
    )
    changed_ml = canonical_kem_secret_input(
        profile=PQCProfile.HIGH,
        ml_kem_shared_secret=_flipped(ml_secret),
        hqc_shared_secret=hqc_secret,
    )
    changed_hqc = canonical_kem_secret_input(
        profile=PQCProfile.HIGH,
        ml_kem_shared_secret=ml_secret,
        hqc_shared_secret=_flipped(hqc_secret),
    )
    swapped = canonical_kem_secret_input(
        profile=PQCProfile.HIGH,
        ml_kem_shared_secret=hqc_secret,
        hqc_shared_secret=ml_secret,
    )
    salt = b"T" * PQC_TRANSCRIPT_HASH_LENGTH
    info = _session_key_info(protocol_version=1, profile=PQCProfile.HIGH)
    derived = derive_hkdf_sha384(
        key_material=encoded,
        salt=salt,
        info=info,
        length=PQC_SESSION_KEY_LENGTH,
    )

    assert encoded == expected
    assert encoded != changed_ml
    assert encoded != changed_hqc
    assert encoded != swapped
    assert encoded.index(b"ML-KEM-768") < encoded.index(b"HQC-3")
    for changed_input in (changed_ml, changed_hqc, swapped):
        assert (
            derive_hkdf_sha384(
                key_material=changed_input,
                salt=salt,
                info=info,
                length=PQC_SESSION_KEY_LENGTH,
            )
            != derived
        )


def test_low_and_high_kem_inputs_are_profile_separated() -> None:
    shared_bytes = b"S" * ml_kem_768_metadata().shared_secret_length
    low_input = canonical_kem_secret_input(
        profile=PQCProfile.LOW,
        ml_kem_shared_secret=shared_bytes,
    )
    high_input = canonical_kem_secret_input(
        profile=PQCProfile.HIGH,
        ml_kem_shared_secret=shared_bytes,
        hqc_shared_secret=shared_bytes,
    )
    salt = b"T" * PQC_TRANSCRIPT_HASH_LENGTH

    low_key = derive_hkdf_sha384(
        key_material=low_input,
        salt=salt,
        info=_session_key_info(protocol_version=1, profile=PQCProfile.LOW),
        length=PQC_SESSION_KEY_LENGTH,
    )
    high_key = derive_hkdf_sha384(
        key_material=high_input,
        salt=salt,
        info=_session_key_info(protocol_version=1, profile=PQCProfile.HIGH),
        length=PQC_SESSION_KEY_LENGTH,
    )

    assert low_input != high_input
    assert low_key != high_key


def test_high_kem_input_requires_both_valid_length_secrets() -> None:
    ml_secret = b"M" * ml_kem_768_metadata().shared_secret_length
    hqc_secret = b"H" * hqc_3_metadata().shared_secret_length

    with pytest.raises(ValueError, match="requires an HQC shared secret"):
        canonical_kem_secret_input(profile=PQCProfile.HIGH, ml_kem_shared_secret=ml_secret)
    with pytest.raises(ValueError, match="ml_kem_shared_secret must contain"):
        canonical_kem_secret_input(
            profile=PQCProfile.HIGH,
            ml_kem_shared_secret=b"short",
            hqc_shared_secret=hqc_secret,
        )
    with pytest.raises(ValueError, match="hqc_shared_secret must contain"):
        canonical_kem_secret_input(
            profile=PQCProfile.HIGH,
            ml_kem_shared_secret=ml_secret,
            hqc_shared_secret=b"short",
        )


@pytest.mark.parametrize("role", ["initiator", "responder"])
def test_closed_secret_state_cannot_derive(role: str) -> None:
    flow = _create_flow(PQCProfile.HIGH)
    deriver = PQCSessionKeyDeriver()

    if role == "initiator":
        _initiator_state(flow).close()
        derive = lambda: deriver.derive_initiator(  # noqa: E731
            processed_server_offer=flow.processed_server_offer,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )
    else:
        _responder_state(flow).close()
        derive = lambda: deriver.derive_responder(  # noqa: E731
            processed_client_exchange=flow.processed_client_exchange,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )

    with pytest.raises(RuntimeError, match="state is closed"):
        derive()


def test_key_derivation_requires_successful_phase_results() -> None:
    valid = _create_flow(PQCProfile.LOW)
    untrusted_alice = PQCParty.create("Untrusted Alice")
    rejected_phase3 = ServerKeyOfferProcessor().process(
        initiator=untrusted_alice,
        signed_offer=valid.signed_server_offer,
    )
    deriver = PQCSessionKeyDeriver()

    with pytest.raises(ValueError, match="authenticated Phase 3"):
        deriver.derive_initiator(
            processed_server_offer=rejected_phase3,
            signed_server_offer=valid.signed_server_offer,
            signed_client_exchange=valid.signed_client_exchange,
        )

    alice = PQCParty.create("Alice")
    bob_without_alice_trust = PQCParty.create("Bob without Alice trust")
    alice.trust_peer(bob_without_alice_trust.public_identity)
    responder_kem_state, signed_server_offer = ServerKeyOfferFactory().create(
        responder=bob_without_alice_trust,
        profile=PQCProfile.LOW,
    )
    processed_server_offer = ServerKeyOfferProcessor().process(
        initiator=alice,
        signed_offer=signed_server_offer,
    )
    signed_client_exchange = ClientKeyExchangeFactory().create(
        initiator=alice,
        signed_server_offer=signed_server_offer,
        processed_offer=processed_server_offer,
    )
    rejected_phase4 = ClientKeyExchangeProcessor().process(
        responder=bob_without_alice_trust,
        responder_state=responder_kem_state,
        server_offer=signed_server_offer,
        signed_exchange=signed_client_exchange,
    )
    assert not rejected_phase4.authenticated
    with pytest.raises(ValueError, match="authenticated Phase 4"):
        deriver.derive_responder(
            processed_client_exchange=rejected_phase4,
            signed_server_offer=signed_server_offer,
            signed_client_exchange=signed_client_exchange,
        )


def test_phase_results_cannot_be_mixed_with_another_authenticated_transcript() -> None:
    first = _create_flow(PQCProfile.LOW)
    second = _create_flow(PQCProfile.LOW)
    deriver = PQCSessionKeyDeriver()

    with pytest.raises(ValueError, match="Phase 3 result does not belong"):
        deriver.derive_initiator(
            processed_server_offer=first.processed_server_offer,
            signed_server_offer=second.signed_server_offer,
            signed_client_exchange=second.signed_client_exchange,
        )
    with pytest.raises(ValueError, match="Phase 4 result does not belong"):
        deriver.derive_responder(
            processed_client_exchange=first.processed_client_exchange,
            signed_server_offer=second.signed_server_offer,
            signed_client_exchange=second.signed_client_exchange,
        )


def test_exact_hkdf_parameters_use_kem_input_transcript_salt_and_session_info() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    expected_kem_input = _initiator_state(flow)._build_kdf_input()
    expected_info = _session_key_info(
        protocol_version=transcript.protocol_version,
        profile=transcript.profile,
    )

    with patch(
        "pqc.protocol.key_schedule.derive_hkdf_sha384",
        return_value=b"K" * PQC_SESSION_KEY_LENGTH,
    ) as derive:
        result = PQCSessionKeyDeriver().derive_initiator(
            processed_server_offer=flow.processed_server_offer,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )

    derive.assert_called_once_with(
        key_material=expected_kem_input,
        salt=transcript.transcript_hash,
        info=expected_info,
        length=PQC_SESSION_KEY_LENGTH,
    )
    assert object.__getattribute__(result, "_session_key") == b"K" * PQC_SESSION_KEY_LENGTH


def test_hkdf_failure_propagates_without_closing_source_state() -> None:
    flow = _create_flow(PQCProfile.LOW)
    source_state = _initiator_state(flow)

    with patch(
        "pqc.protocol.key_schedule.derive_hkdf_sha384",
        side_effect=RuntimeError("HKDF backend failed"),
    ):
        with pytest.raises(RuntimeError, match="HKDF backend failed"):
            PQCSessionKeyDeriver().derive_initiator(
                processed_server_offer=flow.processed_server_offer,
                signed_server_offer=flow.signed_server_offer,
                signed_client_exchange=flow.signed_client_exchange,
            )

    assert not source_state.is_closed


def test_session_key_and_kem_secrets_never_enter_public_repr_or_transport() -> None:
    flow = _create_flow(PQCProfile.HIGH)
    alice_key_state, bob_key_state = _derive_both(flow)
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    session_key = object.__getattribute__(alice_key_state, "_session_key")
    ml_secret = object.__getattribute__(_initiator_state(flow), "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(_initiator_state(flow), "_hqc_shared_secret")
    public_repr = repr(transcript) + repr(alice_key_state) + repr(bob_key_state)
    public_transport = repr(flow.signed_server_offer.to_dict()) + repr(flow.signed_client_exchange.to_dict())

    assert session_key is not None and ml_secret is not None and hqc_secret is not None
    assert not hasattr(alice_key_state, "to_dict")
    for secret in (session_key, ml_secret, hqc_secret):
        assert repr(secret) not in public_repr
        assert repr(secret) not in public_transport
        assert secret not in transcript.canonical_bytes()


def test_derived_session_key_state_context_manager_releases_key() -> None:
    flow = _create_flow(PQCProfile.LOW)
    state, _ = _derive_both(flow)
    session_key = object.__getattribute__(state, "_session_key")

    with state as managed_state:
        assert managed_state is state
        assert not state.is_closed

    assert state.is_closed
    assert object.__getattribute__(state, "_session_key") is None
    assert repr(session_key) not in repr(state)
