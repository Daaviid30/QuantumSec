import pytest
from cryptography.exceptions import InvalidTag

from data_protection import decrypt_aes_256_gcm, encrypt_aes_256_gcm


def test_aes_256_gcm_round_trip_uses_separate_full_tag() -> None:
    plaintext = b"QuantumSec application payload"
    ciphertext, tag = encrypt_aes_256_gcm(b"k" * 32, b"n" * 12, plaintext, b"document:42")
    assert len(ciphertext) == len(plaintext)
    assert len(tag) == 16
    assert decrypt_aes_256_gcm(b"k" * 32, b"n" * 12, ciphertext, tag, b"document:42") == plaintext


def test_aes_256_gcm_supports_empty_plaintext_and_aad() -> None:
    ciphertext, tag = encrypt_aes_256_gcm(b"k" * 32, b"n" * 12, b"", b"")
    assert ciphertext == b""
    assert len(tag) == 16
    assert decrypt_aes_256_gcm(b"k" * 32, b"n" * 12, ciphertext, tag, b"") == b""


@pytest.mark.parametrize("key_length", [16, 24, 31, 33])
def test_aes_256_gcm_rejects_every_non_32_byte_key(key_length: int) -> None:
    with pytest.raises(ValueError, match="32 bytes"):
        encrypt_aes_256_gcm(b"k" * key_length, b"n" * 12, b"payload", b"")


@pytest.mark.parametrize("nonce_length", [0, 8, 11, 13, 16])
def test_aes_256_gcm_rejects_non_96_bit_nonces(nonce_length: int) -> None:
    with pytest.raises(ValueError, match="12 bytes"):
        encrypt_aes_256_gcm(b"k" * 32, b"n" * nonce_length, b"payload", b"")


def test_aes_256_gcm_tamper_and_wrong_key_propagate_invalid_tag() -> None:
    key = b"k" * 32
    nonce = b"n" * 12
    aad = b"document:42"
    ciphertext, tag = encrypt_aes_256_gcm(key, nonce, b"protected payload", aad)
    cases = (
        (bytes((ciphertext[0] ^ 1,)) + ciphertext[1:], tag, aad, key),
        (ciphertext, bytes((tag[0] ^ 1,)) + tag[1:], aad, key),
        (ciphertext, tag, b"document:43", key),
        (ciphertext, tag, aad, b"w" * 32),
    )
    for changed_ciphertext, changed_tag, changed_aad, changed_key in cases:
        with pytest.raises(InvalidTag):
            decrypt_aes_256_gcm(
                changed_key,
                nonce,
                changed_ciphertext,
                changed_tag,
                changed_aad,
            )


def test_aes_256_gcm_rejects_truncated_tag_before_decryption() -> None:
    ciphertext, tag = encrypt_aes_256_gcm(b"k" * 32, b"n" * 12, b"payload", b"")
    with pytest.raises(ValueError, match="16 bytes"):
        decrypt_aes_256_gcm(b"k" * 32, b"n" * 12, ciphertext, tag[:-1], b"")


@pytest.mark.parametrize("payload_size", [15, 16, 17, 31, 32, 1024, 65_536])
def test_aes_256_gcm_round_trips_block_boundaries_and_large_payloads(payload_size: int) -> None:
    plaintext = bytes(index % 251 for index in range(payload_size))
    ciphertext, tag = encrypt_aes_256_gcm(
        b"k" * 32,
        b"n" * 12,
        plaintext,
        b"payload-size-boundary",
    )
    assert len(ciphertext) == payload_size
    assert len(tag) == 16
    assert (
        decrypt_aes_256_gcm(
            b"k" * 32,
            b"n" * 12,
            ciphertext,
            tag,
            b"payload-size-boundary",
        )
        == plaintext
    )
