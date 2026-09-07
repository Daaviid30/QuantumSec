import json
from dataclasses import replace

import pytest
from cryptography.exceptions import InvalidTag

from data_protection import (
    DATA_PLANE_AAD_DOMAIN,
    DataPlaneContext,
    DataPlaneDirection,
    ProtectedRecord,
    ProtectedSession,
    canonical_data_plane_aad,
    nonce_for,
)


def _context(
    session_id: bytes = b"protected-test01",
    *,
    profile: str = "HYBRID",
) -> DataPlaneContext:
    return DataPlaneContext(
        session_id,
        profile,
        1,
        "session_key",
        256,
        (("hybrid_context_hash_sha384", "cd" * 48), ("hybrid_context_version", 1)),
    )


def test_protected_session_round_trip_record_and_safe_public_metadata() -> None:
    key = b"super-secret-session-key-value!!"
    plaintext = b"QuantumSec protected application payload"
    with ProtectedSession(key, _context()) as session:
        record = session.encrypt(
            plaintext,
            direction=DataPlaneDirection.ALICE_TO_BOB,
            aad=b"document:42",
        )
        assert session.decrypt(record, aad=b"document:42") == plaintext
        assert len(record.nonce) == 12
        assert len(record.tag) == 16
        assert len(record.ciphertext) == len(plaintext)
        public = record.to_public_dict()
        assert json.dumps(public)
        assert public["algorithm"] == "AES-256-GCM"
        sizes = public["sizes"]
        assert isinstance(sizes, dict)
        assert sizes["application_aad_bytes"] == len(b"document:42")
        assert key.hex() not in repr(session)
        assert plaintext.decode() not in repr(record)
        assert record.ciphertext.hex() not in repr(record)
        assert record.tag.hex() not in repr(record)


def test_internal_aad_is_always_nonempty_and_session_bound() -> None:
    first = canonical_data_plane_aad(
        _context(),
        DataPlaneDirection.ALICE_TO_BOB,
        0,
        b"",
    )
    second = canonical_data_plane_aad(
        _context(b"protected-test02"),
        DataPlaneDirection.ALICE_TO_BOB,
        0,
        b"",
    )
    different_profile = canonical_data_plane_aad(
        _context(profile="PQC-BASE"),
        DataPlaneDirection.ALICE_TO_BOB,
        0,
        b"",
    )
    different_public_context = canonical_data_plane_aad(
        replace(
            _context(),
            public_context=(("hybrid_context_hash_sha384", "ef" * 48),),
        ),
        DataPlaneDirection.ALICE_TO_BOB,
        0,
        b"",
    )
    assert DATA_PLANE_AAD_DOMAIN in first
    assert len({first, second, different_profile, different_public_context}) == 4


def test_public_context_order_is_canonical_and_mapping_input_is_supported() -> None:
    entries = (
        ("zeta", 7),
        ("alpha", "value"),
    )
    tuple_context = DataPlaneContext(
        b"protected-test01",
        "PQC-BASE",
        1,
        "session_key",
        256,
        entries,
    )
    reverse_context = replace(tuple_context, public_context=tuple(reversed(entries)))
    mapping_context = replace(tuple_context, public_context=dict(entries))
    assert tuple_context.public_context == (("alpha", "value"), ("zeta", 7))
    assert tuple_context.canonical_bytes() == reverse_context.canonical_bytes()
    assert tuple_context.context_hash == mapping_context.context_hash


def test_application_aad_change_reaches_aead_and_raises_invalid_tag() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(
            b"payload",
            direction=DataPlaneDirection.ALICE_TO_BOB,
            aad=b"message:1",
        )
        with pytest.raises(InvalidTag):
            session.decrypt(record, aad=b"message:2")
        with pytest.raises(InvalidTag):
            session.decrypt(replace(record, application_aad_bytes=99), aad=b"message:1")


