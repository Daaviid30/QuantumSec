#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES ================

import numpy as np

from quantum import linalg

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== FUNCTIONS ===================

def is_normalized_state(psi: np.ndarray, tol:float = ATOL) -> bool:
    """
    Return a boolean indicating whether a state is a normalize state or not.

    Parameters:
    -----------
    psi: vector state that is check.
    tol: tolerance needed in funtions that may have not exact values.

    Returns:
    --------
    True: If the state vector represents a normalize one.
    False: If the state vector does not represent a normalize one.

    Raises:
    -------
    ValueError: If the psi parameter is not a valid vector input.
    """

    psi = linalg.as_ket(psi)
    
    modules_sum = np.sum(np.abs(psi) ** 2)

    return np.isclose(modules_sum, 1, atol=tol, rtol=0.0)

def is_quantum_state(psi: np.ndarray) -> bool:
    """
    Return a boolean indicating whether a state is a quantum state or not.

    Parameters:
    -----------
    psi: vector state that is check.

    Returns:
    --------
    True: If the state vector represents a quantum state
    False: If the state vector does not represent a quantum state

    Raises:
    -------
    ValueError: If the psi parameter is not a valid vector input
    """

    psi = linalg.as_ket(psi)
    
    return is_normalized_state(psi)

def is_unitary(U: np.ndarray, tol:float = ATOL) -> bool:
    """
    Return a boolean indicating whether a operator matrix is unitary or not.

    Parameters:
    -----------
    U: matrix to be check.
    tol: tolerance needed in funtions that may have not exact values.

    Returns:
    --------
    True: If the matrix is unitary
    False: If the matrix is not unitary

    Raises:
    -------
    ValueError: If the U parameter is not a valid matrix input
    """

    U = np.asarray(U, dtype=complex)

    if U.size == 0:
        raise ValueError("[!] The input matrix could not be empty")
    
    if U.ndim != 2:
        raise ValueError("[!] U must be a two-dimensional matrix.")
    
    if U.shape[0] != U.shape[1]:
        return False
    
    operation = U.conj().T @ U

    return np.allclose(operation, np.identity(U.shape[0]), atol=tol, rtol=0.0)
