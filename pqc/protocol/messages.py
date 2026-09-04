"""Immutable public messages for the staged PQC handshake."""

import base64
import binascii
from collections.abc import Mapping
from dataclasses import dataclass, field
from struct import pack
from typing import Final, Self

from pqc._encoding import _length_prefixed
from pqc.kem import (
    hqc_3_metadata,
    ml_kem_768_metadata,
)
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.identity import _validated_identity_name

SERVER_KEY_OFFER_PROTOCOL_VERSION: Final = 1
SERVER_KEY_OFFER_SESSION_ID_LENGTH: Final = 16
SERVER_KEY_OFFER_NONCE_LENGTH: Final = 32
SERVER_KEY_OFFER_DOMAIN_SEPARATOR: Final = b"QuantumSec/PQCHandshake/v1/ServerKeyOffer"
CLIENT_KEY_EXCHANGE_PROTOCOL_VERSION: Final = 1
CLIENT_KEY_EXCHANGE_NONCE_LENGTH: Final = 32
CLIENT_KEY_EXCHANGE_SERVER_OFFER_HASH_LENGTH: Final = 48
CLIENT_KEY_EXCHANGE_DOMAIN_SEPARATOR: Final = b"QuantumSec/PQCHandshake/v1/ClientKeyExchange"


def _require_bytes(value: object, *, name: str, length: int | None = None) -> bytes:
    """Validate that an argument is non-empty bytes and matches an optional expected length."""
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    if length is not None and len(value) != length:
        raise ValueError(f"{name} must contain {length} bytes. Got {len(value)}.")
    if not value:
        raise ValueError(f"{name} must not be empty.")
    return bytes(value)


def _decode_base64_field(value: object, *, name: str) -> bytes:
    """Decode a Base64-encoded string into raw bytes, raising ValueError if the data is invalid."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a Base64 string. Got {type(value).__name__}.")
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"{name} must be valid Base64.") from exc


def _require_transport_fields(
    payload: Mapping[str, object],
    *,
    message_name: str,
    fields: set[str],
) -> None:
    """Ensure all required transport keys exist in the provided payload dictionary."""
    missing = fields.difference(payload)
    if missing:
        raise ValueError(f"{message_name} payload is missing fields: {', '.join(sorted(missing))}.")


@dataclass(frozen=True, slots=True)
class ServerKeyOffer:
    """Immutable message containing responder ephemeral KEM public keys and handshake session parameters."""

    protocol_version: int
    session_id: bytes = field(repr=False)
    profile: PQCProfile
    nonce: bytes = field(repr=False)
    ml_kem_algorithm: str
    ml_kem_public_key: bytes = field(repr=False)
    hqc_algorithm: str | None = None
    hqc_public_key: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate protocol version, session ID, nonce, profile, and algorithm public key buffer lengths."""
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
        definition = profile_definition(self.profile)
        if self.ml_kem_algorithm != definition.ml_kem_algorithm:
            raise ValueError(f"ml_kem_algorithm must be {definition.ml_kem_algorithm!r}.")
        ml_kem_metadata = ml_kem_768_metadata()
        ml_kem_public_key = _require_bytes(
            self.ml_kem_public_key,
            name="ml_kem_public_key",
            length=ml_kem_metadata.public_key_length,
        )

        hqc_fields_present = self.hqc_algorithm is not None or self.hqc_public_key is not None
        hqc_public_key: bytes | None = None
        if definition.hqc_algorithm is None:
            if hqc_fields_present:
                raise ValueError("LOW ServerKeyOffer must not contain HQC fields.")
        else:
            if self.hqc_algorithm != definition.hqc_algorithm or self.hqc_public_key is None:
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
        """Serialize authenticated offer fields into a deterministic length-prefixed byte stream."""

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

    def to_dict(self) -> dict[str, object]:
        """Serialize this public offer to a JSON-compatible mapping."""

        return {
            "protocol_version": self.protocol_version,
            "session_id": base64.b64encode(self.session_id).decode("ascii"),
            "profile": self.profile.value,
            "nonce": base64.b64encode(self.nonce).decode("ascii"),
            "ml_kem_algorithm": self.ml_kem_algorithm,
            "ml_kem_public_key": base64.b64encode(self.ml_kem_public_key).decode("ascii"),
            "hqc_algorithm": self.hqc_algorithm,
            "hqc_public_key": (
                None if self.hqc_public_key is None else base64.b64encode(self.hqc_public_key).decode("ascii")
            ),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Restore and validate an offer from its JSON-compatible mapping."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        _require_transport_fields(
            payload,
            message_name="Server key offer",
            fields={
                "protocol_version",
                "session_id",
                "profile",
                "nonce",
                "ml_kem_algorithm",
                "ml_kem_public_key",
                "hqc_algorithm",
                "hqc_public_key",
            },
        )
        protocol_version = payload["protocol_version"]
        profile_value = payload["profile"]
        ml_kem_algorithm = payload["ml_kem_algorithm"]
        hqc_algorithm = payload["hqc_algorithm"]
        if isinstance(protocol_version, bool) or not isinstance(protocol_version, int):
            raise TypeError("protocol_version must be an integer.")
        if not isinstance(profile_value, str):
            raise TypeError("profile must be a string.")
        try:
            profile = PQCProfile(profile_value)
        except ValueError as exc:
            raise ValueError(f"Unknown PQC profile {profile_value!r}.") from exc
        if not isinstance(ml_kem_algorithm, str):
            raise TypeError("ml_kem_algorithm must be a string.")
        if hqc_algorithm is not None and not isinstance(hqc_algorithm, str):
            raise TypeError("hqc_algorithm must be a string or null.")
        encoded_hqc_public_key = payload["hqc_public_key"]
        hqc_public_key = (
            None
            if encoded_hqc_public_key is None
            else _decode_base64_field(encoded_hqc_public_key, name="hqc_public_key")
        )
        return cls(
            protocol_version=protocol_version,
            session_id=_decode_base64_field(payload["session_id"], name="session_id"),
            profile=profile,
            nonce=_decode_base64_field(payload["nonce"], name="nonce"),
            ml_kem_algorithm=ml_kem_algorithm,
            ml_kem_public_key=_decode_base64_field(
                payload["ml_kem_public_key"],
                name="ml_kem_public_key",
            ),
            hqc_algorithm=hqc_algorithm,
            hqc_public_key=hqc_public_key,
        )


