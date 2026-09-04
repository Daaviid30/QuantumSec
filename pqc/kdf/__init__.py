"""Canonical KEM input construction and HKDF primitives for QuantumSec."""

from pqc.kdf.combiner import KEM_SECRET_INPUT_DOMAIN, canonical_kem_secret_input
from pqc.kdf.hkdf import derive_hkdf_sha384

__all__ = [
    "KEM_SECRET_INPUT_DOMAIN",
    "canonical_kem_secret_input",
    "derive_hkdf_sha384",
]
