import csv
import io
import json

import pytest

from experiments import ExperimentConfig, ExperimentKind, ExperimentRunner, ExperimentRuntimeFactory
from experiments.cli import main
from experiments.export import dumps_csv, dumps_json, export_csv, export_json
from orchestration import SessionConfig, SessionProfile


def test_json_and_csv_exports_are_secret_free_and_analysis_ready(monkeypatch, tmp_path) -> None:
    secrets = iter((b"sentinel-alice-" * 8192, b"sentinel-bob--" * 8192))
    monkeypatch.setattr("experiments.runtime.token_bytes", lambda _size: next(secrets))
    runner = ExperimentRunner(ExperimentRuntimeFactory(minimum_psk_bytes=1))
    config = ExperimentConfig(
        ExperimentKind.E4_QKD_AUTHENTICATION,
        "wegman-carter",
        0,
        SessionConfig(SessionProfile.QKD_CLASSICAL_AUTH, qkd_signal_count=512),
        seed=444,
    )
    record = runner.run(config)
    json_text = dumps_json(record)
    csv_text = dumps_csv((record,))
    lowered = (json_text + csv_text).lower()
    assert "sentinel-alice" not in lowered
    assert "sentinel-bob" not in lowered
    assert "metrics.qkd.estimated_qber_z" in csv_text.splitlines()[0]
    assert "trace_json" in csv_text.splitlines()[0]
    assert json.loads(json_text)["result"]["established_key"].get("value") is None

    json_path = tmp_path / "record.json"
    csv_path = tmp_path / "record.csv"
    assert export_json(record, json_path) == len(json_path.read_bytes())
    assert export_csv((record,), csv_path) == len(csv_path.read_bytes())


def test_missing_profile_metrics_are_empty_not_zero(experiment_runner) -> None:
    record = experiment_runner.run(
        ExperimentConfig(
            ExperimentKind.E1_PQC_COST,
            "pqc-base-csv",
            0,
            SessionConfig(SessionProfile.PQC_BASE),
        )
    )
    row = next(csv.DictReader(io.StringIO(dumps_csv((record,)))))
    assert row["metrics.qkd.estimated_qber_z"] == ""
    assert row["metrics.pqc.crypto_software_time_ns"] != ""


def test_minimal_cli_runs_saved_config(tmp_path) -> None:
    output = tmp_path / "qkd-record.json"
    assert (
        main(
            (
                "run",
                "examples/experiments/qkd_eve_example.json",
                "--output",
                str(output),
            )
        )
        == 0
    )
    public = json.loads(output.read_text(encoding="utf-8"))
    assert public["experiment_kind"] == "E3"
    assert public["result"]["status"] in {"established", "aborted"}


def test_cli_batch_exports_json_and_csv_with_reproducible_plan(tmp_path) -> None:
    config = ExperimentConfig(
        ExperimentKind.E1_PQC_COST,
        "cli-batch-pqc",
        0,
        SessionConfig(SessionProfile.PQC_BASE),
    )
    configs_path = tmp_path / "configs.json"
    configs_path.write_text(json.dumps([config.to_public_dict()]), encoding="utf-8")
    json_path = tmp_path / "records.json"
    csv_path = tmp_path / "records.csv"

    assert (
        main(
            (
                "batch",
                str(configs_path),
                "--json",
                str(json_path),
                "--csv",
                str(csv_path),
                "--shuffle",
                "--order-seed",
                "77",
                "--warmup-runs",
                "1",
            )
        )
        == 0
    )
    public = json.loads(json_path.read_text(encoding="utf-8"))
    assert public[0]["batch"]["shuffle"] is True
    assert public[0]["batch"]["order_seed"] == 77
    assert public[0]["batch"]["warmup_runs"] == 1
    row = next(csv.DictReader(io.StringIO(csv_path.read_text(encoding="utf-8"))))
    assert row["batch.shuffle"] == "true"
    assert row["batch.order_seed"] == "77"
    assert row["batch.warmup_runs"] == "1"


def test_cli_batch_requires_an_output(tmp_path, capsys) -> None:
    config = ExperimentConfig(
        ExperimentKind.E1_PQC_COST,
        "cli-no-output",
        0,
        SessionConfig(SessionProfile.PQC_BASE),
    )
    path = tmp_path / "configs.json"
    path.write_text(json.dumps([config.to_public_dict()]), encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        main(("batch", str(path)))
    assert exc_info.value.code == 2
    assert "requires at least one" in capsys.readouterr().err


def test_cli_reports_invalid_json_without_running_a_session(tmp_path, capsys) -> None:
    config_path = tmp_path / "invalid.json"
    config_path.write_text('{"version": 1, "version": 1}', encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        main(("run", str(config_path), "--output", str(tmp_path / "unused.json")))
    assert exc_info.value.code == 2
    assert "Duplicate JSON field" in capsys.readouterr().err
