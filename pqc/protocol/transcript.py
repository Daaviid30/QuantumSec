"""Canonical public transcript for mutually authenticated PQC handshake messages."""

import hmac
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha384
from typing import Final, Self

from pqc._encoding import _length_prefixed
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.messages import SignedClientKeyExchange, SignedServerKeyOffer

PQC_HANDSHAKE_TRANSCRIPT_DOMAIN: Final = b"QuantumSec/PQCHandshake/v1/Transcript"
PQC_TRANSCRIPT_HASH_LENGTH: Final = 48


@dataclass(frozen=True, slots=True, repr=False)
class PQCHandshakeTranscript:
    """Immutable authenticated public context shared by Alice and Bob."""

    signed_server_offer: SignedServerKeyOffer
    signed_client_exchange: SignedClientKeyExchange

    def __post_init__(self) -> None:
        if not isinstance(self.signed_server_offer, SignedServerKeyOffer):
            raise TypeError(
                "signed_server_offer must be a SignedServerKeyOffer. "
                f"Got {type(self.signed_server_offer).__name__}."
            )
        if not isinstance(self.signed_client_exchange, SignedClientKeyExchange):
            raise TypeError(
                "signed_client_exchange must be a SignedClientKeyExchange. "
                f"Got {type(self.signed_client_exchange).__name__}."
            )

        offer = self.signed_server_offer.offer
        exchange = self.signed_client_exchange.exchange
        if offer.protocol_version != exchange.protocol_version:
            raise ValueError("Handshake transcript protocol versions do not match.")
        if offer.session_id != exchange.session_id:
            raise ValueError("Handshake transcript session IDs do not match.")
        if offer.profile is not exchange.profile:
            raise ValueError("Handshake transcript profiles do not match.")
        expected_offer_hash = sha384(offer.canonical_bytes()).digest()
        if not hmac.compare_digest(expected_offer_hash, exchange.server_offer_hash):
            raise ValueError("Client exchange is not bound to the transcript's server offer.")

        definition = profile_definition(offer.profile)
        if (
            offer.ml_kem_algorithm != exchange.ml_kem_algorithm
            or offer.hqc_algorithm != exchange.hqc_algorithm
            or (offer.hqc_public_key is None) != (definition.hqc_algorithm is None)
            or (exchange.hqc_ciphertext is None) != (definition.hqc_algorithm is None)
            or self.signed_server_offer.signature_algorithm != definition.signature_algorithm
            or self.signed_client_exchange.signature_algorithm != definition.signature_algorithm
        ):
            raise ValueError("Handshake transcript algorithms do not match its profile.")
        if self.signed_server_offer.signer == self.signed_client_exchange.signer:
            raise ValueError("Handshake transcript requires distinct initiator and responder identities.")

    @classmethod
    def from_messages(
        cls,
        signed_server_offer: SignedServerKeyOffer,
        signed_client_exchange: SignedClientKeyExchange,
    ) -> Self:
        """Construct and validate a transcript from the two authenticated wire messages."""

        return cls(
            signed_server_offer=signed_server_offer,
            signed_client_exchange=signed_client_exchange,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this public transcript to a JSON-compatible mapping."""

        return {
            "signed_server_offer": self.signed_server_offer.to_dict(),
            "signed_client_exchange": self.signed_client_exchange.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> Self:
        """Deserialize public messages without authenticating their signatures.

        Successful Phase 3/4 results remain mandatory before this transcript can
        be consumed by :class:`PQCSessionKeyDeriver`.
        """

        if not isinstance(payload, Mapping):
            raise TypeError(f"payload must be a mapping. Got {type(payload).__name__}.")
        required_fields = {"signed_server_offer", "signed_client_exchange"}
        missing = required_fields.difference(payload)
        if missing:
            raise ValueError(
                f"PQC handshake transcript payload is missing fields: {', '.join(sorted(missing))}."
            )
        server_payload = payload["signed_server_offer"]
        client_payload = payload["signed_client_exchange"]
        if not isinstance(server_payload, Mapping):
            raise TypeError("signed_server_offer must be a mapping.")
        if not isinstance(client_payload, Mapping):
            raise TypeError("signed_client_exchange must be a mapping.")
        return cls.from_messages(
            SignedServerKeyOffer.from_dict(server_payload),
            SignedClientKeyExchange.from_dict(client_payload),
        )

    @property
    def protocol_version(self) -> int:
        return self.signed_server_offer.offer.protocol_version

    @property
    def session_id(self) -> bytes:
        return self.signed_server_offer.offer.session_id

    @property
    def profile(self) -> PQCProfile:
        return self.signed_server_offer.offer.profile

    def canonical_bytes(self) -> bytes:
        """Encode the exact signed server and client messages in fixed protocol order."""

        server = self.signed_server_offer
        client = self.signed_client_exchange
        return b"".join(
            (
                _length_prefixed(PQC_HANDSHAKE_TRANSCRIPT_DOMAIN),
                _length_prefixed(server.offer.canonical_bytes()),
                _length_prefixed(server.signer.encode("utf-8")),
                _length_prefixed(server.signature_algorithm.encode("ascii")),
                _length_prefixed(server.signature),
                _length_prefixed(client.exchange.canonical_bytes()),
                _length_prefixed(client.signer.encode("utf-8")),
                _length_prefixed(client.signature_algorithm.encode("ascii")),
                _length_prefixed(client.signature),
            )
        )

    @property
    def transcript_hash(self) -> bytes:
        """Return the public SHA-384 digest of this canonical authenticated transcript."""

        digest = sha384(self.canonical_bytes()).digest()
        if len(digest) != PQC_TRANSCRIPT_HASH_LENGTH:
            raise RuntimeError("SHA-384 returned an invalid transcript hash length.")
        return digest

    def __repr__(self) -> str:
        return (
            f"PQCHandshakeTranscript(profile={self.profile.value!r}, "
            f"server_signer={self.signed_server_offer.signer!r}, "
            f"client_signer={self.signed_client_exchange.signer!r}, "
            f"transcript_hash={self.transcript_hash.hex()!r})"
        )
