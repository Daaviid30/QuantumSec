"""Capability discovery backed by the features that exist in the repository."""

from importlib.metadata import PackageNotFoundError, version

from ui.backend.schemas import (
    CapabilitiesResponse,
    ChannelCapability,
    FeatureCapability,
    ParameterCapability,
    ProtocolCapability,
)

MAX_CHANNELS = 12
MAX_SIGNALS = 100_000
INSPECTOR_LIMIT = 64


def project_version() -> str:
    """Return the installed project version with a source-tree fallback."""

    try:
        return version("quantumsec")
    except PackageNotFoundError:
        return "0.1.0"


def _probability(
    key: str,
    label: str,
    symbol: str,
    default: float,
    description: str,
) -> ParameterCapability:
    return ParameterCapability(
        key=key,
        label=label,
        symbol=symbol,
        minimum=0.0,
        maximum=1.0,
        step=0.01,
        default=default,
        description=description,
    )


def get_capabilities() -> CapabilitiesResponse:
    """Describe implemented and planned features without implying future support."""

    return CapabilitiesResponse(
        version=project_version(),
        protocols=[
            ProtocolCapability(
                id="bb84",
                name="BB84",
                implemented=True,
                description=(
                    "Prepare-and-measure BB84 with sampled parameter estimation, Cascade, "
                    "key confirmation, and Toeplitz privacy amplification."
                ),
            ),
            ProtocolCapability(
                id="b92",
                name="B92",
                implemented=False,
                description="Future non-orthogonal-state protocol; outside the current TFM scope.",
            ),
            ProtocolCapability(
                id="e91",
                name="E91",
                implemented=False,
                description="Future entanglement-based protocol; outside the current TFM scope.",
            ),
            ProtocolCapability(
                id="bbm92",
                name="BBM92",
                implemented=False,
                description="Future entanglement-based BB84 variant; outside the current TFM scope.",
            ),
        ],
        channels=[
            ChannelCapability(
                id="identity",
                name="Identity channel",
                implemented=True,
                description="Ideal transmission with no state transformation.",
                parameters=[],
            ),
            ChannelCapability(
                id="depolarizing",
                name="Depolarizing",
                implemented=True,
                description="Mixes a qubit toward the maximally mixed state.",
                parameters=[_probability("p", "Noise probability", "p", 0.03, "Mixing strength")],
            ),
            ChannelCapability(
                id="bit_flip",
                name="Bit flip",
                implemented=True,
                description="Applies Pauli X with the configured probability.",
                parameters=[_probability("p", "Flip probability", "p", 0.02, "Pauli X probability")],
            ),
            ChannelCapability(
                id="phase_flip",
                name="Phase flip",
                implemented=True,
                description="Applies Pauli Z with the configured probability.",
                parameters=[_probability("p", "Flip probability", "p", 0.02, "Pauli Z probability")],
            ),
            ChannelCapability(
                id="amplitude_damping",
                name="Amplitude damping",
                implemented=True,
                description="Models qubit relaxation from |1> to |0>, not optical loss.",
                parameters=[_probability("gamma", "Damping probability", "γ", 0.01, "Relaxation strength")],
            ),
            ChannelCapability(
                id="pauli",
                name="Pauli mixture",
                implemented=True,
                description="Independent incoherent X, Y and Z error probabilities.",
                parameters=[
                    _probability("px", "X probability", "pₓ", 0.01, "Pauli X probability"),
                    _probability("py", "Y probability", "pᵧ", 0.01, "Pauli Y probability"),
                    _probability("pz", "Z probability", "p_z", 0.01, "Pauli Z probability"),
                ],
            ),
        ],
        features=[
            FeatureCapability(
                id="seeded_rng",
                name="Seeded reproducibility",
                implemented=True,
                description="Runs use the engine's injected SeededRNG.",
            ),
            FeatureCapability(
                id="channel_pipeline",
                name="Sequential channel pipeline",
                implemented=True,
                description="Channels are applied in the configured order.",
            ),
            FeatureCapability(
                id="sifting",
                name="Basis sifting",
                implemented=True,
                description="Matching-basis positions are retained.",
            ),
            FeatureCapability(
                id="qber",
                name="QBER",
                implemented=True,
                description="Error fraction over the complete sifted material.",
            ),
            FeatureCapability(
                id="parameter_estimation",
                name="Parameter estimation",
                implemented=True,
                description="Seeded sampling estimates QBER and removes every disclosed position.",
            ),
            FeatureCapability(
                id="reconciliation",
                name="Error reconciliation",
                implemented=True,
                description="Multi-pass Cascade corrects errors and records public parity leakage.",
            ),
            FeatureCapability(
                id="verification",
                name="Key confirmation",
                implemented=True,
                description="Universal-hash tags confirm reconciliation and record tag leakage.",
            ),
            FeatureCapability(
                id="privacy_amplification",
                name="Privacy amplification",
                implemented=True,
                description="FFT Toeplitz hashing extracts the asymptotically estimated key length.",
            ),
            FeatureCapability(
                id="pqc_authentication",
                name="PQC session integration",
                implemented=False,
                description=(
                    "The standalone PQC handshake exists, but it has no Web API and is not connected "
                    "to QKD session orchestration."
                ),
            ),
            FeatureCapability(
                id="experiments",
                name="Experiment orchestration",
                implemented=False,
                description="Sweeps and Monte Carlo orchestration are planned.",
            ),
            FeatureCapability(
                id="qkdn",
                name="QKD networks",
                implemented=False,
                description="QKDN topology and routing are future work outside the current TFM scope.",
            ),
        ],
        limits={
            "max_signals": MAX_SIGNALS,
            "max_channels": MAX_CHANNELS,
            "inspector_records": INSPECTOR_LIMIT,
        },
    )
