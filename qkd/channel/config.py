"""Public, Pydantic-free specifications for reproducible QKD channel pipelines."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256

from core.rng import BaseRNG, SeededRNG
from qkd.channel.attacks import InterceptResendAttack
from qkd.channel.base import QuantumChannel
from qkd.channel.ideal import IdentityChannel
from qkd.channel.noise import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    DepolarizingChannel,
    PauliChannel,
    PhaseFlipChannel,
)
from qkd.channel.pipeline import ChannelPipeline


class QKDChannelStageType(StrEnum):
    IDENTITY = "identity"
    DEPOLARIZING = "depolarizing"
    BIT_FLIP = "bit_flip"
    PHASE_FLIP = "phase_flip"
    AMPLITUDE_DAMPING = "amplitude_damping"
    PAULI = "pauli"
    INTERCEPT_RESEND = "intercept_resend"


@dataclass(frozen=True, slots=True)
class QKDChannelStageSpec:
    """Strict public description of one ordered channel or adversary stage."""

    type: QKDChannelStageType
    p: float | None = None
    gamma: float | None = None
    px: float | None = None
    py: float | None = None
    pz: float | None = None
    intercept_fraction: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.type, QKDChannelStageType):
            raise TypeError("type must be a QKDChannelStageType.")
        expected = {
            QKDChannelStageType.IDENTITY: (),
            QKDChannelStageType.DEPOLARIZING: ("p",),
            QKDChannelStageType.BIT_FLIP: ("p",),
            QKDChannelStageType.PHASE_FLIP: ("p",),
            QKDChannelStageType.AMPLITUDE_DAMPING: ("gamma",),
            QKDChannelStageType.PAULI: ("px", "py", "pz"),
            QKDChannelStageType.INTERCEPT_RESEND: ("intercept_fraction",),
        }[self.type]
        parameter_names = ("p", "gamma", "px", "py", "pz", "intercept_fraction")
        for name in parameter_names:
            value = getattr(self, name)
            if name in expected:
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(f"{self.type.value} requires numeric parameter {name}.")
                clean = float(value)
                if not 0.0 <= clean <= 1.0:
                    raise ValueError(f"{name} must lie in [0, 1].")
                object.__setattr__(self, name, clean)
            elif value is not None:
                raise ValueError(f"{self.type.value} does not accept parameter {name}.")
        if self.type is QKDChannelStageType.PAULI:
            assert self.px is not None and self.py is not None and self.pz is not None
            if self.px + self.py + self.pz > 1.0:
                raise ValueError("Pauli probabilities must satisfy px + py + pz <= 1.")

    def to_public_dict(self) -> dict[str, object]:
        data: dict[str, object] = {"type": self.type.value}
        for name in ("p", "gamma", "px", "py", "pz", "intercept_fraction"):
            value = getattr(self, name)
            if value is not None:
                data[name] = value
        return data

    @classmethod
    def from_public_dict(cls, data: Mapping[str, object]) -> QKDChannelStageSpec:
        if not isinstance(data, Mapping):
            raise TypeError("A QKD channel stage must be a mapping.")
        allowed = {"type", "p", "gamma", "px", "py", "pz", "intercept_fraction"}
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"Unknown QKD channel stage fields: {sorted(unknown)}.")
        stage_type = data.get("type")
        if not isinstance(stage_type, str):
            raise ValueError("A QKD channel stage requires a string type.")
        try:
            normalized_type = QKDChannelStageType(stage_type)
        except ValueError as exc:
            raise ValueError(f"Unsupported QKD channel stage type: {stage_type!r}.") from exc
        return cls(
            type=normalized_type,
            p=_optional_number(data.get("p"), "p"),
            gamma=_optional_number(data.get("gamma"), "gamma"),
            px=_optional_number(data.get("px"), "px"),
            py=_optional_number(data.get("py"), "py"),
            pz=_optional_number(data.get("pz"), "pz"),
            intercept_fraction=_optional_number(
                data.get("intercept_fraction"), "intercept_fraction"
            ),
        )


def _optional_number(value: object, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric when provided.")
    return float(value)


def _stage_seed(root_seed: int, stage_index: int) -> int:
    material = f"quantumsec/adversary-rng/v1:{root_seed}:{stage_index}".encode("ascii")
    return int.from_bytes(sha256(material).digest()[:16], byteorder="big")


def build_channel_stage(
    spec: QKDChannelStageSpec,
    *,
    rng: BaseRNG,
    intercept_resend_factory: Callable[[float, BaseRNG], QuantumChannel] = InterceptResendAttack,
) -> QuantumChannel:
    """Build one domain channel from a validated neutral stage specification."""

    if not isinstance(spec, QKDChannelStageSpec):
        raise TypeError("spec must be a QKDChannelStageSpec.")
    if not isinstance(rng, BaseRNG):
        raise TypeError("rng must implement BaseRNG.")
    match spec.type:
        case QKDChannelStageType.IDENTITY:
            return IdentityChannel()
        case QKDChannelStageType.DEPOLARIZING:
            assert spec.p is not None
            return DepolarizingChannel(p=spec.p)
        case QKDChannelStageType.BIT_FLIP:
            assert spec.p is not None
            return BitFlipChannel(p=spec.p)
        case QKDChannelStageType.PHASE_FLIP:
            assert spec.p is not None
            return PhaseFlipChannel(p=spec.p)
        case QKDChannelStageType.AMPLITUDE_DAMPING:
            assert spec.gamma is not None
            return AmplitudeDampingChannel(gamma=spec.gamma)
        case QKDChannelStageType.PAULI:
            assert spec.px is not None and spec.py is not None and spec.pz is not None
            return PauliChannel(px=spec.px, py=spec.py, pz=spec.pz)
        case QKDChannelStageType.INTERCEPT_RESEND:
            assert spec.intercept_fraction is not None
            return intercept_resend_factory(spec.intercept_fraction, rng)


def build_channel_pipeline(
    specs: Iterable[QKDChannelStageSpec],
    *,
    root_seed: int,
    rng_factory: Callable[[int], BaseRNG] = SeededRNG,
    intercept_resend_factory: Callable[[float, BaseRNG], QuantumChannel] = InterceptResendAttack,
) -> ChannelPipeline:
    """Build an ordered pipeline with domain-separated RNG streams for adversaries."""

    if isinstance(root_seed, bool) or not isinstance(root_seed, int) or root_seed < 0:
        raise ValueError("root_seed must be a non-negative integer.")
    clean_specs = tuple(specs)
    channels = tuple(
        build_channel_stage(
            spec,
            rng=rng_factory(_stage_seed(root_seed, index)),
            intercept_resend_factory=intercept_resend_factory,
        )
        for index, spec in enumerate(clean_specs)
    )
    return ChannelPipeline(channels)
