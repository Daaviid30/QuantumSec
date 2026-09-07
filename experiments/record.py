"""Immutable, versioned public evidence produced by one experiment run."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Final, cast
from uuid import UUID, uuid4

from experiments.config import ExperimentConfig, ExperimentKind
from experiments.environment import ExperimentEnvironment
from experiments.runtime import RuntimeProvisioning
from orchestration.result import SessionResult

EXPERIMENT_RECORD_VERSION: Final = 1


@dataclass(frozen=True, slots=True)
class ExperimentRecord:
    version: int
    run_id: str
    timestamp_utc: datetime
    config: ExperimentConfig
    environment: ExperimentEnvironment
    provisioning: RuntimeProvisioning
    result: Mapping[str, object]
    trace: Mapping[str, object]
    metrics: Mapping[str, object]
    execution_order_index: int | None = None

    def __post_init__(self) -> None:
        if self.version != EXPERIMENT_RECORD_VERSION:
            raise ValueError(f"version must be {EXPERIMENT_RECORD_VERSION}.")
        try:
            identifier = UUID(self.run_id)
        except (ValueError, AttributeError) as exc:
            raise ValueError("run_id must be a valid UUID4 string.") from exc
        if identifier.version != 4:
            raise ValueError("run_id must be a UUID4 string.")
        if not isinstance(self.timestamp_utc, datetime) or self.timestamp_utc.tzinfo is None:
            raise ValueError("timestamp_utc must be a timezone-aware datetime.")
        if self.timestamp_utc.utcoffset() != UTC.utcoffset(self.timestamp_utc):
            raise ValueError("timestamp_utc must use UTC.")
        if not isinstance(self.config, ExperimentConfig):
            raise TypeError("config must be an ExperimentConfig.")
        if not isinstance(self.environment, ExperimentEnvironment):
            raise TypeError("environment must be an ExperimentEnvironment.")
        if not isinstance(self.provisioning, RuntimeProvisioning):
            raise TypeError("provisioning must be RuntimeProvisioning.")
        order = self.execution_order_index
        if order is not None and (
            isinstance(order, bool) or not isinstance(order, int) or order < 0
        ):
            raise ValueError("execution_order_index must be a non-negative integer or None.")
        object.__setattr__(self, "result", _freeze_mapping(self.result, "result"))
        object.__setattr__(self, "trace", _freeze_mapping(self.trace, "trace"))
        object.__setattr__(self, "metrics", _freeze_mapping(self.metrics, "metrics"))

    @classmethod
    def from_session_result(
        cls,
        *,
        config: ExperimentConfig,
        environment: ExperimentEnvironment,
        provisioning: RuntimeProvisioning,
        session_result: SessionResult,
        execution_order_index: int | None = None,
    ) -> ExperimentRecord:
        """Copy public evidence before the caller closes the live session capability."""

        public = session_result.to_public_dict()
        trace = public.pop("trace")
        metrics = public.pop("metrics")
        if not isinstance(trace, Mapping) or not isinstance(metrics, Mapping):
            raise RuntimeError("SessionResult returned an invalid public trace or metrics structure.")
        return cls(
            version=EXPERIMENT_RECORD_VERSION,
            run_id=str(uuid4()),
            timestamp_utc=datetime.now(UTC),
            config=config,
            environment=environment,
            provisioning=provisioning,
            result=public,
            trace=trace,
            metrics=metrics,
            execution_order_index=execution_order_index,
        )

    @property
    def experiment_kind(self) -> ExperimentKind:
        return self.config.experiment_kind

    @property
    def condition_id(self) -> str:
        return self.config.condition_id

    @property
    def replicate_index(self) -> int:
        return self.config.replicate_index

    @property
    def seed(self) -> int | None:
        return self.config.seed

    @property
    def profile(self) -> str:
        return self.config.profile.value

    def to_public_dict(self) -> dict[str, object]:
        data = self._public_without_artifact()
        artifact = {"experiment_record_json_bytes": 0}
        data["artifact"] = artifact
        while True:
            size = len(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
            if artifact["experiment_record_json_bytes"] == size:
                return data
            artifact["experiment_record_json_bytes"] = size

    def _public_without_artifact(self) -> dict[str, object]:
        return {
            "version": self.version,
            "run_id": self.run_id,
            "experiment_kind": self.experiment_kind.value,
            "condition_id": self.condition_id,
            "replicate_index": self.replicate_index,
            "execution_order_index": self.execution_order_index,
            "timestamp_utc": self.timestamp_utc.isoformat(),
            "seed": self.seed,
            "profile": self.profile,
            "environment": self.environment.to_public_dict(),
            "config": self.config.to_public_dict(),
            "provisioning": self.provisioning.to_public_dict(),
            "result": _thaw(self.result),
            "trace": _thaw(self.trace),
            "metrics": _thaw(self.metrics),
        }


def _freeze_mapping(value: Mapping[str, object], name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping.")
    frozen = _freeze(value)
    return cast(Mapping[str, object], frozen)


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        clean: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("Public record mappings require string keys.")
            clean[key] = _freeze(item)
        return MappingProxyType(clean)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Unsupported public record value: {type(value).__name__}.")


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value
