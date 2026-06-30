#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES ================

import numpy as np

#=================== CONSTANTS ===================

X = np.array([
    [0, 1],
    [1, 0]
], dtype = complex)

Y = np.array([
    [0, -1j],
    [1j, 0]
], dtype = complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype = complex)

H = np.array([
    [1, 1],
    [1, -1]
], dtype = complex) / np.sqrt(2)