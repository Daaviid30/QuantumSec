import numpy as np
import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import CascadeConfig, reconcile_cascade


def test_cascade_identical_keys_remain_identical_and_disclose_parities():
    key = np.arange(64, dtype=np.uint8) % 2
    result = reconcile_cascade(key, key, 0.0, SeededRNG(2))

    assert_array_equal(result.bob_corrected_key, key)
    assert result.corrected_errors == 0
    assert result.residual_mismatch_count == 0
    assert result.leak_ec == 4
    assert not result.bob_corrected_key.flags.writeable


def test_cascade_locates_single_error_through_parity_binary_search():
    alice = np.zeros(32, dtype=np.uint8)
    bob = alice.copy()
    bob[19] = 1
    result = reconcile_cascade(
        alice,
        bob,
        1 / 32,
        SeededRNG(8),
        config=CascadeConfig(passes=3),
    )

    assert_array_equal(result.bob_corrected_key, alice)
    assert result.corrected_errors == 1
    assert result.leak_ec > result.passes


def test_cascade_corrects_sparse_errors_with_permutation_lookback():
    alice = np.zeros(64, dtype=np.uint8)
    bob = alice.copy()
    bob[[3, 11, 29, 44]] = 1
    result = reconcile_cascade(alice, bob, 4 / 64, SeededRNG(7))

    assert_array_equal(result.bob_corrected_key, alice)
    assert result.corrected_errors == 4
    assert result.residual_mismatch_count == 0
    assert sum(item.corrected_errors for item in result.pass_statistics) == 4


def test_cascade_permutations_and_leakage_are_reproducible():
    alice = np.zeros(96, dtype=np.uint8)
    bob = alice.copy()
    bob[[5, 21, 65]] = 1
    first = reconcile_cascade(alice, bob, 0.04, SeededRNG(27))
    second = reconcile_cascade(alice, bob, 0.04, SeededRNG(27))

    assert first.leak_ec == second.leak_ec
    assert first.corrected_errors == second.corrected_errors
    for first_pass, second_pass in zip(first.pass_statistics, second.pass_statistics, strict=True):
        assert_array_equal(first_pass.permutation, second_pass.permutation)


@pytest.mark.parametrize(
    ("alice", "bob", "qber"),
    [([0], [0, 1], 0.1), ([0, 2], [0, 1], 0.1), ([0, 1], [0, 1], -0.1)],
)
def test_cascade_rejects_invalid_inputs(alice, bob, qber):
    with pytest.raises(ValueError):
        reconcile_cascade(alice, bob, qber, SeededRNG(1))
