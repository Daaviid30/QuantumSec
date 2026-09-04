"""Phase 6 role-separated Finished exchange and PQC session establishment."""

import hmac
from dataclasses import dataclass, field
from hashlib import sha384
from struct import pack
from types import TracebackType
from typing import Final, Self

from pqc._encoding import _length_prefixed
from pqc.kdf.hkdf import derive_hkdf_sha384
from pqc.profiles import PQCProfile
from pqc.protocol._shared_secret_state import _KEMSharedSecretStateBase
from pqc.protocol.client_exchange import ProcessedClientKeyExchange
from pqc.protocol.initiator import ProcessedServerOffer
from pqc.protocol.key_schedule import (
    DerivedSessionKeyState,
    _key_schedule_info,
    _validated_initiator_secret_state,
    _validated_responder_secret_state,
)
from pqc.protocol.messages import (
    PQC_FINISHED_MAC_ALGORITHM,
    PQC_FINISHED_PROTOCOL_VERSION,
    PQC_FINISHED_SESSION_ID_LENGTH,
    PQC_FINISHED_TRANSCRIPT_HASH_LENGTH,
    PQC_FINISHED_VERIFY_DATA_LENGTH,
    PQCFinishedMessage,
    PQCFinishedRole,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
    _require_bytes,
)
from pqc.protocol.transcript import PQCHandshakeTranscript

PQC_CONFIRMATION_KEY_LENGTH: Final = 32
PQC_CONFIRMATION_KEY_INFO_DOMAIN: Final = b"QuantumSec/PQCHandshake/v1/ConfirmationKey"
PQC_FINISHED_MAC_INPUT_DOMAIN: Final = b"QuantumSec/PQCHandshake/v1/Finished"

_CONFIRMED_HANDSHAKE_PROOF: Final = object()
_ESTABLISHED_SESSION_PROOF: Final = object()


def _confirmation_key_info(*, protocol_version: int, profile: PQCProfile) -> bytes:
    """Build explicit HKDF info for the Phase 6 confirmation-key purpose."""

    return _key_schedule_info(
        domain=PQC_CONFIRMATION_KEY_INFO_DOMAIN,
        protocol_version=protocol_version,
        profile=profile,
    )


def _finished_mac_input(
    *,
    protocol_version: int,
    session_id: bytes,
    profile: PQCProfile,
    sender_role: PQCFinishedRole,
    transcript_hash: bytes,
    responder_verify_data: bytes | None = None,
) -> bytes:
    """Build the canonical, role-separated HMAC input for one Finished message."""

    if (
        isinstance(protocol_version, bool)
        or not isinstance(protocol_version, int)
        or protocol_version != PQC_FINISHED_PROTOCOL_VERSION
    ):
        raise ValueError(f"protocol_version must be {PQC_FINISHED_PROTOCOL_VERSION}.")
    clean_session_id = _require_bytes(
        session_id,
        name="session_id",
        length=PQC_FINISHED_SESSION_ID_LENGTH,
    )
    if not isinstance(profile, PQCProfile):
        raise TypeError(f"profile must be a PQCProfile. Got {type(profile).__name__}.")
    if not isinstance(sender_role, PQCFinishedRole):
        raise TypeError(f"sender_role must be a PQCFinishedRole. Got {type(sender_role).__name__}.")
    clean_transcript_hash = _require_bytes(
        transcript_hash,
        name="transcript_hash",
        length=PQC_FINISHED_TRANSCRIPT_HASH_LENGTH,
    )

    if sender_role is PQCFinishedRole.RESPONDER:
        if responder_verify_data is not None:
            raise ValueError("Responder Finished must not bind previous verify_data.")
        previous_verify_data = b""
    else:
        if responder_verify_data is None:
            raise ValueError("Initiator Finished must bind the responder Finished verify_data.")
        previous_verify_data = _require_bytes(
            responder_verify_data,
            name="responder_verify_data",
            length=PQC_FINISHED_VERIFY_DATA_LENGTH,
        )

    return b"".join(
        (
            _length_prefixed(PQC_FINISHED_MAC_INPUT_DOMAIN),
            pack(">H", protocol_version),
            _length_prefixed(clean_session_id),
            _length_prefixed(profile.value.encode("ascii")),
            _length_prefixed(sender_role.value.encode("ascii")),
            _length_prefixed(PQC_FINISHED_MAC_ALGORITHM.encode("ascii")),
            _length_prefixed(clean_transcript_hash),
            _length_prefixed(previous_verify_data),
        )
    )


