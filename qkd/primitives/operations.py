"""Named single-qubit operators commonly used by QKD protocols."""

import numpy as np


def _immutable(values: list[list[complex]] | np.ndarray) -> np.ndarray:
    result = np.asarray(values, dtype=np.complex128)
    result.flags.writeable = False
    return result


X = _immutable([[0, 1], [1, 0]])
Y = _immutable([[0, -1j], [1j, 0]])
Z = _immutable([[1, 0], [0, -1]])
H = _immutable(np.array([[1, 1], [1, -1]]) / np.sqrt(2))
