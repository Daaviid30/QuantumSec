import json
from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime
from uuid import UUID

import pytest


def test_record_is_versioned_utc_public_evidence(experiment_runner, qkd_config) -> None:
    record = experiment_runner.run(qkd_config)
    public = record.to_public_dict()
    assert record.version == 1
    assert UUID(record.run_id).version == 4
    assert datetime.fromisoformat(str(public["timestamp_utc"])).utcoffset() is not None
    assert public["seed"] == 2026
    assert public["profile"] == "QKD-ASSUMED"
    assert isinstance(public["result"], dict)
    assert isinstance(public["trace"], dict)
    assert isinstance(public["metrics"], dict)
    rendered = json.dumps(public, indent=2, ensure_ascii=False)
    artifact = public["artifact"]
    assert isinstance(artifact, dict)
    assert artifact["experiment_record_json_bytes"] == len(rendered.encode("utf-8"))


def test_record_recursively_freezes_copied_session_structures(experiment_runner, qkd_config) -> None:
    record = experiment_runner.run(qkd_config)
    assert isinstance(record.metrics, Mapping)
    with pytest.raises(TypeError):
        record.metrics["qkd"] = None  # type: ignore[index]


def test_record_rejects_secret_fields_and_non_finite_public_values(
    experiment_runner,
    qkd_config,
) -> None:
    record = experiment_runner.run(qkd_config)
    result = dict(record.result)
    result["public_context"] = {"k_session": "forbidden"}
    with pytest.raises(ValueError, match="Forbidden secret-bearing"):
        replace(record, result=result)

    metrics = dict(record.metrics)
    metrics["orchestration_software_wall_time_ns"] = float("nan")
    with pytest.raises(ValueError, match="non-finite"):
        replace(record, metrics=metrics)
