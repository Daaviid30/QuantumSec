"""Authenticated public context binding every hybrid session input."""

import hmac
from dataclasses import dataclass, field
from hashlib import sha384
from typing import Final

from orchestration._encoding import length_prefixed, unsigned
from orchestration.hybrid.encoding import HYBRID_ENCODING_VERSION
from orchestration.profiles import QKDProfile, SessionProfile, session_profile_definition
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH
from pqc.profiles import PQCProfile
from pqc.protocol.transcript import PQC_TRANSCRIPT_HASH_LENGTH

HYBRID_TRANSCRIPT_DOMAIN: Final = b"QuantumSec/HybridSession/v1/Transcript"
HYBRID_CONTEXT_HASH_LENGTH: Final = 48
HYBRID_PUBLIC_CONTEXT_VERSION: Final = 1


@dataclass(frozen=True, slots=True, repr=False)
class HybridPublicContext:
    session_id: bytes = field(repr=False)
    profile: SessionProfile
    qkd_profile: QKDProfile
    qkd_transcript_version: int
    qkd_transcript_hash: bytes
    pqc_protocol_version: int
    pqc_profile: PQCProfile
    pqc_transcript_hash: bytes
    algorithms: tuple[str, ...]
    encoding_version: int = HYBRID_ENCODING_VERSION
    version: int = HYBRID_PUBLIC_CONTEXT_VERSION

    def __post_init__(self) -> None:
        if len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError("Hybrid session_id must contain 16 bytes.")
        if self.profile not in (SessionProfile.HYBRID, SessionProfile.HYBRID_DIVERSE):
            raise ValueError("profile must be a hybrid profile.")
        if not isinstance(self.qkd_profile, QKDProfile):
            raise TypeError("qkd_profile must be a QKDProfile.")
        if not isinstance(self.pqc_profile, PQCProfile):
            raise TypeError("pqc_profile must be a PQCProfile.")
        if len(self.qkd_transcript_hash) != 48:
            raise ValueError("qkd_transcript_hash must be a SHA-384 digest.")
        if len(self.pqc_transcript_hash) != PQC_TRANSCRIPT_HASH_LENGTH:
            raise ValueError("pqc_transcript_hash must be a SHA-384 digest.")
        if self.encoding_version != HYBRID_ENCODING_VERSION:
            raise ValueError(f"encoding_version must be {HYBRID_ENCODING_VERSION}.")
        if self.version != HYBRID_PUBLIC_CONTEXT_VERSION:
            raise ValueError(f"version must be {HYBRID_PUBLIC_CONTEXT_VERSION}.")
        definition = session_profile_definition(self.profile)
        if self.pqc_profile is not definition.internal_pqc_profile:
            raise ValueError("PQC internal profile conflicts with the hybrid public profile.")
        if tuple(self.algorithms) != definition.establishment_algorithms:
            raise ValueError("Establishment algorithm list conflicts with the hybrid public profile.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "qkd_transcript_hash", bytes(self.qkd_transcript_hash))
        object.__setattr__(self, "pqc_transcript_hash", bytes(self.pqc_transcript_hash))
        object.__setattr__(self, "algorithms", tuple(self.algorithms))

    def canonical_bytes(self) -> bytes:
        return b"".join(
            (
                length_prefixed(HYBRID_TRANSCRIPT_DOMAIN),
                unsigned(self.version, width=2),
                unsigned(self.encoding_version, width=2),
                length_prefixed(self.session_id),
                length_prefixed(self.profile.value.encode("ascii")),
                length_prefixed(self.qkd_profile.value.encode("ascii")),
                unsigned(self.qkd_transcript_version, width=2),
                length_prefixed(self.qkd_transcript_hash),
                unsigned(self.pqc_protocol_version, width=2),
                length_prefixed(self.pqc_profile.value.encode("ascii")),
                length_prefixed(self.pqc_transcript_hash),
                unsigned(len(self.algorithms), width=2),
                b"".join(length_prefixed(item.encode("ascii")) for item in self.algorithms),
            )
        )

    @property
    def context_hash(self) -> bytes:
        digest = sha384(self.canonical_bytes()).digest()
        if len(digest) != HYBRID_CONTEXT_HASH_LENGTH:
            raise RuntimeError("SHA-384 returned an invalid hybrid context hash.")
        return digest

    def matches_hash(self, candidate: bytes) -> bool:
        return hmac.compare_digest(self.context_hash, candidate)

    def __repr__(self) -> str:
        return (
            f"HybridPublicContext(profile={self.profile.value!r}, "
            f"qkd_profile={self.qkd_profile.value!r}, pqc_profile={self.pqc_profile.value!r}, "
            f"context_hash={self.context_hash.hex()!r})"
        )
