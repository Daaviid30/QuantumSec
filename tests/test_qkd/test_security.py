import pytest

from qkd.metrics import asymptotic_bb84_secret_length, binary_entropy


def test_binary_entropy_known_values_and_symmetry():
    assert binary_entropy(0.0) == 0.0
    assert binary_entropy(1.0) == 0.0
    assert binary_entropy(0.5) == 1.0
    assert binary_entropy(0.17) == pytest.approx(binary_entropy(0.83))


def test_secret_length_subtracts_actual_leakage_exactly_once():
    baseline = asymptotic_bb84_secret_length(100, 0.0, 0, 0)
    leaked = asymptotic_bb84_secret_length(100, 0.0, 17, 8)
    assert baseline == 100
    assert leaked == 75


def test_secret_length_clamps_non_positive_result_to_zero():
    assert asymptotic_bb84_secret_length(100, 0.5, 1, 1) == 0


@pytest.mark.parametrize("probability", [-0.1, 1.1, float("nan"), True])
def test_binary_entropy_rejects_invalid_probabilities(probability):
    with pytest.raises(ValueError):
        binary_entropy(probability)
