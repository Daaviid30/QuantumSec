from core.rng import SeededRNG
from qkd.channel import PhaseFlipChannel
from qkd.protocols import BB84Protocol, BB84SessionStatus


def test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error():
    """A basis average must not authorize extraction on an asymmetric channel."""

    session = BB84Protocol(PhaseFlipChannel(0.16), SeededRNG(2026)).run_session(8_000)
    qber_z = session.diagnostic_qber_z
    qber_x = session.diagnostic_qber_x
    qber_aggregated = session.diagnostic_qber_aggregated

    assert qber_z is not None and qber_x is not None and qber_aggregated is not None
    assert qber_z < 0.01
    assert 0.12 < qber_x < 0.20
    assert qber_z < qber_aggregated < qber_x
    estimated_z = session.estimated_qber_z
    estimated_x = session.estimated_qber_x
    assert session.estimated_qber_aggregated is not None
    assert session.phase_error_bound is not None
    assert estimated_z is not None and estimated_x is not None
    assert session.estimated_qber_aggregated < session.config.phase_error_abort_threshold
    assert session.phase_error_bound > session.config.phase_error_abort_threshold
    assert session.phase_error_bound == max(estimated_z, estimated_x)

    # Before the fix, the aggregate sample (~8%) was substituted for phase
    # error, the session completed, and 244 unjustified bits were extracted.
    assert session.status is BB84SessionStatus.ABORTED
    assert session.n_final == 0
