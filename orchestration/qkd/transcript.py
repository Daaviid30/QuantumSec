"""Canonical, versioned transcript of public security-relevant BB84 communication."""

from dataclasses import dataclass, field
from enum import StrEnum
from struct import pack
from typing import Final

import numpy as np
import numpy.typing as npt

from orchestration._encoding import length_prefixed, unsigned
from qkd.postprocessing.reconciliation import CascadePublicEvent
from qkd.primitives import Basis
from qkd.protocols import BB84SessionResult

QKD_CLASSICAL_TRANSCRIPT_VERSION: Final = 1
QKD_CLASSICAL_SESSION_ID_LENGTH: Final = 16
QKD_CLASSICAL_EVENT_DOMAIN: Final = b"QuantumSec/QKDClassical/v1/Event"
QKD_CLASSICAL_TRANSCRIPT_DOMAIN: Final = b"QuantumSec/QKDClassical/v1/Transcript"


class QKDClassicalDirection(StrEnum):
    ALICE_TO_BOB = "alice_to_bob"
    BOB_TO_ALICE = "bob_to_alice"


class QKDClassicalMessageType(StrEnum):
    ALICE_BASIS_ANNOUNCEMENT = "alice_basis_announcement"
    BOB_BASIS_ANNOUNCEMENT = "bob_basis_announcement"
    SIFTING_SELECTION = "sifting_selection"
    PARAMETER_ESTIMATION_DISCLOSURE = "parameter_estimation_disclosure"
    CASCADE_PERMUTATION = "cascade_permutation"
    CASCADE_ROOT_PARITY = "cascade_root_parity"
    CASCADE_BINARY_PARITY = "cascade_binary_parity"
    KEY_VERIFICATION_SEED = "key_verification_seed"
    KEY_VERIFICATION_TAG = "key_verification_tag"
    PRIVACY_AMPLIFICATION_SEED = "privacy_amplification_seed"


def _binary_payload(values: npt.ArrayLike) -> bytes:
    bits = np.asarray(values, dtype=np.uint8)
    if bits.ndim != 1 or np.any((bits != 0) & (bits != 1)):
        raise ValueError("A transcript bit vector must be one-dimensional and binary.")
    packed = np.packbits(bits, bitorder="big").tobytes()
    return unsigned(int(bits.size)) + length_prefixed(packed)


def _indices_payload(values: npt.ArrayLike) -> bytes:
    indices = np.asarray(values)
    if indices.ndim != 1 or not np.issubdtype(indices.dtype, np.integer) or np.any(indices < 0):
        raise ValueError("Transcript indices must be a one-dimensional non-negative integer vector.")
    encoded = b"".join(unsigned(int(index)) for index in indices)
    return unsigned(int(indices.size)) + length_prefixed(encoded)


def _bases_payload(values: tuple[Basis, ...]) -> bytes:
    try:
        encoded = bytes(0 if basis is Basis.Z else 1 if basis is Basis.X else 2 for basis in values)
    except TypeError as exc:
        raise ValueError("Transcript bases must contain Basis values.") from exc
    if any(basis not in (Basis.Z, Basis.X) for basis in values):
        raise ValueError("The BB84 transcript supports only Z and X bases.")
    return unsigned(len(values)) + length_prefixed(encoded)


def _fields(*values: bytes) -> bytes:
    return b"".join(length_prefixed(value) for value in values)


