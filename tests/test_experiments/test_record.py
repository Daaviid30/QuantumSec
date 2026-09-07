import json
from collections.abc import Mapping
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
