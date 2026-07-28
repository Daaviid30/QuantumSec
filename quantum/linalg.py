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
    """
    Convert a vector into the canonical one-dimensional ket representation.

    Parameters:
    -----------
    psi: np.ndarray
        Vector with shape (n,) or column-vector shape (n, 1).

    Returns:
    --------
    np.ndarray
        Non-empty complex vector with shape (n,).

    Raises:
    -------
    ValueError
        If psi is empty, non-finite, or does not have an accepted ket shape.
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
    """
    Calculate the complex inner product <phi|psi> between two kets.

    Parameters:
    -----------
    phi: np.ndarray
        Ket whose complex conjugate is applied.
    psi: np.ndarray
        Ket multiplied by the conjugate of phi.

    Returns:
    --------
    complex
        Scalar inner product of phi and psi.

    Raises:
    -------
    ValueError
        If either input is not a valid ket or their dimensions differ.
    """

    phi = as_ket(phi)
    psi = as_ket(psi)

    if phi.size != psi.size:
        raise ValueError(
            "[!] The vectors have different sizes:" 
            f"phi size -> {phi.size} and psi size -> {psi.size}.")
    
    return complex(np.vdot(phi, psi))

def outer_product(phi: np.ndarray, psi: np.ndarray) -> np.ndarray:
    """
    Calculate the outer product |phi><psi| between two kets.

    Parameters:
    -----------
    phi: np.ndarray
        Ket placed on the left side of the product.
    psi: np.ndarray
        Ket whose complex conjugate is placed on the right side.

    Returns:
    --------
    np.ndarray
        Complex matrix representing |phi><psi|.

    Raises:
    -------
    ValueError
        If either input is not a valid ket or their dimensions differ.
    """

    phi = as_ket(phi)
    psi = as_ket(psi)

    if phi.size != psi.size:
        raise ValueError(
            "[!] The vectors have different sizes:" 
            f"phi size -> {phi.size} and psi size -> {psi.size}.")
    
    return np.outer(phi, psi.conj())

def normalize(psi: np.ndarray, tol: float = ATOL) -> np.ndarray:
    """
    Normalize a ket to unit Euclidean norm.

    Parameters:
    -----------
    psi: np.ndarray
        Ket to normalize.
    tol: float
        Absolute tolerance below which the norm is treated as zero.

    Returns:
    --------
    np.ndarray
        Canonical one-dimensional ket with unit norm.

    Raises:
    -------
    ValueError
        If psi is not a valid ket or its norm is zero within tolerance.
    """
    
    psi = as_ket(psi)

    norm = np.linalg.norm(psi)

    if np.isclose(norm, 0, atol=tol, rtol=0):
        raise ValueError("[!] Psi norm can not be 0.")
    
    return psi / norm

def probabilities_from_ket(psi: np.ndarray, tol: float = ATOL) -> np.ndarray:
    """
    Calculate computational-basis probabilities for a normalized ket.

    Parameters:
    -----------
    psi: np.ndarray
        Normalized quantum-state ket.
    tol: float
        Absolute tolerance used when checking normalization.

    Returns:
    --------
    np.ndarray
        Real vector containing the squared magnitude of each amplitude.

    Raises:
    -------
    ValueError
        If psi is not a valid ket or is not normalized within tolerance.
    """

    psi = as_ket(psi)

    norm_squared = float(np.vdot(psi, psi).real)

    if not np.isclose(norm_squared, 1.0, atol=tol, rtol=0.0):
        raise ValueError("[!] psi must be normalized.")

    return np.abs(psi) ** 2

