"""Tests for Phase 6 role-separated Finished key confirmation."""

import json
from dataclasses import dataclass, replace
from unittest.mock import patch

import pytest

from pqc import (
    PQC_CONFIRMATION_KEY_LENGTH,
    PQC_FINISHED_VERIFY_DATA_LENGTH,
    ClientKeyExchangeProcessingStatus,
    ConfirmedPQCHandshake,
    DerivedSessionKeyState,
    EstablishedPQCSession,
    PQCConfirmationKeyDeriver,
    PQCConfirmationKeyState,
    PQCFinishedMessage,
    PQCFinishedRole,
    PQCHandshakeTranscript,
    PQCKeyConfirmation,
    PQCProfile,
    ProcessedClientKeyExchange,
    ProcessedServerOffer,
    ServerOfferProcessingStatus,
)
from pqc._encoding import _length_prefixed
from pqc.protocol.key_confirmation import (
    PQC_CONFIRMATION_KEY_INFO_DOMAIN,
    PQC_FINISHED_MAC_INPUT_DOMAIN,
    _confirmation_key_info,
    _finished_mac_input,
)
from pqc.protocol.key_schedule import PQC_SESSION_KEY_INFO_DOMAIN, _session_key_info
from pqc.protocol.messages import (
    PQC_FINISHED_MAC_ALGORITHM,
    PQC_FINISHED_PROTOCOL_VERSION,
)
from tests.test_pqc._handshake import (
    Phase5Flow,
    create_phase5_flow,
    derive_session_keys,
    initiator_secret_state,
    responder_secret_state,
)


@dataclass(slots=True)
class _Phase6States:
    flow: Phase5Flow
    alice_session_key: DerivedSessionKeyState
    bob_session_key: DerivedSessionKeyState
    alice_confirmation: PQCConfirmationKeyState
    bob_confirmation: PQCConfirmationKeyState


