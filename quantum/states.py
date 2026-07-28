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
    """
    Construct the density matrix |psi><psi| of a pure quantum state.

    Parameters:
    -----------
    psi: np.ndarray
        Normalized ket representing a pure quantum state.

    Returns:
    --------
    np.ndarray
        Complex density matrix associated with psi.

    Raises:
    -------
    ValueError
        If psi is not a valid normalized quantum-state ket.
    """

    psi = linalg.as_ket(psi)
    v.validate_quantum_state(psi)
    
    return linalg.outer_product(psi, psi)

def dm_from_ensemble(states: Sequence[np.ndarray], probs: np.ndarray) -> np.ndarray:
    """
    Construct the density matrix of a probabilistic ensemble of pure states.

    Parameters:
    -----------
    states: Sequence[np.ndarray]
        Normalized kets that form the ensemble.
    probs: np.ndarray
        Probability assigned to each ket in states.

    Returns:
    --------
    np.ndarray
        Weighted sum of the pure-state density matrices.

    Raises:
    -------
    ValueError
        If probabilities are invalid, lengths differ, a ket is invalid, or state dimensions differ.
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
