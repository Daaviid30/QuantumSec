import csv
import io
import json

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