def _derive_confirmation_states(profile: PQCProfile) -> _Phase6States:
    flow = create_phase5_flow(profile)
    alice_session_key, bob_session_key = derive_session_keys(flow)
    deriver = PQCConfirmationKeyDeriver()
    alice_confirmation = deriver.derive_initiator(
        processed_server_offer=flow.processed_server_offer,
        session_key_state=alice_session_key,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    bob_confirmation = deriver.derive_responder(
        processed_client_exchange=flow.processed_client_exchange,
        session_key_state=bob_session_key,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    return _Phase6States(
        flow=flow,
        alice_session_key=alice_session_key,
        bob_session_key=bob_session_key,
        alice_confirmation=alice_confirmation,
        bob_confirmation=bob_confirmation,
    )


def _exchange_finished(
    states: _Phase6States,
) -> tuple[PQCFinishedMessage, PQCFinishedMessage, ConfirmedPQCHandshake]:
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    initiator_finished = PQCKeyConfirmation.verify_responder_and_create_initiator(
        states.alice_confirmation,
        responder_finished,
    )
    confirmed = PQCKeyConfirmation.verify_initiator_and_confirm(
        states.bob_confirmation,
        initiator_finished,
    )
    return responder_finished, initiator_finished, confirmed


def _flipped(value: bytes) -> bytes:
    return bytes([value[0] ^ 1]) + value[1:]


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_phase6_establishes_both_local_sessions_only_through_finished(
    profile: PQCProfile,
) -> None:
    states = _derive_confirmation_states(profile)

    responder_finished, initiator_finished, confirmed = _exchange_finished(states)
    alice_session = PQCKeyConfirmation.establish_local_session(
        confirmed,
        states.alice_confirmation,
    )
    bob_session = PQCKeyConfirmation.establish_local_session(
        confirmed,
        states.bob_confirmation,
    )

    assert isinstance(alice_session, EstablishedPQCSession)
    assert isinstance(bob_session, EstablishedPQCSession)
    assert alice_session.established and bob_session.established
    assert alice_session.role is PQCFinishedRole.INITIATOR
    assert bob_session.role is PQCFinishedRole.RESPONDER
    assert responder_finished.sender_role is PQCFinishedRole.RESPONDER
    assert initiator_finished.sender_role is PQCFinishedRole.INITIATOR
    assert confirmed.responder_finished is responder_finished
    assert confirmed.initiator_finished is initiator_finished
    assert not alice_session.is_closed
    assert not bob_session.is_closed


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_confirmation_material_matches_and_is_separate_from_session_key(
    profile: PQCProfile,
) -> None:
    states = _derive_confirmation_states(profile)
    alice_confirmation_key = object.__getattribute__(
        states.alice_confirmation,
        "_confirmation_key",
    )
    bob_confirmation_key = object.__getattribute__(
        states.bob_confirmation,
        "_confirmation_key",
    )

    assert alice_confirmation_key == bob_confirmation_key
    assert alice_confirmation_key is not None
    assert len(alice_confirmation_key) == PQC_CONFIRMATION_KEY_LENGTH
    assert states.alice_session_key.export_session_key() != alice_confirmation_key
    assert states.bob_session_key.export_session_key() != bob_confirmation_key


def test_low_and_high_confirmation_keys_are_context_separated() -> None:
    low = _derive_confirmation_states(PQCProfile.LOW)
    high = _derive_confirmation_states(PQCProfile.HIGH)

    low_key = object.__getattribute__(low.alice_confirmation, "_confirmation_key")
    high_key = object.__getattribute__(high.alice_confirmation, "_confirmation_key")

    assert low_key is not None and high_key is not None
    assert low_key != high_key
    assert low.alice_confirmation.transcript_hash != high.alice_confirmation.transcript_hash


def test_confirmation_info_and_finished_inputs_are_explicitly_domain_separated() -> None:
    session_id = b"S" * 16
    transcript_hash = b"T" * 48
    responder_verify_data = b"B" * PQC_FINISHED_VERIFY_DATA_LENGTH
    confirmation_info = _confirmation_key_info(
        protocol_version=1,
        profile=PQCProfile.HIGH,
    )
    session_info = _session_key_info(protocol_version=1, profile=PQCProfile.HIGH)
    responder_input = _finished_mac_input(
        protocol_version=1,
        session_id=session_id,
        profile=PQCProfile.HIGH,
        sender_role=PQCFinishedRole.RESPONDER,
        transcript_hash=transcript_hash,
    )
    initiator_input = _finished_mac_input(
        protocol_version=1,
        session_id=session_id,
        profile=PQCProfile.HIGH,
        sender_role=PQCFinishedRole.INITIATOR,
        transcript_hash=transcript_hash,
        responder_verify_data=responder_verify_data,
    )

    assert confirmation_info != session_info
    assert _length_prefixed(PQC_CONFIRMATION_KEY_INFO_DOMAIN) in confirmation_info
    assert _length_prefixed(PQC_SESSION_KEY_INFO_DOMAIN) in session_info
    assert _length_prefixed(PQC_FINISHED_MAC_INPUT_DOMAIN) in responder_input
    assert _length_prefixed(b"responder") in responder_input
    assert _length_prefixed(b"initiator") in initiator_input
    assert _length_prefixed(responder_verify_data) in initiator_input
    assert responder_input != initiator_input


def test_finished_messages_are_role_separated_and_chained() -> None:
    states = _derive_confirmation_states(PQCProfile.HIGH)
    responder_finished, initiator_finished, _ = _exchange_finished(states)

    assert responder_finished.verify_data != initiator_finished.verify_data
    assert len(responder_finished.verify_data) == PQC_FINISHED_VERIFY_DATA_LENGTH
    assert len(initiator_finished.verify_data) == PQC_FINISHED_VERIFY_DATA_LENGTH
    assert responder_finished.canonical_bytes() != initiator_finished.canonical_bytes()


def test_tampered_responder_finished_fails_without_alice_response() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    tampered = replace(
        responder_finished,
        verify_data=_flipped(responder_finished.verify_data),
    )

    with pytest.raises(ValueError, match="verify_data authentication failed"):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            states.alice_confirmation,
            tampered,
        )

    assert not states.alice_confirmation.is_closed
    assert object.__getattribute__(states.alice_confirmation, "_local_finished") is None


def test_tampered_initiator_finished_does_not_confirm_bob() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    initiator_finished = PQCKeyConfirmation.verify_responder_and_create_initiator(
        states.alice_confirmation,
        responder_finished,
    )
    tampered = replace(
        initiator_finished,
        verify_data=_flipped(initiator_finished.verify_data),
    )

    with pytest.raises(ValueError, match="verify_data authentication failed"):
        PQCKeyConfirmation.verify_initiator_and_confirm(
            states.bob_confirmation,
            tampered,
        )

    assert not states.bob_confirmation.is_closed
    assert object.__getattribute__(states.bob_confirmation, "_peer_finished") is None


def test_finished_role_reflection_is_rejected() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)

    with pytest.raises(ValueError, match="Expected initiator Finished"):
        PQCKeyConfirmation.verify_initiator_and_confirm(
            states.bob_confirmation,
            responder_finished,
        )

    reflected = replace(responder_finished, sender_role=PQCFinishedRole.INITIATOR)
    with pytest.raises(ValueError, match="verify_data authentication failed"):
        PQCKeyConfirmation.verify_initiator_and_confirm(
            states.bob_confirmation,
            reflected,
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("session_id", b"X" * 16, "session does not match"),
        ("profile", PQCProfile.HIGH, "profile does not match"),
        ("transcript_hash", b"X" * 48, "transcript hash does not match"),
    ],
)
def test_finished_context_mismatches_are_rejected(
    field: str,
    value: object,
    message: str,
) -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    mismatched = replace(responder_finished, **{field: value})

    with pytest.raises(ValueError, match=message):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            states.alice_confirmation,
            mismatched,
        )


