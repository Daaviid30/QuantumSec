"""Efficient binary Toeplitz universal hashing for QKD post-processing."""

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG
from qkd.postprocessing._validation import copy_binary_vector, validate_non_negative_int


def toeplitz_seed_length(input_length: int, output_length: int) -> int:
    """Return the public seed length for an ``output_length x input_length`` matrix."""

    n = validate_non_negative_int(input_length, name="input_length")
    m = validate_non_negative_int(output_length, name="output_length")
    if m > n:
        raise ValueError(f"output_length cannot exceed input_length. Got {m} > {n}.")
    if n == 0 or m == 0:
        return 0
    return m + n - 1


def generate_toeplitz_seed(input_length: int, output_length: int, rng: BaseRNG) -> npt.NDArray[np.uint8]:
    """Generate the public Toeplitz diagonal seed through the injected RNG."""

    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    length = toeplitz_seed_length(input_length, output_length)
    seed = np.asarray(rng.gen.integers(0, 2, size=length), dtype=np.uint8)
    seed.flags.writeable = False
    return seed


def toeplitz_hash(
    bits: npt.ArrayLike,
    output_length: int,
    seed: npt.ArrayLike,
) -> npt.NDArray[np.uint8]:
    """Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution.

    For input length ``n`` and output length ``m``, seed index
    ``n - 1 + i - j`` defines matrix element ``T[i, j]``. Consequently the
    desired product is the ``[n-1:n-1+m]`` slice of ``convolve(seed, bits)``.
    The implementation never materializes the dense ``m x n`` matrix.
    """

    vector = copy_binary_vector(bits, name="bits")
    m = validate_non_negative_int(output_length, name="output_length")
    if m > vector.size:
        raise ValueError(f"output_length cannot exceed input length. Got {m} > {vector.size}.")
    clean_seed = copy_binary_vector(seed, name="seed")
    expected_seed_length = toeplitz_seed_length(int(vector.size), m)
    if clean_seed.size != expected_seed_length:
        raise ValueError(f"seed must contain exactly {expected_seed_length} bits. Got {clean_seed.size}.")
    if m == 0:
        result = np.empty(0, dtype=np.uint8)
        result.flags.writeable = False
        return result

    convolution_length = clean_seed.size + vector.size - 1
    fft_length = 1 << (convolution_length - 1).bit_length()
    spectrum = np.fft.rfft(clean_seed, fft_length) * np.fft.rfft(vector, fft_length)
    convolution = np.fft.irfft(spectrum, fft_length)
    integer_slice = np.rint(convolution[vector.size - 1 : vector.size - 1 + m]).astype(np.int64)
    result = np.asarray(integer_slice & 1, dtype=np.uint8)
    result.flags.writeable = False
    return result
