from collections.abc import Mapping

from experiments import ExperimentConfig, ExperimentKind
from orchestration import SessionConfig, SessionProfile


def _qkd_protocol_values(record) -> dict[str, object]:
    qkd = record.metrics["qkd"]
    assert isinstance(qkd, Mapping)
    excluded = {"simulation_time_ns"}
    return {key: value for key, value in qkd.items() if key not in excluded}


def test_same_qkd_config_and_seed_reproduce_protocol_outcome(
    experiment_runner, e3_config
) -> None:
    first = experiment_runner.run(e3_config)
    second = experiment_runner.run(e3_config)
    assert _qkd_protocol_values(first) == _qkd_protocol_values(second)
    assert first.result["status"] == second.result["status"]
    assert first.result["abort_reason"] == second.result["abort_reason"]
    assert first.run_id != second.run_id
    assert first.timestamp_utc != second.timestamp_utc


def test_pqc_reproducibility_preserves_method_not_random_artifacts(experiment_runner) -> None:
    config = ExperimentConfig(
        ExperimentKind.E1_PQC_COST,
        "pqc-method",
        0,
        SessionConfig(SessionProfile.PQC_BASE),
    )
    first = experiment_runner.run(config)
    second = experiment_runner.run(config)
    first_metrics = first.metrics["pqc"]
    second_metrics = second.metrics["pqc"]
    assert isinstance(first_metrics, Mapping) and isinstance(second_metrics, Mapping)
    assert first.profile == second.profile == "PQC-BASE"
    assert first_metrics["algorithms"] == second_metrics["algorithms"]
    assert set(first_metrics) == set(second_metrics)
    assert first.result["session_id"] != second.result["session_id"]
