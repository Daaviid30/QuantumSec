"""Transcript-bound Phase 5 session-key derivation shared by Alice and Bob."""

from dataclasses import dataclass, field
from struct import pack
from types import TracebackType
from typing import Final, Self

from pqc._encoding import _length_prefixed
from pqc.kdf.hkdf import derive_hkdf_sha384
from pqc.profiles import PQCProfile
from pqc.protocol._shared_secret_state import _KEMSharedSecretStateBase
from pqc.protocol.client_exchange import ProcessedClientKeyExchange, ResponderSharedSecretState
from pqc.protocol.initiator import InitiatorKEMState, ProcessedServerOffer
from pqc.protocol.messages import (
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
    _require_bytes,
)
from pqc.protocol.transcript import (
    PQC_TRANSCRIPT_HASH_LENGTH,
    PQCHandshakeTranscript,
)

PQC_SESSION_KEY_LENGTH: Final = 32
PQC_SESSION_KEY_INFO_DOMAIN: Final = b"QuantumSec/PQCHandshake/v1/SessionKey"


def _session_key_info(*, protocol_version: int, profile: PQCProfile) -> bytes:
    """Build explicit HKDF info for the Phase 5 session-key purpose."""

    if isinstance(protocol_version, bool) or not isinstance(protocol_version, int):
        raise TypeError("protocol_version must be an integer.")
    if not 0 <= protocol_version <= 0xFFFF:
        raise ValueError("protocol_version must fit in an unsigned 16-bit integer.")
    if not isinstance(profile, PQCProfile):
        raise TypeError(f"profile must be a PQCProfile. Got {type(profile).__name__}.")
    return b"".join(
        (
            _length_prefixed(PQC_SESSION_KEY_INFO_DOMAIN),
            pack(">H", protocol_version),
            _length_prefixed(profile.value.encode("ascii")),
        )
    )


