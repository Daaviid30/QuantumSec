import inspect

import numpy as np
import pytest
from numpy.testing import assert_allclose

from core.rng import SeededRNG
from qkd.channel import DepolarizingChannel, InterceptResendAttack
from qkd.primitives.states import KET0, PLUS
from quantum.states import dm_from_ket
from quantum.validation import validate_density_matrix


@pytest.mark.parametrize("fraction", [-0.01, 1.01, float("nan"), True])
def test_intercept_resend_rejects_invalid_fraction(fraction):
    with pytest.raises(ValueError, match="intercept_fraction"):
        InterceptResendAttack(fraction, SeededRNG(1))


def test_intercept_resend_requires_an_injected_rng():
    with pytest.raises(TypeError, match="BaseRNG"):
        InterceptResendAttack(0.5, object())  # pyright: ignore[reportArgumentType]


def test_zero_fraction_is_an_exact_passthrough_without_consuming_rng():
    attack_rng = SeededRNG(91)
    untouched_rng = SeededRNG(91)
    attack = InterceptResendAttack(0.0, attack_rng)
    rho = dm_from_ket(PLUS)

    output = attack.apply(rho)

    assert_allclose(output, rho, atol=0.0, rtol=0.0)
    assert not np.shares_memory(output, rho)
    assert attack_rng.gen.random() == untouched_rng.gen.random()
    assert attack.diagnostics.n_signals_seen == 1
    assert attack.diagnostics.n_intercepted == 0


def test_full_interception_resends_a_valid_bb84_state_and_counts_observations():
    attack = InterceptResendAttack(1.0, SeededRNG(7))

    outputs = [attack.apply(dm_from_ket(KET0)) for _ in range(40)]

    for output in outputs:
        validate_density_matrix(output)
    diagnostics = attack.diagnostics
    assert diagnostics.attack_type == "intercept_resend"
    assert diagnostics.n_signals_seen == diagnostics.n_intercepted == 40
    assert diagnostics.eve_z_measurements + diagnostics.eve_x_measurements == 40
    assert diagnostics.eve_zero_outcomes + diagnostics.eve_one_outcomes == 40


def test_intercept_resend_is_reproducible_with_the_same_seed():
    first = InterceptResendAttack(0.63, SeededRNG(2026))
    second = InterceptResendAttack(0.63, SeededRNG(2026))
    inputs = [dm_from_ket(KET0), dm_from_ket(PLUS)] * 50

    first_outputs = [first.apply(rho) for rho in inputs]
    second_outputs = [second.apply(rho) for rho in inputs]

    for first_output, second_output in zip(first_outputs, second_outputs, strict=True):
        assert_allclose(first_output, second_output, atol=0.0, rtol=0.0)
    assert first.diagnostics == second.diagnostics


def test_attack_contract_exposes_only_the_quantum_state_and_validation_flag():
    parameters = inspect.signature(InterceptResendAttack.apply).parameters

    assert tuple(parameters) == ("self", "rho", "validate_state")


def test_bb84_has_no_attack_specific_dependency():
    import qkd.protocols.bb84 as bb84_module

    source = inspect.getsource(bb84_module)

    assert "InterceptResend" not in source
    assert "channel.attacks" not in source


def test_intercept_resend_composes_in_pipeline_order():
    from qkd.channel import ChannelPipeline

    rho = dm_from_ket(PLUS)
    pipeline_attack = InterceptResendAttack(1.0, SeededRNG(121))
    manual_attack = InterceptResendAttack(1.0, SeededRNG(121))
    noise = DepolarizingChannel(p=0.18)

    actual = ChannelPipeline((pipeline_attack, noise)).apply(rho)
    expected = noise.apply(manual_attack.apply(rho), validate_state=False)

    assert_allclose(actual, expected, atol=0.0, rtol=0.0)
    assert pipeline_attack.diagnostics == manual_attack.diagnostics
