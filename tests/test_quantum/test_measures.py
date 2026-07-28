from dataclasses import FrozenInstanceError
from typing import Any

import numpy as np
import pytest
from numpy.testing import assert_allclose

from core.constants import DEFAULT_ATOL
from core.rng import BaseRNG, SeededRNG
from qkd.primitives.measurements import MEASUREMENT_X, MEASUREMENT_Z, P0, P1
from qkd.primitives.states import KET0, KET1, PLUS
from quantum import validation as v
from quantum.measures import (
    MeasurementResult,
    ProjectiveMeasurement,
    measure_projective,
    sample_projective_outcome,
)
from quantum.states import dm_from_ket


class _ChoiceGenerator:
    def __init__(self, index: int):
        self.index = index
        self.probabilities: np.ndarray | None = None

    def choice(self, number_of_outcomes: int, *, p: np.ndarray) -> int:
        assert number_of_outcomes == p.size
        self.probabilities = p.copy()
        return self.index


class _ChoiceRNG(BaseRNG):
    def __init__(self, index: int):
        self.generator = _ChoiceGenerator(index)

    @property
    def gen(self) -> Any:
        return self.generator


def test_measurement_result_is_frozen_slotted_compact_and_has_no_array_equality():
    result = MeasurementResult(outcome=0, probability=1.0, post_state=P0.copy())

    assert MeasurementResult.__eq__ is object.__eq__
    assert not hasattr(result, "__dict__")
    assert "post_state" not in repr(result)
    with pytest.raises(FrozenInstanceError):
        result.outcome = 1  # pyright: ignore[reportAttributeAccessIssue]


def test_projective_measurement_valid_construction_and_properties():
    measurement = ProjectiveMeasurement(projectors=(P0, P1), outcomes=(10, 20))

    assert measurement.dimension == 2
    assert measurement.number_of_outcomes == 2
    assert measurement.outcomes == (10, 20)
    assert isinstance(measurement.projectors, tuple)


@pytest.mark.parametrize(
    ("projectors", "outcomes"),
    [
        ((), ()),
        ((P0, P1), (0,)),
        ((P0, P0), (0, 1)),
        ((P0,), (0,)),
    ],
)
def test_projective_measurement_rejects_empty_mismatched_or_invalid_sets(projectors, outcomes):
    with pytest.raises(ValueError):
        ProjectiveMeasurement(projectors=projectors, outcomes=outcomes)


def test_projective_measurement_copies_inputs_and_makes_storage_read_only():
    source_p0 = P0.copy()
    source_p1 = P1.copy()
    measurement = ProjectiveMeasurement(projectors=(source_p0, source_p1), outcomes=(0, 1))

    source_p0[0, 0] = 0.0
    assert measurement.projectors[0][0, 0] == 1.0
    assert measurement.projectors[0].dtype == np.complex128
    assert not measurement.projectors[0].flags.writeable
    with pytest.raises(ValueError):
        measurement.projectors[0][0, 0] = 0.0


@pytest.mark.parametrize(
    ("state", "measurement", "expected_outcome"),
    [
        (KET0, MEASUREMENT_Z, 0),
        (KET1, MEASUREMENT_Z, 1),
        (PLUS, MEASUREMENT_X, 0),
    ],
)
def test_eigenstates_sample_deterministically(state, measurement, expected_outcome):
    sample = sample_projective_outcome(dm_from_ket(state), measurement, SeededRNG(12))

    assert sample.outcome == expected_outcome
    assert sample.probability == pytest.approx(1.0, abs=DEFAULT_ATOL)


def test_maximally_mixed_qubit_has_equal_z_probabilities():
    rng = _ChoiceRNG(index=0)

    sample = sample_projective_outcome(np.identity(2) / 2.0, MEASUREMENT_Z, rng)

    assert sample.probability == pytest.approx(0.5, abs=DEFAULT_ATOL)
    assert rng.generator.probabilities is not None
    assert_allclose(rng.generator.probabilities, [0.5, 0.5], atol=DEFAULT_ATOL)


def test_equal_seeds_produce_equal_sampled_sequences():
    rho = dm_from_ket(PLUS)
    first_rng = SeededRNG(12345)
    second_rng = SeededRNG(12345)

    first = [sample_projective_outcome(rho, MEASUREMENT_Z, first_rng).index for _ in range(64)]
    second = [sample_projective_outcome(rho, MEASUREMENT_Z, second_rng).index for _ in range(64)]

    assert first == second


def test_fast_sampling_path_skips_density_validation(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("spectral validation was called")

    monkeypatch.setattr(v, "validate_density_matrix", fail_if_called)

    sample = sample_projective_outcome(
        np.identity(2) / 2.0,
        MEASUREMENT_Z,
        SeededRNG(1),
        validate_state=False,
    )

    assert sample.probability == pytest.approx(0.5, abs=DEFAULT_ATOL)


@pytest.mark.parametrize(
    ("rho", "message"),
    [
        (np.diag([-0.1, 1.1]), "non-negative"),
        (np.diag([0.0, 1.1]), "cannot exceed one"),
        (np.diag([0.4, 0.4]), "sum to one"),
        (np.diag([0.5 + 0.1j, 0.5 - 0.1j]), "must be real"),
    ],
)
def test_fast_sampling_path_keeps_probability_checks_before_clipping(rho, message):
    with pytest.raises(ValueError, match=message):
        sample_projective_outcome(
            rho,
            MEASUREMENT_Z,
            SeededRNG(1),
            validate_state=False,
        )


def test_full_measurement_collapses_plus_state_to_a_z_eigenstate():
    result = measure_projective(dm_from_ket(PLUS), MEASUREMENT_Z, SeededRNG(7))

    expected = P0 if result.outcome == 0 else P1
    assert_allclose(result.post_state, expected, atol=DEFAULT_ATOL)
    assert_allclose(np.trace(result.post_state), 1.0, atol=DEFAULT_ATOL)
    assert_allclose(result.post_state, result.post_state.conj().T, atol=DEFAULT_ATOL)
    assert np.min(np.linalg.eigvalsh(result.post_state)) >= -DEFAULT_ATOL


def test_repeating_projective_measurement_returns_same_outcome_with_certainty():
    first = measure_projective(dm_from_ket(PLUS), MEASUREMENT_Z, SeededRNG(9))
    second = measure_projective(first.post_state, MEASUREMENT_Z, SeededRNG(100))

    assert second.outcome == first.outcome
    assert second.probability == pytest.approx(1.0, abs=DEFAULT_ATOL)
    assert_allclose(second.post_state, first.post_state, atol=DEFAULT_ATOL)


def test_sampling_and_full_measurement_use_same_seeded_selection():
    rho = dm_from_ket(PLUS)
    sample = sample_projective_outcome(rho, MEASUREMENT_Z, SeededRNG(77))
    result = measure_projective(rho, MEASUREMENT_Z, SeededRNG(77))

    assert result.outcome == sample.outcome
    assert result.probability == pytest.approx(sample.probability, abs=DEFAULT_ATOL)


def test_full_measurement_rejects_a_faulty_rng_selecting_zero_probability():
    with pytest.raises(RuntimeError, match="numerically zero"):
        measure_projective(dm_from_ket(KET0), MEASUREMENT_Z, _ChoiceRNG(index=1))
