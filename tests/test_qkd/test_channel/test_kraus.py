import numpy as np
import pytest
from numpy.testing import assert_allclose

from qkd.channel import KrausChannel
from qkd.primitives.operations import X
from qkd.primitives.states import KET0, KET1, PLUS
from quantum.states import dm_from_ket


def test_kraus_channel_validates_once_and_defensively_copies_operators():
    source_operator = np.eye(2)
    channel = KrausChannel((source_operator,))

    source_operator[0, 0] = 0.0

    assert channel.dimension == 2
    assert channel.operators[0].dtype == np.complex128
    assert not channel.operators[0].flags.writeable
    assert_allclose(channel.operators[0], np.eye(2))
    with pytest.raises(ValueError):
        channel.operators[0][0, 0] = 0.0


def test_kraus_channel_applies_operator_sum_without_mutating_input():
    rho = dm_from_ket(KET0)
    original = rho.copy()

    output = KrausChannel((X,)).apply(rho)

    assert_allclose(output, dm_from_ket(KET1))
    assert_allclose(rho, original)
    assert output.dtype == np.complex128


def test_kraus_channel_supports_general_finite_dimension():
    rho = np.eye(3, dtype=np.complex128) / 3.0
    channel = KrausChannel((np.eye(3),))

    assert channel.dimension == 3
    assert_allclose(channel.apply(rho), rho)


@pytest.mark.parametrize(
    "operators",
    [
        (),
        (np.ones((2, 3)),),
        (np.eye(2), np.eye(3)),
        (np.array([[1.0, 0.0], [0.0, np.nan]]),),
        (0.5 * np.eye(2),),
    ],
)
def test_kraus_channel_rejects_invalid_operator_sets(operators):
    with pytest.raises(ValueError):
        KrausChannel(operators)


def test_kraus_dimension_check_remains_enabled_on_fast_path():
    channel = KrausChannel((np.eye(2),))
    qutrit_state = np.eye(3) / 3.0

    with pytest.raises(ValueError, match="dimensions must match"):
        channel.apply(qutrit_state, validate_state=False)


def test_kraus_channel_rejects_invalid_state_when_validation_is_enabled():
    invalid_state = dm_from_ket(PLUS) * 2.0

    with pytest.raises(ValueError, match="unit trace"):
        KrausChannel((np.eye(2),)).apply(invalid_state)
