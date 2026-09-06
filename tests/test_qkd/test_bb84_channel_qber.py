from math import sqrt

import pytest

from core.rng import SeededRNG
from qkd.channel import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    DepolarizingChannel,
    IdentityChannel,
    PauliChannel,
    PhaseFlipChannel,
)
from qkd.protocols import BB84Protocol


@pytest.mark.parametrize(
    ("channel", "expected_z", "expected_x"),
    [
        pytest.param(IdentityChannel(), 0.0, 0.0, id="identity"),
        # E(rho)=(1-p)rho+pI/2 gives p/2 disagreement in either basis.
        pytest.param(DepolarizingChannel(0.24), 0.12, 0.12, id="depolarizing"),
        pytest.param(BitFlipChannel(0.18), 0.18, 0.0, id="bit-flip"),
        pytest.param(PhaseFlipChannel(0.18), 0.0, 0.18, id="phase-flip"),
        # Z errors are px+py; X errors are pz+py.
        pytest.param(PauliChannel(px=0.08, py=0.03, pz=0.17), 0.11, 0.20, id="pauli"),
        # Uniform BB84 inputs under relaxation gamma give gamma/2 in Z and
        # (1-sqrt(1-gamma))/2 in X.
        pytest.param(
            AmplitudeDampingChannel(0.20),
            0.10,
            (1.0 - sqrt(0.80)) / 2.0,
            id="amplitude-damping",
        ),
    ],
)
def test_supported_channels_match_analytical_per_basis_qber(channel, expected_z, expected_x):
    # 12k signals yield roughly 3k matched observations per basis. A 0.03
    # tolerance exceeds three worst-case Bernoulli standard errors (~0.027).
    result = BB84Protocol(channel, SeededRNG(7301)).run(12_000)
    metrics = result.qber_by_basis

    assert metrics.qber_z is not None and metrics.qber_x is not None
    assert metrics.n_z > 2_500
    assert metrics.n_x > 2_500
    assert metrics.qber_z == pytest.approx(expected_z, abs=0.03)
    assert metrics.qber_x == pytest.approx(expected_x, abs=0.03)
    assert metrics.qber_aggregated == pytest.approx(
        (metrics.n_z * metrics.qber_z + metrics.n_x * metrics.qber_x) / (metrics.n_z + metrics.n_x)
    )
    if abs(expected_z - expected_x) >= 0.04:
        assert abs(metrics.qber_z - metrics.qber_x) >= 0.015
