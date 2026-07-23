#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

from collections.abc import Sequence

import numpy as np

from quantum import linalg
from quantum import validation as v

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== FUNCTIONS ===================

def dm_from_ket(psi: np.ndarray) -> np.ndarray:
    """Return the density matrix |psi><psi| associated with a pure state.

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
    v.validate_quantum_state(psi)
    
    return linalg.outer_product(psi, psi)

def dm_from_ensemble(states: Sequence[np.ndarray], probs: np.ndarray) -> np.ndarray:
    """Return an ensemble of quantum states as a density matrix state.

    Parameters:
    -----------
    states: Quantum states array that represents an ensemble.
    probs: Probabilities associated to quantum states.

    Returns:
    --------
    density_matrix: Matrix that represents the ensemble of quantum states.

    Raises:
    -------
    ValueError: 
        If psi is not a valid quantum state.
        If len(states) is not equal to len(probs).
        If probs is not a valid probability state vector.
    """
    probs = linalg.as_ket(probs)
    v.validate_probability_state(probs)
    probs = np.real(probs)

    if len(states) != probs.size:
        raise ValueError("[!] Probability vector and state vector have different size.")

    density: np.ndarray | None = None
    dimension: int | None = None

    for index, state in enumerate(states):

        state = linalg.as_ket(state)
        v.validate_quantum_state(state)

        if density is None:
            density = np.zeros((state.size, state.size), dtype=complex)
            dimension = state.size

        elif dimension != state.size:
            raise ValueError("[!] The dimension of the states must be equal.")
        
        density += linalg.outer_product(state, state) * probs[index]

    if density is None:
        raise ValueError("[!] Density matrix must not be None.")
    return density
