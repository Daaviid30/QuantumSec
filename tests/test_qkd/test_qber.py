import numpy as np
import pytest

from qkd.metrics import qber


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
