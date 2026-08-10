"""Named pure states commonly used by QKD protocols."""

import numpy as np

KET0 = np.array([1, 0], dtype=np.complex128)
KET1 = np.array([0, 1], dtype=np.complex128)
PLUS = np.array([1, 1], dtype=np.complex128) / np.sqrt(2)
MINUS = np.array([1, -1], dtype=np.complex128) / np.sqrt(2)
PLUS_I = np.array([1, 1j], dtype=np.complex128) / np.sqrt(2)
MINUS_I = np.array([1, -1j], dtype=np.complex128) / np.sqrt(2)

PHI_PLUS = np.array([1, 0, 0, 1], dtype=np.complex128) / np.sqrt(2)
PHI_MINUS = np.array([1, 0, 0, -1], dtype=np.complex128) / np.sqrt(2)
PSI_PLUS = np.array([0, 1, 1, 0], dtype=np.complex128) / np.sqrt(2)
PSI_MINUS = np.array([0, 1, -1, 0], dtype=np.complex128) / np.sqrt(2)
