"""AES-256-GCM protection for application payloads under established 256-bit keys."""

from cryptography.exceptions import InvalidTag

from data_protection.aes_gcm import (
    AES_256_KEY_BYTES,
    decrypt_aes_256_gcm,
    encrypt_aes_256_gcm,
)
from data_protection.context import (
    DATA_PLANE_AAD_DOMAIN,
    DATA_PLANE_ALGORITHM,
    DATA_PLANE_CONTEXT_DOMAIN,
    DATA_PLANE_KEY_BITS,
    DATA_PLANE_NONCE_BYTES,
    DATA_PLANE_TAG_BYTES,
    DATA_PLANE_VERSION,
    MAX_SEQUENCE_NUMBER,
    DataPlaneContext,
    DataPlaneDirection,
    canonical_data_plane_aad,
    nonce_for,
)
from data_protection.record import PROTECTED_RECORD_VERSION, ProtectedRecord
from data_protection.session import ProtectedSession

__all__ = [
    "AES_256_KEY_BYTES",
    "DATA_PLANE_AAD_DOMAIN",
    "DATA_PLANE_ALGORITHM",
    "DATA_PLANE_CONTEXT_DOMAIN",
    "DATA_PLANE_KEY_BITS",
    "DATA_PLANE_NONCE_BYTES",
    "DATA_PLANE_TAG_BYTES",
    "DATA_PLANE_VERSION",
    "MAX_SEQUENCE_NUMBER",
    "PROTECTED_RECORD_VERSION",
    "DataPlaneContext",
    "DataPlaneDirection",
    "InvalidTag",
    "ProtectedRecord",
    "ProtectedSession",
    "canonical_data_plane_aad",
    "decrypt_aes_256_gcm",
    "encrypt_aes_256_gcm",
    "nonce_for",
]