def test_finished_replay_across_sessions_is_rejected() -> None:
    first = _derive_confirmation_states(PQCProfile.LOW)
    second = _derive_confirmation_states(PQCProfile.LOW)
    replayed = PQCKeyConfirmation.create_responder_finished(first.bob_confirmation)

    with pytest.raises(ValueError, match="session does not match"):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            second.alice_confirmation,
            replayed,
        )


def test_different_confirmation_key_fails_finished_authentication() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    alice_key = object.__getattribute__(states.alice_confirmation, "_confirmation_key")
    assert alice_key is not None
    object.__setattr__(states.alice_confirmation, "_confirmation_key", _flipped(alice_key))

    with pytest.raises(ValueError, match="verify_data authentication failed"):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            states.alice_confirmation,
            responder_finished,
        )


def test_closed_confirmation_states_reject_finished_operations() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    states.bob_confirmation.close()
    states.alice_confirmation.close()

    with pytest.raises(RuntimeError, match="Confirmation key state is closed"):
        PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    with pytest.raises(RuntimeError, match="Confirmation key state is closed"):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            states.alice_confirmation,
            PQCFinishedMessage(
                protocol_version=PQC_FINISHED_PROTOCOL_VERSION,
                session_id=states.alice_confirmation.session_id,
                profile=states.alice_confirmation.profile,
                sender_role=PQCFinishedRole.RESPONDER,
                mac_algorithm=PQC_FINISHED_MAC_ALGORITHM,
                transcript_hash=states.alice_confirmation.transcript_hash,
                verify_data=b"V" * PQC_FINISHED_VERIFY_DATA_LENGTH,
            ),
        )


@pytest.mark.parametrize("profile", [PQCProfile.LOW, PQCProfile.HIGH])
def test_confirmation_derivation_retires_kem_secrets_but_keeps_session_keys(
    profile: PQCProfile,
) -> None:
    states = _derive_confirmation_states(profile)

    assert initiator_secret_state(states.flow).is_closed
    assert responder_secret_state(states.flow).is_closed
    assert not states.alice_session_key.is_closed
    assert not states.bob_session_key.is_closed
    assert (
        object.__getattribute__(
            initiator_secret_state(states.flow),
            "_ml_kem_shared_secret",
        )
        is None
    )
    assert (
        object.__getattribute__(
            responder_secret_state(states.flow),
            "_ml_kem_shared_secret",
        )
        is None
    )


def test_confirmation_hkdf_failure_does_not_close_source_kem_state() -> None:
    flow = create_phase5_flow(PQCProfile.HIGH)
    alice_session_key, _ = derive_session_keys(flow)
    source_state = initiator_secret_state(flow)

    with patch(
        "pqc.protocol.key_confirmation.derive_hkdf_sha384",
        side_effect=RuntimeError("HKDF backend failed"),
    ):
        with pytest.raises(RuntimeError, match="HKDF backend failed"):
            PQCConfirmationKeyDeriver().derive_initiator(
                processed_server_offer=flow.processed_server_offer,
                session_key_state=alice_session_key,
                signed_server_offer=flow.signed_server_offer,
                signed_client_exchange=flow.signed_client_exchange,
            )

    assert not source_state.is_closed


