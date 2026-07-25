#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from core.rng import BaseRNG
from quantum import linalg
from quantum import validation as v

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== CLASSES ===================

@dataclass(frozen=True, slots=True)
class MeasurementResult:
    outcome: int
    probability: float
    poststate: np.ndarray

#=================== FUNCTIONS ===================

def dm_purity(
        rho: np.ndarray
    ) -> float:
    """
    Returns the purity value of a density matrix.

    Parameters:
    -----------
    rho: Density matrix that represents a quantum state.

    Returns:
    --------
    purity: The purity of the density matrix.

    Raises:
    -------
    ValueError: 
        If rho is not a valid density matrix.
    """

    rho = np.asarray(rho, dtype = complex)
    v.validate_density_matrix(rho)

    purity = np.trace(rho @ rho)

    return float(purity.real)
