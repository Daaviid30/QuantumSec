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


class ChannelCapability(StrictModel):
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
    protocols: list[ProtocolCapability]
    channels: list[ChannelCapability]
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


ChannelConfiguration = Annotated[
    IdentityChannelConfiguration
    | DepolarizingChannelConfiguration
    | BitFlipChannelConfiguration
    | PhaseFlipChannelConfiguration
    | AmplitudeDampingChannelConfiguration
    | PauliChannelConfiguration,
    Field(discriminator="type"),
]


class BB84SimulationRequest(StrictModel):
    protocol: Literal["bb84"] = "bb84"
    n_signals: int = Field(default=512, ge=1, le=100_000)
    seed: int = Field(default=2026, ge=0, le=4_294_967_295)
    channels: list[ChannelConfiguration] = Field(default_factory=list, max_length=12)


class ChannelSummary(StrictModel):
    type: str
    name: str
    parameters: dict[str, float]


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


class PostprocessingSummary(StrictModel):
    """Browser-facing post-processing result for the educational simulator."""

    status: Literal["completed", "aborted"]
    abort_reason: str | None
    n_disclosed: int
    estimated_qber: float | None
    n_candidate: int
    leak_ec: int
    corrected_errors: int
    verification_passed: bool | None
    verification_leakage: int
    n_reconciled: int
    n_final: int
    compression_ratio: float | None
    final_secret_fraction: float
    final_key: str | None


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
