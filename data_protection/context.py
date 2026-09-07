"""Public context and deterministic nonce policy for the AES-256-GCM data plane."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha384
from struct import pack
from types import MappingProxyType
from typing import Final

DATA_PLANE_VERSION: Final = 1
DATA_PLANE_CONTEXT_DOMAIN: Final = b"QuantumSec/DataPlane/v1/Context"
DATA_PLANE_AAD_DOMAIN: Final = b"QuantumSec/DataPlane/v1/AAD"
DATA_PLANE_ALGORITHM: Final = "AES-256-GCM"
DATA_PLANE_KEY_TYPE: Final = "session_key"
DATA_PLANE_KEY_BITS: Final = 256
DATA_PLANE_SESSION_ID_BYTES: Final = 16
DATA_PLANE_NONCE_BYTES: Final = 12
DATA_PLANE_TAG_BYTES: Final = 16
MAX_SEQUENCE_NUMBER: Final = (1 << 64) - 1

type PublicContextEntries = tuple[tuple[str, str | int], ...]
type PublicContextInput = PublicContextEntries | Mapping[str, str | int]


class DataPlaneDirection(StrEnum):
    ALICE_TO_BOB = "alice_to_bob"
    BOB_TO_ALICE = "bob_to_alice"


DIRECTION_NONCE_PREFIXES: Final = MappingProxyType(
    {
        DataPlaneDirection.ALICE_TO_BOB: b"\x00\x00\x00\x01",
        DataPlaneDirection.BOB_TO_ALICE: b"\x00\x00\x00\x02",
    }
)


def _require_bytes(
    value: object,
    *,
    name: str,
    length: int | None = None,
    allow_empty: bool = True,
) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes.")
    if length is not None and len(value) != length:
        raise ValueError(f"{name} must contain exactly {length} bytes.")
    if not allow_empty and not value:
        raise ValueError(f"{name} must not be empty.")
    return memoryview(value).tobytes()


def _require_text(value: object, *, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string.")
    value.encode("utf-8")
    return value


def _require_uint(value: object, *, name: str, maximum: int = MAX_SEQUENCE_NUMBER) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ValueError(f"{name} must be an unsigned integer no greater than {maximum}.")
    return value


def _length_prefixed(value: bytes) -> bytes:
    return pack(">Q", len(value)) + value


def _encode_public_context(entries: PublicContextEntries) -> bytes:
    encoded = [pack(">H", len(entries))]
    for name, value in entries:
        encoded.append(_length_prefixed(name.encode("utf-8")))
        if isinstance(value, str):
            encoded.extend((b"S", _length_prefixed(value.encode("utf-8"))))
        else:
            encoded.extend((b"I", pack(">Q", value)))
    return b"".join(encoded)


@dataclass(frozen=True, slots=True, repr=False)
class DataPlaneContext:
    """Immutable public binding between an established session and protected records."""

    session_id: bytes = field(repr=False)
    profile: str
    session_result_version: int
    key_type: str
    key_bits: int
    public_context: PublicContextInput
    version: int = DATA_PLANE_VERSION

    def __post_init__(self) -> None:
        if self.version != DATA_PLANE_VERSION:
            raise ValueError(f"version must be {DATA_PLANE_VERSION}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=DATA_PLANE_SESSION_ID_BYTES,
        )
        profile = _require_text(self.profile, name="profile")
        session_result_version = _require_uint(
            self.session_result_version,
            name="session_result_version",
            maximum=0xFFFF,
        )
        if session_result_version == 0:
            raise ValueError("session_result_version must be positive.")
        if self.key_type != DATA_PLANE_KEY_TYPE:
            raise ValueError(f"key_type must be {DATA_PLANE_KEY_TYPE!r}.")
        if self.key_bits != DATA_PLANE_KEY_BITS:
            raise ValueError(f"key_bits must be {DATA_PLANE_KEY_BITS}.")

        entries = (
            tuple(self.public_context.items())
            if isinstance(self.public_context, Mapping)
            else tuple(self.public_context)
        )
        if not entries:
            raise ValueError("public_context must contain the established session binding.")
        clean_entries: list[tuple[str, str | int]] = []
        for entry in entries:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise ValueError("public_context entries must be key/value tuples.")
            name = _require_text(entry[0], name="public_context key")
            value = entry[1]
            if isinstance(value, bool) or not isinstance(value, (str, int)):
                raise ValueError("public_context values must be strings or unsigned integers.")
            if isinstance(value, str):
                clean_value: str | int = _require_text(value, name=f"public_context[{name!r}]")
            else:
                clean_value = _require_uint(value, name=f"public_context[{name!r}]")
            clean_entries.append((name, clean_value))
        if len({name for name, _value in clean_entries}) != len(clean_entries):
            raise ValueError("public_context keys must be unique.")
        clean_entries.sort(key=lambda entry: entry[0].encode("utf-8"))

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "profile", profile)
        object.__setattr__(self, "session_result_version", session_result_version)
        object.__setattr__(self, "public_context", tuple(clean_entries))

    def canonical_bytes(self) -> bytes:
        return b"".join(
            (
                _length_prefixed(DATA_PLANE_CONTEXT_DOMAIN),
                pack(">H", self.version),
                _length_prefixed(self.session_id),
                _length_prefixed(self.profile.encode("utf-8")),
                pack(">H", self.session_result_version),
                _length_prefixed(self.key_type.encode("ascii")),
                pack(">H", self.key_bits),
                _encode_public_context(
                    tuple(self.public_context.items())
                    if isinstance(self.public_context, Mapping)
                    else self.public_context
                ),
            )
        )

    @property
    def context_hash(self) -> bytes:
        return sha384(self.canonical_bytes()).digest()

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "session_id": self.session_id.hex(),
            "profile": self.profile,
            "session_result_version": self.session_result_version,
            "key_type": self.key_type,
            "key_bits": self.key_bits,
            "public_context": dict(self.public_context),
            "context_hash_sha384": self.context_hash.hex(),
        }

    def __repr__(self) -> str:
        return (
            f"DataPlaneContext(version={self.version}, profile={self.profile!r}, "
            f"session_result_version={self.session_result_version}, key_type={self.key_type!r}, "
            f"key_bits={self.key_bits}, context_hash={self.context_hash.hex()!r})"
        )


def nonce_for(direction: DataPlaneDirection, sequence_number: int) -> bytes:
    """Build one 96-bit nonce from a disjoint direction prefix and uint64 sequence."""

    if not isinstance(direction, DataPlaneDirection):
        raise TypeError("direction must be a DataPlaneDirection.")
    sequence = _require_uint(sequence_number, name="sequence_number")
    return DIRECTION_NONCE_PREFIXES[direction] + pack(">Q", sequence)


def canonical_data_plane_aad(
    context: DataPlaneContext,
    direction: DataPlaneDirection,
    sequence_number: int,
    application_aad: bytes = b"",
    *,
    declared_application_aad_bytes: int | None = None,
) -> bytes:
    """Encode complete session, record, and application binding for AES-GCM."""

    if not isinstance(context, DataPlaneContext):
        raise TypeError("context must be a DataPlaneContext.")
    if not isinstance(direction, DataPlaneDirection):
        raise TypeError("direction must be a DataPlaneDirection.")
    sequence = _require_uint(sequence_number, name="sequence_number")
    aad = _require_bytes(application_aad, name="application_aad")
    aad_bytes = (
        len(aad)
        if declared_application_aad_bytes is None
        else _require_uint(
            declared_application_aad_bytes,
            name="declared_application_aad_bytes",
        )
    )
    return b"".join(
        (
            _length_prefixed(DATA_PLANE_AAD_DOMAIN),
            pack(">H", DATA_PLANE_VERSION),
            _length_prefixed(context.canonical_bytes()),
            _length_prefixed(direction.value.encode("ascii")),
            pack(">Q", sequence),
            pack(">Q", aad_bytes),
            _length_prefixed(aad),
        )
    )
