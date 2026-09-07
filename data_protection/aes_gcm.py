"""Strict AES-256-GCM primitive adapter backed by pyca/cryptography."""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from data_protection.context import DATA_PLANE_NONCE_BYTES, DATA_PLANE_TAG_BYTES, _require_bytes

AES_256_KEY_BYTES = 32


def _validated_inputs(
    key: bytes,
    nonce: bytes,
    data: bytes,
    aad: bytes,
    *,
    data_name: str,
) -> tuple[bytes, bytes, bytes, bytes]:
    return (
        _require_bytes(key, name="key", length=AES_256_KEY_BYTES),
        _require_bytes(nonce, name="nonce", length=DATA_PLANE_NONCE_BYTES),
        _require_bytes(data, name=data_name),
        _require_bytes(aad, name="aad"),
    )


def encrypt_aes_256_gcm(
    key: bytes,
    nonce: bytes,
    plaintext: bytes,
    aad: bytes,
) -> tuple[bytes, bytes]:
    """Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately."""

    clean_key, clean_nonce, clean_plaintext, clean_aad = _validated_inputs(
        key,
        nonce,
        plaintext,
        aad,
        data_name="plaintext",
    )
    ciphertext_and_tag = AESGCM(clean_key).encrypt(clean_nonce, clean_plaintext, clean_aad)
    if len(ciphertext_and_tag) < DATA_PLANE_TAG_BYTES:
        raise RuntimeError("AESGCM returned output shorter than its authentication tag.")
    return (
        bytes(ciphertext_and_tag[:-DATA_PLANE_TAG_BYTES]),
        bytes(ciphertext_and_tag[-DATA_PLANE_TAG_BYTES:]),
    )


def decrypt_aes_256_gcm(
    key: bytes,
    nonce: bytes,
    ciphertext: bytes,
    tag: bytes,
    aad: bytes,
) -> bytes:
    """Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag unchanged."""

    clean_key, clean_nonce, clean_ciphertext, clean_aad = _validated_inputs(
        key,
        nonce,
        ciphertext,
        aad,
        data_name="ciphertext",
    )
    clean_tag = _require_bytes(tag, name="tag", length=DATA_PLANE_TAG_BYTES)
    return AESGCM(clean_key).decrypt(
        clean_nonce,
        clean_ciphertext + clean_tag,
        clean_aad,
    )
