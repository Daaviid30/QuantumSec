"""Typed HTTP contracts for the QuantumSec web interface."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    """Base API model that rejects fields outside the documented contract."""

    model_config = ConfigDict(extra="forbid")


class HealthResponse(StrictModel):
    status: Literal["ok"]
    service: str
    version: str


class ParameterCapability(StrictModel):
    key: str
    label: str
    symbol: str
    minimum: float
    maximum: float
    step: float
    default: float
    description: str


class ProtocolCapability(StrictModel):
    id: str
    name: str
    implemented: bool
    description: str


PublicSessionProfile = Literal[
    "QKD-ASSUMED",
    "QKD-CLASSICAL-AUTH",
    "QKD-PQC-AUTH",
    "PQC-BASE",
    "PQC-DIVERSE",
    "HYBRID",
    "HYBRID-DIVERSE",
]


class ProfileCapability(StrictModel):
    id: PublicSessionProfile
    name: str
    family: Literal["qkd", "pqc", "hybrid"]
    implemented: bool
    status: Literal["current", "partial", "planned", "future"]
    description: str
    establishment: list[str]
    authentication: list[str]
    algorithms: list[str]
    hybrid: bool
    diversified: bool
    supports_qkd: bool
    supports_data_plane: bool


class ChannelCapability(StrictModel):
    id: str
    name: str
    implemented: bool
    description: str
    parameters: list[ParameterCapability]


class AdversaryCapability(StrictModel):
    id: str
    name: str
    implemented: bool
    description: str
    parameters: list[ParameterCapability]


class FeatureCapability(StrictModel):
    id: str
    name: str
    implemented: bool
    description: str


class CapabilitiesResponse(StrictModel):
    version: str
    profiles: list[ProfileCapability]
    protocols: list[ProtocolCapability]
    channels: list[ChannelCapability]
    adversaries: list[AdversaryCapability]
    features: list[FeatureCapability]
    limits: dict[str, int]


class IdentityChannelConfiguration(StrictModel):
    type: Literal["identity"]


class DepolarizingChannelConfiguration(StrictModel):
    type: Literal["depolarizing"]
    p: float = Field(ge=0.0, le=1.0)


class BitFlipChannelConfiguration(StrictModel):
    type: Literal["bit_flip"]
    p: float = Field(ge=0.0, le=1.0)


class PhaseFlipChannelConfiguration(StrictModel):
    type: Literal["phase_flip"]
    p: float = Field(ge=0.0, le=1.0)


class AmplitudeDampingChannelConfiguration(StrictModel):
    type: Literal["amplitude_damping"]
    gamma: float = Field(ge=0.0, le=1.0)


class PauliChannelConfiguration(StrictModel):
    type: Literal["pauli"]
    px: float = Field(ge=0.0, le=1.0)
    py: float = Field(ge=0.0, le=1.0)
    pz: float = Field(ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_total_probability(self) -> PauliChannelConfiguration:
        if self.px + self.py + self.pz > 1.0:
            raise ValueError("Pauli probabilities must satisfy px + py + pz <= 1")
        return self


class InterceptResendConfiguration(StrictModel):
    type: Literal["intercept_resend"]
    intercept_fraction: float = Field(ge=0.0, le=1.0)


ChannelConfiguration = Annotated[
    IdentityChannelConfiguration
    | DepolarizingChannelConfiguration
    | BitFlipChannelConfiguration
    | PhaseFlipChannelConfiguration
    | AmplitudeDampingChannelConfiguration
    | PauliChannelConfiguration
    | InterceptResendConfiguration,
    Field(discriminator="type"),
]


class BB84SimulationRequest(StrictModel):
    protocol: Literal["bb84"] = "bb84"
    n_signals: int = Field(default=512, ge=1, le=100_000)
    seed: int = Field(default=2026, ge=0, le=4_294_967_295)
    channels: list[ChannelConfiguration] = Field(default_factory=list, max_length=12)


class QKDPostprocessingRequest(StrictModel):
    sample_fraction: float = Field(default=0.2, gt=0.0, lt=1.0)
    phase_error_abort_threshold: float = Field(default=0.11, ge=0.0, le=1.0)
    cascade_passes: int = Field(default=4, ge=1, le=16)
    cascade_initial_block_factor: float = Field(default=0.73, gt=0.0, le=10.0)
    verification_tag_length: int = Field(default=32, ge=1, le=512)
    security_margin_bits: int = Field(default=0, ge=0, le=100_000)


class SessionRunRequest(StrictModel):
    profile: PublicSessionProfile
    qkd_authentication_profile: Literal["QKD-ASSUMED", "QKD-CLASSICAL-AUTH", "QKD-PQC-AUTH"] | None = None
    n_signals: int | None = Field(default=None, ge=1, le=100_000)
    seed: int | None = Field(default=None, ge=0, le=4_294_967_295)
    channels: list[ChannelConfiguration] = Field(default_factory=list, max_length=12)
    postprocessing: QKDPostprocessingRequest = Field(default_factory=QKDPostprocessingRequest)

    @model_validator(mode="after")
    def validate_profile_configuration(self) -> SessionRunRequest:
        uses_qkd = self.profile.startswith("QKD-") or self.profile.startswith("HYBRID")
        is_hybrid = self.profile.startswith("HYBRID")
        if uses_qkd:
            if self.n_signals is None or self.seed is None:
                raise ValueError("QKD and hybrid profiles require n_signals and seed.")
        elif self.n_signals is not None or self.seed is not None or self.channels:
            raise ValueError("PQC-only profiles cannot configure QKD signals, seed, or channels.")
        if is_hybrid and self.qkd_authentication_profile is None:
            raise ValueError("Hybrid profiles require an explicit qkd_authentication_profile.")
        if not is_hybrid and self.qkd_authentication_profile is not None:
            raise ValueError("qkd_authentication_profile is configurable only for hybrid profiles.")
        return self


class ChannelSummary(StrictModel):
    stage_kind: Literal["channel", "adversary"]
    type: str
    name: str
    parameters: dict[str, float]


class AttackDiagnosticsSummary(StrictModel):
    stage_index: int
    attack_type: Literal["intercept_resend"]
    intercept_fraction: float
    n_signals_seen: int
    n_intercepted: int
    eve_z_measurements: int
    eve_x_measurements: int
    eve_zero_outcomes: int
    eve_one_outcomes: int


class RunRecord(StrictModel):
    version: int
    run_id: str
    experiment_kind: str
    condition_id: str
    replicate_index: int
    batch: dict[str, object] | None
    execution_order_index: int | None
    timestamp_utc: str
    seed: int | None
    profile: PublicSessionProfile
    environment: dict[str, object]
    config: dict[str, object]
    provisioning: dict[str, object]
    result: dict[str, object]
    trace: dict[str, object]
    metrics: dict[str, object]
    artifact: dict[str, object]


class SessionRunResponse(StrictModel):
    record: RunRecord
    attack_diagnostics: list[AttackDiagnosticsSummary]
    data_plane_available: bool


class RunListResponse(StrictModel):
    runs: list[SessionRunResponse]


class CompareRequest(StrictModel):
    run_ids: list[str] = Field(min_length=2, max_length=2)

    @model_validator(mode="after")
    def validate_distinct_runs(self) -> CompareRequest:
        if self.run_ids[0] == self.run_ids[1]:
            raise ValueError("Comparison requires two distinct run IDs.")
        return self


class ComparisonCompatibility(StrictModel):
    qkd_metrics: bool
    pqc_timing: bool
    same_environment: bool
    notes: list[str]


class CompareResponse(StrictModel):
    left: SessionRunResponse
    right: SessionRunResponse
    compatibility: ComparisonCompatibility


class ProtectedMessageRequest(StrictModel):
    plaintext: str = Field(min_length=1, max_length=512)
    aad: str = Field(default="QuantumSec/WebLab/v1", max_length=256)


class ProtectedMessageResponse(StrictModel):
    algorithm: Literal["AES-256-GCM"]
    plaintext_bytes: int
    ciphertext_bytes: int
    nonce_bytes: int
    tag_bytes: int
    application_aad_bytes: int
    round_trip_verified: bool
    tamper_rejected: bool
    ciphertext_preview: str


class SimulationMetadata(StrictModel):
    request_id: str
    protocol: Literal["bb84"]
    seed: int
    duration_ms: float
    inspector_limit: int
    inspector_truncated: bool


class SimulationMetrics(StrictModel):
    n_raw: int
    n_sifted: int
    sifting_efficiency: float
    qber: float | None
    qber_z: float | None
    qber_x: float | None
    qber_aggregated: float | None


class PostprocessingSummary(StrictModel):
    """Browser-facing post-processing result for the educational simulator."""

    status: Literal["completed", "aborted"]
    abort_reason: str | None
    n_disclosed: int
    estimated_qber: float | None = Field(
        description=(
            "Backward-compatible alias for aggregate sampled bit QBER; used to configure "
            "reconciliation, not as the security-abort threshold variable."
        )
    )
    estimated_qber_z: float | None
    estimated_qber_x: float | None
    estimated_qber_aggregated: float | None = Field(
        description="Aggregate sampled bit QBER used to configure reconciliation."
    )
    phase_error_bound: float | None = Field(
        description="Per-basis-derived bound used by the security abort and secret-length estimator."
    )
    n_candidate: int
    leak_ec: int
    corrected_errors: int
    verification_passed: bool | None
    verification_leakage: int
    n_reconciled: int
    n_final: int
    compression_ratio: float | None
    final_secret_fraction: float


class BasisCounts(StrictModel):
    Z: int
    X: int


class OutcomeCounts(StrictModel):
    zero: int
    one: int


class TransmissionRecord(StrictModel):
    index: int
    alice_bit: int
    alice_basis: Literal["Z", "X"]
    bob_basis: Literal["Z", "X"]
    bob_result: int
    basis_match: bool
    sifted_error: bool | None


class BB84SimulationResponse(StrictModel):
    metadata: SimulationMetadata
    channels: list[ChannelSummary]
    attack_diagnostics: list[AttackDiagnosticsSummary]
    metrics: SimulationMetrics
    postprocessing: PostprocessingSummary
    alice_basis_counts: BasisCounts
    bob_basis_counts: BasisCounts
    bob_outcome_counts: OutcomeCounts
    transmissions: list[TransmissionRecord]


class ApiError(StrictModel):
    code: str
    message: str
    details: str | None = None
