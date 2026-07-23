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

def _error_probability_state(probs: np.ndarray, tol: float = ATOL) -> str | None:

    probs = linalg.as_ket(probs)

    if not np.all(np.isreal(probs)):
        return "[!] Some entries are not real."

    probs = np.real(probs)

    if np.any(probs < -tol): # Equivalent to < 0.0
        return "[!] Vector entries must be non-negative"

    if not np.isclose(np.sum(probs), 1, atol=tol, rtol=0):
        return "[!] The sum of entries is not 1"

    return None

def is_probability_state(probs: np.ndarray, tol: float = ATOL) -> bool:
    """
    Return a boolean indicating whether a vector is a probability state or not.

    Parameters:
    -----------
    probs: vector state that is check.

    Raises:
    -------
    ValueError: If the probs parameter is not a valid vector input.
    """

    return _error_probability_state(probs, tol) is None

def validate_probability_state(probs: np.ndarray, tol: float = ATOL) -> None:
    """
    Parameters:
    -----------
    probs: vector state that is check.

    Raises:
    -------
    ValueError: If the probs parameter is not a valid vector input.
    """

    error = _error_probability_state(probs, tol)
    if error is not None:
        raise ValueError(error)

def _error_normalized_state(psi: np.ndarray, tol:float = ATOL) -> str | None:

    psi = linalg.as_ket(psi)
    
    modules_sum = np.sum(np.abs(psi) ** 2)

    if not np.isclose(modules_sum, 1, atol=tol, rtol=0.0):
        return "[!] The state is not normalized."

    return None

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

    return _error_normalized_state(psi, tol) is None

def validate_normalized_state(psi: np.ndarray, tol:float = ATOL) -> None:
    """
    Parameters:
    -----------
    psi: vector state that is check.
    tol: tolerance needed in funtions that may have not exact values.

    Raises:
    -------
    ValueError: If the psi parameter is not a valid vector input.
    """

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)

def is_quantum_state(psi: np.ndarray, tol:float = ATOL) -> bool:
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

    return _error_normalized_state(psi, tol) is None

def validate_quantum_state(psi: np.ndarray, tol:float = ATOL) -> None:
    """
    Parameters:
    -----------
    psi: vector state that is check.

    Raises:
    -------
    ValueError: If the psi parameter is not a valid vector input
    """

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)

def _error_unitary(U: np.ndarray, tol:float = ATOL) -> str | None:

    U = np.asarray(U, dtype=complex)

    if U.size == 0:
        return "[!] The input matrix could not be empty"
    
    if U.ndim != 2:
        return "[!] U must be a two-dimensional matrix."
    
    if U.shape[0] != U.shape[1]:
        return "[!] U is not a square matrix."

    if not np.all(np.isfinite(U)):
        return "[!] Matrix entries must be finite."
    
    operation = U.conj().T @ U

    if not np.allclose(operation, np.identity(U.shape[0]), atol=tol, rtol=0.0):
        return "[!] U is not an unitary matrix, U†U is not equal to I."

    return None

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

    return _error_unitary(U, tol) is None

def validate_unitary(U: np.ndarray, tol:float = ATOL) -> None:
    """
    Parameters:
    -----------
    U: matrix to be check.
    tol: tolerance needed in funtions that may have not exact values.

    Raises:
    -------
    ValueError: If the U parameter is not a valid matrix input
    """

    error = _error_unitary(U, tol)
    if error is not None:
        raise ValueError(error)
