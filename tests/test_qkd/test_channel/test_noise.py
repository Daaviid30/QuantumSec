import numpy as np
import pytest
from numpy.testing import assert_allclose

from core.constants import DEFAULT_ATOL
from qkd.channel import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    DepolarizingChannel,
    PauliChannel,
    PhaseFlipChannel,
)
from qkd.primitives.operations import X, Y, Z
from qkd.primitives.states import KET0, KET1, MINUS, PLUS
from quantum import validation as v
from quantum.states import dm_from_ket

RHO_ZERO = dm_from_ket(KET0)
RHO_ONE = dm_from_ket(KET1)
RHO_PLUS = dm_from_ket(PLUS)
RHO_MINUS = dm_from_ket(MINUS)
MAXIMALLY_MIXED = np.eye(2, dtype=np.complex128) / 2.0


def assert_valid_qubit_density_matrix(rho):
    assert rho.shape == (2, 2)
    assert rho.dtype == np.complex128
    assert_allclose(np.trace(rho), 1.0, atol=DEFAULT_ATOL, rtol=0.0)
    assert_allclose(rho, rho.conj().T, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.min(np.linalg.eigvalsh(rho)) >= -DEFAULT_ATOL
    assert v.validate_density_matrix(rho) is None


def test_depolarizing_extremes_match_documented_parameterization():
    assert_allclose(DepolarizingChannel(p=0.0).apply(RHO_PLUS), RHO_PLUS)
    assert_allclose(DepolarizingChannel(p=1.0).apply(RHO_PLUS), MAXIMALLY_MIXED)


def test_depolarizing_channel_fixes_maximally_mixed_state():
    assert_allclose(DepolarizingChannel(p=0.37).apply(MAXIMALLY_MIXED), MAXIMALLY_MIXED)


def test_depolarizing_channel_preserves_qubit_physics():
    output = DepolarizingChannel(p=0.42).apply(RHO_PLUS)

    assert_valid_qubit_density_matrix(output)
    assert_allclose(output, 0.58 * RHO_PLUS + 0.42 * MAXIMALLY_MIXED)


def test_depolarizing_channel_rejects_non_qubit_states():
    with pytest.raises(ValueError, match="dimensions must match"):
        DepolarizingChannel(p=0.2).apply(np.eye(4) / 4.0)


@pytest.mark.parametrize("p", [-0.01, 1.01, np.nan, np.inf, True, "0.5"])
def test_depolarizing_channel_rejects_invalid_probabilities(p):
    with pytest.raises(ValueError):
        DepolarizingChannel(p=p)


def test_general_pauli_channel_matches_analytical_mixture():
    channel = PauliChannel(px=0.1, py=0.2, pz=0.3)

    output = channel.apply(RHO_PLUS)
    expected = (
        channel.pi * RHO_PLUS
        + channel.px * X @ RHO_PLUS @ X
        + channel.py * Y @ RHO_PLUS @ Y
        + channel.pz * Z @ RHO_PLUS @ Z
    )

    assert channel.pi == pytest.approx(0.4)
    assert_allclose(output, expected, atol=DEFAULT_ATOL, rtol=0.0)
    assert_valid_qubit_density_matrix(output)


def test_bit_flip_channel_extremes():
    assert_allclose(BitFlipChannel(p=0.0).apply(RHO_ZERO), RHO_ZERO)
    assert_allclose(BitFlipChannel(p=1.0).apply(RHO_ZERO), RHO_ONE)


def test_phase_flip_maps_plus_to_minus():
    assert_allclose(PhaseFlipChannel(p=1.0).apply(RHO_PLUS), RHO_MINUS)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"px": -0.1, "py": 0.0, "pz": 0.0},
        {"px": 0.0, "py": 1.1, "pz": 0.0},
        {"px": 0.0, "py": 0.0, "pz": np.nan},
        {"px": 0.4, "py": 0.4, "pz": 0.3},
    ],
)
def test_pauli_channel_rejects_invalid_probabilities(kwargs):
    with pytest.raises(ValueError):
        PauliChannel(**kwargs)


@pytest.mark.parametrize("channel_type", [BitFlipChannel, PhaseFlipChannel])
@pytest.mark.parametrize("p", [-0.01, 1.01, np.inf])
def test_specialized_pauli_channels_reject_invalid_probabilities(channel_type, p):
    with pytest.raises(ValueError):
        channel_type(p=p)


def test_amplitude_damping_extremes_and_fixed_ground_state():
    assert_allclose(AmplitudeDampingChannel(gamma=0.0).apply(RHO_ONE), RHO_ONE)
    assert_allclose(AmplitudeDampingChannel(gamma=1.0).apply(RHO_ONE), RHO_ZERO)
    assert_allclose(AmplitudeDampingChannel(gamma=0.71).apply(RHO_ZERO), RHO_ZERO)


def test_amplitude_damping_matches_analytical_superposition_result():
    gamma = 0.36
    output = AmplitudeDampingChannel(gamma=gamma).apply(RHO_PLUS)
    expected = np.array(
        [
            [(1.0 + gamma) / 2.0, np.sqrt(1.0 - gamma) / 2.0],
            [np.sqrt(1.0 - gamma) / 2.0, (1.0 - gamma) / 2.0],
        ],
        dtype=np.complex128,
    )

    assert_allclose(output, expected, atol=DEFAULT_ATOL, rtol=0.0)
    assert_valid_qubit_density_matrix(output)


@pytest.mark.parametrize("gamma", [-0.01, 1.01, np.nan, -np.inf, True])
def test_amplitude_damping_rejects_invalid_gamma(gamma):
    with pytest.raises(ValueError):
        AmplitudeDampingChannel(gamma=gamma)


@pytest.mark.parametrize(
    "channel",
    [
        DepolarizingChannel(p=0.2),
        PauliChannel(px=0.1, py=0.2, pz=0.3),
        BitFlipChannel(p=0.4),
        PhaseFlipChannel(p=0.4),
        AmplitudeDampingChannel(gamma=0.4),
    ],
)
def test_noise_channels_do_not_mutate_input(channel):
    rho = RHO_PLUS.copy()
    original = rho.copy()

    channel.apply(rho)

    assert_allclose(rho, original)
