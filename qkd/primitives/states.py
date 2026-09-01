"""Named pure states commonly used by QKD protocols."""

import numpy as np


def _immutable(values: list[complex] | np.ndarray) -> np.ndarray:
    result = np.asarray(values, dtype=np.complex128)
    result.flags.writeable = False
    return result


KET0 = _immutable([1, 0])
KET1 = _immutable([0, 1])
PLUS = _immutable(np.array([1, 1]) / np.sqrt(2))
MINUS = _immutable(np.array([1, -1]) / np.sqrt(2))
PLUS_I = _immutable(np.array([1, 1j]) / np.sqrt(2))
MINUS_I = _immutable(np.array([1, -1j]) / np.sqrt(2))

PHI_PLUS = _immutable(np.array([1, 0, 0, 1]) / np.sqrt(2))
PHI_MINUS = _immutable(np.array([1, 0, 0, -1]) / np.sqrt(2))
PSI_PLUS = _immutable(np.array([0, 1, 1, 0]) / np.sqrt(2))
PSI_MINUS = _immutable(np.array([0, 1, -1, 0]) / np.sqrt(2))
