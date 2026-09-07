import pytest

from experiments import ExperimentConfig, ExperimentKind, ExperimentRunner, ExperimentRuntimeFactory
from orchestration import SessionConfig, SessionProfile
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType


@pytest.fixture(scope="session")
def experiment_runner() -> ExperimentRunner:
    return ExperimentRunner(ExperimentRuntimeFactory())


@pytest.fixture
def qkd_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_kind=ExperimentKind.E2_BB84_VALIDATION,
        condition_id="identity",
        replicate_index=0,
        session_config=SessionConfig(SessionProfile.QKD_ASSUMED, qkd_signal_count=512),
        seed=2026,
    )


@pytest.fixture
def e3_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_kind=ExperimentKind.E3_INTERCEPT_RESEND,
        condition_id="eve-f-0.50",
        replicate_index=0,
        session_config=SessionConfig(SessionProfile.QKD_ASSUMED, qkd_signal_count=4_000),
        seed=202603,
        qkd_stages=(
            QKDChannelStageSpec(
                QKDChannelStageType.INTERCEPT_RESEND,
                intercept_fraction=0.5,
            ),
        ),
    )
