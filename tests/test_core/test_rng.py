# ================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

# =================================================

# ================= IMPORT MODULES ================

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from core import rng
from core.constants import DEFAULT_ATOL

# =================== CONSTANTS ===================

ATOL = DEFAULT_ATOL

# ===================== TESTS =====================


def test_base_rng_cannot_be_instantiated():
    with pytest.raises(TypeError):
        rng.BaseRNG()  # pyright: ignore[reportAbstractUsage]


def test_seeded_rng_is_reproducible_and_keeps_one_generator():
    first = rng.SeededRNG(1234)
    second = rng.SeededRNG(1234)

    assert isinstance(first.gen, np.random.Generator)
    assert first.gen is first.gen
    assert_array_equal(
        first.gen.integers(0, 100, size=20),
        second.gen.integers(0, 100, size=20),
    )


def test_different_seeds_produce_different_streams():
    first = rng.SeededRNG(1).gen.integers(0, 2, size=64)
    second = rng.SeededRNG(2).gen.integers(0, 2, size=64)

    assert not np.array_equal(first, second)


def test_global_rng_is_a_singleton():
    first = rng.GlobalRNG()
    second = rng.GlobalRNG()

    assert first is second
    assert first.gen is second.gen
    assert isinstance(first.gen, np.random.Generator)


def test_qrng_simulator_exposes_injected_generator():
    base_rng = rng.SeededRNG(7)
    simulator = rng.QRNGSimulator(base_rng)

    assert simulator.gen is base_rng.gen


@pytest.mark.parametrize("size", [0, 1, 32])
def test_qrng_uncorrelated_bits_have_expected_shape_and_values(size):
    simulator = rng.QRNGSimulator(rng.SeededRNG(7))

    bits = simulator.generate_raw_bits(size)

    assert bits.shape == (size,)
    assert np.issubdtype(bits.dtype, np.integer)
    assert set(bits.tolist()) <= {0, 1}


@pytest.mark.parametrize(("bias_prob", "expected"), [(0.0, 0), (1.0, 1)])
def test_qrng_bias_boundaries_are_deterministic(bias_prob, expected):
    simulator = rng.QRNGSimulator(rng.SeededRNG(7), bias_prob=bias_prob)

    assert_array_equal(simulator.generate_raw_bits(32), np.full(32, expected))


def test_qrng_same_seed_reproduces_correlated_sequence():
    first = rng.QRNGSimulator(rng.SeededRNG(99), bias_prob=0.6, correlation=0.4)
    second = rng.QRNGSimulator(rng.SeededRNG(99), bias_prob=0.6, correlation=0.4)

    assert_array_equal(first.generate_raw_bits(64), second.generate_raw_bits(64))


def test_qrng_maximum_positive_correlation_repeats_initial_bit():
    bits = rng.QRNGSimulator(rng.SeededRNG(4), correlation=1.0).generate_raw_bits(32)

    assert_array_equal(bits, np.full(32, bits[0]))


def test_qrng_maximum_negative_correlation_alternates_bits():
    bits = rng.QRNGSimulator(rng.SeededRNG(4), correlation=-1.0).generate_raw_bits(32)

    assert_array_equal(bits[1:], 1 - bits[:-1])


def test_qrng_correlated_mode_accepts_empty_output():
    simulator = rng.QRNGSimulator(rng.SeededRNG(7), correlation=0.5)

    assert_array_equal(simulator.generate_raw_bits(0), np.array([], dtype=int))


@pytest.mark.parametrize("correlation", [0.0, 0.5])
def test_qrng_rejects_negative_size(correlation):
    simulator = rng.QRNGSimulator(rng.SeededRNG(7), correlation=correlation)

    with pytest.raises(ValueError):
        simulator.generate_raw_bits(-1)


@pytest.mark.parametrize("bias_prob", [-0.01, 1.01])
def test_qrng_rejects_probability_outside_unit_interval(bias_prob):
    simulator = rng.QRNGSimulator(rng.SeededRNG(7), bias_prob=bias_prob)

    with pytest.raises(ValueError):
        simulator.generate_raw_bits(1)


@pytest.mark.parametrize("helper", [rng.random_bit, rng.random_basis])
def test_random_binary_helpers_return_scalar_bit(helper):
    result = helper(rng.SeededRNG(21))

    assert isinstance(result, (int, np.integer))
    assert result in (0, 1)


@pytest.mark.parametrize("helper", [rng.random_bit, rng.random_basis])
@pytest.mark.parametrize("size", [0, 1, 50])
def test_random_binary_helpers_are_reproducible(helper, size):
    first = helper(rng.SeededRNG(21), size=size)
    second = helper(rng.SeededRNG(21), size=size)

    assert_array_equal(first, second)
    assert first.shape == (size,)
    assert set(first.tolist()) <= {0, 1}


@pytest.mark.parametrize("helper", [rng.random_bit, rng.random_basis])
def test_random_binary_helpers_reject_negative_size(helper):
    with pytest.raises(ValueError):
        helper(rng.SeededRNG(21), size=-1)


@pytest.mark.parametrize("dimension", [1, 2, 4])
def test_random_unitary_returns_reproducible_unitary_matrix(dimension):
    first = rng.random_unitary(rng.SeededRNG(123), dimension)
    second = rng.random_unitary(rng.SeededRNG(123), dimension)

    assert_allclose(first, second, atol=ATOL)
    assert first.shape == (dimension, dimension)
    assert_allclose(first.conj().T @ first, np.identity(dimension), atol=ATOL)


@pytest.mark.parametrize("dimension", [0, -1])
def test_random_unitary_rejects_non_positive_dimensions(dimension):
    with pytest.raises(ValueError):
        rng.random_unitary(rng.SeededRNG(123), dimension)