@dataclass(slots=True, repr=False)
class DerivedSessionKeyState:
    """Private transcript-bound 256-bit session-key state.

    Source KEM secret states intentionally remain open after derivation so Phase
    6 can derive a distinct confirmation key with a separate HKDF context.
    """

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    transcript_hash: bytes
    _session_key: bytes | None = field(repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        self.session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        self.transcript_hash = _require_bytes(
            self.transcript_hash,
            name="transcript_hash",
            length=PQC_TRANSCRIPT_HASH_LENGTH,
        )
        self._session_key = _require_bytes(
            self._session_key,
            name="session_key",
            length=PQC_SESSION_KEY_LENGTH,
        )

    @property
    def is_closed(self) -> bool:
        """Return whether the private session-key reference was released."""

        return self._closed

    def close(self) -> None:
        """Release the session-key reference idempotently without claiming memory zeroization."""

        self._session_key = None
        self._closed = True

    def __enter__(self) -> Self:
        """Enter a managed lifetime for this private derived-key state."""

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release the session key when leaving a managed lifetime."""

        self.close()

    def __repr__(self) -> str:
        return (
            f"DerivedSessionKeyState(profile={self.profile.value!r}, "
            f"transcript_hash={self.transcript_hash.hex()!r}, "
            f"key_length={PQC_SESSION_KEY_LENGTH}, closed={self._closed!r})"
        )


class PQCSessionKeyDeriver:
    """Derive the same key for either role using one shared transcript-bound schedule."""

    def derive_initiator(
        self,
        *,
        processed_server_offer: ProcessedServerOffer,
        signed_server_offer: SignedServerKeyOffer,
        signed_client_exchange: SignedClientKeyExchange,
    ) -> DerivedSessionKeyState:
        """Derive Alice's key only from a successful authenticated Phase 3 result."""

        if not isinstance(processed_server_offer, ProcessedServerOffer):
            raise TypeError(
                "processed_server_offer must be a ProcessedServerOffer. "
                f"Got {type(processed_server_offer).__name__}."
            )
        transcript = PQCHandshakeTranscript.from_messages(
            signed_server_offer,
            signed_client_exchange,
        )
        state = self._validated_initiator_state(processed_server_offer, transcript)
        return self._derive(state, transcript)

    def derive_responder(
        self,
        *,
        processed_client_exchange: ProcessedClientKeyExchange,
        signed_server_offer: SignedServerKeyOffer,
        signed_client_exchange: SignedClientKeyExchange,
    ) -> DerivedSessionKeyState:
        """Derive Bob's key only from a successful authenticated Phase 4 result."""

        if not isinstance(processed_client_exchange, ProcessedClientKeyExchange):
            raise TypeError(
                "processed_client_exchange must be a ProcessedClientKeyExchange. "
                f"Got {type(processed_client_exchange).__name__}."
            )
        transcript = PQCHandshakeTranscript.from_messages(
            signed_server_offer,
            signed_client_exchange,
        )
        state = self._validated_responder_state(processed_client_exchange, transcript)
        return self._derive(state, transcript)

    @staticmethod
    def _validated_initiator_state(
        processed: ProcessedServerOffer,
        transcript: PQCHandshakeTranscript,
    ) -> InitiatorKEMState:
        if not processed.authenticated or processed.initiator_state is None:
            raise ValueError("Initiator key derivation requires an authenticated Phase 3 result.")
        if processed.authenticated_offer != transcript.signed_server_offer:
            raise ValueError("Phase 3 result does not belong to the transcript's signed server offer.")
        response = processed.public_encapsulation
        if response is None:
            raise ValueError("Authenticated Phase 3 result is missing its public encapsulation.")
        exchange = transcript.signed_client_exchange.exchange
        if processed.signer != transcript.signed_server_offer.signer:
            raise ValueError("Phase 3 responder identity does not match the handshake transcript.")
        if (
            response.session_id != exchange.session_id
            or response.profile is not exchange.profile
            or response.ml_kem_algorithm != exchange.ml_kem_algorithm
            or response.ml_kem_ciphertext != exchange.ml_kem_ciphertext
            or response.hqc_algorithm != exchange.hqc_algorithm
            or response.hqc_ciphertext != exchange.hqc_ciphertext
        ):
            raise ValueError("Phase 3 encapsulation does not match the signed client exchange.")
        return processed.initiator_state

    @staticmethod
    def _validated_responder_state(
        processed: ProcessedClientKeyExchange,
        transcript: PQCHandshakeTranscript,
    ) -> ResponderSharedSecretState:
        if not processed.authenticated or processed.responder_state is None:
            raise ValueError("Responder key derivation requires an authenticated Phase 4 result.")
        if processed.authenticated_exchange != transcript.signed_client_exchange:
            raise ValueError("Phase 4 result does not belong to the transcript's signed client exchange.")
        if processed.signer != transcript.signed_client_exchange.signer:
            raise ValueError("Phase 4 initiator identity does not match the handshake transcript.")
        return processed.responder_state

    @staticmethod
    def _derive(
        secret_state: _KEMSharedSecretStateBase,
        transcript: PQCHandshakeTranscript,
    ) -> DerivedSessionKeyState:
        if secret_state.profile is not transcript.profile:
            raise ValueError("KEM secret-state profile does not match the handshake transcript.")
        if secret_state.session_id != transcript.session_id:
            raise ValueError("KEM secret-state session does not match the handshake transcript.")

        session_key = derive_hkdf_sha384(
            key_material=secret_state._build_kdf_input(),
            salt=transcript.transcript_hash,
            info=_session_key_info(
                protocol_version=transcript.protocol_version,
                profile=transcript.profile,
            ),
            length=PQC_SESSION_KEY_LENGTH,
        )
        return DerivedSessionKeyState(
            session_id=transcript.session_id,
            profile=transcript.profile,
            transcript_hash=transcript.transcript_hash,
            _session_key=session_key,
        )
