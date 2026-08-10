"""Reusable standard projective measurements for QKD protocols."""

from qkd.primitives.bases import Basis
from qkd.primitives.states import KET0, KET1, MINUS, MINUS_I, PLUS, PLUS_I
from quantum.measures import ProjectiveMeasurement
from quantum.states import dm_from_ket

P0 = dm_from_ket(KET0)
P1 = dm_from_ket(KET1)
P_PLUS = dm_from_ket(PLUS)
P_MINUS = dm_from_ket(MINUS)
P_I = dm_from_ket(PLUS_I)
P_MINUS_I = dm_from_ket(MINUS_I)

MEASUREMENT_Z = ProjectiveMeasurement(projectors=(P0, P1), outcomes=(0, 1))
MEASUREMENT_X = ProjectiveMeasurement(projectors=(P_PLUS, P_MINUS), outcomes=(0, 1))
MEASUREMENT_Y = ProjectiveMeasurement(projectors=(P_I, P_MINUS_I), outcomes=(0, 1))

MEASUREMENTS_BY_BASIS = {
    Basis.Z: MEASUREMENT_Z,
    Basis.X: MEASUREMENT_X,
    Basis.Y: MEASUREMENT_Y,
}
