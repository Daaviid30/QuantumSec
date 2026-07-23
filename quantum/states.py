#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

import numpy as np

from quantum import linalg, validation

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== FUNCTIONS ===================

def dm_from_ket(psi: np.ndarray) -> np.ndarray:
    """Return psi as a density matrix state.

    Parameters:
    -----------
    psi: Vector that represents a quantum state.

    Returns:
    --------
    density_matrix: Matrix that represents quantum state psi.

    Raises:
    -------
    ValueError: 
        If psi is not a valid quantum state.
    """

    psi = linalg.as_ket(psi)
    if not validation.is_quantum_state(psi):
        raise ValueError("[!] Psi is not a valid quantum state.")
    
    return linalg.outer_product(psi, psi)
