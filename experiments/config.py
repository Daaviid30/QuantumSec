"""Strict, versioned, secret-free experiment configuration."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from orchestration.config import SESSION_CONFIG_VERSION, SessionConfig
from orchestration.profiles import QKDProfile, SessionProfile, session_profile_definition
from pqc.profiles import PQCProfile
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType
from qkd.postprocessing import CascadeConfig
from qkd.protocols import BB84PostprocessingConfig

EXPERIMENT_CONFIG_VERSION: Final = 1
_MAX_SEED: Final = 2**64 - 1
_CONDITION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_TAG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:=+-]{0,63}$")


class ExperimentKind(StrEnum):
    E1_PQC_COST = "E1"
    E2_BB84_VALIDATION = "E2"
    E3_INTERCEPT_RESEND = "E3"
    E4_QKD_AUTHENTICATION = "E4"
    E5_HYBRID_OVERHEAD = "E5"
    D1_PROTECTED_SESSION = "D1"


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    """One normalized instruction for an experimental session execution."""

    experiment_kind: ExperimentKind
    condition_id: str
    replicate_index: int
    session_config: SessionConfig
    seed: int | None = None
    qkd_stages: tuple[QKDChannelStageSpec, ...] = ()
    tags: tuple[str, ...] = ()
    version: int = EXPERIMENT_CONFIG_VERSION

    def __post_init__(self) -> None:
        if self.version != EXPERIMENT_CONFIG_VERSION:
            raise ValueError(f"version must be {EXPERIMENT_CONFIG_VERSION}.")
        if not isinstance(self.experiment_kind, ExperimentKind):
            raise TypeError("experiment_kind must be an ExperimentKind.")
        if not isinstance(self.condition_id, str) or not _CONDITION_PATTERN.fullmatch(self.condition_id):
            raise ValueError("condition_id must contain 1-128 ASCII letters, digits, '.', '_', or '-'.")
        if (
            isinstance(self.replicate_index, bool)
            or not isinstance(self.replicate_index, int)
            or self.replicate_index < 0
        ):
            raise ValueError("replicate_index must be a non-negative integer.")
        if not isinstance(self.session_config, SessionConfig):
            raise TypeError("session_config must be a SessionConfig.")

        definition = session_profile_definition(self.session_config.profile)
        uses_qkd = definition.qkd_profile is not None or definition.hybrid
        if uses_qkd:
            if (
                isinstance(self.seed, bool)
                or not isinstance(self.seed, int)
                or not 0 <= self.seed <= _MAX_SEED
            ):
                raise ValueError("QKD and hybrid experiments require a seed in [0, 2^64 - 1].")
        elif self.seed is not None:
            raise ValueError("PQC-only experiments use backend randomness and must not configure a seed.")

        stages = tuple(self.qkd_stages)
        if not all(isinstance(stage, QKDChannelStageSpec) for stage in stages):
            raise TypeError("qkd_stages must contain only QKDChannelStageSpec values.")
        if len(stages) > 32:
            raise ValueError("qkd_stages cannot contain more than 32 ordered stages.")
        if not uses_qkd and stages:
            raise ValueError("PQC-only experiments cannot configure QKD stages.")
        object.__setattr__(self, "qkd_stages", stages)

        uses_pqc = definition.internal_pqc_profile is not None
        if (
            self.experiment_kind
            in {
                ExperimentKind.E2_BB84_VALIDATION,
                ExperimentKind.E3_INTERCEPT_RESEND,
                ExperimentKind.E4_QKD_AUTHENTICATION,
            }
            and not uses_qkd
        ):
            raise ValueError(f"{self.experiment_kind.value} experiments require a QKD profile.")
        if self.experiment_kind is ExperimentKind.E3_INTERCEPT_RESEND and not any(
            stage.type is QKDChannelStageType.INTERCEPT_RESEND for stage in stages
        ):
            raise ValueError("E3 experiments require an intercept_resend QKD stage.")
        if (
            self.experiment_kind
            in {
                ExperimentKind.E1_PQC_COST,
                ExperimentKind.E5_HYBRID_OVERHEAD,
                ExperimentKind.D1_PROTECTED_SESSION,
            }
            and not uses_pqc
        ):
            raise ValueError(f"{self.experiment_kind.value} experiments require a PQC component.")

        tags = tuple(self.tags)
        if len(tags) > 16 or len(set(tags)) != len(tags):
            raise ValueError("tags must contain at most 16 unique values.")
        if not all(isinstance(tag, str) and _TAG_PATTERN.fullmatch(tag) for tag in tags):
            raise ValueError("Each tag must be a short, non-empty public label.")
        object.__setattr__(self, "tags", tags)

    @property
    def profile(self) -> SessionProfile:
        return self.session_config.profile

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "experiment_kind": self.experiment_kind.value,
            "condition_id": self.condition_id,
            "replicate_index": self.replicate_index,
            "seed": self.seed,
            "session": self.session_config.to_public_dict(),
            "qkd_stages": tuple(stage.to_public_dict() for stage in self.qkd_stages),
            "tags": self.tags,
        }

    @classmethod
    def from_public_dict(cls, data: Mapping[str, object]) -> ExperimentConfig:
        if not isinstance(data, Mapping):
            raise TypeError("Experiment configuration must be a mapping.")
        allowed = {
            "version",
            "experiment_kind",
            "condition_id",
            "replicate_index",
            "seed",
            "session",
            "qkd_stages",
            "tags",
        }
        _reject_unknown(data, allowed, "experiment config")
        version = _integer(data.get("version"), "version")
        kind_value = data.get("experiment_kind")
        condition_id = data.get("condition_id")
        session_data = data.get("session")
        if not isinstance(kind_value, str):
            raise ValueError("experiment_kind must be a string.")
        if not isinstance(condition_id, str):
            raise ValueError("condition_id must be a string.")
        if not isinstance(session_data, Mapping):
            raise ValueError("session must be a mapping.")
        try:
            kind = ExperimentKind(kind_value)
        except ValueError as exc:
            raise ValueError(f"Unknown experiment kind: {kind_value!r}.") from exc

        raw_stages = data.get("qkd_stages", ())
        if not isinstance(raw_stages, (list, tuple)):
            raise ValueError("qkd_stages must be an array.")
        stages = tuple(
            QKDChannelStageSpec.from_public_dict(stage)
            if isinstance(stage, Mapping)
            else _invalid_stage(index)
            for index, stage in enumerate(raw_stages)
        )
        raw_tags = data.get("tags", ())
        if not isinstance(raw_tags, (list, tuple)) or not all(isinstance(tag, str) for tag in raw_tags):
            raise ValueError("tags must be an array of strings.")
        seed_value = data.get("seed")
        seed = None if seed_value is None else _integer(seed_value, "seed")
        return cls(
            version=version,
            experiment_kind=kind,
            condition_id=condition_id,
            replicate_index=_integer(data.get("replicate_index"), "replicate_index"),
            session_config=_session_from_public_dict(session_data),
            seed=seed,
            qkd_stages=stages,
            tags=tuple(raw_tags),
        )


def _invalid_stage(index: int) -> QKDChannelStageSpec:
    raise ValueError(f"qkd_stages[{index}] must be an object.")


def _integer(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer.")
    return value


def _optional_integer(value: object, name: str) -> int | None:
    return None if value is None else _integer(value, name)


def _number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric.")
    return float(value)


def _reject_unknown(data: Mapping[str, object], allowed: set[str], label: str) -> None:
    unknown = set(data) - allowed
    if unknown:
        raise ValueError(f"Unknown {label} fields: {sorted(unknown)}.")


def _session_from_public_dict(data: Mapping[str, object]) -> SessionConfig:
    allowed = {
        "version",
        "profile",
        "qkd_authentication_profile",
        "qkd_signal_count",
        "qkd_postprocessing",
        "internal_pqc_profile",
    }
    _reject_unknown(data, allowed, "session")
    version = _integer(data.get("version"), "session.version")
    if version != SESSION_CONFIG_VERSION:
        raise ValueError(f"session.version must be {SESSION_CONFIG_VERSION}.")
    profile_value = data.get("profile")
    if not isinstance(profile_value, str):
        raise ValueError("session.profile must be a string.")
    try:
        profile = SessionProfile(profile_value)
    except ValueError as exc:
        raise ValueError(f"Unknown session profile: {profile_value!r}.") from exc

    auth_value = data.get("qkd_authentication_profile")
    if auth_value is not None and not isinstance(auth_value, str):
        raise ValueError("session.qkd_authentication_profile must be a string or null.")
    internal_value = data.get("internal_pqc_profile")
    if internal_value is not None and not isinstance(internal_value, str):
        raise ValueError("session.internal_pqc_profile must be a string or null.")
    postprocessing_data = data.get("qkd_postprocessing")
    if postprocessing_data is not None and not isinstance(postprocessing_data, Mapping):
        raise ValueError("session.qkd_postprocessing must be an object or null.")
    return SessionConfig(
        version=version,
        profile=profile,
        qkd_authentication_profile=(QKDProfile(auth_value) if auth_value is not None else None),
        qkd_signal_count=_optional_integer(data.get("qkd_signal_count"), "qkd_signal_count"),
        qkd_postprocessing=(
            _postprocessing_from_public_dict(postprocessing_data) if postprocessing_data is not None else None
        ),
        internal_pqc_profile=(PQCProfile(internal_value) if internal_value is not None else None),
    )


def _postprocessing_from_public_dict(data: Mapping[str, object]) -> BB84PostprocessingConfig:
    allowed = {
        "sample_fraction",
        "phase_error_abort_threshold",
        "cascade_passes",
        "cascade_initial_block_factor",
        "cascade_maximum_initial_block_size",
        "cascade_maximum_lookback_steps",
        "verification_tag_length",
        "security_margin_bits",
    }
    _reject_unknown(data, allowed, "QKD post-processing")
    required = allowed - {
        "cascade_maximum_initial_block_size",
        "cascade_maximum_lookback_steps",
    }
    missing = required - set(data)
    if missing:
        raise ValueError(f"Missing QKD post-processing fields: {sorted(missing)}.")
    cascade = CascadeConfig(
        passes=_integer(data.get("cascade_passes"), "cascade_passes"),
        initial_block_factor=_number(
            data.get("cascade_initial_block_factor"), "cascade_initial_block_factor"
        ),
        maximum_initial_block_size=_optional_integer(
            data.get("cascade_maximum_initial_block_size"), "cascade_maximum_initial_block_size"
        ),
        maximum_lookback_steps=_optional_integer(
            data.get("cascade_maximum_lookback_steps"), "cascade_maximum_lookback_steps"
        ),
    )
    return BB84PostprocessingConfig(
        sample_fraction=_number(data.get("sample_fraction"), "sample_fraction"),
        phase_error_abort_threshold=_number(
            data.get("phase_error_abort_threshold"), "phase_error_abort_threshold"
        ),
        cascade=cascade,
        verification_tag_length=_integer(data.get("verification_tag_length"), "verification_tag_length"),
        security_margin_bits=_integer(data.get("security_margin_bits"), "security_margin_bits"),
    )
