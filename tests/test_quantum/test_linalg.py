# ================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

# =================================================

# ================= IMPORT MODULES ================

import numpy as np
import pytest
from numpy.testing import assert_allclose

from qkd.primitives import states
from quantum import linalg

# =================== CONSTANTS ===================

ATOL = 1e-10

# ===================== TESTS =====================


@pytest.mark.parametrize(
    ("psi", "expected"),
    [
        (np.array([1, 0]), np.array([1, 0], dtype=complex)),
        (np.array([[1], [0]]), np.array([1, 0], dtype=complex)),
        (np.array([[1]]), np.array([1], dtype=complex)),
        ([1 / np.sqrt(2), 1j / np.sqrt(2)], np.array([1, 1j]) / np.sqrt(2)),
    ],
)
def test_as_ket_returns_canonical_complex_vector(psi, expected):
    result = linalg.as_ket(psi)

    assert result.ndim == 1
    assert np.issubdtype(result.dtype, np.complexfloating)
    assert_allclose(result, expected, atol=ATOL)


@pytest.mark.parametrize(
    "psi",
    [
        np.array([]),
        np.empty((0, 1)),
        np.array([[1, 0]]),
        np.identity(2),
        np.array(1),
        np.ones((2, 1, 1)),
        np.array([np.nan, 0]),
        np.array([np.inf, 0]),
    ],
)
def test_as_ket_rejects_invalid_inputs(psi):
    with pytest.raises(ValueError):
        linalg.as_ket(psi)


@pytest.mark.parametrize(
    ("phi", "psi", "expected"),
    [
        (states.KET0, states.KET0, 1 + 0j),
        (states.KET0, states.KET1, 0 + 0j),
        (states.PLUS, states.MINUS, 0 + 0j),
        (np.array([1j, 0]), np.array([1, 0]), -1j),
        (states.KET1.reshape(-1, 1), states.KET1, 1 + 0j),
    ],
)
def test_inner_product(phi, psi, expected):
    assert_allclose(linalg.inner_product(phi, psi), expected, atol=ATOL)


@pytest.mark.parametrize(
    ("phi", "psi"),
    [
        (np.array([1]), np.array([1, 0])),
        (np.array([[1, 0]]), states.KET0),
        (states.KET0, np.array([])),
        (np.array([np.nan, 0]), states.KET0),
    ],
)
def test_inner_product_rejects_invalid_or_different_sized_kets(phi, psi):
    with pytest.raises(ValueError):
        linalg.inner_product(phi, psi)


@pytest.mark.parametrize(
    ("phi", "psi", "expected"),
    [
        (states.KET0, states.KET1, np.array([[0, 1], [0, 0]])),
        (states.KET1, states.KET0, np.array([[0, 0], [1, 0]])),
        (np.array([1j, 0]), states.KET0, np.array([[1j, 0], [0, 0]])),
        (
            states.PLUS.reshape(-1, 1),
            states.PLUS,
            np.full((2, 2), 0.5),
        ),
    ],
)
def test_outer_product(phi, psi, expected):
    assert_allclose(linalg.outer_product(phi, psi), expected, atol=ATOL)


@pytest.mark.parametrize(
    ("phi", "psi"),
    [
        (np.array([1]), np.array([1, 0])),
        (np.identity(2), states.KET0),
        (states.KET0, np.array([])),
        (states.KET0, np.array([0, np.inf])),
    ],
)
def test_outer_product_rejects_invalid_or_different_sized_kets(phi, psi):
    with pytest.raises(ValueError):
        linalg.outer_product(phi, psi)


@pytest.mark.parametrize(
    ("psi", "expected"),
    [
        (np.array([3, 4]), np.array([0.6, 0.8])),
        (np.array([1j, 1]), np.array([1j, 1]) / np.sqrt(2)),
        (np.array([[0], [-5]]), np.array([0, -1])),
        (np.array([2 * ATOL, 0]), states.KET0),
    ],
)
def test_normalize(psi, expected):
    result = linalg.normalize(psi)

    assert result.ndim == 1
    assert_allclose(result, expected, atol=ATOL)
    assert_allclose(np.linalg.norm(result), 1, atol=ATOL)


@pytest.mark.parametrize(
    "psi",
    [
        np.array([0, 0]),
        np.array([ATOL / 2, 0]),
        np.array([ATOL, 0]),
        np.array([]),
        np.array([[1, 0]]),
        np.array([np.inf, 0]),
    ],
)
def test_normalize_rejects_zero_norm_and_invalid_kets(psi):
    with pytest.raises(ValueError):
        linalg.normalize(psi)


@pytest.mark.parametrize(
    ("psi", "expected"),
    [
        (states.KET0, np.array([1.0, 0.0])),
        (states.PLUS, np.array([0.5, 0.5])),
        (np.array([1, 1j]) / np.sqrt(2), np.array([0.5, 0.5])),
        (states.MINUS.reshape(-1, 1), np.array([0.5, 0.5])),
    ],
)
def test_probabilities_from_ket(psi, expected):
    result = linalg.probabilities_from_ket(psi)

    assert np.all(np.isreal(result))
    assert_allclose(result, expected, atol=ATOL)


def test_probabilities_from_ket_honors_custom_tolerance():
    psi = np.array([np.sqrt(1 + 5e-8), 0])

    assert_allclose(
        linalg.probabilities_from_ket(psi, tol=1e-7),
        np.array([1 + 5e-8, 0]),
        atol=ATOL,
    )
    with pytest.raises(ValueError):
        linalg.probabilities_from_ket(psi, tol=1e-9)


@pytest.mark.parametrize(
    "psi",
    [
        np.array([1, 1]),
        np.array([0, 0]),
        np.array([]),
        np.array([[1, 0]]),
        np.array([np.nan, 0]),
    ],
)
def test_probabilities_from_ket_rejects_invalid_quantum_states(psi):
    with pytest.raises(ValueError):
        linalg.probabilities_from_ket(psi)
