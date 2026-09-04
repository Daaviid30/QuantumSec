"""Internal canonical binary encoding primitives shared across PQC domains."""

from struct import pack


def _length_prefixed(value: bytes) -> bytes:
    """Prefix bytes with an unsigned 32-bit big-endian length."""

    if len(value) > 0xFFFFFFFF:
        raise ValueError("Canonical field exceeds the 32-bit length prefix.")
    return pack(">I", len(value)) + value
