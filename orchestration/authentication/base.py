"""Common contracts for executed or explicitly assumed QKD classical authentication."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from threading import Lock
from typing import Final

from orchestration._encoding import length_prefixed, unsigned
from orchestration.profiles import ClassicalAuthenticationMode
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH, QKDClassicalDirection

AUTHENTICATION_FRAME_VERSION: Final = 1
AUTHENTICATION_FRAME_DOMAIN: Final = b"QuantumSec/QKDClassicalAuth/v1/Frame"
TRANSCRIPT_CHECKPOINT_TYPE: Final = "qkd_classical_transcript_checkpoint"


class AuthenticationState(StrEnum):
    ASSUMED_NOT_EXECUTED = "assumed_not_executed"
    EXECUTED_VERIFIED = "executed_verified"
    EXECUTED_FAILED = "executed_failed"


class AuthenticationSessionReplayError(RuntimeError):
    """Raised when a session identifier is reused within persistent authentication state."""


class AuthenticationSessionRegistry:
    """Thread-safe replay registry that contains identifiers, never authentication secrets."""

    __slots__ = ("_lock", "_session_ids")

    def __init__(self) -> None:
        self._session_ids: set[bytes] = set()
        self._lock = Lock()

    def reserve(self, session_id: bytes) -> None:
        if not isinstance(session_id, bytes) or len(session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        clean = bytes(session_id)
        with self._lock:
            if clean in self._session_ids:
                raise AuthenticationSessionReplayError(
                    "The authentication context has already used this QKD session identifier."
                )
            self._session_ids.add(clean)

    def __repr__(self) -> str:
        with self._lock:
            count = len(self._session_ids)
        return f"AuthenticationSessionRegistry(reserved_sessions={count})"


@dataclass(frozen=True, slots=True, repr=False)
class AuthenticationFrame:
    """Canonical authentication unit binding payload to anti-replay context."""

    session_id: bytes = field(repr=False)
    direction: QKDClassicalDirection
    sequence_number: int
    message_type: str
    payload: bytes = field(repr=False)
    version: int = AUTHENTICATION_FRAME_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, bytes) or len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        if not isinstance(self.direction, QKDClassicalDirection):
            raise TypeError("direction must be a QKDClassicalDirection.")
        unsigned(self.sequence_number)
        if not isinstance(self.message_type, str) or not self.message_type.strip():
            raise ValueError("message_type must be a non-empty string.")
        if not isinstance(self.payload, bytes):
            raise TypeError(f"payload must be bytes. Got {type(self.payload).__name__}.")
        if self.version != AUTHENTICATION_FRAME_VERSION:
            raise ValueError(f"version must be {AUTHENTICATION_FRAME_VERSION}.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "message_type", self.message_type.strip())
        object.__setattr__(self, "payload", bytes(self.payload))

    def canonical_context_bytes(self) -> bytes:
        """Encode replay-relevant context without the authenticated payload."""

        return b"".join(
            (
                length_prefixed(AUTHENTICATION_FRAME_DOMAIN),
                unsigned(self.version, width=2),
                length_prefixed(self.session_id),
                length_prefixed(self.direction.value.encode("ascii")),
                unsigned(self.sequence_number),
                length_prefixed(self.message_type.encode("ascii")),
            )
        )

    def canonical_bytes(self) -> bytes:
        return self.canonical_context_bytes() + length_prefixed(self.payload)

    def __repr__(self) -> str:
        return (
            f"AuthenticationFrame(session_id={self.session_id.hex()!r}, "
            f"direction={self.direction.value!r}, sequence_number={self.sequence_number}, "
            f"message_type={self.message_type!r}, payload_bytes={len(self.payload)})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class AuthenticationEvidence:
    mechanism: ClassicalAuthenticationMode
    algorithm: str
    signer: str
    verifier: str
    session_id: bytes = field(repr=False)
    direction: QKDClassicalDirection
    sequence_number: int
    message_type: str
    value: bytes = field(repr=False)
    secret_bits_consumed: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.mechanism, ClassicalAuthenticationMode):
            raise TypeError("mechanism must be a ClassicalAuthenticationMode.")
        for name in ("algorithm", "signer", "verifier", "message_type"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")
            object.__setattr__(self, name, value.strip())
        if not isinstance(self.session_id, bytes) or len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        if not isinstance(self.direction, QKDClassicalDirection):
            raise TypeError("direction must be a QKDClassicalDirection.")
        unsigned(self.sequence_number)
        if not isinstance(self.value, bytes) or not self.value:
            raise ValueError("Authentication evidence must be non-empty bytes.")
        consumed = self.secret_bits_consumed
        if consumed is not None and (
            isinstance(consumed, bool) or not isinstance(consumed, int) or consumed < 0
        ):
            raise ValueError("secret_bits_consumed must be a non-negative integer or None.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "value", bytes(self.value))

    @property
    def evidence_bytes(self) -> int:
        return len(self.value)

    def matches_frame(self, frame: AuthenticationFrame) -> bool:
        return (
            self.session_id == frame.session_id
            and self.direction is frame.direction
            and self.sequence_number == frame.sequence_number
            and self.message_type == frame.message_type
        )

    def __repr__(self) -> str:
        return (
            f"AuthenticationEvidence(mechanism={self.mechanism.value!r}, algorithm={self.algorithm!r}, "
            f"signer={self.signer!r}, verifier={self.verifier!r}, "
            f"direction={self.direction.value!r}, sequence_number={self.sequence_number}, "
            f"message_type={self.message_type!r}, evidence_bytes={len(self.value)}, "
            f"secret_bits_consumed={self.secret_bits_consumed!r})"
        )


@dataclass(frozen=True, slots=True)
class AuthenticationVerification:
    verified: bool
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.verified, bool):
            raise TypeError("verified must be a bool.")
        if self.verified and self.failure_reason is not None:
            raise ValueError("Successful verification cannot have a failure reason.")
        if not self.verified and not self.failure_reason:
            raise ValueError("Failed verification requires a failure reason.")


@dataclass(frozen=True, slots=True)
class AuthenticatorMetadata:
    mechanism: ClassicalAuthenticationMode
    algorithm: str
    family: str
    trust_assumption: str
    public_key_provisioning_bytes: int | None
    forgery_bound: str | None


class DirectionalAuthenticator(ABC):
    """Generate and verify evidence for one authenticated communication direction."""

    @property
    @abstractmethod
    def metadata(self) -> AuthenticatorMetadata:
        raise NotImplementedError

    @abstractmethod
    def generate_evidence(self, frame: AuthenticationFrame) -> AuthenticationEvidence:
        raise NotImplementedError

    @abstractmethod
    def verify_evidence(
        self,
        frame: AuthenticationFrame,
        evidence: AuthenticationEvidence | None,
    ) -> AuthenticationVerification:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AuthenticationMetrics:
    mechanism: ClassicalAuthenticationMode
    algorithm: str
    family: str
    authenticated_bytes: int
    evidence_bytes: int
    checkpoints: int
    generation_operations: int
    verification_operations: int
    generation_time_ns: int
    verification_time_ns: int
    total_time_ns: int
    trust_assumption: str
    secret_bits_consumed: int | None
    public_key_provisioning_bytes: int | None
    forgery_bound: str | None
    runtime_environment: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.mechanism, ClassicalAuthenticationMode):
            raise TypeError("mechanism must be a ClassicalAuthenticationMode.")
        for name in ("algorithm", "family"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")
        if not isinstance(self.trust_assumption, str) or not self.trust_assumption.strip():
            raise ValueError("trust_assumption must be a non-empty string.")
        for name in (
            "authenticated_bytes",
            "evidence_bytes",
            "checkpoints",
            "generation_operations",
            "verification_operations",
            "generation_time_ns",
            "verification_time_ns",
            "total_time_ns",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a non-negative integer.")
        if self.total_time_ns != self.generation_time_ns + self.verification_time_ns:
            raise ValueError("total_time_ns must equal generation plus verification time.")
        for name in ("secret_bits_consumed", "public_key_provisioning_bytes"):
            value = getattr(self, name)
            if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
                raise ValueError(f"{name} must be a non-negative integer or None.")
        environment = tuple(self.runtime_environment)
        if not environment or not all(
            isinstance(key, str) and key.strip() and isinstance(value, str) and value.strip()
            for key, value in environment
        ):
            raise ValueError("runtime_environment must contain non-empty string pairs.")
        object.__setattr__(self, "runtime_environment", environment)


@dataclass(frozen=True, slots=True, repr=False)
class ClassicalAuthenticationResult:
    state: AuthenticationState
    executed: bool
    verified: bool | None
    metrics: AuthenticationMetrics
    failure_reason: str | None = None
    evidence: tuple[AuthenticationEvidence, ...] = field(default=(), repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.state, AuthenticationState):
            raise TypeError("state must be an AuthenticationState.")
        if self.state is AuthenticationState.ASSUMED_NOT_EXECUTED:
            if self.executed or self.verified is not None or self.evidence or self.failure_reason is not None:
                raise ValueError(
                    "Assumed authentication must not claim execution, evidence, or verification."
                )
        elif self.state is AuthenticationState.EXECUTED_VERIFIED:
            if not self.executed or self.verified is not True or self.failure_reason is not None:
                raise ValueError("Verified authentication requires executed=True and verified=True.")
        elif not self.executed or self.verified is not False or not self.failure_reason:
            raise ValueError("Failed authentication requires execution, verified=False, and a reason.")
        object.__setattr__(self, "evidence", tuple(self.evidence))

    def __repr__(self) -> str:
        return (
            f"ClassicalAuthenticationResult(state={self.state.value!r}, executed={self.executed}, "
            f"verified={self.verified!r}, metrics={self.metrics!r}, "
            f"failure_reason={self.failure_reason!r}, evidence_count={len(self.evidence)})"
        )
