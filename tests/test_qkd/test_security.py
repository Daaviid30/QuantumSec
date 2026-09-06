import pytest

from qkd.metrics import asymptotic_bb84_secret_length, binary_entropy


def test_binary_entropy_known_values_and_symmetry():
    assert binary_entropy(0.0) == 0.0
    assert binary_entropy(1.0) == 0.0
    assert binary_entropy(0.5) == 1.0
    assert binary_entropy(0.17) == pytest.approx(binary_entropy(0.83))


def test_secret_length_subtracts_actual_leakage_exactly_once():
    baseline = asymptotic_bb84_secret_length(
        100,
        phase_error_bound=0.0,
        reconciliation_leakage=0,
        verification_leakage=0,
    )
    leaked = asymptotic_bb84_secret_length(
        100,
        phase_error_bound=0.0,
        reconciliation_leakage=17,
        verification_leakage=8,
    )
    assert baseline == 100
    assert leaked == 75


def test_secret_length_returns_zero_when_explicit_phase_bound_cannot_justify_material():
    assert (
        asymptotic_bb84_secret_length(
            100,
            phase_error_bound=0.5,
            reconciliation_leakage=1,
            verification_leakage=1,
        )
        == 0
    )


def test_asymmetric_phase_bound_prevents_aggregate_qber_overextraction():
    optimistic_aggregate = asymptotic_bb84_secret_length(
        1_000,
        phase_error_bound=0.08,
        reconciliation_leakage=500,
        verification_leakage=16,
    )
    justified_per_basis = asymptotic_bb84_secret_length(
        1_000,
        phase_error_bound=0.16,
        reconciliation_leakage=500,
        verification_leakage=16,
    )

    assert optimistic_aggregate > 0
    assert justified_per_basis == 0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"candidate_length": -1}, "candidate_length"),
        ({"phase_error_bound": float("nan")}, "phase_error_bound"),
        ({"phase_error_bound": 0.51}, r"\[0, 0.5\]"),
        ({"reconciliation_leakage": -1}, "reconciliation_leakage"),
        ({"verification_leakage": -1}, "verification_leakage"),
    ],
)
def test_secret_length_rejects_invalid_security_inputs(kwargs, message):
    arguments = {
        "candidate_length": 100,
        "phase_error_bound": 0.1,
        "reconciliation_leakage": 5,
        "verification_leakage": 5,
    }
    arguments.update(kwargs)

    with pytest.raises(ValueError, match=message):
        asymptotic_bb84_secret_length(**arguments)


@pytest.mark.parametrize("probability", [-0.1, 1.1, float("nan"), True])
def test_binary_entropy_rejects_invalid_probabilities(probability):
    with pytest.raises(ValueError):
        binary_entropy(probability)