def test_confirmation_derivation_uses_exact_kem_transcript_and_info_inputs() -> None:
    flow = create_phase5_flow(PQCProfile.HIGH)
    alice_session_key, _ = derive_session_keys(flow)
    source_state = initiator_secret_state(flow)
    expected_kem_input = source_state._build_kdf_input()
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    expected_info = _confirmation_key_info(
        protocol_version=transcript.protocol_version,
        profile=transcript.profile,
    )

    with patch(
        "pqc.protocol.key_confirmation.derive_hkdf_sha384",
        return_value=b"C" * PQC_CONFIRMATION_KEY_LENGTH,
    ) as hkdf:
        state = PQCConfirmationKeyDeriver().derive_initiator(
            processed_server_offer=flow.processed_server_offer,
            session_key_state=alice_session_key,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )

    hkdf.assert_called_once_with(
        key_material=expected_kem_input,
        salt=transcript.transcript_hash,
        info=expected_info,
        length=PQC_CONFIRMATION_KEY_LENGTH,
    )
    assert not state.is_closed
    assert source_state.is_closed


def test_hmac_failure_does_not_advance_or_close_confirmation_state() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)

    with patch(
        "pqc.protocol.key_confirmation.hmac.new",
        side_effect=RuntimeError("HMAC backend failed"),
    ):
        with pytest.raises(RuntimeError, match="HMAC backend failed"):
            PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)

    assert not states.bob_confirmation.is_closed
    assert object.__getattribute__(states.bob_confirmation, "_local_finished") is None


