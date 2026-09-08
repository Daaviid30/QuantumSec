"""Immutable, versioned public evidence produced by one experiment run."""

from __future__ import annotations

import json
import math
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
BATCH_PROVENANCE_VERSION: Final = 1

_RESULT_FIELDS: Final = frozenset(
    {
        "version",
        "session_id",
        "profile",
        "status",
        "abort_reason",
        "established_key",
        "provenance",
        "authentication",
        "public_context",
    }
)
_TRACE_FIELDS: Final = frozenset({"version", "events"})
_METRIC_FIELDS: Final = frozenset(
    {
        "qkd",
        "pqc",
        "qkd_authentication",
        "pqc_authentication",
        "hybrid",
        "orchestration_software_wall_time_ns",
    }
)
_FORBIDDEN_SECRET_FIELDS: Final = frozenset(
    {
        "aes_key",
        "k_confirm",
        "k_session",
        "kem_private_key",
        "mldsa_private_key",
        "ml_dsa_private_key",
        "raw_qkd_final_key",
        "ss_hqc",
        "ss_mlkem",
        "wegman_carter_psk",
    }
)


@dataclass(frozen=True, slots=True)
class BatchProvenance:
    """Public, versioned provenance shared by every retained run in one batch."""

    batch_run_id: str
    shuffle: bool
    order_seed: int | None
    warmup_runs: int
    version: int = BATCH_PROVENANCE_VERSION

    def __post_init__(self) -> None:
        if self.version != BATCH_PROVENANCE_VERSION:
            raise ValueError(f"version must be {BATCH_PROVENANCE_VERSION}.")
        _validate_uuid4(self.batch_run_id, "batch_run_id")
        if not isinstance(self.shuffle, bool):
            raise TypeError("shuffle must be a bool.")
        if self.shuffle:
            if (
                isinstance(self.order_seed, bool)
                or not isinstance(self.order_seed, int)
                or self.order_seed < 0
            ):
                raise ValueError("shuffle=True requires a non-negative integer order_seed.")
        elif self.order_seed is not None:
            raise ValueError("order_seed must be None when shuffle=False.")
        if (
            isinstance(self.warmup_runs, bool)
            or not isinstance(self.warmup_runs, int)
            or self.warmup_runs < 0
        ):
            raise ValueError("warmup_runs must be a non-negative integer.")

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "batch_run_id": self.batch_run_id,
            "shuffle": self.shuffle,
            "order_seed": self.order_seed,
            "warmup_runs": self.warmup_runs,
        }


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
    batch: BatchProvenance | None = None
    execution_order_index: int | None = None

    def __post_init__(self) -> None:
        if self.version != EXPERIMENT_RECORD_VERSION:
            raise ValueError(f"version must be {EXPERIMENT_RECORD_VERSION}.")
        _validate_uuid4(self.run_id, "run_id")
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
        if order is not None and (isinstance(order, bool) or not isinstance(order, int) or order < 0):
            raise ValueError("execution_order_index must be a non-negative integer or None.")
        if self.batch is None and order is not None:
            raise ValueError("execution_order_index requires batch provenance.")
        if self.batch is not None:
            if not isinstance(self.batch, BatchProvenance):
                raise TypeError("batch must be BatchProvenance or None.")
            if order is None:
                raise ValueError("Batch records require execution_order_index.")
        _validate_public_mapping(self.result, "result", _RESULT_FIELDS)
        _validate_public_mapping(self.trace, "trace", _TRACE_FIELDS)
        _validate_public_mapping(self.metrics, "metrics", _METRIC_FIELDS)
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
        batch: BatchProvenance | None = None,
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
            batch=batch,
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
            size = len(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8"))
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
            "batch": self.batch.to_public_dict() if self.batch is not None else None,
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


def _validate_uuid4(value: object, name: str) -> None:
    try:
        identifier = UUID(value) if isinstance(value, str) else None
    except (ValueError, AttributeError) as exc:
        raise ValueError(f"{name} must be a valid UUID4 string.") from exc
    if identifier is None or identifier.version != 4 or str(identifier) != value:
        raise ValueError(f"{name} must be a canonical UUID4 string.")


def _validate_public_mapping(
    value: Mapping[str, object],
    name: str,
    expected_fields: frozenset[str],
) -> None:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping.")
    actual = set(value)
    if actual != expected_fields:
        missing = sorted(expected_fields - actual)
        unknown = sorted(actual - expected_fields)
        raise ValueError(f"{name} schema mismatch: missing={missing}, unknown={unknown}.")
    _validate_public_value(value, name)


def _validate_public_value(value: object, path: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"{path} mappings require string keys.")
            if key.casefold() in _FORBIDDEN_SECRET_FIELDS:
                raise ValueError(f"Forbidden secret-bearing public field: {path}.{key}.")
            _validate_public_value(item, f"{path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _validate_public_value(item, f"{path}[{index}]")
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{path} must not contain non-finite floats.")
    if value is None or isinstance(value, (str, int, float, bool)):
        return
    raise TypeError(f"Unsupported public record value at {path}: {type(value).__name__}.")


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