def _compute_finished_verify_data(*, confirmation_key: bytes, mac_input: bytes) -> bytes:
    """Compute one Finished value with the standard-library HMAC-SHA-384 primitive."""

    clean_confirmation_key = _require_bytes(
        confirmation_key,
        name="confirmation_key",
        length=PQC_CONFIRMATION_KEY_LENGTH,
    )
    clean_mac_input = _require_bytes(mac_input, name="mac_input")
    verify_data = hmac.new(clean_confirmation_key, clean_mac_input, digestmod=sha384).digest()
    if len(verify_data) != PQC_FINISHED_VERIFY_DATA_LENGTH:
        raise RuntimeError("HMAC-SHA-384 returned an invalid Finished length.")
    return verify_data


def _validated_session_key_state(
    state: DerivedSessionKeyState,
    transcript: PQCHandshakeTranscript,
) -> DerivedSessionKeyState:
    """Require a live Phase 5 key state bound to the exact Phase 6 transcript."""

    if not isinstance(state, DerivedSessionKeyState):
        raise TypeError(f"session_key_state must be a DerivedSessionKeyState. Got {type(state).__name__}.")
    if state.is_closed:
        raise RuntimeError("Session key state is closed.")
    if state.session_id != transcript.session_id:
        raise ValueError("Session key state does not belong to the handshake session.")
    if state.profile is not transcript.profile:
        raise ValueError("Session key state does not match the handshake profile.")
    if not hmac.compare_digest(state.transcript_hash, transcript.transcript_hash):
        raise ValueError("Session key state does not belong to the handshake transcript.")
    return state