def test_finished_transport_round_trip_preserves_canonical_bytes() -> None:
    states = _derive_confirmation_states(PQCProfile.HIGH)
    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)

    payload = json.loads(json.dumps(responder_finished.to_dict()))
    restored = PQCFinishedMessage.from_dict(payload)

    assert restored == responder_finished
    assert restored.canonical_bytes() == responder_finished.canonical_bytes()


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {"protocol_version": 1},
        {
            "protocol_version": 1,
            "session_id": "not base64!",
            "profile": "low",
            "sender_role": "responder",
            "mac_algorithm": "HMAC-SHA-384",
            "transcript_hash": "VA==",
            "verify_data": "Vg==",
        },
        {
            "protocol_version": 1,
            "session_id": "U1NTU1NTU1NTU1NTU1NTUw==",
            "profile": "low",
            "sender_role": "server",
            "mac_algorithm": "HMAC-SHA-384",
            "transcript_hash": "VA==",
            "verify_data": "Vg==",
        },
    ],
)
def test_finished_transport_rejects_malformed_payloads(payload: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        PQCFinishedMessage.from_dict(payload)  # type: ignore[arg-type]


def test_phase6_rejects_incomplete_prior_phases_and_closed_session_key() -> None:
    flow = create_phase5_flow(PQCProfile.LOW)
    alice_session_key, bob_session_key = derive_session_keys(flow)
    rejected_phase3 = ProcessedServerOffer(
        status=ServerOfferProcessingStatus.UNTRUSTED_SIGNER,
        signer=flow.bob.name,
        profile=PQCProfile.LOW,
        failure_reason="Phase 3 rejected",
    )
    rejected_phase4 = ProcessedClientKeyExchange(
        status=ClientKeyExchangeProcessingStatus.UNTRUSTED_SIGNER,
        signer=flow.alice.name,
        profile=PQCProfile.LOW,
        failure_reason="Phase 4 rejected",
    )
    deriver = PQCConfirmationKeyDeriver()

    with pytest.raises(ValueError, match="authenticated Phase 3"):
        deriver.derive_initiator(
            processed_server_offer=rejected_phase3,
            session_key_state=alice_session_key,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )
    with pytest.raises(ValueError, match="authenticated Phase 4"):
        deriver.derive_responder(
            processed_client_exchange=rejected_phase4,
            session_key_state=bob_session_key,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )

    alice_session_key.close()
    with pytest.raises(RuntimeError, match="Session key state is closed"):
        deriver.derive_initiator(
            processed_server_offer=flow.processed_server_offer,
            session_key_state=alice_session_key,
            signed_server_offer=flow.signed_server_offer,
            signed_client_exchange=flow.signed_client_exchange,
        )
    assert not initiator_secret_state(flow).is_closed


def test_phase6_rejects_mixed_phase_results_transcript_and_session_state() -> None:
    first = create_phase5_flow(PQCProfile.LOW)
    second = create_phase5_flow(PQCProfile.LOW)
    first_alice_key, _ = derive_session_keys(first)
    second_alice_key, _ = derive_session_keys(second)
    deriver = PQCConfirmationKeyDeriver()

    with pytest.raises(ValueError, match="does not belong to the transcript"):
        deriver.derive_initiator(
            processed_server_offer=first.processed_server_offer,
            session_key_state=first_alice_key,
            signed_server_offer=second.signed_server_offer,
            signed_client_exchange=second.signed_client_exchange,
        )
    with pytest.raises(ValueError, match="does not belong to the handshake session"):
        deriver.derive_initiator(
            processed_server_offer=first.processed_server_offer,
            session_key_state=second_alice_key,
            signed_server_offer=first.signed_server_offer,
            signed_client_exchange=first.signed_client_exchange,
        )


def test_session_cannot_be_established_before_both_finished_verify() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    premature_initiator = PQCFinishedMessage(
        protocol_version=PQC_FINISHED_PROTOCOL_VERSION,
        session_id=states.bob_confirmation.session_id,
        profile=states.bob_confirmation.profile,
        sender_role=PQCFinishedRole.INITIATOR,
        mac_algorithm=PQC_FINISHED_MAC_ALGORITHM,
        transcript_hash=states.bob_confirmation.transcript_hash,
        verify_data=b"V" * PQC_FINISHED_VERIFY_DATA_LENGTH,
    )

    with pytest.raises(RuntimeError, match="Responder Finished must be created"):
        PQCKeyConfirmation.verify_initiator_and_confirm(
            states.bob_confirmation,
            premature_initiator,
        )

    with pytest.raises(TypeError, match="confirmation must be a ConfirmedPQCHandshake"):
        PQCKeyConfirmation.establish_local_session(
            object(),  # type: ignore[arg-type]
            states.alice_confirmation,
        )

    responder_finished = PQCKeyConfirmation.create_responder_finished(states.bob_confirmation)
    invalid = replace(responder_finished, verify_data=_flipped(responder_finished.verify_data))
    with pytest.raises(ValueError, match="verify_data authentication failed"):
        PQCKeyConfirmation.verify_responder_and_create_initiator(
            states.alice_confirmation,
            invalid,
        )
    assert object.__getattribute__(states.alice_confirmation, "_local_finished") is None


def test_secret_material_never_enters_finished_transport_or_public_repr() -> None:
    flow = create_phase5_flow(PQCProfile.HIGH)
    alice_session_key, bob_session_key = derive_session_keys(flow)
    ml_secret = object.__getattribute__(initiator_secret_state(flow), "_ml_kem_shared_secret")
    hqc_secret = object.__getattribute__(initiator_secret_state(flow), "_hqc_shared_secret")
    deriver = PQCConfirmationKeyDeriver()
    alice_confirmation = deriver.derive_initiator(
        processed_server_offer=flow.processed_server_offer,
        session_key_state=alice_session_key,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    bob_confirmation = deriver.derive_responder(
        processed_client_exchange=flow.processed_client_exchange,
        session_key_state=bob_session_key,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    confirmation_key = object.__getattribute__(alice_confirmation, "_confirmation_key")
    states = _Phase6States(
        flow=flow,
        alice_session_key=alice_session_key,
        bob_session_key=bob_session_key,
        alice_confirmation=alice_confirmation,
        bob_confirmation=bob_confirmation,
    )
    responder_finished, initiator_finished, confirmed = _exchange_finished(states)
    established = PQCKeyConfirmation.establish_local_session(confirmed, alice_confirmation)
    transcript = PQCHandshakeTranscript.from_messages(
        flow.signed_server_offer,
        flow.signed_client_exchange,
    )
    session_key = alice_session_key.export_session_key()
    public_repr = "".join(
        repr(value)
        for value in (
            transcript,
            responder_finished,
            initiator_finished,
            alice_confirmation,
            bob_confirmation,
            confirmed,
            established,
        )
    )
    public_transport = repr(responder_finished.to_dict()) + repr(initiator_finished.to_dict())

    assert ml_secret is not None and hqc_secret is not None and confirmation_key is not None
    assert not hasattr(alice_confirmation, "to_dict")
    assert not hasattr(established, "to_dict")
    for secret in (ml_secret, hqc_secret, session_key, confirmation_key):
        assert repr(secret) not in public_repr
        assert repr(secret) not in public_transport
        assert secret not in responder_finished.canonical_bytes()
        assert secret not in initiator_finished.canonical_bytes()


def test_established_session_owns_session_key_lifecycle() -> None:
    states = _derive_confirmation_states(PQCProfile.LOW)
    _, _, confirmed = _exchange_finished(states)
    established = PQCKeyConfirmation.establish_local_session(
        confirmed,
        states.alice_confirmation,
    )
    session_key = established.export_session_key()

    with established as managed:
        assert managed is established
        assert managed.export_session_key() == session_key

    assert established.is_closed
    assert states.alice_session_key.is_closed
    with pytest.raises(RuntimeError, match="Derived session key state is closed"):
        established.export_session_key()
