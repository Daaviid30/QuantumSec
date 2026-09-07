"""Versioned, role-separated HMAC-SHA-384 Finished exchange for hybrid keys."""

import hmac
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha384
from typing import Final

from orchestration._encoding import length_prefixed, unsigned
from orchestration.hybrid.context import HybridPublicContext
from orchestration.profiles import SessionProfile
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH

HYBRID_FINISHED_DOMAIN: Final = b"QuantumSec/HybridSession/v1/Finished"
HYBRID_FINISHED_VERSION: Final = 1
HYBRID_FINISHED_LENGTH: Final = 48
HYBRID_FINISHED_MAC_ALGORITHM: Final = "HMAC-SHA-384"


class HybridFinishedRole(StrEnum):
    RESPONDER = "responder"
    INITIATOR = "initiator"


@dataclass(frozen=True, slots=True, repr=False)
class HybridFinishedMessage:
    version: int
    session_id: bytes = field(repr=False)
    profile: SessionProfile
    sender_role: HybridFinishedRole
    mac_algorithm: str
    transcript_hash: bytes
    verify_data: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if self.version != HYBRID_FINISHED_VERSION:
            raise ValueError(f"Hybrid Finished version must be {HYBRID_FINISHED_VERSION}.")
        if len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError("Hybrid Finished session_id must contain 16 bytes.")
        if self.profile not in (SessionProfile.HYBRID, SessionProfile.HYBRID_DIVERSE):
            raise ValueError("Hybrid Finished requires a hybrid profile.")
        if self.mac_algorithm != HYBRID_FINISHED_MAC_ALGORITHM:
            raise ValueError(f"mac_algorithm must be {HYBRID_FINISHED_MAC_ALGORITHM}.")
        if len(self.transcript_hash) != 48 or len(self.verify_data) != HYBRID_FINISHED_LENGTH:
            raise ValueError("Hybrid Finished hashes must contain 48 bytes.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "transcript_hash", bytes(self.transcript_hash))
        object.__setattr__(self, "verify_data", bytes(self.verify_data))

    def canonical_bytes(self) -> bytes:
        return b"".join(
            (
                length_prefixed(HYBRID_FINISHED_DOMAIN),
                unsigned(self.version, width=2),
                length_prefixed(self.session_id),
                length_prefixed(self.profile.value.encode("ascii")),
                length_prefixed(self.sender_role.value.encode("ascii")),
                length_prefixed(self.mac_algorithm.encode("ascii")),
                length_prefixed(self.transcript_hash),
                length_prefixed(self.verify_data),
            )
        )

    def __repr__(self) -> str:
        return (
            f"HybridFinishedMessage(version={self.version}, profile={self.profile.value!r}, "
            f"sender_role={self.sender_role.value!r}, mac_algorithm={self.mac_algorithm!r}, "
            f"transcript_hash={self.transcript_hash.hex()!r}, verify_data_length=48)"
        )


def _mac_input(
    context: HybridPublicContext,
    role: HybridFinishedRole,
    previous: bytes | None = None,
) -> bytes:
    if role is HybridFinishedRole.RESPONDER and previous is not None:
        raise ValueError("Responder Finished cannot bind a previous message.")
    if role is HybridFinishedRole.INITIATOR and previous is None:
        raise ValueError("Initiator Finished must bind the responder verify_data.")
    return b"".join(
        (
            length_prefixed(HYBRID_FINISHED_DOMAIN),
            unsigned(HYBRID_FINISHED_VERSION, width=2),
            length_prefixed(context.session_id),
            length_prefixed(context.profile.value.encode("ascii")),
            length_prefixed(role.value.encode("ascii")),
            length_prefixed(HYBRID_FINISHED_MAC_ALGORITHM.encode("ascii")),
            length_prefixed(context.context_hash),
            length_prefixed(previous or b""),
        )
    )


def create_finished(
    confirmation_key: bytes,
    context: HybridPublicContext,
    role: HybridFinishedRole,
    *,
    previous: bytes | None = None,
) -> HybridFinishedMessage:
    verify_data = hmac.new(
        confirmation_key,
        _mac_input(context, role, previous),
        digestmod=sha384,
    ).digest()
    return HybridFinishedMessage(
        HYBRID_FINISHED_VERSION,
        context.session_id,
        context.profile,
        role,
        HYBRID_FINISHED_MAC_ALGORITHM,
        context.context_hash,
        verify_data,
    )


def verify_finished(
    confirmation_key: bytes,
    context: HybridPublicContext,
    message: HybridFinishedMessage,
    expected_role: HybridFinishedRole,
    *,
    previous: bytes | None = None,
) -> bool:
    if not isinstance(message, HybridFinishedMessage):
        return False
    metadata_matches = (
        message.version == HYBRID_FINISHED_VERSION
        and message.session_id == context.session_id
        and message.profile is context.profile
        and message.sender_role is expected_role
        and message.mac_algorithm == HYBRID_FINISHED_MAC_ALGORITHM
        and hmac.compare_digest(message.transcript_hash, context.context_hash)
    )
    if not metadata_matches:
        return False
    expected = hmac.new(
        confirmation_key,
        _mac_input(context, expected_role, previous),
        digestmod=sha384,
    ).digest()
    return hmac.compare_digest(expected, message.verify_data)
