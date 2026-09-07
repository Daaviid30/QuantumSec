"""Profile-compatible metrics that keep unlike timing categories separate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orchestration.authentication import AuthenticationMetrics


@dataclass(frozen=True, slots=True)
class QKDSessionMetrics:
    simulation_time_ns: int
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
    transcript_bytes: int


@dataclass(frozen=True, slots=True)
class PQCSessionMetrics:
    internal_profile: str
    algorithms: tuple[str, ...]
    server_offer_time_ns: int
    server_processing_time_ns: int
    client_exchange_time_ns: int
    client_processing_time_ns: int
    key_schedule_time_ns: int
    confirmation_time_ns: int
    crypto_software_time_ns: int
    canonical_protocol_bytes: int
    transcript_bytes: int
    signature_bytes: int
    finished_bytes: int
    public_key_provisioning_bytes: int


@dataclass(frozen=True, slots=True)
class PQCAuthenticationMetrics:
    mechanism: str
    algorithm: str
    executed: bool
    verified: bool
    signatures_generated: int
    signatures_verified: int
    signature_bytes: int
    trust_assumption: str


@dataclass(frozen=True, slots=True)
class HybridSessionMetrics:
    component_count: int
    component_metadata_bytes: tuple[int, ...]
    qkd_contribution_bits: int
    ml_kem_contribution_bytes: int
    hqc_contribution_bytes: int | None
    canonical_combiner_input_bytes: int
    encoding_overhead_bytes: int
    public_context_bytes: int
    encoding_time_ns: int
    hkdf_session_time_ns: int
    hkdf_confirmation_time_ns: int
    finished_generation_time_ns: int
    finished_verification_time_ns: int
    finished_responder_bytes: int
    finished_initiator_bytes: int
    derived_session_key_bits: int


@dataclass(frozen=True, slots=True)
class SessionMetrics:
    qkd: QKDSessionMetrics | None = None
    pqc: PQCSessionMetrics | None = None
    qkd_authentication: AuthenticationMetrics | None = None
    pqc_authentication: PQCAuthenticationMetrics | None = None
    hybrid: HybridSessionMetrics | None = None
    orchestration_software_wall_time_ns: int = 0

    def __post_init__(self) -> None:
        if (
            isinstance(self.orchestration_software_wall_time_ns, bool)
            or not isinstance(self.orchestration_software_wall_time_ns, int)
            or self.orchestration_software_wall_time_ns < 0
        ):
            raise ValueError("orchestration_software_wall_time_ns must be non-negative.")

    def to_public_dict(self) -> dict[str, object]:
        """Return categorized JSON-compatible metrics without combining unlike clocks."""

        qkd_auth = self.qkd_authentication
        return {
            "qkd": asdict(self.qkd) if self.qkd is not None else None,
            "pqc": asdict(self.pqc) if self.pqc is not None else None,
            "qkd_authentication": (
                None
                if qkd_auth is None
                else {
                    "mechanism": qkd_auth.mechanism.value,
                    "algorithm": qkd_auth.algorithm,
                    "family": qkd_auth.family,
                    "authenticated_bytes": qkd_auth.authenticated_bytes,
                    "evidence_bytes": qkd_auth.evidence_bytes,
                    "checkpoints": qkd_auth.checkpoints,
                    "generation_operations": qkd_auth.generation_operations,
                    "verification_operations": qkd_auth.verification_operations,
                    "generation_time_ns": qkd_auth.generation_time_ns,
                    "verification_time_ns": qkd_auth.verification_time_ns,
                    "total_time_ns": qkd_auth.total_time_ns,
                    "trust_assumption": qkd_auth.trust_assumption,
                    "secret_bits_consumed": qkd_auth.secret_bits_consumed,
                    "public_key_provisioning_bytes": qkd_auth.public_key_provisioning_bytes,
                    "forgery_bound": qkd_auth.forgery_bound,
                    "runtime_environment": dict(qkd_auth.runtime_environment),
                }
            ),
            "pqc_authentication": (
                asdict(self.pqc_authentication) if self.pqc_authentication is not None else None
            ),
            "hybrid": asdict(self.hybrid) if self.hybrid is not None else None,
            "orchestration_software_wall_time_ns": self.orchestration_software_wall_time_ns,
        }
