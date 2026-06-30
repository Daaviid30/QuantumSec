#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES ================

import numpy as np
import pytest
from numpy.testing import assert_allclose

from qkd.primitives import operations, states
from quantum import validation as v

#=================== CONSTANTS ===================

ATOL = 1e-10

#===================== TESTS =====================

@pytest.mark.parametrize(
        ("psi", "expected_error", "expected"),
        [
            (states.KET0, None, True),
            (states.PLUS, None, True),
            (np.array([1, 1]), None, False),
            (np.array([]), ValueError, None),
            (np.array([[1, 0]]), ValueError, None),
            (np.array([
                [1, 1],
                [1, 2]
            ], dtype=complex), ValueError, None),
        ]
)
def test_is_normalized_state(psi, expected_error, expected):

    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_normalized_state(psi)
    else:
        assert v.is_normalized_state(psi) == expected

@pytest.mark.parametrize(
        ("psi", "expected_error", "expected"),
        [
            (states.KET0, None, True),
            (states.KET1, None, True),
            (states.PLUS, None, True),
            (states.MINUS, None, True),
            (np.array([1, 1]), None, False),
            (np.array([]), ValueError, None)
        ]
)
def test_is_quantum_state(psi, expected_error, expected):

    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_quantum_state(psi)
    else:
        assert v.is_quantum_state(psi) == expected

@pytest.mark.parametrize(
        ("U", "expected_error", "expected"),
        [
            (operations.X, None, True),
            (operations.Y, None, True),
            (operations.Z, None, True),
            (operations.H, None, True),
            (np.array([
                [1, 1],
                [1, 2]
            ], dtype=complex), None, False),
            (np.array([1, 1]), ValueError, None),
            (np.array([]), ValueError, None)
        ]
)
def test_is_unitary(U, expected_error, expected):
    if expected_error is not None:
        with pytest.raises(expected_error):
            v.is_unitary(U)
    else:
        assert v.is_unitary(U) == expected