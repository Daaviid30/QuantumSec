"""Secret-free JSON/CSV serialization for experiment configs and records."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable, Mapping
from dataclasses import fields
from pathlib import Path
from typing import cast

from experiments.config import ExperimentConfig
from experiments.environment import ExperimentEnvironment
from experiments.record import ExperimentRecord
from orchestration.authentication import AuthenticationMetrics
from orchestration.metrics import (
    HybridSessionMetrics,
    PQCAuthenticationMetrics,
    PQCSessionMetrics,
    QKDSessionMetrics,
)


def config_from_json(text: str) -> ExperimentConfig:
    value = _loads_without_duplicate_keys(text)
    if not isinstance(value, Mapping):
        raise ValueError("A config JSON document must contain one object.")
    return ExperimentConfig.from_public_dict(cast(Mapping[str, object], value))


def configs_from_json(text: str) -> tuple[ExperimentConfig, ...]:
    value = _loads_without_duplicate_keys(text)
    if not isinstance(value, list) or not value:
        raise ValueError("A batch config JSON document must contain a non-empty array.")
    configs: list[ExperimentConfig] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise ValueError(f"Batch config item {index} must be an object.")
        configs.append(ExperimentConfig.from_public_dict(cast(Mapping[str, object], item)))
    return tuple(configs)


def load_config_json(path: str | Path) -> ExperimentConfig:
    return config_from_json(Path(path).read_text(encoding="utf-8"))


def load_configs_json(path: str | Path) -> tuple[ExperimentConfig, ...]:
    return configs_from_json(Path(path).read_text(encoding="utf-8"))


def dumps_json(
    value: ExperimentRecord | Iterable[ExperimentRecord],
) -> str:
    payload: object
    if isinstance(value, ExperimentRecord):
        payload = value.to_public_dict()
    else:
        records = tuple(value)
        if not all(isinstance(record, ExperimentRecord) for record in records):
            raise TypeError("JSON export accepts only ExperimentRecord values.")
        payload = [record.to_public_dict() for record in records]
    return json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)


def export_json(
    value: ExperimentRecord | Iterable[ExperimentRecord],
    destination: str | Path,
) -> int:
    """Write UTF-8 JSON and return the serialized artifact byte count."""

    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = dumps_json(value) + "\n"
    output.write_text(text, encoding="utf-8", newline="")
    return len(text.encode("utf-8"))


def dumps_csv(records: Iterable[ExperimentRecord]) -> str:
    clean_records = tuple(records)
    if not clean_records:
        raise ValueError("CSV export requires at least one ExperimentRecord.")
    if not all(isinstance(record, ExperimentRecord) for record in clean_records):
        raise TypeError("CSV export accepts only ExperimentRecord values.")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for record in clean_records:
        public = record.to_public_dict()
        row = {column: _csv_value(_lookup(public, column)) for column in CSV_COLUMNS}
        row["config_json"] = _canonical_cell(public["config"])
        config = cast(Mapping[str, object], public["config"])
        row["qkd_stages_json"] = _canonical_cell(config["qkd_stages"])
        row["result.provenance_json"] = _canonical_cell(_lookup(public, "result.provenance"))
        row["result.authentication_json"] = _canonical_cell(_lookup(public, "result.authentication"))
        row["result.public_context_json"] = _canonical_cell(_lookup(public, "result.public_context"))
        row["trace_json"] = _canonical_cell(public["trace"])
        writer.writerow(row)
    return buffer.getvalue()


def export_csv(records: Iterable[ExperimentRecord], destination: str | Path) -> int:
    """Write one analysis-ready UTF-8 CSV row per record and return byte count."""

    output = Path(destination)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = dumps_csv(records)
    output.write_text(text, encoding="utf-8", newline="")
    return len(text.encode("utf-8"))


def _loads_without_duplicate_keys(text: str) -> object:
    if not isinstance(text, str):
        raise TypeError("JSON input must be text.")

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON field: {key!r}.")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}.") from exc


def _lookup(data: Mapping[str, object], dotted_path: str) -> object:
    current: object = data
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _csv_value(value: object) -> object:
    if value is None:
        return ""
    if isinstance(value, (Mapping, list, tuple)):
        return _canonical_cell(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def _canonical_cell(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


_BASE_COLUMNS = (
    "version",
    "run_id",
    "experiment_kind",
    "condition_id",
    "replicate_index",
    "batch.version",
    "batch.batch_run_id",
    "batch.shuffle",
    "batch.order_seed",
    "batch.warmup_runs",
    "execution_order_index",
    "timestamp_utc",
    "seed",
    "profile",
    "artifact.experiment_record_json_bytes",
)
_ENVIRONMENT_COLUMNS = tuple(f"environment.{field.name}" for field in fields(ExperimentEnvironment))
_CONFIG_COLUMNS = (
    "config.version",
    "config.experiment_kind",
    "config.condition_id",
    "config.replicate_index",
    "config.seed",
    "config.session.version",
    "config.session.profile",
    "config.session.qkd_authentication_profile",
    "config.session.qkd_signal_count",
    "config.session.qkd_postprocessing",
    "config.session.internal_pqc_profile",
    "config.tags",
    "config_json",
    "qkd_stages_json",
)
_PROVISIONING_COLUMNS = (
    "provisioning.pqc_identities",
    "provisioning.qkd_authentication_material",
    "provisioning.qkd_authentication_material_bytes_per_direction",
    "provisioning.included_in_session_timings",
)
_RESULT_COLUMNS = (
    "result.version",
    "result.session_id",
    "result.profile",
    "result.status",
    "result.abort_reason",
    "result.established_key.type",
    "result.established_key.bit_length",
    "result.provenance_json",
    "result.authentication_json",
    "result.public_context_json",
)
_METRIC_COLUMNS = (
    *(f"metrics.qkd.{field.name}" for field in fields(QKDSessionMetrics)),
    *(f"metrics.pqc.{field.name}" for field in fields(PQCSessionMetrics)),
    *(f"metrics.qkd_authentication.{field.name}" for field in fields(AuthenticationMetrics)),
    *(f"metrics.pqc_authentication.{field.name}" for field in fields(PQCAuthenticationMetrics)),
    *(f"metrics.hybrid.{field.name}" for field in fields(HybridSessionMetrics)),
    "metrics.orchestration_software_wall_time_ns",
)
CSV_COLUMNS = (
    *_BASE_COLUMNS,
    *_ENVIRONMENT_COLUMNS,
    *_CONFIG_COLUMNS,
    *_PROVISIONING_COLUMNS,
    *_RESULT_COLUMNS,
    *_METRIC_COLUMNS,
    "trace_json",
)
