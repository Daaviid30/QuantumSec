"""Immutable public record produced by the AES-256-GCM data plane."""

from dataclasses import dataclass, field
from struct import pack, unpack
from typing import Final, Self

from data_protection.context import (
    DATA_PLANE_ALGORITHM,
    DATA_PLANE_NONCE_BYTES,
    DATA_PLANE_SESSION_ID_BYTES,
    DATA_PLANE_TAG_BYTES,
    MAX_SEQUENCE_NUMBER,
    DataPlaneDirection,
    _length_prefixed,
    _require_bytes,
    _require_text,
    _require_uint,
    nonce_for,
)

PROTECTED_RECORD_VERSION: Final = 1
PROTECTED_RECORD_DOMAIN: Final = b"QuantumSec/ProtectedRecord/v1"


class _RecordReader:
    __slots__ = ("_data", "_offset")

    def __init__(self, data: bytes) -> None:
        self._data = _require_bytes(data, name="data")
        self._offset = 0

    def _take(self, length: int) -> bytes:
        end = self._offset + length
        if end > len(self._data):
            raise ValueError("Protected record encoding is truncated.")
        value = self._data[self._offset : end]
        self._offset = end
        return value

    def uint16(self) -> int:
        return unpack(">H", self._take(2))[0]

    def uint64(self) -> int:
        return unpack(">Q", self._take(8))[0]

    def length_prefixed(self) -> bytes:
        return self._take(self.uint64())

    def require_end(self) -> None:
        if self._offset != len(self._data):
            raise ValueError("Protected record encoding contains trailing bytes.")


@dataclass(frozen=True, slots=True, repr=False)
class ProtectedRecord:
    version: int
    session_id: bytes = field(repr=False)
    profile: str
    context_hash: bytes
    algorithm: str
    direction: DataPlaneDirection
    sequence_number: int
    nonce: bytes
    ciphertext: bytes = field(repr=False)
    tag: bytes = field(repr=False)
    application_aad_bytes: int

    def __post_init__(self) -> None:
        if self.version != PROTECTED_RECORD_VERSION:
            raise ValueError(f"version must be {PROTECTED_RECORD_VERSION}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=DATA_PLANE_SESSION_ID_BYTES,
        )
        profile = _require_text(self.profile, name="profile")
        context_hash = _require_bytes(self.context_hash, name="context_hash", length=48)
        if self.algorithm != DATA_PLANE_ALGORITHM:
            raise ValueError(f"algorithm must be {DATA_PLANE_ALGORITHM}.")
        if not isinstance(self.direction, DataPlaneDirection):
            raise TypeError("direction must be a DataPlaneDirection.")
        sequence = _require_uint(self.sequence_number, name="sequence_number")
        nonce = _require_bytes(self.nonce, name="nonce", length=DATA_PLANE_NONCE_BYTES)
        if nonce != nonce_for(self.direction, sequence):
            raise ValueError("nonce does not match the record direction and sequence number.")
        ciphertext = _require_bytes(self.ciphertext, name="ciphertext")
        tag = _require_bytes(self.tag, name="tag", length=DATA_PLANE_TAG_BYTES)
        aad_bytes = _require_uint(
            self.application_aad_bytes,
            name="application_aad_bytes",
            maximum=MAX_SEQUENCE_NUMBER,
        )

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "profile", profile)
        object.__setattr__(self, "context_hash", context_hash)
        object.__setattr__(self, "sequence_number", sequence)
        object.__setattr__(self, "nonce", nonce)
        object.__setattr__(self, "ciphertext", ciphertext)
        object.__setattr__(self, "tag", tag)
        object.__setattr__(self, "application_aad_bytes", aad_bytes)

    def canonical_bytes(self) -> bytes:
        """Encode this public transport record with deterministic binary framing."""

        return b"".join(
            (
                _length_prefixed(PROTECTED_RECORD_DOMAIN),
                pack(">H", self.version),
                _length_prefixed(self.session_id),
                _length_prefixed(self.profile.encode("utf-8")),
                _length_prefixed(self.context_hash),
                _length_prefixed(self.algorithm.encode("ascii")),
                _length_prefixed(self.direction.value.encode("ascii")),
                pack(">Q", self.sequence_number),
                _length_prefixed(self.nonce),
                _length_prefixed(self.ciphertext),
                _length_prefixed(self.tag),
                pack(">Q", self.application_aad_bytes),
            )
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Parse one complete canonical record and reject malformed or trailing input."""

        reader = _RecordReader(data)
        if reader.length_prefixed() != PROTECTED_RECORD_DOMAIN:
            raise ValueError("Protected record domain is invalid.")
        version = reader.uint16()
        session_id = reader.length_prefixed()
        try:
            profile = reader.length_prefixed().decode("utf-8")
            context_hash = reader.length_prefixed()
            algorithm = reader.length_prefixed().decode("ascii")
            direction = DataPlaneDirection(reader.length_prefixed().decode("ascii"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError("Protected record text metadata is invalid.") from exc
        sequence_number = reader.uint64()
        nonce = reader.length_prefixed()
        ciphertext = reader.length_prefixed()
        tag = reader.length_prefixed()
        application_aad_bytes = reader.uint64()
        reader.require_end()
        return cls(
            version,
            session_id,
            profile,
            context_hash,
            algorithm,
            direction,
            sequence_number,
            nonce,
            ciphertext,
            tag,
            application_aad_bytes,
        )

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "session_id": self.session_id.hex(),
            "profile": self.profile,
            "context_hash_sha384": self.context_hash.hex(),
            "algorithm": self.algorithm,
            "key_bits": 256,
            "direction": self.direction.value,
            "sequence_number": self.sequence_number,
            "nonce": self.nonce.hex(),
            "ciphertext": self.ciphertext.hex(),
            "tag": self.tag.hex(),
            "sizes": {
                "nonce_bytes": len(self.nonce),
                "tag_bytes": len(self.tag),
                "application_aad_bytes": self.application_aad_bytes,
                "plaintext_bytes": len(self.ciphertext),
                "ciphertext_bytes": len(self.ciphertext),
            },
        }

    def __repr__(self) -> str:
        return (
            f"ProtectedRecord(direction={self.direction.value!r}, "
            f"sequence_number={self.sequence_number}, nonce_bytes={len(self.nonce)}, "
            f"ciphertext_bytes={len(self.ciphertext)}, tag_bytes={len(self.tag)})"
        )