@dataclass(slots=True, repr=False)
class PQCConfirmationKeyState:
    """Private role-local Phase 6 key and Finished state machine."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    transcript_hash: bytes
    role: PQCFinishedRole
    _session_key_state: DerivedSessionKeyState = field(repr=False)
    _confirmation_key: bytes | None = field(repr=False)
    _closed: bool = field(default=False, init=False, repr=False)
    _local_finished: PQCFinishedMessage | None = field(default=None, init=False, repr=False)
    _peer_finished: PQCFinishedMessage | None = field(default=None, init=False, repr=False)
    _session_established: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        self.session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=PQC_FINISHED_SESSION_ID_LENGTH,
        )
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        self.transcript_hash = _require_bytes(
            self.transcript_hash,
            name="transcript_hash",
            length=PQC_FINISHED_TRANSCRIPT_HASH_LENGTH,
        )
        if not isinstance(self.role, PQCFinishedRole):
            raise TypeError(f"role must be a PQCFinishedRole. Got {type(self.role).__name__}.")
        if not isinstance(self._session_key_state, DerivedSessionKeyState):
            raise TypeError("_session_key_state must be a DerivedSessionKeyState.")
        if self._session_key_state.is_closed:
            raise RuntimeError("Session key state is closed.")
        if (
            self._session_key_state.session_id != self.session_id
            or self._session_key_state.profile is not self.profile
            or not hmac.compare_digest(
                self._session_key_state.transcript_hash,
                self.transcript_hash,
            )
        ):
            raise ValueError("Session key state does not match the confirmation-key context.")
        self._confirmation_key = _require_bytes(
            self._confirmation_key,
            name="confirmation_key",
            length=PQC_CONFIRMATION_KEY_LENGTH,
        )

    @property
    def is_closed(self) -> bool:
        """Return whether the private confirmation-key reference was released."""

        return self._closed

    def close(self) -> None:
        """Release the confirmation-key reference without closing the session key."""

        self._confirmation_key = None
        self._closed = True

    def _require_open_key(self) -> bytes:
        if self._closed or self._confirmation_key is None:
            raise RuntimeError("Confirmation key state is closed.")
        return self._confirmation_key

    def _build_local_finished(
        self,
        *,
        responder_verify_data: bytes | None = None,
    ) -> PQCFinishedMessage:
        if self._local_finished is not None:
            raise RuntimeError("Local Finished has already been created.")
        confirmation_key = self._require_open_key()
        mac_input = _finished_mac_input(
            protocol_version=PQC_FINISHED_PROTOCOL_VERSION,
            session_id=self.session_id,
            profile=self.profile,
            sender_role=self.role,
            transcript_hash=self.transcript_hash,
            responder_verify_data=responder_verify_data,
        )
        return PQCFinishedMessage(
            protocol_version=PQC_FINISHED_PROTOCOL_VERSION,
            session_id=self.session_id,
            profile=self.profile,
            sender_role=self.role,
            mac_algorithm=PQC_FINISHED_MAC_ALGORITHM,
            transcript_hash=self.transcript_hash,
            verify_data=_compute_finished_verify_data(
                confirmation_key=confirmation_key,
                mac_input=mac_input,
            ),
        )

    def _verify_peer_finished(
        self,
        message: PQCFinishedMessage,
        *,
        expected_role: PQCFinishedRole,
        responder_verify_data: bytes | None = None,
    ) -> None:
        confirmation_key = self._require_open_key()
        if not isinstance(message, PQCFinishedMessage):
            raise TypeError(f"message must be a PQCFinishedMessage. Got {type(message).__name__}.")
        if message.sender_role is not expected_role:
            raise ValueError(f"Expected {expected_role.value} Finished message.")
        if message.protocol_version != PQC_FINISHED_PROTOCOL_VERSION:
            raise ValueError("Finished protocol version does not match the handshake.")
        if message.session_id != self.session_id:
            raise ValueError("Finished session does not match the handshake.")
        if message.profile is not self.profile:
            raise ValueError("Finished profile does not match the handshake.")
        if not hmac.compare_digest(message.transcript_hash, self.transcript_hash):
            raise ValueError("Finished transcript hash does not match the handshake.")
        if message.mac_algorithm != PQC_FINISHED_MAC_ALGORITHM:
            raise ValueError("Finished MAC algorithm does not match the protocol.")

        expected = _compute_finished_verify_data(
            confirmation_key=confirmation_key,
            mac_input=_finished_mac_input(
                protocol_version=message.protocol_version,
                session_id=message.session_id,
                profile=message.profile,
                sender_role=expected_role,
                transcript_hash=message.transcript_hash,
                responder_verify_data=responder_verify_data,
            ),
        )
        if not hmac.compare_digest(message.verify_data, expected):
            raise ValueError("Finished verify_data authentication failed.")

    def __enter__(self) -> Self:
        """Enter a managed lifetime for this private confirmation-key state."""

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release the confirmation key when leaving its managed lifetime."""

        self.close()

    def __repr__(self) -> str:
        return (
            f"PQCConfirmationKeyState(profile={self.profile.value!r}, "
            f"role={self.role.value!r}, transcript_hash={self.transcript_hash.hex()!r}, "
            f"closed={self._closed!r})"
        )


