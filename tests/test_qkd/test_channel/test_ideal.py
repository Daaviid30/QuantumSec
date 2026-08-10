import numpy as np
import pytest
from numpy.testing import assert_allclose

from qkd.channel import IdentityChannel
from qkd.primitives.states import KET0, PLUS
from quantum.states import dm_from_ensemble, dm_from_ket


@pytest.mark.parametrize(
    "rho",
    [
        dm_from_ket(PLUS),
        dm_from_ensemble((KET0, PLUS), np.array([0.25, 0.75])),
    ],
)
def test_identity_preserves_pure_and_mixed_states_without_aliasing(rho):
    original = rho.copy()

    output = IdentityChannel().apply(rho)

    assert_allclose(output, original)
    assert_allclose(rho, original)
    assert output.dtype == np.complex128
    assert not np.shares_memory(output, rho)


@pytest.mark.parametrize(
    "rho",
    [
        np.array([[0.5, 1.0], [0.0, 0.5]]),
        np.diag([1.1, -0.1]),
        np.diag([0.4, 0.4]),
    ],
)
def test_identity_rejects_nonphysical_density_matrices_by_default(rho):
    with pytest.raises(ValueError):
        IdentityChannel().apply(rho)


@pytest.mark.parametrize(
    "rho",
    [np.array([1.0, 0.0]), np.ones((2, 3)), np.array([[np.inf]])],
)
def test_identity_keeps_cheap_checks_when_full_validation_is_disabled(rho):
    with pytest.raises(ValueError):
        IdentityChannel().apply(rho, validate_state=False)
