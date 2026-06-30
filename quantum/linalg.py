#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

import numpy as np

#=================== FUNCTIONS ===================

def as_ket(psi: np.ndarray) -> np.ndarray:
    """Return psi as a canonical one-dimensional ket.

    Accepted shapes:
    - (n,) one dimensional ket
    - (n, 1) column vector

    Rejected shapes:
    - (1, n), explicit row vectors are not accepted as kets
    - (n, m), because that may be an operator or density matrix
    - higher-dimensional arrays
    """
    psi = np.asarray(psi, dtype=complex)

    if psi.ndim == 1:
        if psi.size == 0:
            raise ValueError("[!] ket must not be empty.")
        return psi

    if psi.ndim == 2 and psi.shape[1] == 1:
        if psi.size == 0:
            raise ValueError("[!] ket must not be empty.")
        return psi[:, 0]

    raise ValueError(
        f"ket must have shape (n,) or (n, 1). Got shape {psi.shape}."
    )