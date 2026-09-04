"""Thin validated adapter around cryptography's HKDF-SHA-384 implementation."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def _validated_bytes(value: object, *, name: str) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    if not value:
        raise ValueError(f"{name} must not be empty.")
    return bytes(value)


def derive_hkdf_sha384(
    *,
    key_material: bytes,
    salt: bytes,
    info: bytes,
    length: int,
) -> bytes:
    """Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance."""

    clean_key_material = _validated_bytes(key_material, name="key_material")
    clean_salt = _validated_bytes(salt, name="salt")
    clean_info = _validated_bytes(info, name="info")
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError(f"length must be an integer. Got {type(length).__name__}.")
    if length <= 0:
        raise ValueError(f"length must be positive. Got {length}.")

    return HKDF(
        algorithm=hashes.SHA384(),
        length=length,
        salt=clean_salt,
        info=clean_info,
    ).derive(clean_key_material)