@dataclass(frozen=True, slots=True)
class SignedServerKeyOffer:
    """Immutable container wrapping a ServerKeyOffer and its responder signature."""

    offer: ServerKeyOffer
    signer: str
    signature_algorithm: str
    signature: bytes = field(repr=False)

    def __post_init__(self) -> None:
        """Validate wrapped offer type, signer name, signature algorithm, and signature bytes."""
        if not isinstance(self.offer, ServerKeyOffer):
            raise TypeError(f"offer must be a ServerKeyOffer. Got {type(self.offer).__name__}.")
        object.__setattr__(self, "signer", _validated_identity_name(self.signer))
        expected_algorithm = profile_definition(self.offer.profile).signature_algorithm
        if self.signature_algorithm != expected_algorithm:
            raise ValueError(f"signature_algorithm must be {expected_algorithm!r}.")
        object.__setattr__(self, "signature", _require_bytes(self.signature, name="signature"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this signed public offer to a JSON-compatible mapping."""

        return {
            "offer": self.offer.to_dict(),
            "signer": self.signer,
            "signature_algorithm": self.signature_algorithm,
            "signature": base64.b64encode(self.signature).decode("ascii"),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize a signed server key offer from a dictionary without verifying signatures."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        _require_transport_fields(
            payload,
            message_name="Signed server key offer",
            fields={"offer", "signer", "signature_algorithm", "signature"},
        )
        offer_payload = payload["offer"]
        signer = payload["signer"]
        signature_algorithm = payload["signature_algorithm"]
        if not isinstance(offer_payload, Mapping):
            raise TypeError("offer must be a mapping.")
        if not isinstance(signer, str) or not isinstance(signature_algorithm, str):
            raise TypeError("signer and signature_algorithm must be strings.")
        return cls(
            offer=ServerKeyOffer.from_dict(offer_payload),
            signer=signer,
            signature_algorithm=signature_algorithm,
            signature=_decode_base64_field(payload["signature"], name="signature"),
        )


@dataclass(frozen=True, slots=True, repr=False)
class EncapsulationResponse:
    """Unsigned public KEM ciphertext message prepared for the next phase."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    ml_kem_algorithm: str
    ml_kem_ciphertext: bytes = field(repr=False)
    hqc_algorithm: str | None = None
    hqc_ciphertext: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        definition = profile_definition(self.profile)
        if self.ml_kem_algorithm != definition.ml_kem_algorithm:
            raise ValueError(f"ml_kem_algorithm must be {definition.ml_kem_algorithm!r}.")
        ml_kem_ciphertext = _require_bytes(
            self.ml_kem_ciphertext,
            name="ml_kem_ciphertext",
            length=ml_kem_768_metadata().ciphertext_length,
        )

        hqc_fields_present = self.hqc_algorithm is not None or self.hqc_ciphertext is not None
        hqc_ciphertext: bytes | None = None
        if definition.hqc_algorithm is None:
            if hqc_fields_present:
                raise ValueError("LOW encapsulation response must not contain HQC fields.")
        else:
            if self.hqc_algorithm != definition.hqc_algorithm or self.hqc_ciphertext is None:
                raise ValueError("HIGH encapsulation response must contain an HQC-3 ciphertext.")
            hqc_ciphertext = _require_bytes(
                self.hqc_ciphertext,
                name="hqc_ciphertext",
                length=hqc_3_metadata().ciphertext_length,
            )

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "ml_kem_ciphertext", ml_kem_ciphertext)
        object.__setattr__(self, "hqc_ciphertext", hqc_ciphertext)

    def to_dict(self) -> dict[str, object]:
        """Serialize this public response to a JSON-compatible mapping."""

        return {
            "session_id": base64.b64encode(self.session_id).decode("ascii"),
            "profile": self.profile.value,
            "ml_kem_algorithm": self.ml_kem_algorithm,
            "ml_kem_ciphertext": base64.b64encode(self.ml_kem_ciphertext).decode("ascii"),
            "hqc_algorithm": self.hqc_algorithm,
            "hqc_ciphertext": (
                None if self.hqc_ciphertext is None else base64.b64encode(self.hqc_ciphertext).decode("ascii")
            ),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Restore and validate a public response from a transport mapping."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        _require_transport_fields(
            payload,
            message_name="Encapsulation response",
            fields={
                "session_id",
                "profile",
                "ml_kem_algorithm",
                "ml_kem_ciphertext",
                "hqc_algorithm",
                "hqc_ciphertext",
            },
        )
        profile_value = payload["profile"]
        ml_kem_algorithm = payload["ml_kem_algorithm"]
        hqc_algorithm = payload["hqc_algorithm"]
        if not isinstance(profile_value, str):
            raise TypeError("profile must be a string.")
        try:
            profile = PQCProfile(profile_value)
        except ValueError as exc:
            raise ValueError(f"Unknown PQC profile {profile_value!r}.") from exc
        if not isinstance(ml_kem_algorithm, str):
            raise TypeError("ml_kem_algorithm must be a string.")
        if hqc_algorithm is not None and not isinstance(hqc_algorithm, str):
            raise TypeError("hqc_algorithm must be a string or null.")
        encoded_hqc_ciphertext = payload["hqc_ciphertext"]
        hqc_ciphertext = (
            None
            if encoded_hqc_ciphertext is None
            else _decode_base64_field(encoded_hqc_ciphertext, name="hqc_ciphertext")
        )
        return cls(
            session_id=_decode_base64_field(payload["session_id"], name="session_id"),
            profile=profile,
            ml_kem_algorithm=ml_kem_algorithm,
            ml_kem_ciphertext=_decode_base64_field(
                payload["ml_kem_ciphertext"],
                name="ml_kem_ciphertext",
            ),
            hqc_algorithm=hqc_algorithm,
            hqc_ciphertext=hqc_ciphertext,
        )

    def __repr__(self) -> str:
        hqc_length = None if self.hqc_ciphertext is None else len(self.hqc_ciphertext)
        return (
            f"EncapsulationResponse(profile={self.profile.value!r}, "
            f"ml_kem_algorithm={self.ml_kem_algorithm!r}, "
            f"ml_kem_ciphertext_length={len(self.ml_kem_ciphertext)}, "
            f"hqc_algorithm={self.hqc_algorithm!r}, hqc_ciphertext_length={hqc_length!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class ClientKeyExchange:
    """Immutable public KEM ciphertext message bound to Bob's exact signed offer."""

    protocol_version: int
    session_id: bytes = field(repr=False)
    profile: PQCProfile
    client_nonce: bytes = field(repr=False)
    server_offer_hash: bytes = field(repr=False)
    ml_kem_algorithm: str
    ml_kem_ciphertext: bytes = field(repr=False)
    hqc_algorithm: str | None = None
    hqc_ciphertext: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate the protocol binding and profile-specific ciphertext fields."""

        if (
            isinstance(self.protocol_version, bool)
            or self.protocol_version != CLIENT_KEY_EXCHANGE_PROTOCOL_VERSION
        ):
            raise ValueError(
                f"protocol_version must be {CLIENT_KEY_EXCHANGE_PROTOCOL_VERSION}. "
                f"Got {self.protocol_version!r}."
            )
        client_nonce = _require_bytes(
            self.client_nonce,
            name="client_nonce",
            length=CLIENT_KEY_EXCHANGE_NONCE_LENGTH,
        )
        server_offer_hash = _require_bytes(
            self.server_offer_hash,
            name="server_offer_hash",
            length=CLIENT_KEY_EXCHANGE_SERVER_OFFER_HASH_LENGTH,
        )
        encapsulation = EncapsulationResponse(
            session_id=self.session_id,
            profile=self.profile,
            ml_kem_algorithm=self.ml_kem_algorithm,
            ml_kem_ciphertext=self.ml_kem_ciphertext,
            hqc_algorithm=self.hqc_algorithm,
            hqc_ciphertext=self.hqc_ciphertext,
        )

        object.__setattr__(self, "session_id", encapsulation.session_id)
        object.__setattr__(self, "client_nonce", client_nonce)
        object.__setattr__(self, "server_offer_hash", server_offer_hash)
        object.__setattr__(self, "ml_kem_ciphertext", encapsulation.ml_kem_ciphertext)
        object.__setattr__(self, "hqc_ciphertext", encapsulation.hqc_ciphertext)

    def canonical_bytes(self) -> bytes:
        """Serialize every authenticated field deterministically and unambiguously."""

        fields = [
            _length_prefixed(CLIENT_KEY_EXCHANGE_DOMAIN_SEPARATOR),
            pack(">H", self.protocol_version),
            _length_prefixed(self.session_id),
            _length_prefixed(self.profile.value.encode("ascii")),
            _length_prefixed(self.client_nonce),
            _length_prefixed(self.server_offer_hash),
            _length_prefixed(self.ml_kem_algorithm.encode("ascii")),
            _length_prefixed(self.ml_kem_ciphertext),
        ]
        if self.hqc_algorithm is None or self.hqc_ciphertext is None:
            fields.append(b"\x00")
        else:
            fields.extend(
                (
                    b"\x01",
                    _length_prefixed(self.hqc_algorithm.encode("ascii")),
                    _length_prefixed(self.hqc_ciphertext),
                )
            )
        return b"".join(fields)

    def to_dict(self) -> dict[str, object]:
        """Serialize this public client exchange to a JSON-compatible mapping."""

        return {
            "protocol_version": self.protocol_version,
            "session_id": base64.b64encode(self.session_id).decode("ascii"),
            "profile": self.profile.value,
            "client_nonce": base64.b64encode(self.client_nonce).decode("ascii"),
            "server_offer_hash": base64.b64encode(self.server_offer_hash).decode("ascii"),
            "ml_kem_algorithm": self.ml_kem_algorithm,
            "ml_kem_ciphertext": base64.b64encode(self.ml_kem_ciphertext).decode("ascii"),
            "hqc_algorithm": self.hqc_algorithm,
            "hqc_ciphertext": (
                None if self.hqc_ciphertext is None else base64.b64encode(self.hqc_ciphertext).decode("ascii")
            ),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Restore and validate a client exchange from a transport mapping."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        _require_transport_fields(
            payload,
            message_name="Client key exchange",
            fields={
                "protocol_version",
                "session_id",
                "profile",
                "client_nonce",
                "server_offer_hash",
                "ml_kem_algorithm",
                "ml_kem_ciphertext",
                "hqc_algorithm",
                "hqc_ciphertext",
            },
        )
        protocol_version = payload["protocol_version"]
        if isinstance(protocol_version, bool) or not isinstance(protocol_version, int):
            raise TypeError("protocol_version must be an integer.")
        encapsulation = EncapsulationResponse.from_dict(
            {
                "session_id": payload["session_id"],
                "profile": payload["profile"],
                "ml_kem_algorithm": payload["ml_kem_algorithm"],
                "ml_kem_ciphertext": payload["ml_kem_ciphertext"],
                "hqc_algorithm": payload["hqc_algorithm"],
                "hqc_ciphertext": payload["hqc_ciphertext"],
            }
        )
        return cls(
            protocol_version=protocol_version,
            session_id=encapsulation.session_id,
            profile=encapsulation.profile,
            client_nonce=_decode_base64_field(payload["client_nonce"], name="client_nonce"),
            server_offer_hash=_decode_base64_field(
                payload["server_offer_hash"],
                name="server_offer_hash",
            ),
            ml_kem_algorithm=encapsulation.ml_kem_algorithm,
            ml_kem_ciphertext=encapsulation.ml_kem_ciphertext,
            hqc_algorithm=encapsulation.hqc_algorithm,
            hqc_ciphertext=encapsulation.hqc_ciphertext,
        )

    def __repr__(self) -> str:
        hqc_length = None if self.hqc_ciphertext is None else len(self.hqc_ciphertext)
        return (
            f"ClientKeyExchange(profile={self.profile.value!r}, "
            f"ml_kem_algorithm={self.ml_kem_algorithm!r}, "
            f"ml_kem_ciphertext_length={len(self.ml_kem_ciphertext)}, "
            f"hqc_algorithm={self.hqc_algorithm!r}, hqc_ciphertext_length={hqc_length!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class SignedClientKeyExchange:
    """Immutable container wrapping Alice's client exchange and ML-DSA signature."""

    exchange: ClientKeyExchange
    signer: str
    signature_algorithm: str
    signature: bytes = field(repr=False)

    def __post_init__(self) -> None:
        """Validate the wrapped exchange, signer identity, algorithm, and signature bytes."""

        if not isinstance(self.exchange, ClientKeyExchange):
            raise TypeError(f"exchange must be a ClientKeyExchange. Got {type(self.exchange).__name__}.")
        object.__setattr__(self, "signer", _validated_identity_name(self.signer))
        expected_algorithm = profile_definition(self.exchange.profile).signature_algorithm
        if self.signature_algorithm != expected_algorithm:
            raise ValueError(f"signature_algorithm must be {expected_algorithm!r}.")
        object.__setattr__(self, "signature", _require_bytes(self.signature, name="signature"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this signed public client exchange to a JSON-compatible mapping."""

        return {
            "exchange": self.exchange.to_dict(),
            "signer": self.signer,
            "signature_algorithm": self.signature_algorithm,
            "signature": base64.b64encode(self.signature).decode("ascii"),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize a signed client exchange without authenticating its signature."""

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        _require_transport_fields(
            payload,
            message_name="Signed client key exchange",
            fields={"exchange", "signer", "signature_algorithm", "signature"},
        )
        exchange_payload = payload["exchange"]
        signer = payload["signer"]
        signature_algorithm = payload["signature_algorithm"]
        if not isinstance(exchange_payload, Mapping):
            raise TypeError("exchange must be a mapping.")
        if not isinstance(signer, str) or not isinstance(signature_algorithm, str):
            raise TypeError("signer and signature_algorithm must be strings.")
        return cls(
            exchange=ClientKeyExchange.from_dict(exchange_payload),
            signer=signer,
            signature_algorithm=signature_algorithm,
            signature=_decode_base64_field(payload["signature"], name="signature"),
        )

    def __repr__(self) -> str:
        return (
            f"SignedClientKeyExchange(exchange={self.exchange!r}, signer={self.signer!r}, "
            f"signature_algorithm={self.signature_algorithm!r}, "
            f"signature_length={len(self.signature)})"
        )
