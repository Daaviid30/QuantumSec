"""Safe immutable result and bounded trace for authenticated QKD orchestration."""

from dataclasses import dataclass, field
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from orchestration.authentication.base import ClassicalAuthenticationResult
from orchestration.profiles import QKDProfile
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH, QKDClassicalTranscript
from qkd.protocols import BB84SessionResult, BB84SessionStatus


class QKDOrchestrationStatus(StrEnum):
    ACCEPTED = "accepted"
    ABORTED = "aborted"


@dataclass(frozen=True, slots=True)
class QKDSessionSummary:
    """Non-secret BB84 outcome metadata suitable for backend serialization."""

    status: BB84SessionStatus
    abort_reason: str | None
    n_raw: int
    n_sifted: int
    n_disclosed: int
    n_candidate: int
    n_reconciled: int
    n_final: int
    sifting_efficiency: float
    final_secret_fraction: float
    estimated_qber_z: float | None
    estimated_qber_x: float | None
    estimated_qber_aggregated: float | None
    phase_error_bound: float | None
    diagnostic_full_sifted_qber: float | None
    diagnostic_qber_z: float | None
    diagnostic_qber_x: float | None
    diagnostic_qber_aggregated: float | None

    @classmethod
    def from_session(cls, session: BB84SessionResult) -> QKDSessionSummary:
        estimation = session.parameter_estimation
        return cls(
            status=session.status,
            abort_reason=session.abort_reason,
            n_raw=session.n_raw,
            n_sifted=session.n_sifted,
            n_disclosed=session.n_disclosed,
            n_candidate=session.n_candidate,
            n_reconciled=session.n_reconciled,
            n_final=session.n_final,
            sifting_efficiency=(session.n_sifted / session.n_raw if session.n_raw else 0.0),
            final_secret_fraction=session.final_secret_fraction,
            estimated_qber_z=(estimation.estimated_qber_z if estimation is not None else None),
            estimated_qber_x=(estimation.estimated_qber_x if estimation is not None else None),
            estimated_qber_aggregated=(
                estimation.estimated_qber_aggregated if estimation is not None else None
            ),
            phase_error_bound=(estimation.phase_error_bound if estimation is not None else None),
            diagnostic_full_sifted_qber=session.diagnostic_full_sifted_qber,
            diagnostic_qber_z=session.diagnostic_qber_z,
            diagnostic_qber_x=session.diagnostic_qber_x,
            diagnostic_qber_aggregated=session.diagnostic_qber_aggregated,
        )