@dataclass(frozen=True, slots=True, repr=False)
class QKDClassicalEvent:
    sequence_number: int
    direction: QKDClassicalDirection
    message_type: QKDClassicalMessageType
    payload: bytes = field(repr=False)

    def __post_init__(self) -> None:
        unsigned(self.sequence_number)
        if not isinstance(self.direction, QKDClassicalDirection):
            raise TypeError("direction must be a QKDClassicalDirection.")
        if not isinstance(self.message_type, QKDClassicalMessageType):
            raise TypeError("message_type must be a QKDClassicalMessageType.")
        if not isinstance(self.payload, bytes):
            raise TypeError(f"payload must be bytes. Got {type(self.payload).__name__}.")
        object.__setattr__(self, "payload", bytes(self.payload))

    def canonical_bytes(self, session_id: bytes) -> bytes:
        """Bind payload to domain, version, session, direction, sequence, and message type."""

        if not isinstance(session_id, bytes) or len(session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        return b"".join(
            (
                length_prefixed(QKD_CLASSICAL_EVENT_DOMAIN),
                unsigned(QKD_CLASSICAL_TRANSCRIPT_VERSION, width=2),
                length_prefixed(session_id),
                length_prefixed(self.direction.value.encode("ascii")),
                unsigned(self.sequence_number),
                length_prefixed(self.message_type.value.encode("ascii")),
                length_prefixed(self.payload),
            )
        )

    def __repr__(self) -> str:
        return (
            f"QKDClassicalEvent(sequence_number={self.sequence_number}, "
            f"direction={self.direction.value!r}, message_type={self.message_type.value!r}, "
            f"payload_bytes={len(self.payload)})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class QKDClassicalTranscript:
    session_id: bytes = field(repr=False)
    events: tuple[QKDClassicalEvent, ...] = field(repr=False)
    version: int = QKD_CLASSICAL_TRANSCRIPT_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, bytes) or len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        if self.version != QKD_CLASSICAL_TRANSCRIPT_VERSION:
            raise ValueError(f"version must be {QKD_CLASSICAL_TRANSCRIPT_VERSION}.")
        events = tuple(self.events)
        if not events or not all(isinstance(event, QKDClassicalEvent) for event in events):
            raise ValueError("events must contain at least one QKDClassicalEvent.")
        if tuple(event.sequence_number for event in events) != tuple(range(len(events))):
            raise ValueError("Transcript event sequence numbers must be contiguous and ordered from zero.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "events", events)

    @property
    def message_count(self) -> int:
        return len(self.events)

    def canonical_bytes(self) -> bytes:
        encoded_events = b"".join(
            length_prefixed(event.canonical_bytes(self.session_id)) for event in self.events
        )
        return b"".join(
            (
                length_prefixed(QKD_CLASSICAL_TRANSCRIPT_DOMAIN),
                unsigned(self.version, width=2),
                length_prefixed(self.session_id),
                unsigned(len(self.events)),
                encoded_events,
            )
        )

    def __repr__(self) -> str:
        return (
            f"QKDClassicalTranscript(session_id={self.session_id.hex()!r}, "
            f"version={self.version}, message_count={self.message_count}, "
            f"canonical_bytes={len(self.canonical_bytes())})"
        )


def _cascade_payload(event: CascadePublicEvent) -> bytes:
    parity = b"\xff" if event.parity is None else bytes((event.parity,))
    return _fields(
        unsigned(event.pass_index),
        unsigned(event.active_pass_index),
        pack(">q", event.block_index),
        unsigned(event.query_index),
        b"\x01" if event.active_pass_index != event.pass_index else b"\x00",
        _indices_payload(event.indices),
        parity,
    )


def build_qkd_classical_transcript(
    session: BB84SessionResult,
    session_id: bytes,
) -> QKDClassicalTranscript:
    """Extract the exact modeled public BB84 communication into canonical ordered events."""

    if not isinstance(session, BB84SessionResult):
        raise TypeError(f"session must be a BB84SessionResult. Got {type(session).__name__}.")
    events: list[QKDClassicalEvent] = []

    def append(
        direction: QKDClassicalDirection,
        message_type: QKDClassicalMessageType,
        payload: bytes,
    ) -> None:
        events.append(QKDClassicalEvent(len(events), direction, message_type, payload))

    raw = session.raw
    append(
        QKDClassicalDirection.ALICE_TO_BOB,
        QKDClassicalMessageType.ALICE_BASIS_ANNOUNCEMENT,
        _bases_payload(raw.alice_bases),
    )
    append(
        QKDClassicalDirection.BOB_TO_ALICE,
        QKDClassicalMessageType.BOB_BASIS_ANNOUNCEMENT,
        _bases_payload(raw.bob_bases),
    )
    append(
        QKDClassicalDirection.BOB_TO_ALICE,
        QKDClassicalMessageType.SIFTING_SELECTION,
        _indices_payload(raw.matching_indices),
    )

    estimation = session.parameter_estimation
    if estimation is not None:
        shared_context = _fields(
            _indices_payload(estimation.disclosed_indices),
            _bases_payload(estimation.disclosed_bases),
        )
        append(
            QKDClassicalDirection.ALICE_TO_BOB,
            QKDClassicalMessageType.PARAMETER_ESTIMATION_DISCLOSURE,
            _fields(shared_context, _binary_payload(estimation.alice_disclosed_bits)),
        )
        append(
            QKDClassicalDirection.BOB_TO_ALICE,
            QKDClassicalMessageType.PARAMETER_ESTIMATION_DISCLOSURE,
            _fields(shared_context, _binary_payload(estimation.bob_disclosed_bits)),
        )

    reconciliation = session.reconciliation
    if reconciliation is not None:
        type_map = {
            "permutation": QKDClassicalMessageType.CASCADE_PERMUTATION,
            "root_parity": QKDClassicalMessageType.CASCADE_ROOT_PARITY,
            "binary_parity": QKDClassicalMessageType.CASCADE_BINARY_PARITY,
        }
        for event in reconciliation.public_events:
            direction = (
                QKDClassicalDirection.ALICE_TO_BOB
                if event.sender == "alice"
                else QKDClassicalDirection.BOB_TO_ALICE
            )
            append(direction, type_map[event.event_type], _cascade_payload(event))

    verification = session.verification
    if verification is not None:
        append(
            QKDClassicalDirection.ALICE_TO_BOB,
            QKDClassicalMessageType.KEY_VERIFICATION_SEED,
            _binary_payload(verification.public_seed),
        )
        append(
            QKDClassicalDirection.ALICE_TO_BOB,
            QKDClassicalMessageType.KEY_VERIFICATION_TAG,
            _binary_payload(verification.alice_tag),
        )
        append(
            QKDClassicalDirection.BOB_TO_ALICE,
            QKDClassicalMessageType.KEY_VERIFICATION_TAG,
            _binary_payload(verification.bob_tag),
        )

    amplification = session.privacy_amplification
    if amplification is not None:
        append(
            QKDClassicalDirection.ALICE_TO_BOB,
            QKDClassicalMessageType.PRIVACY_AMPLIFICATION_SEED,
            _binary_payload(amplification.public_seed),
        )

    return QKDClassicalTranscript(session_id=session_id, events=tuple(events))
