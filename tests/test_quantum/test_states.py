# ================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

# =================================================

# ================= IMPORT MODULES ================

import numpy as np
import pytest
from numpy.testing import assert_allclose

from core.constants import DEFAULT_ATOL
from qkd.primitives import states as primitive_states
from quantum import states

# =================== CONSTANTS ===================

ATOL = DEFAULT_ATOL

# ===================== TESTS =====================


@pytest.mark.parametrize(
    ("psi", "expected"),
    [
        (primitive_states.KET0, np.array([[1, 0], [0, 0]])),
        (primitive_states.KET1.reshape(-1, 1), np.array([[0, 0], [0, 1]])),
        (primitive_states.PLUS, np.full((2, 2), 0.5)),
        (
            np.array([1, 1j, 0]) / np.sqrt(2),
            np.array([[0.5, -0.5j, 0], [0.5j, 0.5, 0], [0, 0, 0]]),
        ),
    ],
)
def test_dm_from_ket(psi, expected):
    density = states.dm_from_ket(psi)

    assert_allclose(density, expected, atol=ATOL)
    assert_allclose(density, density.conj().T, atol=ATOL)
    assert_allclose(np.trace(density), 1, atol=ATOL)


def test_dm_from_ket_is_invariant_under_global_phase():
    psi = primitive_states.PLUS

    assert_allclose(states.dm_from_ket(1j * psi), states.dm_from_ket(psi), atol=ATOL)


@pytest.mark.parametrize(
    "psi",
    [
        np.array([1, 1]),
        np.array([]),
        np.array([[1, 0]]),
        np.identity(2),
        np.array([np.nan, 0]),
    ],
)
def test_dm_from_ket_rejects_invalid_quantum_states(psi):
    with pytest.raises(ValueError):
        states.dm_from_ket(psi)


@pytest.mark.parametrize(
    ("ensemble", "probs", "expected"),
    [
        (
            [primitive_states.KET0, primitive_states.KET1],
            np.array([0.25, 0.75]),
            np.diag([0.25, 0.75]),
        ),
        (
            (primitive_states.PLUS, primitive_states.MINUS),
            np.array([[0.5], [0.5]]),
            np.identity(2) / 2,
        ),
        (
            [np.array([1, 0, 0])],
            np.array([1.0]),
            np.diag([1.0, 0.0, 0.0]),
        ),
    ],
)
def test_dm_from_ensemble(ensemble, probs, expected):
    density = states.dm_from_ensemble(ensemble, probs)

    assert_allclose(density, expected, atol=ATOL)
    assert_allclose(density, density.conj().T, atol=ATOL)
    assert_allclose(np.trace(density), 1, atol=ATOL)


@pytest.mark.parametrize(
    ("ensemble", "probs"),
    [
        ([primitive_states.KET0], np.array([0.5, 0.5])),
        ([], np.array([1.0])),
        ([primitive_states.KET0, primitive_states.KET1], np.array([0.4, 0.4])),
        ([primitive_states.KET0, primitive_states.KET1], np.array([-0.1, 1.1])),
        ([primitive_states.KET0, primitive_states.KET1], np.array([0.5 + 0.1j, 0.5 - 0.1j])),
        ([np.array([1, 1])], np.array([1.0])),
        ([primitive_states.KET0, np.array([1, 0, 0])], np.array([0.5, 0.5])),
        ([primitive_states.KET0], np.array([])),
    ],
)
def test_dm_from_ensemble_rejects_invalid_inputs(ensemble, probs):
    with pytest.raises(ValueError):
        states.dm_from_ensemble(ensemble, probs)