@dataclass(frozen=True, slots=True)
class QKDTraceEvent:
    stage: str
    state: str
    detail: str

    def __post_init__(self) -> None:
        for name in ("stage", "state", "detail"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")


def _optional_key_copy(
    value: npt.NDArray[np.uint8] | None,
) -> npt.NDArray[np.uint8] | None:
    if value is None:
        return None
    copied = np.array(value, dtype=np.uint8, copy=True)
    copied.flags.writeable = False
    return copied


@dataclass(frozen=True, slots=True, eq=False, repr=False)
class AuthenticatedQKDSessionResult:
    """Terminal QKD decision; key fields exist only after all required checks pass."""

    profile: QKDProfile
    session_id: bytes = field(repr=False)
    status: QKDOrchestrationStatus
    qkd: QKDSessionSummary
    authentication: ClassicalAuthenticationResult
    transcript: QKDClassicalTranscript = field(repr=False)
    abort_reason: str | None = None
    trace: tuple[QKDTraceEvent, ...] = ()
    _alice_final_key: npt.NDArray[np.uint8] | None = field(default=None, repr=False)
    _bob_final_key: npt.NDArray[np.uint8] | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, QKDProfile):
            raise TypeError("profile must be a QKDProfile.")
        if not isinstance(self.session_id, bytes) or len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        if not isinstance(self.status, QKDOrchestrationStatus):
            raise TypeError("status must be a QKDOrchestrationStatus.")
        if not isinstance(self.qkd, QKDSessionSummary):
            raise TypeError("qkd must be a QKDSessionSummary.")
        if not isinstance(self.authentication, ClassicalAuthenticationResult):
            raise TypeError("authentication must be a ClassicalAuthenticationResult.")
        if not isinstance(self.transcript, QKDClassicalTranscript):
            raise TypeError("transcript must be a QKDClassicalTranscript.")
        if self.transcript.session_id != self.session_id:
            raise ValueError("Transcript and result session identifiers must match.")
        trace = tuple(self.trace)
        if not trace or not all(isinstance(event, QKDTraceEvent) for event in trace):
            raise ValueError("trace must contain at least one QKDTraceEvent.")
        alice = _optional_key_copy(self._alice_final_key)
        bob = _optional_key_copy(self._bob_final_key)
        if self.status is QKDOrchestrationStatus.ACCEPTED:
            auth_allows_release = not self.authentication.executed or self.authentication.verified is True
            if (
                self.qkd.status is not BB84SessionStatus.COMPLETED
                or not auth_allows_release
                or self.abort_reason is not None
                or alice is None
                or bob is None
                or not np.array_equal(alice, bob)
            ):
                raise ValueError("An accepted QKD session requires matching keys and satisfied checks.")
        elif self.abort_reason is None or alice is not None or bob is not None:
            raise ValueError("An aborted QKD session must withhold both final keys and give a reason.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "trace", trace)
        object.__setattr__(self, "_alice_final_key", alice)
        object.__setattr__(self, "_bob_final_key", bob)

    @property
    def final_key_length(self) -> int:
        return 0 if self._alice_final_key is None else int(self._alice_final_key.size)

    def release_final_keys(
        self,
    ) -> tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]]:
        """Return defensive immutable copies only for an accepted session."""

        if (
            self.status is not QKDOrchestrationStatus.ACCEPTED
            or self._alice_final_key is None
            or self._bob_final_key is None
        ):
            raise RuntimeError("Final QKD key material is withheld because the session was not accepted.")
        alice = _optional_key_copy(self._alice_final_key)
        bob = _optional_key_copy(self._bob_final_key)
        assert alice is not None and bob is not None
        return alice, bob

    def to_public_dict(self) -> dict[str, object]:
        """Serialize bounded public metadata, never transcript payloads or key material."""

        metrics = self.authentication.metrics
        return {
            "profile": self.profile.value,
            "session_id": self.session_id.hex(),
            "status": self.status.value,
            "abort_reason": self.abort_reason,
            "final_key_length": self.final_key_length,
            "qkd": {
                "status": self.qkd.status.value,
                "abort_reason": self.qkd.abort_reason,
                "n_raw": self.qkd.n_raw,
                "n_sifted": self.qkd.n_sifted,
                "n_disclosed": self.qkd.n_disclosed,
                "n_candidate": self.qkd.n_candidate,
                "n_reconciled": self.qkd.n_reconciled,
                "n_final": self.qkd.n_final,
                "sifting_efficiency": self.qkd.sifting_efficiency,
                "final_secret_fraction": self.qkd.final_secret_fraction,
                "estimated_qber_z": self.qkd.estimated_qber_z,
                "estimated_qber_x": self.qkd.estimated_qber_x,
                "estimated_qber_aggregated": self.qkd.estimated_qber_aggregated,
                "phase_error_bound": self.qkd.phase_error_bound,
                "diagnostic_full_sifted_qber": self.qkd.diagnostic_full_sifted_qber,
                "diagnostic_qber_z": self.qkd.diagnostic_qber_z,
                "diagnostic_qber_x": self.qkd.diagnostic_qber_x,
                "diagnostic_qber_aggregated": self.qkd.diagnostic_qber_aggregated,
            },
            "authentication": {
                "state": self.authentication.state.value,
                "executed": self.authentication.executed,
                "verified": self.authentication.verified,
                "failure_reason": self.authentication.failure_reason,
                "mechanism": metrics.mechanism.value,
                "algorithm": metrics.algorithm,
                "family": metrics.family,
                "authenticated_bytes": metrics.authenticated_bytes,
                "evidence_bytes": metrics.evidence_bytes,
                "checkpoints": metrics.checkpoints,
                "generation_operations": metrics.generation_operations,
                "verification_operations": metrics.verification_operations,
                "generation_time_ns": metrics.generation_time_ns,
                "verification_time_ns": metrics.verification_time_ns,
                "total_time_ns": metrics.total_time_ns,
                "trust_assumption": metrics.trust_assumption,
                "secret_bits_consumed": metrics.secret_bits_consumed,
                "public_key_provisioning_bytes": metrics.public_key_provisioning_bytes,
                "forgery_bound": metrics.forgery_bound,
                "runtime_environment": dict(metrics.runtime_environment),
            },
            "transcript": {
                "version": self.transcript.version,
                "message_count": self.transcript.message_count,
                "canonical_bytes": len(self.transcript.canonical_bytes()),
            },
            "trace": tuple(
                {"stage": event.stage, "state": event.state, "detail": event.detail} for event in self.trace
            ),
        }

    def __repr__(self) -> str:
        return (
            f"AuthenticatedQKDSessionResult(profile={self.profile.value!r}, "
            f"session_id={self.session_id.hex()!r}, status={self.status.value!r}, "
            f"qkd={self.qkd!r}, authentication={self.authentication!r}, "
            f"abort_reason={self.abort_reason!r}, final_key_length={self.final_key_length}, "
            f"trace_events={len(self.trace)})"
        )
