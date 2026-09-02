"""Immutable public messages for the staged PQC handshake."""

from dataclasses import dataclass, field
from struct import pack
from typing import Final

from pqc.kem import (
    HQC_3_ALGORITHM,
    ML_KEM_768_ALGORITHM,
    hqc_3_metadata,
    ml_kem_768_metadata,
)
from pqc.profiles import PQCProfile
from pqc.protocol.identity import _validated_identity_name
from pqc.signatures import ML_DSA_65_METADATA

SERVER_KEY_OFFER_PROTOCOL_VERSION: Final = 1
SERVER_KEY_OFFER_SESSION_ID_LENGTH: Final = 16
SERVER_KEY_OFFER_NONCE_LENGTH: Final = 32
SERVER_KEY_OFFER_DOMAIN_SEPARATOR: Final = b"QuantumSec/PQCHandshake/v1/ServerKeyOffer"


def _require_bytes(value: object, *, name: str, length: int | None = None) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    if length is not None and len(value) != length:
        raise ValueError(f"{name} must contain {length} bytes. Got {len(value)}.")
    if not value:
        raise ValueError(f"{name} must not be empty.")
    return bytes(value)


def _length_prefixed(value: bytes) -> bytes:
    if len(value) > 0xFFFFFFFF:
        raise ValueError("Canonical field exceeds the 32-bit length prefix.")
    return pack(">I", len(value)) + value


@dataclass(frozen=True, slots=True)
class ServerKeyOffer:
    """Public responder KEM material authenticated as one canonical message."""

    protocol_version: int
    session_id: bytes = field(repr=False)
    profile: PQCProfile
    nonce: bytes = field(repr=False)
    ml_kem_algorithm: str
    ml_kem_public_key: bytes = field(repr=False)
    hqc_algorithm: str | None = None
    hqc_public_key: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if (
            isinstance(self.protocol_version, bool)
            or self.protocol_version != SERVER_KEY_OFFER_PROTOCOL_VERSION
        ):
            raise ValueError(
                f"protocol_version must be {SERVER_KEY_OFFER_PROTOCOL_VERSION}. "
                f"Got {self.protocol_version!r}."
            )
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        nonce = _require_bytes(self.nonce, name="nonce", length=SERVER_KEY_OFFER_NONCE_LENGTH)
        if self.ml_kem_algorithm != ML_KEM_768_ALGORITHM:
            raise ValueError(f"ml_kem_algorithm must be {ML_KEM_768_ALGORITHM!r}.")
        ml_kem_metadata = ml_kem_768_metadata()
        ml_kem_public_key = _require_bytes(
            self.ml_kem_public_key,
            name="ml_kem_public_key",
            length=ml_kem_metadata.public_key_length,
        )

        hqc_fields_present = self.hqc_algorithm is not None or self.hqc_public_key is not None
        hqc_public_key: bytes | None = None
        if self.profile is PQCProfile.LOW:
            if hqc_fields_present:
                raise ValueError("LOW ServerKeyOffer must not contain HQC fields.")
        else:
            if self.hqc_algorithm != HQC_3_ALGORITHM or self.hqc_public_key is None:
                raise ValueError("HIGH ServerKeyOffer must contain an HQC-3 public key.")
            hqc_public_key = _require_bytes(
                self.hqc_public_key,
                name="hqc_public_key",
                length=hqc_3_metadata().public_key_length,
            )

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "nonce", nonce)
        object.__setattr__(self, "ml_kem_public_key", ml_kem_public_key)
        object.__setattr__(self, "hqc_public_key", hqc_public_key)

    def canonical_bytes(self) -> bytes:
        """Serialize authenticated fields in one deterministic, unambiguous order."""

        fields = [
            _length_prefixed(SERVER_KEY_OFFER_DOMAIN_SEPARATOR),
            pack(">H", self.protocol_version),
            _length_prefixed(self.session_id),
            _length_prefixed(self.profile.value.encode("ascii")),
            _length_prefixed(self.nonce),
            _length_prefixed(self.ml_kem_algorithm.encode("ascii")),
            _length_prefixed(self.ml_kem_public_key),
        ]
        if self.hqc_algorithm is None or self.hqc_public_key is None:
            fields.append(b"\x00")
        else:
            fields.extend(
                (
                    b"\x01",
                    _length_prefixed(self.hqc_algorithm.encode("ascii")),
                    _length_prefixed(self.hqc_public_key),
                )
            )
        return b"".join(fields)


@dataclass(frozen=True, slots=True)
class SignedServerKeyOffer:
    """A server key offer plus its long-lived responder identity signature."""

    offer: ServerKeyOffer
    signer: str
    signature_algorithm: str
    signature: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.offer, ServerKeyOffer):
            raise TypeError(f"offer must be a ServerKeyOffer. Got {type(self.offer).__name__}.")
        object.__setattr__(self, "signer", _validated_identity_name(self.signer))
        if self.signature_algorithm != ML_DSA_65_METADATA.name:
            raise ValueError(f"signature_algorithm must be {ML_DSA_65_METADATA.name!r}.")
        object.__setattr__(self, "signature", _require_bytes(self.signature, name="signature"))
