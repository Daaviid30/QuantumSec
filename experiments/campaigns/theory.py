"""Analytical BB84 error predictions for the E2 validation campaign."""

from __future__ import annotations

import math
from dataclasses import dataclass

from qkd.channel import QKDChannelStageSpec, QKDChannelStageType


@dataclass(frozen=True, slots=True)
class AnalyticalQBER:
    """Expected Z-, X-, and uniform-basis aggregate QBER."""

    qber_z: float
    qber_x: float
    qber_aggregate: float


def analytical_qber(stage: QKDChannelStageSpec) -> AnalyticalQBER:
    """Return the exact E2 prediction implied by the implemented channel."""

    if not isinstance(stage, QKDChannelStageSpec):
        raise TypeError("stage must be a QKDChannelStageSpec.")
    match stage.type:
        case QKDChannelStageType.IDENTITY:
            z_error = x_error = 0.0
        case QKDChannelStageType.DEPOLARIZING:
            assert stage.p is not None
            z_error = x_error = stage.p / 2.0
        case QKDChannelStageType.BIT_FLIP:
            assert stage.p is not None
            z_error, x_error = stage.p, 0.0
        case QKDChannelStageType.PHASE_FLIP:
            assert stage.p is not None
            z_error, x_error = 0.0, stage.p
        case QKDChannelStageType.AMPLITUDE_DAMPING:
            assert stage.gamma is not None
            z_error = stage.gamma / 2.0
            x_error = (1.0 - math.sqrt(1.0 - stage.gamma)) / 2.0
        case QKDChannelStageType.PAULI:
            assert stage.px is not None and stage.py is not None and stage.pz is not None
            z_error = stage.px + stage.py
            x_error = stage.py + stage.pz
        case _:
            raise ValueError("E2 analytical predictions do not cover adversarial stages.")
    return AnalyticalQBER(z_error, x_error, (z_error + x_error) / 2.0)
