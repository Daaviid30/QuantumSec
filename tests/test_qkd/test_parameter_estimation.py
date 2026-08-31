import numpy as np
import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import estimate_qber_from_sample


def test_parameter_estimation_is_reproducible_and_removes_disclosures():
    alice = np.arange(20, dtype=np.uint8) % 2
    bob = alice.copy()
    bob[[2, 7, 13]] ^= 1

    first = estimate_qber_from_sample(alice, bob, SeededRNG(18), sample_fraction=0.25)
    second = estimate_qber_from_sample(alice, bob, SeededRNG(18), sample_fraction=0.25)

    assert_array_equal(first.disclosed_indices, second.disclosed_indices)
    assert first.sample_size == 5
    assert np.unique(first.disclosed_indices).size == first.sample_size
    retain = np.delete(np.arange(alice.size), first.disclosed_indices)
    assert_array_equal(first.alice_candidate_key, alice[retain])
    assert_array_equal(first.bob_candidate_key, bob[retain])
    assert (
        first.estimated_qber
        == np.count_nonzero(alice[first.disclosed_indices] != bob[first.disclosed_indices])
        / first.sample_size
    )
    assert not first.disclosed_indices.flags.writeable
    assert not first.alice_candidate_key.flags.writeable


def test_parameter_estimation_explicit_sample_size_preserves_alignment():
    alice = np.array([0, 1, 1, 0, 1, 0])
    bob = np.array([1, 1, 0, 0, 1, 1])
    result = estimate_qber_from_sample(alice, bob, SeededRNG(4), sample_fraction=0.5, sample_size=2)

    assert_array_equal(result.alice_disclosed_bits, alice[result.disclosed_indices])
    assert_array_equal(result.bob_disclosed_bits, bob[result.disclosed_indices])
    assert result.n_candidate == 4


@pytest.mark.parametrize("fraction", [0.0, 1.0, -0.1, True])
def test_parameter_estimation_rejects_invalid_fraction(fraction):
    with pytest.raises(ValueError, match="sample_fraction"):
        estimate_qber_from_sample([0, 1], [0, 1], SeededRNG(1), sample_fraction=fraction)


def test_parameter_estimation_rejects_too_little_sifted_material():
    with pytest.raises(ValueError, match="at least two"):
        estimate_qber_from_sample([0], [0], SeededRNG(1))


def test_parameter_estimation_rejects_sample_that_consumes_key():
    with pytest.raises(ValueError, match="leave at least one"):
        estimate_qber_from_sample([0, 1], [0, 1], SeededRNG(1), sample_size=2)
