from collections.abc import Mapping

from experiments import ExperimentConfig, ExperimentKind, run_batch
from orchestration import QKDProfile, SessionConfig, SessionProfile
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType


def _hybrid_config() -> ExperimentConfig:
    return ExperimentConfig(
        ExperimentKind.E5_HYBRID_OVERHEAD,
        "hybrid-base",
        0,
        SessionConfig(
            SessionProfile.HYBRID,
            qkd_authentication_profile=QKDProfile.QKD_ASSUMED,
            qkd_signal_count=512,
        ),
        seed=705,
    )


def test_e3_record_exposes_protocol_estimates_without_secret_inspection(
    experiment_runner, e3_config
) -> None:
    record = experiment_runner.run(e3_config)
    public = record.to_public_dict()
    qkd = record.metrics["qkd"]
    assert isinstance(qkd, Mapping)
    assert public["config"]["qkd_stages"][0]["intercept_fraction"] == 0.5
    assert qkd["estimated_qber_z"] is not None
    assert qkd["estimated_qber_x"] is not None
    assert qkd["estimated_qber_aggregated"] is not None
    assert qkd["phase_error_bound"] is not None
    assert qkd["n_final"] >= 0
    assert record.result["status"] in {"established", "aborted"}


def test_protocol_abort_is_a_valid_record(experiment_runner) -> None:
    config = ExperimentConfig(
        ExperimentKind.E3_INTERCEPT_RESEND,
        "eve-full",
        0,
        SessionConfig(SessionProfile.QKD_ASSUMED, qkd_signal_count=4_000),
        seed=991,
        qkd_stages=(
            QKDChannelStageSpec(
                QKDChannelStageType.INTERCEPT_RESEND,
                intercept_fraction=1.0,
            ),
        ),
    )
    record = experiment_runner.run(config)
    assert record.result["status"] == "aborted"
    assert record.result["abort_reason"]


def test_generic_runner_closes_live_session_result(monkeypatch, experiment_runner, qkd_config) -> None:
    from orchestration.runner import run_session as real_run_session

    captured = []

    def capture_result(config, context):
        result = real_run_session(config, context)
        captured.append(result)
        return result

    monkeypatch.setattr("experiments.runner.run_session", capture_result)
    record = experiment_runner.run(qkd_config)
    assert record.result["status"] == "established"
    assert len(captured) == 1 and captured[0].is_closed


def test_e1_and_e5_keep_metric_categories_separate(experiment_runner) -> None:
    pqc = experiment_runner.run(
        ExperimentConfig(
            ExperimentKind.E1_PQC_COST,
            "pqc-base",
            0,
            SessionConfig(SessionProfile.PQC_BASE),
        )
    )
    hybrid = experiment_runner.run(_hybrid_config())
    assert pqc.metrics["qkd"] is None
    assert isinstance(pqc.metrics["pqc"], Mapping)
    assert pqc.result["status"] == "established"
    assert isinstance(hybrid.metrics["qkd"], Mapping)
    assert isinstance(hybrid.metrics["pqc"], Mapping)
    assert isinstance(hybrid.metrics["hybrid"], Mapping)
    assert "quantum_safe_latency" not in hybrid.metrics
    assert hybrid.provisioning.included_in_session_timings is False


def test_batch_shuffle_is_reproducible_and_records_execution_order() -> None:
    configs = tuple(
        ExperimentConfig(
            ExperimentKind.E2_BB84_VALIDATION,
            f"condition-{index}",
            0,
            SessionConfig(SessionProfile.QKD_ASSUMED, qkd_signal_count=64),
            seed=100 + index,
        )
        for index in range(4)
    )
    first = run_batch(configs, shuffle=True, order_seed=77, warmup_runs=1)
    second = run_batch(configs, shuffle=True, order_seed=77)
    assert tuple(record.condition_id for record in first) == tuple(
        record.condition_id for record in second
    )
    assert tuple(record.execution_order_index for record in first) == (0, 1, 2, 3)
