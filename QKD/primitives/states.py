#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES ================

import numpy as np

#=================== CONSTANTS ===================

KET0 = np.array([1, 0], dtype = complex)
KET1 = np.array([0, 1], dtype = complex)
PLUS = np.array([1, 1], dtype = complex) / np.sqrt(2)
MINUS = np.array([1, -1], dtype = complex) / np.sqrt(2)

# 2 qubit states
PHI_PLUS = np.array([1, 0, 0, 1], dtype = complex) / np.sqrt(2)
PHI_MINUS = np.array([1, 0, 0, -1], dtype = complex) / np.sqrt(2)
PSI_PLUS = np.array([0, 1, 1, 0], dtype = complex) / np.sqrt(2)
PSI_MINUS = np.array([0, 1, -1, 1], dtype = complex) / np.sqrt(2)