class PQCConfirmationKeyDeriver:
    """Derive a private role-local confirmation key from authenticated Phase 5 state."""

    def derive_initiator(
        self,
        *,
        processed_server_offer: ProcessedServerOffer,
        session_key_state: DerivedSessionKeyState,
        signed_server_offer: SignedServerKeyOffer,
        signed_client_exchange: SignedClientKeyExchange,
    ) -> PQCConfirmationKeyState:
        """Derive Alice's confirmation state and retire her KEM secret state."""

        if not isinstance(processed_server_offer, ProcessedServerOffer):
            raise TypeError(
                "processed_server_offer must be a ProcessedServerOffer. "
                f"Got {type(processed_server_offer).__name__}."
            )
        transcript = PQCHandshakeTranscript.from_messages(
            signed_server_offer,
            signed_client_exchange,
        )
        secret_state = _validated_initiator_secret_state(processed_server_offer, transcript)
        return self._derive(
            secret_state=secret_state,
            session_key_state=session_key_state,
            transcript=transcript,
            role=PQCFinishedRole.INITIATOR,
        )

    def derive_responder(
        self,
        *,
        processed_client_exchange: ProcessedClientKeyExchange,
        session_key_state: DerivedSessionKeyState,
        signed_server_offer: SignedServerKeyOffer,
        signed_client_exchange: SignedClientKeyExchange,
    ) -> PQCConfirmationKeyState:
        """Derive Bob's confirmation state and retire his KEM secret state."""

        if not isinstance(processed_client_exchange, ProcessedClientKeyExchange):
            raise TypeError(
                "processed_client_exchange must be a ProcessedClientKeyExchange. "
                f"Got {type(processed_client_exchange).__name__}."
            )
        transcript = PQCHandshakeTranscript.from_messages(
            signed_server_offer,
            signed_client_exchange,
        )
        secret_state = _validated_responder_secret_state(processed_client_exchange, transcript)
        return self._derive(
            secret_state=secret_state,
            session_key_state=session_key_state,
            transcript=transcript,
            role=PQCFinishedRole.RESPONDER,
        )

    @staticmethod
    def _derive(
        *,
        secret_state: _KEMSharedSecretStateBase,
        session_key_state: DerivedSessionKeyState,
        transcript: PQCHandshakeTranscript,
        role: PQCFinishedRole,
    ) -> PQCConfirmationKeyState:
        if secret_state.session_id != transcript.session_id:
            raise ValueError("KEM secret-state session does not match the handshake transcript.")
        if secret_state.profile is not transcript.profile:
            raise ValueError("KEM secret-state profile does not match the handshake transcript.")
        live_session_key_state = _validated_session_key_state(session_key_state, transcript)

        confirmation_key = derive_hkdf_sha384(
            key_material=secret_state._build_kdf_input(),
            salt=transcript.transcript_hash,
            info=_confirmation_key_info(
                protocol_version=transcript.protocol_version,
                profile=transcript.profile,
            ),
            length=PQC_CONFIRMATION_KEY_LENGTH,
        )
        confirmation_state = PQCConfirmationKeyState(
            session_id=transcript.session_id,
            profile=transcript.profile,
            transcript_hash=transcript.transcript_hash,
            role=role,
            _session_key_state=live_session_key_state,
            _confirmation_key=confirmation_key,
        )
        secret_state.close()
        return confirmation_state


