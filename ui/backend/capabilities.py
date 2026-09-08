"""Capability discovery backed by the features that exist in the repository."""

from importlib.metadata import PackageNotFoundError, version

from orchestration import SessionProfile, session_capabilities
from ui.backend.schemas import (
    AdversaryCapability,
    CapabilitiesResponse,
    ChannelCapability,
    FeatureCapability,
    ParameterCapability,
    ProfileCapability,
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
        profiles=[_profile_capability(definition.profile) for definition in session_capabilities()],
        protocols=[
            ProtocolCapability(
                id="bb84",
                name="BB84",
                implemented=True,
                description=(
                    "Prepare-and-measure BB84 with sampled parameter estimation, Cascade, "
                    "reconciled-key verification, Toeplitz privacy amplification, and an "
                    "explicitly assumed authenticated classical channel."
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
        adversaries=[
            AdversaryCapability(
                id="intercept_resend",
                name="Eve: intercept-resend",
                implemented=True,
                description=(
                    "Eve independently intercepts a configured fraction of qubits, measures each "
                    "in a uniformly random Z/X basis, and resends the state implied by her outcome."
                ),
                parameters=[
                    _probability(
                        "intercept_fraction",
                        "Intercept fraction",
                        "f",
                        1.0,
                        "Independent probability that Eve intercepts each signal",
                    )
                ],
            )
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
                name="Per-basis QBER",
                implemented=True,
                description=(
                    "Diagnostic error fractions e_Z, e_X, and their aggregate over complete sifted material."
                ),
            ),
            FeatureCapability(
                id="parameter_estimation",
                name="Stratified parameter estimation",
                implemented=True,
                description=(
                    "Seeded per-basis sampling estimates e_Z and e_X and removes every disclosed "
                    "position before reconciliation."
                ),
            ),
            FeatureCapability(
                id="intercept_resend",
                name="Intercept-resend adversary",
                implemented=True,
                description=(
                    "A seeded stochastic pipeline stage models Eve without exposing Alice's or "
                    "Bob's private protocol choices."
                ),
            ),
            FeatureCapability(
                id="reconciliation",
                name="Error reconciliation",
                implemented=True,
                description="Multi-pass Cascade corrects errors and records public parity leakage.",
            ),
            FeatureCapability(
                id="verification",
                name="Reconciled-key verification",
                implemented=True,
                description=(
                    "Universal-hash tags detect residual disagreement and record leakage; they do "
                    "not authenticate the classical channel."
                ),
            ),
            FeatureCapability(
                id="privacy_amplification",
                name="Privacy amplification",
                implemented=True,
                description="FFT Toeplitz hashing extracts the asymptotically estimated key length.",
            ),
            FeatureCapability(
                id="pqc_authentication",
                name="PQC session establishment",
                implemented=True,
                description=(
                    "Mutually authenticated ML-KEM/HQC profile execution, HKDF-SHA-384, and "
                    "Finished confirmation are exposed through the common session API."
                ),
            ),
            FeatureCapability(
                id="experiments",
                name="Reproducible run records",
                implemented=True,
                description=(
                    "Versioned configurations, environment provenance, ordered traces, categorized "
                    "metrics, and secret-safe records are current."
                ),
            ),
            FeatureCapability(
                id="qkd_authentication",
                name="Executed QKD authentication",
                implemented=True,
                description=(
                    "Assumed, one-time Wegman-Carter-style, and ML-DSA-65 classical-channel "
                    "authentication policies are explicit and executable."
                ),
            ),
            FeatureCapability(
                id="hybrid_sessions",
                name="Hybrid QKD–PQC sessions",
                implemented=True,
                description=(
                    "Independent BB84 and PQC contributions are composed above both domains with "
                    "canonical ordering, provenance, HKDF, and Finished confirmation."
                ),
            ),
            FeatureCapability(
                id="data_plane",
                name="AES-256-GCM data plane",
                implemented=True,
                description=(
                    "Established 256-bit session keys can be consumed by a backend-only protected "
                    "session with nonce allocation, AAD binding, and tamper rejection."
                ),
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


def _profile_capability(profile: SessionProfile) -> ProfileCapability:
    definition = next(item for item in session_capabilities() if item.profile is profile)
    descriptions = {
        SessionProfile.QKD_ASSUMED: (
            "BB84 baseline with an authenticated classical channel stated as an external assumption."
        ),
        SessionProfile.QKD_CLASSICAL_AUTH: (
            "BB84 with executed one-time universal-hash authentication from provisioned PSK material."
        ),
        SessionProfile.QKD_PQC_AUTH: (
            "BB84 with executed ML-DSA-65 authentication over the canonical public transcript."
        ),
        SessionProfile.PQC_BASE: (
            "Mutually authenticated ML-KEM-768 session establishment and key confirmation."
        ),
        SessionProfile.PQC_DIVERSE: (
            "PQC session establishment diversified with independent ML-KEM-768 and HQC-3 inputs."
        ),
        SessionProfile.HYBRID: (
            "Upper-layer composition of authenticated BB84 material and ML-KEM-768 material."
        ),
        SessionProfile.HYBRID_DIVERSE: (
            "Upper-layer composition of BB84, ML-KEM-768, and HQC-3 material with explicit provenance."
        ),
    }
    if definition.hybrid:
        family = "hybrid"
    elif definition.qkd_profile is not None:
        family = "qkd"
    else:
        family = "pqc"
    return ProfileCapability(
        id=profile.value,
        name=profile.value,
        family=family,
        implemented=definition.supported,
        status=definition.status.value,
        description=descriptions[profile],
        establishment=list(definition.establishment_algorithms),
        authentication=list(definition.authentication_policy),
        algorithms=list(definition.algorithms),
        hybrid=definition.hybrid,
        diversified=definition.diversified,
        supports_qkd=definition.qkd_profile is not None or definition.hybrid,
        supports_data_plane=profile
        in {
            SessionProfile.PQC_BASE,
            SessionProfile.PQC_DIVERSE,
            SessionProfile.HYBRID,
            SessionProfile.HYBRID_DIVERSE,
        },
    )
