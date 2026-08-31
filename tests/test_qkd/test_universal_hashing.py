import numpy as np
import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import generate_toeplitz_seed, toeplitz_hash


def _dense_reference(bits: np.ndarray, output_length: int, seed: np.ndarray) -> np.ndarray:
    n = bits.size
    matrix = np.fromfunction(
        lambda i, j: seed[(n - 1 + i - j).astype(np.intp)],
        (output_length, n),
        dtype=int,
    ).astype(np.uint8)
    return np.asarray((matrix @ bits) % 2, dtype=np.uint8)


def test_fft_toeplitz_hash_matches_dense_reference_for_small_random_cases():
    rng = SeededRNG(91)
    for n in range(1, 25):
        for m in range(1, n + 1):
            bits = np.asarray(rng.gen.integers(0, 2, size=n), dtype=np.uint8)
            seed = generate_toeplitz_seed(n, m, rng)
            assert_array_equal(toeplitz_hash(bits, m, seed), _dense_reference(bits, m, seed))


def test_toeplitz_seed_and_hash_are_reproducible_binary_and_immutable():
    first_seed = generate_toeplitz_seed(20, 7, SeededRNG(5))
    second_seed = generate_toeplitz_seed(20, 7, SeededRNG(5))
    bits = np.arange(20, dtype=np.uint8) % 2
    first = toeplitz_hash(bits, 7, first_seed)
    second = toeplitz_hash(bits, 7, second_seed)

    assert_array_equal(first_seed, second_seed)
    assert_array_equal(first, second)
    assert first.shape == (7,)
    assert set(first.tolist()) <= {0, 1}
    assert not first.flags.writeable


def test_toeplitz_zero_output_is_explicit_and_seedless():
    result = toeplitz_hash([0, 1, 0], 0, [])
    assert result.shape == (0,)
    assert not result.flags.writeable


def test_toeplitz_hash_handles_supported_large_inputs_without_a_dense_matrix():
    bits = np.zeros(100_000, dtype=np.uint8)
    seed = np.ones(149_999, dtype=np.uint8)
    result = toeplitz_hash(bits, 50_000, seed)

    assert result.shape == (50_000,)
    assert np.count_nonzero(result) == 0


@pytest.mark.parametrize("seed", [[0], [0, 1, 0]])
def test_toeplitz_rejects_wrong_seed_length(seed):
    with pytest.raises(ValueError, match="exactly"):
        toeplitz_hash([0, 1], 1, seed)
