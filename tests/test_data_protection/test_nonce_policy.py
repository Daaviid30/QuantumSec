from concurrent.futures import ThreadPoolExecutor

import pytest

from data_protection import (
    MAX_SEQUENCE_NUMBER,
    DataPlaneContext,
    DataPlaneDirection,
    ProtectedSession,
    nonce_for,
)


def _context() -> DataPlaneContext:
    return DataPlaneContext(
        b"data-plane-test1",
        "PQC-BASE",
        1,
        "session_key",
        256,
        (("pqc_transcript_hash_sha384", "ab" * 48),),
    )


def test_nonce_layout_is_direction_prefix_plus_uint64_big_endian() -> None:
    alice = nonce_for(DataPlaneDirection.ALICE_TO_BOB, 7)
    bob = nonce_for(DataPlaneDirection.BOB_TO_ALICE, 7)
    assert alice == b"\x00\x00\x00\x01" + (7).to_bytes(8, "big")
    assert bob == b"\x00\x00\x00\x02" + (7).to_bytes(8, "big")
    assert len(alice) == len(bob) == 12
    assert alice != bob
    assert nonce_for(DataPlaneDirection.ALICE_TO_BOB, 8) != alice


def test_direction_spaces_and_monotonic_sequences_never_overlap() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        alice = [session.encrypt(b"payload", direction=DataPlaneDirection.ALICE_TO_BOB) for _ in range(32)]
        bob = [session.encrypt(b"payload", direction=DataPlaneDirection.BOB_TO_ALICE) for _ in range(32)]
    alice_nonces = {record.nonce for record in alice}
    bob_nonces = {record.nonce for record in bob}
    assert len(alice_nonces) == len(alice)
    assert len(bob_nonces) == len(bob)
    assert alice_nonces.isdisjoint(bob_nonces)
    assert [record.sequence_number for record in alice] == list(range(32))
    assert [record.sequence_number for record in bob] == list(range(32))


def test_concurrent_encryptions_issue_unique_nonces() -> None:
    with ProtectedSession(b"k" * 32, _context()) as session:
        with ThreadPoolExecutor(max_workers=12) as executor:
            records = tuple(
                executor.map(
                    lambda _: session.encrypt(
                        b"concurrent payload",
                        direction=DataPlaneDirection.ALICE_TO_BOB,
                    ),
                    range(256),
                )
            )
    assert len({record.nonce for record in records}) == len(records)
    assert {record.sequence_number for record in records} == set(range(256))


def test_counter_exhaustion_uses_last_nonce_once_and_never_wraps() -> None:
    session = ProtectedSession(b"k" * 32, _context())
    session._next_sequences[DataPlaneDirection.ALICE_TO_BOB] = MAX_SEQUENCE_NUMBER
    final = session.encrypt(b"last", direction=DataPlaneDirection.ALICE_TO_BOB)
    assert final.sequence_number == MAX_SEQUENCE_NUMBER
    assert final.nonce[-8:] == b"\xff" * 8
    with pytest.raises(RuntimeError, match="nonce space is exhausted"):
        session.encrypt(b"wrapped", direction=DataPlaneDirection.ALICE_TO_BOB)
    unaffected = session.encrypt(b"other direction", direction=DataPlaneDirection.BOB_TO_ALICE)
    assert unaffected.sequence_number == 0
    session.close()


def test_nonce_policy_rejects_invalid_sequences() -> None:
    with pytest.raises(ValueError, match="sequence_number"):
        nonce_for(DataPlaneDirection.ALICE_TO_BOB, -1)
    with pytest.raises(ValueError, match="sequence_number"):
        nonce_for(DataPlaneDirection.ALICE_TO_BOB, MAX_SEQUENCE_NUMBER + 1)