def test_wrong_key_with_same_public_context_raises_invalid_tag() -> None:
    with (
        ProtectedSession(b"a" * 32, _context()) as sender,
        ProtectedSession(b"b" * 32, _context()) as receiver,
    ):
        record = sender.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
        with pytest.raises(InvalidTag):
            receiver.decrypt(record)


def test_decrypt_is_explicitly_stateless_and_transport_owns_replay_policy() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(b"idempotent payload", direction=DataPlaneDirection.ALICE_TO_BOB)
        assert session.decrypt(record) == b"idempotent payload"
        assert session.decrypt(record) == b"idempotent payload"
    assert "anti-replay" in (ProtectedSession.decrypt.__doc__ or "")


def test_record_from_other_session_is_rejected_before_aead() -> None:
    with (
        ProtectedSession(b"k" * 32, _context(b"protected-test01")) as first,
        ProtectedSession(b"k" * 32, _context(b"protected-test02")) as second,
    ):
        record = first.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
        with pytest.raises(ValueError, match="does not belong"):
            second.decrypt(record)


def test_direction_is_authenticated_and_cannot_be_reinterpreted() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
        reinterpreted = replace(
            record,
            direction=DataPlaneDirection.BOB_TO_ALICE,
            nonce=nonce_for(DataPlaneDirection.BOB_TO_ALICE, record.sequence_number),
        )
        with pytest.raises(InvalidTag):
            session.decrypt(reinterpreted)


def test_record_rejects_nonce_inconsistent_with_direction_and_sequence() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
    with pytest.raises(ValueError, match="nonce does not match"):
        replace(record, nonce=nonce_for(DataPlaneDirection.ALICE_TO_BOB, 99))


def test_close_and_context_manager_retire_key_reference() -> None:
    session = ProtectedSession(b"k" * 32, _context())
    record = session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
    session.close()
    assert session.is_closed
    with pytest.raises(RuntimeError, match="closed"):
        session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
    with pytest.raises(RuntimeError, match="closed"):
        session.decrypt(record)

    managed = ProtectedSession(b"k" * 32, _context())
    with managed:
        assert not managed.is_closed
    assert managed.is_closed


def test_encrypt_api_does_not_accept_a_caller_selected_nonce() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        with pytest.raises(TypeError, match="nonce"):
            session.encrypt(
                b"payload",
                direction=DataPlaneDirection.ALICE_TO_BOB,
                nonce=b"n" * 12,  # pyright: ignore[reportCallIssue]
            )


def test_protected_record_is_immutable() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB)
    with pytest.raises((AttributeError, TypeError)):
        record.sequence_number = 7  # type: ignore[misc]
    assert isinstance(record, ProtectedRecord)


def test_protected_record_binary_transport_round_trip() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        record = session.encrypt(
            b"x" * 1024,
            direction=DataPlaneDirection.BOB_TO_ALICE,
            aad=b"transport metadata",
        )
        encoded = record.canonical_bytes()
        decoded = ProtectedRecord.from_bytes(encoded)
        assert decoded == record
        assert decoded.canonical_bytes() == encoded
        assert session.decrypt(decoded, aad=b"transport metadata") == b"x" * 1024
        assert len(encoded) < len(json.dumps(record.to_public_dict()).encode("utf-8"))


@pytest.mark.parametrize("mutation", ["truncated", "trailing", "domain"])
def test_protected_record_binary_parser_rejects_malformed_input(mutation: str) -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        encoded = session.encrypt(
            b"payload",
            direction=DataPlaneDirection.ALICE_TO_BOB,
        ).canonical_bytes()
    if mutation == "truncated":
        changed = encoded[:-1]
    elif mutation == "trailing":
        changed = encoded + b"unexpected"
    else:
        changed = bytearray(encoded)
        changed[8] ^= 1
        changed = bytes(changed)
    with pytest.raises(ValueError):
        ProtectedRecord.from_bytes(changed)
