# ================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

# =================================================

# ================= IMPORT MODULES ================

import numpy as np
import pytest

from qkd.primitives import operations, states
from quantum import validation as v

# =================== CONSTANTS ===================

ATOL = 1e-10

# ===================== TESTS =====================


@pytest.mark.parametrize(
    ("probs", "expected_error", "expected"),
    [
        (np.array([1.0, 0.0]), None, True),
        (np.array([0.25, 0.75]), None, True),
        (np.array([[0.25], [0.75]]), None, True),
        (np.array([-ATOL / 2, 1 + ATOL / 2]), None, True),
        (np.array([0.25, 0.5]), None, False),
        (np.array([-2 * ATOL, 1 + 2 * ATOL]), None, False),
        (np.array([0.5 + 0.1j, 0.5 - 0.1j]), None, False),
        (np.array([]), ValueError, None),
        (np.array([[0.5, 0.5]]), ValueError, None),
        (np.array([np.nan, 0.0]), ValueError, None),
    ],
)
def test_is_probability_state(probs, expected_error, expected):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_probability_state(probs)
    else:
        assert v.is_probability_state(probs) is expected


@pytest.mark.parametrize(
    ("probs", "expected_error"),
    [
        (np.array([0.4, 0.6]), None),
        (np.array([0.4, 0.5]), ValueError),
        (np.array([-0.1, 1.1]), ValueError),
        (np.array([0.5 + 0.1j, 0.5 - 0.1j]), ValueError),
        (np.array([]), ValueError),
    ],
)
def test_validate_probability_state(probs, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.validate_probability_state(probs)
    else:
        assert v.validate_probability_state(probs) is None


@pytest.mark.parametrize(
    ("psi", "expected_error", "expected"),
    [
        (states.KET0, None, True),
        (states.PLUS, None, True),
        (states.PHI_PLUS, None, True),
        (states.KET1.reshape(-1, 1), None, True),
        (np.array([np.sqrt(1 + ATOL / 2), 0]), None, True),
        (np.array([1, 1]), None, False),
        (np.array([np.sqrt(1 + 2 * ATOL), 0]), None, False),
        (np.array([]), ValueError, None),
        (np.array([[1, 0]]), ValueError, None),
        (np.array([[1, 1], [1, 2]], dtype=complex), ValueError, None),
        (np.array([np.inf, 0]), ValueError, None),
    ],
)
def test_is_normalized_state(psi, expected_error, expected):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_normalized_state(psi)
    else:
        assert v.is_normalized_state(psi) is expected


@pytest.mark.parametrize(
    ("psi", "expected_error"),
    [
        (states.MINUS, None),
        (np.array([1, 1]), ValueError),
        (np.array([]), ValueError),
        (np.array([[1, 0]]), ValueError),
    ],
)
def test_validate_normalized_state(psi, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.validate_normalized_state(psi)
    else:
        assert v.validate_normalized_state(psi) is None


@pytest.mark.parametrize(
    ("psi", "tol", "expected_error", "expected"),
    [
        (states.KET0, ATOL, None, True),
        (states.KET1, ATOL, None, True),
        (states.PLUS, ATOL, None, True),
        (states.MINUS, ATOL, None, True),
        (np.array([1, 1]), ATOL, None, False),
        (np.array([np.sqrt(1 + 5e-8), 0]), 1e-7, None, True),
        (np.array([np.sqrt(1 + 5e-8), 0]), 1e-9, None, False),
        (np.array([]), ATOL, ValueError, None),
        (np.array([[1, 0]]), ATOL, ValueError, None),
    ],
)
def test_is_quantum_state(psi, tol, expected_error, expected):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_quantum_state(psi, tol=tol)
    else:
        assert v.is_quantum_state(psi, tol=tol) is expected


@pytest.mark.parametrize(
    ("psi", "tol", "expected_error"),
    [
        (states.PLUS, ATOL, None),
        (np.array([np.sqrt(1 + 5e-8), 0]), 1e-7, None),
        (np.array([np.sqrt(1 + 5e-8), 0]), 1e-9, ValueError),
        (np.array([1, 1]), ATOL, ValueError),
        (np.array([]), ATOL, ValueError),
    ],
)
def test_validate_quantum_state(psi, tol, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.validate_quantum_state(psi, tol=tol)
    else:
        assert v.validate_quantum_state(psi, tol=tol) is None


@pytest.mark.parametrize(
    ("unitary", "expected_error", "expected"),
    [
        (operations.X, None, True),
        (operations.Y, None, True),
        (operations.Z, None, True),
        (operations.H, None, True),
        (np.identity(4), None, True),
        (np.array([[np.sqrt(1 + ATOL / 2), 0], [0, 1]]), None, True),
        (np.array([[1, 1], [1, 2]], dtype=complex), None, False),
        (np.array([[np.sqrt(1 + 2 * ATOL), 0], [0, 1]]), None, False),
        (np.array([1, 1]), None, False),
        (np.array([]), None, False),
        (np.ones((2, 3)), None, False),
        (np.array([[1, 0], [0, np.inf]]), None, False),
    ],
)
def test_is_unitary(unitary, expected_error, expected):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_unitary(unitary)
    else:
        assert v.is_unitary(unitary) is expected


@pytest.mark.parametrize(
    ("unitary", "expected_error"),
    [
        (operations.H, None),
        (np.identity(1), None),
        (np.array([[1, 1], [1, 2]], dtype=complex), ValueError),
        (np.ones((2, 3)), ValueError),
        (np.array([]), ValueError),
        (np.array([[np.nan]]), ValueError),
    ],
)
def test_validate_unitary(unitary, expected_error):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.validate_unitary(unitary)
    else:
        assert v.validate_unitary(unitary) is None
