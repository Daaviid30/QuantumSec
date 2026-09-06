import numpy as np
import pytest

from qkd.metrics import qber, qber_by_basis
from qkd.primitives import Basis


@pytest.mark.parametrize(
    ("alice_key", "bob_key", "expected"),
    [
        (np.array([0, 1, 1, 0]), np.array([0, 1, 1, 0]), 0.0),
        (np.array([0, 1, 1, 0]), np.array([1, 0, 0, 1]), 1.0),
        (np.array([0, 0, 1, 1]), np.array([0, 1, 1, 0]), 0.5),
        (np.array([0, 0, 0]), np.array([0, 0, 1]), 1 / 3),
    ],
)
def test_qber_matches_analytical_bit_error_fraction(alice_key, bob_key, expected):
    assert qber(alice_key, bob_key) == expected


def test_qber_rejects_unequal_key_lengths():
    with pytest.raises(ValueError, match="equal lengths"):
        qber(np.array([0, 1]), np.array([0]))


@pytest.mark.parametrize(
    ("alice_key", "bob_key", "message"),
    [
        (np.array([[0, 1]]), np.array([0, 1]), "one-dimensional"),
        (np.array([0, 1]), np.array([[0, 1]]), "one-dimensional"),
        (np.array([0, 2]), np.array([0, 1]), "only 0 and 1"),
        (np.array([0, 1]), np.array([-1, 1]), "only 0 and 1"),
        (np.array([0.0, 1.0]), np.array([0, 1]), "integer bits"),
    ],
)
def test_qber_rejects_non_binary_or_non_vector_inputs(alice_key, bob_key, message):
    with pytest.raises(ValueError, match=message):
        qber(alice_key, bob_key)


def test_qber_is_explicitly_undefined_for_empty_keys():
    empty = np.array([], dtype=int)

    with pytest.raises(ValueError, match="undefined"):
        qber(empty, empty)


def test_qber_by_basis_preserves_asymmetric_errors_and_weighted_aggregate():
    alice = np.zeros(8, dtype=np.uint8)
    bob = np.array([1, 0, 0, 0, 1, 1, 0, 0], dtype=np.uint8)
    bases = (Basis.Z, Basis.Z, Basis.Z, Basis.Z, Basis.X, Basis.X, Basis.X, Basis.X)

    result = qber_by_basis(alice, bob, bases)

    assert result.qber_z == 0.25
    assert result.qber_x == 0.5
    assert result.qber_aggregated == 0.375
    assert result.n_z == result.n_x == 4


def test_qber_by_basis_marks_an_absent_basis_as_undefined():
    result = qber_by_basis([0, 1], [0, 0], (Basis.Z, Basis.Z))

    assert result.qber_z == 0.5
    assert result.qber_x is None
    assert result.qber_aggregated == 0.5


@pytest.mark.parametrize(
    ("alice", "bob", "bases"),
    [
        ([0, 1], [0, 1], (Basis.Z,)),
        ([0, 1], [0, 1], (Basis.Z, Basis.Y)),
        ([], [], ()),
    ],
)
def test_qber_by_basis_rejects_missing_alignment_non_bb84_bases_and_empty_data(alice, bob, bases):
    with pytest.raises(ValueError):
        qber_by_basis(alice, bob, bases)
