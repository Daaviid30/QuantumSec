#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

import numpy as np

#=================== CONSTANTS ===================

ATOL = 1e-10

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

    if not np.all(np.isfinite(psi)):
            raise ValueError("[!] Ket amplitudes must be finite.")

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

def inner_product(phi: np.ndarray, psi: np.ndarray) -> complex:
    """Return the inner product <phi|psi> between 2 vectors.

    Parameters:
    -----------
    phi: First of the inner product vectors, here the complex conjugate is applied.
    psi: Second of the inner product vectors.

    Returns:
    --------
    product: A complex escalar that represents the result of the product

    Raises:
    -------
    ValueError: 
        If phi or psi are not valid as ket vectors.
        If phi and psi do not have the same shape
    """

    phi = as_ket(phi)
    psi = as_ket(psi)

    if phi.size != psi.size:
        raise ValueError(
            "[!] The vectors have different sizes:" 
            f"phi size -> {phi.size} and psi size -> {psi.size}.")
    
    return complex(np.vdot(phi, psi))

def outer_product(phi: np.ndarray, psi: np.ndarray) -> np.ndarray:
    """Return the outer product |phi><psi| between 2 vectors.

    Parameters:
    -----------
    phi: First of the outer product vectors.
    psi: Second of the outer product vectors, here the complex conjugate is applied.

    Returns:
    --------
    product: A matrix that represents the result of the product

    Raises:
    -------
    ValueError: 
        If phi or psi are not valid as ket vectors.
        If phi and psi do not have the same shape
    """

    phi = as_ket(phi)
    psi = as_ket(psi)

    if phi.size != psi.size:
        raise ValueError(
            "[!] The vectors have different sizes:" 
            f"phi size -> {phi.size} and psi size -> {psi.size}.")
    
    return np.outer(phi, psi.conj())

def normalize(psi: np.ndarray, tol: float = ATOL) -> np.ndarray:
    """Return the psi vector in a normalized way.

    Parameters:
    -----------
    psi: Vector to be normalize.

    Returns:
    --------
    psi_normalized: The normalized version of psi

    Raises:
    -------
    ValueError: 
        If psi is not a valid ket vector.
        If the norm of the vector psi is 0.
    """
    
    psi = as_ket(psi)

    norm = np.linalg.norm(psi)

    if np.isclose(norm, 0, atol=tol, rtol=0):
        raise ValueError("[!] Psi norm can not be 0.")
    
    return psi / norm

def probabilities_from_ket(psi: np.ndarray, tol: float = ATOL) -> np.ndarray:
    """Returns a probability vector associated with a quantum state measured in
    the computational basis.

    Parameters:
    -----------
    psi: Vector from where the probabilities are calculated.

    Returns:
    --------
    prob_vector: The probability vector of the psi quantum state

    Raises:
    -------
    ValueError: 
        If psi is not a valid quantum state.
    """

    psi = as_ket(psi)

    norm_squared = float(np.vdot(psi, psi).real)

    if not np.isclose(norm_squared, 1.0, atol=tol, rtol=0.0):
        raise ValueError("[!] psi must be normalized.")

    return np.abs(psi) ** 2