@dataclass(frozen=True, slots=True, repr=False)
class ConfirmedPQCHandshake:
    """Capability produced only after both role-separated Finished MACs verify."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    transcript_hash: bytes
    responder_finished: PQCFinishedMessage = field(repr=False)
    initiator_finished: PQCFinishedMessage = field(repr=False)
    _proof: object = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._proof is not _CONFIRMED_HANDSHAKE_PROOF:
            raise TypeError("ConfirmedPQCHandshake must be created by PQCKeyConfirmation.")
        object.__setattr__(
            self,
            "session_id",
            _require_bytes(
                self.session_id,
                name="session_id",
                length=PQC_FINISHED_SESSION_ID_LENGTH,
            ),
        )
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        object.__setattr__(
            self,
            "transcript_hash",
            _require_bytes(
                self.transcript_hash,
                name="transcript_hash",
                length=PQC_FINISHED_TRANSCRIPT_HASH_LENGTH,
            ),
        )
        if not isinstance(self.responder_finished, PQCFinishedMessage) or not isinstance(
            self.initiator_finished,
            PQCFinishedMessage,
        ):
            raise TypeError("Confirmed handshake requires both Finished messages.")
        if (
            self.responder_finished.sender_role is not PQCFinishedRole.RESPONDER
            or self.initiator_finished.sender_role is not PQCFinishedRole.INITIATOR
        ):
            raise ValueError("Confirmed handshake Finished roles are invalid.")
        for message in (self.responder_finished, self.initiator_finished):
            if (
                message.session_id != self.session_id
                or message.profile is not self.profile
                or not hmac.compare_digest(message.transcript_hash, self.transcript_hash)
            ):
                raise ValueError("Confirmed handshake Finished contexts do not match.")

    @classmethod
    def _from_verified(
        cls,
        *,
        responder_finished: PQCFinishedMessage,
        initiator_finished: PQCFinishedMessage,
    ) -> Self:
        return cls(
            session_id=responder_finished.session_id,
            profile=responder_finished.profile,
            transcript_hash=responder_finished.transcript_hash,
            responder_finished=responder_finished,
            initiator_finished=initiator_finished,
            _proof=_CONFIRMED_HANDSHAKE_PROOF,
        )

    def __repr__(self) -> str:
        return (
            f"ConfirmedPQCHandshake(profile={self.profile.value!r}, "
            f"transcript_hash={self.transcript_hash.hex()!r}, mutually_confirmed=True)"
        )


@dataclass(slots=True, repr=False)
class EstablishedPQCSession:
    """Role-local session-key handle available only after mutual Finished verification."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    transcript_hash: bytes
    role: PQCFinishedRole
    _session_key_state: DerivedSessionKeyState = field(repr=False)
    _proof: object = field(repr=False)

    def __post_init__(self) -> None:
        if self._proof is not _ESTABLISHED_SESSION_PROOF:
            raise TypeError("EstablishedPQCSession must be created from a confirmed handshake.")
        self.session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=PQC_FINISHED_SESSION_ID_LENGTH,
        )
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        self.transcript_hash = _require_bytes(
            self.transcript_hash,
            name="transcript_hash",
            length=PQC_FINISHED_TRANSCRIPT_HASH_LENGTH,
        )
        if not isinstance(self.role, PQCFinishedRole):
            raise TypeError(f"role must be a PQCFinishedRole. Got {type(self.role).__name__}.")
        if not isinstance(self._session_key_state, DerivedSessionKeyState):
            raise TypeError("_session_key_state must be a DerivedSessionKeyState.")
        if self._session_key_state.is_closed:
            raise RuntimeError("Session key state is closed.")
        if (
            self._session_key_state.session_id != self.session_id
            or self._session_key_state.profile is not self.profile
            or not hmac.compare_digest(
                self._session_key_state.transcript_hash,
                self.transcript_hash,
            )
        ):
            raise ValueError("Session key state does not match the established session.")

    @property
    def established(self) -> bool:
        """Return true because this type exists only after mutual confirmation."""

        return True

    @property
    def is_closed(self) -> bool:
        """Return whether the owned session-key state was closed."""

        return self._session_key_state.is_closed

    def export_session_key(self) -> bytes:
        """Explicitly export the established role-local symmetric session key."""

        return self._session_key_state.export_session_key()

    def close(self) -> None:
        """Close the owned session-key state idempotently."""

        self._session_key_state.close()

    def __enter__(self) -> Self:
        """Enter a managed lifetime for this established local session."""

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the session key when leaving the managed lifetime."""

        self.close()

    def __repr__(self) -> str:
        return (
            f"EstablishedPQCSession(profile={self.profile.value!r}, "
            f"role={self.role.value!r}, transcript_hash={self.transcript_hash.hex()!r}, "
            f"established=True, closed={self.is_closed!r})"
        )


class PQCKeyConfirmation:
    """Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order."""

    @staticmethod
    def create_responder_finished(
        responder_state: PQCConfirmationKeyState,
    ) -> PQCFinishedMessage:
        """Create Bob's first Finished flight exactly once."""

        state = PQCKeyConfirmation._require_state(
            responder_state,
            expected_role=PQCFinishedRole.RESPONDER,
        )
        if state._peer_finished is not None:
            raise RuntimeError("Responder confirmation state has already verified its peer.")
        message = state._build_local_finished()
        state._local_finished = message
        return message

    @staticmethod
    def verify_responder_and_create_initiator(
        initiator_state: PQCConfirmationKeyState,
        responder_finished: PQCFinishedMessage,
    ) -> PQCFinishedMessage:
        """Verify Bob before creating Alice's chained Finished response."""

        state = PQCKeyConfirmation._require_state(
            initiator_state,
            expected_role=PQCFinishedRole.INITIATOR,
        )
        if state._peer_finished is not None:
            raise RuntimeError("Initiator confirmation state has already verified its peer.")
        state._verify_peer_finished(
            responder_finished,
            expected_role=PQCFinishedRole.RESPONDER,
        )
        message = state._build_local_finished(
            responder_verify_data=responder_finished.verify_data,
        )
        state._peer_finished = responder_finished
        state._local_finished = message
        state.close()
        return message

    @staticmethod
    def verify_initiator_and_confirm(
        responder_state: PQCConfirmationKeyState,
        initiator_finished: PQCFinishedMessage,
    ) -> ConfirmedPQCHandshake:
        """Verify Alice's chained Finished and produce mutual-confirmation proof."""

        state = PQCKeyConfirmation._require_state(
            responder_state,
            expected_role=PQCFinishedRole.RESPONDER,
        )
        if state._local_finished is None:
            raise RuntimeError("Responder Finished must be created before verifying Alice.")
        if state._peer_finished is not None:
            raise RuntimeError("Responder confirmation state has already verified its peer.")
        state._verify_peer_finished(
            initiator_finished,
            expected_role=PQCFinishedRole.INITIATOR,
            responder_verify_data=state._local_finished.verify_data,
        )
        confirmed = ConfirmedPQCHandshake._from_verified(
            responder_finished=state._local_finished,
            initiator_finished=initiator_finished,
        )
        state._peer_finished = initiator_finished
        state.close()
        return confirmed

    @staticmethod
    def establish_local_session(
        confirmation: ConfirmedPQCHandshake,
        confirmation_state: PQCConfirmationKeyState,
    ) -> EstablishedPQCSession:
        """Materialize one role-local session only from the completed Finished exchange."""

        if not isinstance(confirmation, ConfirmedPQCHandshake):
            raise TypeError(
                f"confirmation must be a ConfirmedPQCHandshake. Got {type(confirmation).__name__}."
            )
        if not isinstance(confirmation_state, PQCConfirmationKeyState):
            raise TypeError(
                "confirmation_state must be a PQCConfirmationKeyState. "
                f"Got {type(confirmation_state).__name__}."
            )
        state = confirmation_state
        if not state.is_closed or state._local_finished is None or state._peer_finished is None:
            raise RuntimeError("Local Finished exchange is incomplete.")
        if state._session_established:
            raise RuntimeError("Local PQC session is already established.")
        if state.role is PQCFinishedRole.INITIATOR:
            expected_local = confirmation.initiator_finished
            expected_peer = confirmation.responder_finished
        else:
            expected_local = confirmation.responder_finished
            expected_peer = confirmation.initiator_finished
        local_matches = hmac.compare_digest(
            state._local_finished.canonical_bytes(),
            expected_local.canonical_bytes(),
        )
        peer_matches = hmac.compare_digest(
            state._peer_finished.canonical_bytes(),
            expected_peer.canonical_bytes(),
        )
        if not local_matches or not peer_matches:
            raise ValueError("Local Finished state does not belong to the confirmed handshake.")

        established = EstablishedPQCSession(
            session_id=confirmation.session_id,
            profile=confirmation.profile,
            transcript_hash=confirmation.transcript_hash,
            role=state.role,
            _session_key_state=state._session_key_state,
            _proof=_ESTABLISHED_SESSION_PROOF,
        )
        state._session_established = True
        return established

    @staticmethod
    def _require_state(
        state: PQCConfirmationKeyState,
        *,
        expected_role: PQCFinishedRole,
    ) -> PQCConfirmationKeyState:
        if not isinstance(state, PQCConfirmationKeyState):
            raise TypeError(f"state must be a PQCConfirmationKeyState. Got {type(state).__name__}.")
        if state.role is not expected_role:
            raise ValueError(f"Confirmation state must belong to the {expected_role.value} role.")
        if state.is_closed:
            raise RuntimeError("Confirmation key state is closed.")
        return state
