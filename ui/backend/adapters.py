"""Adapters between typed HTTP data and the QuantumSec simulation domain."""

from collections import Counter
from time import perf_counter
from typing import Literal
from uuid import uuid4

import numpy as np
import numpy.typing as npt

from core.rng import SeededRNG
from qkd.channel import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    ChannelPipeline,
    DepolarizingChannel,
    IdentityChannel,
    PauliChannel,
    PhaseFlipChannel,
    QuantumChannel,
)
from qkd.primitives import Basis
from qkd.protocols import BB84Protocol
from ui.backend.capabilities import INSPECTOR_LIMIT
from ui.backend.schemas import (
    AmplitudeDampingChannelConfiguration,
    BasisCounts,
    BB84SimulationRequest,
    BB84SimulationResponse,
    BitFlipChannelConfiguration,
    ChannelConfiguration,
    ChannelSummary,
    DepolarizingChannelConfiguration,
    IdentityChannelConfiguration,
    OutcomeCounts,
    PauliChannelConfiguration,
    PhaseFlipChannelConfiguration,
    PostprocessingSummary,
    SimulationMetadata,
    SimulationMetrics,
    TransmissionRecord,
)


def _bb84_basis_value(basis: Basis) -> Literal["Z", "X"]:
    """Narrow the general QKD Basis enum to BB84's two supported bases."""

    if basis is Basis.Z:
        return "Z"
    if basis is Basis.X:
        return "X"
    raise ValueError(f"BB84 returned an unsupported basis: {basis.value}")


def build_channel(configuration: ChannelConfiguration) -> QuantumChannel:
    """Map one validated API channel configuration to the public channel API."""

    match configuration:
        case IdentityChannelConfiguration():
            return IdentityChannel()
        case DepolarizingChannelConfiguration(p=p):
            return DepolarizingChannel(p=p)
        case BitFlipChannelConfiguration(p=p):
            return BitFlipChannel(p=p)
        case PhaseFlipChannelConfiguration(p=p):
            return PhaseFlipChannel(p=p)
        case AmplitudeDampingChannelConfiguration(gamma=gamma):
            return AmplitudeDampingChannel(gamma=gamma)
        case PauliChannelConfiguration(px=px, py=py, pz=pz):
            return PauliChannel(px=px, py=py, pz=pz)

    raise TypeError(f"Unsupported channel configuration: {type(configuration).__name__}")


def _channel_summary(configuration: ChannelConfiguration) -> ChannelSummary:
    names = {
        "identity": "Identity channel",
        "depolarizing": "Depolarizing",
        "bit_flip": "Bit flip",
        "phase_flip": "Phase flip",
        "amplitude_damping": "Amplitude damping",
        "pauli": "Pauli mixture",
    }
    data = configuration.model_dump()
    channel_type = str(data.pop("type"))
    return ChannelSummary(type=channel_type, name=names[channel_type], parameters=data)


def _final_key_string(session_key: npt.NDArray[np.uint8] | None) -> str | None:
    """Serialize a completed simulator key as a binary string for inspection."""

    if session_key is None:
        return None
    return "".join(str(int(bit)) for bit in session_key)


def run_bb84(request: BB84SimulationRequest) -> BB84SimulationResponse:
    """Execute BB84 with the engine's seeded RNG and adapt its immutable result."""

    channels = tuple(build_channel(configuration) for configuration in request.channels)
    pipeline = ChannelPipeline(channels)
    rng = SeededRNG(request.seed)

    started = perf_counter()
    session = BB84Protocol(channel=pipeline, rng=rng).run_session(request.n_signals)
    result = session.raw
    duration_ms = (perf_counter() - started) * 1000.0

    alice_basis_counts = Counter(basis.value for basis in result.alice_bases)
    bob_basis_counts = Counter(basis.value for basis in result.bob_bases)
    bob_outcome_counts = Counter(int(bit) for bit in result.bob_measured_bits)

    records: list[TransmissionRecord] = []
    for index in range(min(result.n_raw, INSPECTOR_LIMIT)):
        basis_match = result.alice_bases[index] is result.bob_bases[index]
        records.append(
            TransmissionRecord(
                index=index,
                alice_bit=int(result.alice_raw_bits[index]),
                alice_basis=_bb84_basis_value(result.alice_bases[index]),
                bob_basis=_bb84_basis_value(result.bob_bases[index]),
                bob_result=int(result.bob_measured_bits[index]),
                basis_match=basis_match,
                sifted_error=(
                    bool(result.alice_raw_bits[index] != result.bob_measured_bits[index])
                    if basis_match
                    else None
                ),
            )
        )

    diagnostic_qber = result.qber_by_basis if result.n_sifted > 0 else None
    summaries = [_channel_summary(configuration) for configuration in request.channels]

    return BB84SimulationResponse(
        metadata=SimulationMetadata(
            request_id=str(uuid4()),
            protocol="bb84",
            seed=request.seed,
            duration_ms=round(duration_ms, 3),
            inspector_limit=INSPECTOR_LIMIT,
            inspector_truncated=result.n_raw > INSPECTOR_LIMIT,
        ),
        channels=summaries,
        metrics=SimulationMetrics(
            n_raw=result.n_raw,
            n_sifted=result.n_sifted,
            sifting_efficiency=result.sifting_efficiency,
            qber=(diagnostic_qber.qber_aggregated if diagnostic_qber is not None else None),
            qber_z=(diagnostic_qber.qber_z if diagnostic_qber is not None else None),
            qber_x=(diagnostic_qber.qber_x if diagnostic_qber is not None else None),
            qber_aggregated=(diagnostic_qber.qber_aggregated if diagnostic_qber is not None else None),
        ),
        postprocessing=PostprocessingSummary(
            status=session.status.value,
            abort_reason=session.abort_reason,
            n_disclosed=session.n_disclosed,
            estimated_qber=session.estimated_qber,
            estimated_qber_z=session.estimated_qber_z,
            estimated_qber_x=session.estimated_qber_x,
            estimated_qber_aggregated=session.estimated_qber_aggregated,
            phase_error_bound=session.phase_error_bound,
            n_candidate=session.n_candidate,
            leak_ec=session.leak_ec,
            corrected_errors=(
                session.reconciliation.corrected_errors if session.reconciliation is not None else 0
            ),
            verification_passed=(session.verification.verified if session.verification is not None else None),
            verification_leakage=session.verification_leakage,
            n_reconciled=session.n_reconciled,
            n_final=session.n_final,
            compression_ratio=(
                session.privacy_amplification.compression_ratio
                if session.privacy_amplification is not None
                else None
            ),
            final_secret_fraction=session.final_secret_fraction,
            final_key=_final_key_string(session.alice_final_key),
        ),
        alice_basis_counts=BasisCounts(Z=alice_basis_counts["Z"], X=alice_basis_counts["X"]),
        bob_basis_counts=BasisCounts(Z=bob_basis_counts["Z"], X=bob_basis_counts["X"]),
        bob_outcome_counts=OutcomeCounts(zero=bob_outcome_counts[0], one=bob_outcome_counts[1]),
        transmissions=records,
    )
