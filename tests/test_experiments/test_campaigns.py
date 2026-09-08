import math

import pytest

from experiments.campaigns.theory import analytical_qber
from experiments.campaigns.thesis_v1 import CampaignPreset, build_campaign_plan, seed_for
from experiments.config import ExperimentKind
from orchestration.pqc.instrumentation import PQCOperationTimer
from orchestration.profiles import QKDProfile, SessionProfile
from pqc.protocol.instrumentation import PQCOperation
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType


@pytest.mark.parametrize(
    ("stage", "expected"),
    [
        (QKDChannelStageSpec(QKDChannelStageType.IDENTITY), (0.0, 0.0)),
        (QKDChannelStageSpec(QKDChannelStageType.DEPOLARIZING, p=0.2), (0.1, 0.1)),
        (QKDChannelStageSpec(QKDChannelStageType.BIT_FLIP, p=0.2), (0.2, 0.0)),
        (QKDChannelStageSpec(QKDChannelStageType.PHASE_FLIP, p=0.16), (0.0, 0.16)),
        (QKDChannelStageSpec(QKDChannelStageType.PAULI, px=0.08, py=0.01, pz=0.02), (0.09, 0.03)),
        (
            QKDChannelStageSpec(QKDChannelStageType.AMPLITUDE_DAMPING, gamma=0.2),
            (0.1, (1 - math.sqrt(0.8)) / 2),
        ),
    ],
)
def test_e2_theory_matches_implemented_channel_conventions(stage, expected) -> None:
    theory = analytical_qber(stage)
    assert theory.qber_z == pytest.approx(expected[0])
    assert theory.qber_x == pytest.approx(expected[1])
    assert theory.qber_aggregate == pytest.approx(sum(expected) / 2)


def test_thesis_plan_locks_complete_matrix_and_controls() -> None:
    plan = build_campaign_plan(CampaignPreset.THESIS)
    assert plan.expected_record_counts == {"e1": 100, "e2": 250, "e3": 550, "e4": 90, "e5": 120, "d1": 1}
    assert len(plan.e1_warmups) == 10
    assert len(plan.e5_warmups) == 12
    assert len({config.condition_id for config in plan.e2}) == 25
    assert len({config.condition_id for config in plan.e3}) == 11
    assert all(config.session_config.qkd_signal_count == 20_000 for config in plan.e2)
    assert all(config.session_config.qkd_signal_count == 10_000 for config in plan.e3)
    e4_by_replicate: dict[int, set[int | None]] = {}
    for config in plan.e4:
        e4_by_replicate.setdefault(config.replicate_index, set()).add(config.seed)
    assert all(len(seeds) == 1 for seeds in e4_by_replicate.values())
    hybrid = [
        config
        for config in plan.e5
        if config.profile in {SessionProfile.HYBRID, SessionProfile.HYBRID_DIVERSE}
    ]
    assert all(config.session_config.qkd_signal_count == 4_096 for config in hybrid)
    assert all(
        config.session_config.qkd_authentication_profile is QKDProfile.QKD_PQC_AUTH for config in hybrid
    )


def test_seed_mapping_is_stable_unique_and_domain_separated() -> None:
    assert seed_for(ExperimentKind.E3_INTERCEPT_RESEND, 2, 7) == seed_for(
        ExperimentKind.E3_INTERCEPT_RESEND, 2, 7
    )
    values = {
        seed_for(kind, condition, replicate)
        for kind in (ExperimentKind.E2_BB84_VALIDATION, ExperimentKind.E3_INTERCEPT_RESEND)
        for condition in range(3)
        for replicate in range(4)
    }
    assert len(values) == 24
    assert all(0 <= value < 2**64 for value in values)


def test_e1_operation_timer_accumulates_only_direct_observations() -> None:
    timer = PQCOperationTimer(hqc_enabled=True)
    for index, operation in enumerate(PQCOperation, start=1):
        timer.observe(operation, index)
        timer.observe(operation, index * 2)
    snapshot = timer.snapshot()
    for index, operation in enumerate(PQCOperation, start=1):
        assert getattr(snapshot, operation.value) == index * 3
    base = PQCOperationTimer(hqc_enabled=False).snapshot()
    assert base.hqc_keygen_time_ns is None
    assert base.hqc_encapsulate_time_ns is None
    assert base.hqc_decapsulate_time_ns is None
