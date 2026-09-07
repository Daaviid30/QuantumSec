"""Canonical binary encoding helpers for upper-layer session protocols."""

from struct import pack


def length_prefixed(value: bytes) -> bytes:
    """Encode bytes with an unsigned 64-bit big-endian length."""

    if not isinstance(value, bytes):
        raise TypeError(f"Canonical fields must be bytes. Got {type(value).__name__}.")
    if len(value) > 0xFFFFFFFFFFFFFFFF:
        raise ValueError("Canonical field exceeds the 64-bit length prefix.")
    return pack(">Q", len(value)) + value


def unsigned(value: int, *, width: int = 8) -> bytes:
    """Encode a non-negative integer at a fixed width."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"Canonical integer must be non-negative. Got {value!r}.")
    if width not in (2, 4, 8):
        raise ValueError(f"Unsupported canonical integer width {width}.")
    try:
        return value.to_bytes(width, byteorder="big", signed=False)
    except OverflowError as exc:
        raise ValueError(f"Canonical integer {value} does not fit in {width} bytes.") from exc
