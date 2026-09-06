import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.channel import ChannelPipeline, DepolarizingChannel, InterceptResendAttack
from qkd.protocols import BB84Protocol, BB84SessionStatus


def _run_with_eve(intercept_fraction: float, *, seed: int, n_signals: int):
    rng = SeededRNG(seed)
    attack = InterceptResendAttack(intercept_fraction, rng)
    result = BB84Protocol(ChannelPipeline((attack,)), rng).run(n_signals)
    return result, attack.diagnostics


@pytest.mark.parametrize("intercept_fraction", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_intercept_resend_qber_follows_the_analytical_f_over_four(intercept_fraction):
    result, diagnostics = _run_with_eve(intercept_fraction, seed=7301, n_signals=12_000)
    metrics = result.qber_by_basis
    expected_qber = intercept_fraction / 4.0

    assert metrics.qber_z is not None and metrics.qber_x is not None
    assert metrics.n_z > 2_500
    assert metrics.n_x > 2_500
    assert metrics.qber_z == pytest.approx(expected_qber, abs=0.03)
    assert metrics.qber_x == pytest.approx(expected_qber, abs=0.03)
    assert metrics.qber_aggregated == pytest.approx(expected_qber, abs=0.025)
    assert diagnostics.n_signals_seen == 12_000
    assert diagnostics.n_intercepted == pytest.approx(
        12_000 * intercept_fraction,
        abs=220,
    )


def test_zero_fraction_matches_an_attack_free_seeded_run_exactly():
    attacked, diagnostics = _run_with_eve(0.0, seed=812, n_signals=1_024)
    reference_rng = SeededRNG(812)
    reference = BB84Protocol(ChannelPipeline(()), reference_rng).run(1_024)

    assert_array_equal(attacked.alice_raw_bits, reference.alice_raw_bits)
    assert attacked.alice_bases == reference.alice_bases
    assert attacked.bob_bases == reference.bob_bases
    assert_array_equal(attacked.bob_measured_bits, reference.bob_measured_bits)
    assert_array_equal(attacked.matching_indices, reference.matching_indices)
    assert diagnostics.n_signals_seen == 1_024
    assert diagnostics.n_intercepted == 0


def test_full_interception_causes_a_security_abort_from_observed_errors():
    rng = SeededRNG(44)
    attack = InterceptResendAttack(1.0, rng)

    session = BB84Protocol(ChannelPipeline((attack,)), rng).run_session(12_000)

    assert session.status is BB84SessionStatus.ABORTED
    assert session.abort_reason is not None
    assert "phase-error" in session.abort_reason.lower()
    assert session.reconciliation is None
    assert session.n_final == 0
    assert attack.diagnostics.n_intercepted == 12_000


def test_attack_and_noise_pipeline_is_reproducible_end_to_end():
    def run(seed: int):
        rng = SeededRNG(seed)
        attack = InterceptResendAttack(0.4, rng)
        pipeline = ChannelPipeline((attack, DepolarizingChannel(p=0.08)))
        result = BB84Protocol(pipeline, rng).run(2_048)
        return result, attack.diagnostics

    first, first_diagnostics = run(991)
    second, second_diagnostics = run(991)

    assert_array_equal(first.alice_raw_bits, second.alice_raw_bits)
    assert first.alice_bases == second.alice_bases
    assert first.bob_bases == second.bob_bases
    assert_array_equal(first.bob_measured_bits, second.bob_measured_bits)
    assert first.qber_by_basis == second.qber_by_basis
    assert first_diagnostics == second_diagnostics
    assert 0.0 <= first.qber_by_basis.qber_aggregated <= 1.0
