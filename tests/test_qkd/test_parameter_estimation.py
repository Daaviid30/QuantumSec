from dataclasses import replace

import numpy as np
import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import ParameterEstimationResult, estimate_qber_from_sample
from qkd.primitives import Basis


def test_parameter_estimation_is_reproducible_and_removes_disclosures():
    alice = np.arange(20, dtype=np.uint8) % 2
    bob = alice.copy()
    bob[[2, 7, 13]] ^= 1
    bases = (Basis.Z, Basis.X) * 10

    first = estimate_qber_from_sample(alice, bob, bases, SeededRNG(18), sample_fraction=0.25)
    second = estimate_qber_from_sample(alice, bob, bases, SeededRNG(18), sample_fraction=0.25)

    assert_array_equal(first.disclosed_indices, second.disclosed_indices)
    assert first.sample_size == 6
    assert first.sample_size_z == first.sample_size_x == 3
    assert np.unique(first.disclosed_indices).size == first.sample_size
    retain = np.delete(np.arange(alice.size), first.disclosed_indices)
    assert_array_equal(first.alice_candidate_key, alice[retain])
    assert_array_equal(first.bob_candidate_key, bob[retain])
    assert (
        first.estimated_qber_aggregated
        == np.count_nonzero(alice[first.disclosed_indices] != bob[first.disclosed_indices])
        / first.sample_size
    )
    assert first.estimated_qber == first.estimated_qber_aggregated
    assert first.phase_error_bound == max(first.estimated_qber_z, first.estimated_qber_x)
    assert set(first.disclosed_bases) == set(first.candidate_bases) == {Basis.Z, Basis.X}
    assert not first.disclosed_indices.flags.writeable
    assert not first.alice_candidate_key.flags.writeable


def test_parameter_estimation_explicit_sample_size_preserves_alignment():
    alice = np.array([0, 1, 1, 0, 1, 0])
    bob = np.array([1, 1, 0, 0, 1, 1])
    bases = (Basis.Z, Basis.X, Basis.Z, Basis.X, Basis.Z, Basis.X)
    result = estimate_qber_from_sample(alice, bob, bases, SeededRNG(4), sample_fraction=0.5, sample_size=2)

    assert_array_equal(result.alice_disclosed_bits, alice[result.disclosed_indices])
    assert_array_equal(result.bob_disclosed_bits, bob[result.disclosed_indices])
    assert result.n_candidate == 4


@pytest.mark.parametrize("fraction", [0.0, 1.0, -0.1, True])
def test_parameter_estimation_rejects_invalid_fraction(fraction):
    with pytest.raises(ValueError, match="sample_fraction"):
        estimate_qber_from_sample(
            [0, 1, 0, 1],
            [0, 1, 0, 1],
            (Basis.Z, Basis.Z, Basis.X, Basis.X),
            SeededRNG(1),
            sample_fraction=fraction,
        )


def test_parameter_estimation_rejects_too_little_sifted_material():
    with pytest.raises(ValueError, match="at least two sifted positions from each"):
        estimate_qber_from_sample([0, 1, 0], [0, 1, 0], (Basis.Z, Basis.Z, Basis.X), SeededRNG(1))


def test_parameter_estimation_rejects_sample_that_consumes_key():
    with pytest.raises(ValueError, match="leave at least one candidate bit in each"):
        estimate_qber_from_sample(
            [0, 1, 0, 1],
            [0, 1, 0, 1],
            (Basis.Z, Basis.Z, Basis.X, Basis.X),
            SeededRNG(1),
            sample_size=4,
        )


def test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error():
    result = ParameterEstimationResult(
        n_sifted=4,
        disclosed_indices=np.array([0, 2]),
        disclosed_bases=(Basis.Z, Basis.X),
        alice_disclosed_bits=np.array([0, 1]),
        bob_disclosed_bits=np.array([1, 1]),
        estimated_qber_z=1.0 - 1e-12,
        estimated_qber_x=0.0,
        estimated_qber_aggregated=0.5 + 1e-12,
        candidate_bases=(Basis.Z, Basis.X),
        alice_candidate_key=np.array([0, 1]),
        bob_candidate_key=np.array([0, 1]),
    )

    assert result.estimated_qber_aggregated == pytest.approx(0.5)


@pytest.mark.parametrize(
    "bases",
    [
        (Basis.Z, Basis.Z, Basis.Z, Basis.Z),
        (Basis.X, Basis.X, Basis.X, Basis.X),
        (Basis.Z, Basis.Z, Basis.X, Basis.Y),
    ],
)
def test_parameter_estimation_fails_closed_without_valid_data_for_both_bb84_bases(bases):
    with pytest.raises(ValueError):
        estimate_qber_from_sample([0, 1, 0, 1], [0, 1, 0, 1], bases, SeededRNG(3))


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("estimated_qber_z", float("nan")),
        ("estimated_qber_x", -0.1),
        ("estimated_qber_aggregated", 1.1),
    ],
)
def test_parameter_estimation_result_rejects_non_finite_and_out_of_range_rates(field_name, value):
    result = estimate_qber_from_sample(
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        (Basis.Z, Basis.Z, Basis.X, Basis.X),
        SeededRNG(3),
    )

    with pytest.raises(ValueError, match=field_name):
        replace(result, **{field_name: value})
