import numpy as np
import pytest

from core.constants import DEFAULT_ATOL
from qkd.primitives.states import KET0, KET1, PLUS
from quantum import information
from quantum.states import dm_from_ket


@pytest.mark.parametrize(
    ("rho", "expected"),
    [
        (dm_from_ket(PLUS), 1.0),
        (np.identity(2) / 2.0, 0.5),
        (np.identity(4) / 4.0, 0.25),
    ],
)
def test_purity_analytical_cases(rho, expected):
    assert information.purity(rho) == pytest.approx(expected, abs=DEFAULT_ATOL)


def test_trace_distance_equal_orthogonal_and_symmetric_cases():
    rho = dm_from_ket(KET0)
    sigma = dm_from_ket(KET1)
    mixed = np.identity(2) / 2.0

    assert information.trace_distance(rho, rho) == pytest.approx(0.0, abs=DEFAULT_ATOL)
    assert information.trace_distance(rho, sigma) == pytest.approx(1.0, abs=DEFAULT_ATOL)
    assert information.trace_distance(rho, mixed) == pytest.approx(
        information.trace_distance(mixed, rho), abs=DEFAULT_ATOL
    )


def test_fidelity_equal_orthogonal_symmetric_and_pure_overlap_cases():
    zero = dm_from_ket(KET0)
    one = dm_from_ket(KET1)
    plus = dm_from_ket(PLUS)

    assert information.fidelity(zero, zero) == pytest.approx(1.0, abs=DEFAULT_ATOL)
    assert information.fidelity(zero, one) == pytest.approx(0.0, abs=DEFAULT_ATOL)
    assert information.fidelity(zero, plus) == pytest.approx(0.5, abs=DEFAULT_ATOL)
    assert information.fidelity(zero, plus) == pytest.approx(
        information.fidelity(plus, zero), abs=DEFAULT_ATOL
    )


@pytest.mark.parametrize(
    ("rho", "expected"),
    [
        (dm_from_ket(KET0), 0.0),
        (np.identity(2) / 2.0, 1.0),
        (np.identity(4) / 4.0, 2.0),
    ],
)
def test_von_neumann_entropy_analytical_cases(rho, expected):
    assert information.von_neumann_entropy(rho) == pytest.approx(expected, abs=DEFAULT_ATOL)


@pytest.mark.parametrize("metric", [information.trace_distance, information.fidelity])
def test_pair_metrics_require_equal_shapes(metric):
    with pytest.raises(ValueError, match="same shape"):
        metric(np.identity(2) / 2.0, np.identity(3) / 3.0)


def test_entropy_rejects_significant_negativity_without_full_validation():
    with pytest.raises(ValueError, match="significant negativity"):
        information.von_neumann_entropy(
            np.diag([1.1, -0.1]),
            validate_state=False,
        )


def test_fidelity_psd_square_root_rejects_significant_negativity():
    with pytest.raises(ValueError, match="significant negativity"):
        information.fidelity(
            np.diag([1.1, -0.1]),
            np.identity(2) / 2.0,
            validate_state=False,
        )
