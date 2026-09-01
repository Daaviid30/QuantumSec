import numpy as np
import pytest
from numpy.testing import assert_allclose

from core.constants import DEFAULT_ATOL
from qkd.primitives import Basis, bases_from_bits, basis_from_bit, operations, states
from qkd.primitives.measurements import (
    MEASUREMENT_X,
    MEASUREMENT_Y,
    MEASUREMENT_Z,
    MEASUREMENTS_BY_BASIS,
)


def test_named_qkd_states_and_operators_are_immutable():
    constants = (
        states.KET0,
        states.KET1,
        states.PLUS,
        states.MINUS,
        states.PLUS_I,
        states.MINUS_I,
        states.PHI_PLUS,
        states.PHI_MINUS,
        states.PSI_PLUS,
        states.PSI_MINUS,
        operations.X,
        operations.Y,
        operations.Z,
        operations.H,
    )

    assert all(not constant.flags.writeable for constant in constants)
    with pytest.raises(ValueError):
        states.KET0[0] = 0


def test_standard_measurement_registry_is_structurally_immutable():
    with pytest.raises(TypeError):
        MEASUREMENTS_BY_BASIS[Basis.Z] = MEASUREMENT_X  # pyright: ignore[reportIndexIssue]


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0, Basis.Z), (1, Basis.X), (np.int64(0), Basis.Z), (np.int64(1), Basis.X)],
)
def test_basis_from_bit_maps_random_integer_convention(value, expected):
    assert basis_from_bit(value) is expected


@pytest.mark.parametrize("value", [-1, 2, 0.0, 1.0, True])
def test_basis_from_bit_rejects_non_binary_integer_values(value):
    with pytest.raises(ValueError):
        basis_from_bit(value)


def test_bases_from_bits_maps_vectors_and_rejects_non_vectors():
    assert bases_from_bits(np.array([0, 1, 1, 0])) == (
        Basis.Z,
        Basis.X,
        Basis.X,
        Basis.Z,
    )
    with pytest.raises(ValueError, match="one-dimensional"):
        bases_from_bits(np.array([[0, 1]]))


def test_standard_measurements_are_complete_and_mapped_by_basis():
    assert MEASUREMENTS_BY_BASIS == {
        Basis.Z: MEASUREMENT_Z,
        Basis.X: MEASUREMENT_X,
        Basis.Y: MEASUREMENT_Y,
    }

    for measurement in MEASUREMENTS_BY_BASIS.values():
        assert measurement.dimension == 2
        assert measurement.outcomes == (0, 1)
        assert_allclose(
            sum(measurement.projectors),
            np.identity(2),
            atol=DEFAULT_ATOL,
        )
        assert all(not projector.flags.writeable for projector in measurement.projectors)
