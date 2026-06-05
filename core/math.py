#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

"""
The math module conteins the linear algebra primitives, that includes density matrices, 
tensor products, partial traces, etc. We use this module in order to not call numpy functions 
directly in the code, but through this module. This allows us to change the backend of the 
operations in the future.
"""


# ================== IMPORTATIONS ==================
import numpy as np
import scipy.linalg
from functools import reduce
# ================================================== 

# Global Tolerance
ATOL = 1e-8


# ================================================== 
# 1. BASIC MATRIX & VECTOR UTILITIES
# ================================================== 

def hermitian_conjugate(matrix: np.ndarray) -> np.ndarray:
    """
    Calculates the hermitian conjugate of a matrix or vector.
    
    Args:
        matrix: The matrix or vector to calculate the hermitian conjugate of.
    
    Returns:
        The hermitian conjugate of the matrix.
    """

    return matrix.conj().T

def euclidean_norm(vector: np.ndarray) -> float:
    """
    Calculates the euclidean norm of a vector.
    
    Args:
        vector: The vector to calculate the norm of.
    
    Returns:
        The euclidean norm of the vector.
    """

    return float(np.linalg.norm(vector))

def matrix_trace(matrix: np.ndarray) -> float:
    """
    Calculates the trace of a matrix.
    
    Args:
        matrix: The matrix to calculate the trace of.
    
    Returns:
        The trace of the matrix.
    """

    return np.trace(matrix)


# ================================================== 
# 2. QUANTUM STATES & PROJECTIONS
# ================================================== 

def dm_from_ket(psi: np.ndarray) -> np.ndarray:
    """
    Constructs a density matrix from a pure state ket vector.
    
    Args:
        psi: A 1D or 2D column vector representing the quantum state |psi>.
    
    Returns:
        The density matrix |psi><psi|.
    """
    psi = np.asarray(psi)
    # Ensure it's a 2D column vector for the outer product
    if psi.ndim == 1:
        psi = psi[:, np.newaxis]
    return psi @ hermitian_conjugate(psi)

def dm_from_ensemble(states: list[np.ndarray], probs: list[float]) -> np.ndarray:
    """
    Constructs a density matrix from an ensemble of pure states with given probabilities.
    
    Args:
        states: A list of pure state ket vectors.
        probs: A list of probabilities corresponding to each state.
    
    Returns:
        The mixed density matrix sum(p_i * |psi_i><psi_i|).
    """
    if len(states) != len(probs):
        raise ValueError("The number of states must match the number of probabilities.")
    
    # Initialize a zero matrix of the same shape as a single state's density matrix
    first_dm = dm_from_ket(states[0])
    rho = np.zeros_like(first_dm, dtype=complex)
    
    for state, prob in zip(states, probs):
        rho += prob * dm_from_ket(state)
        
    return rho

def inner_product(phi: np.ndarray, psi: np.ndarray) -> complex:
    """
    Calculates the inner product <phi|psi> between two pure states.
    
    Args:
        phi: The bra state vector.
        psi: The ket state vector.
    
    Returns:
        The complex inner product.
    """
    phi_vec = np.asarray(phi).flatten()
    psi_vec = np.asarray(psi).flatten()
    return np.vdot(phi_vec, psi_vec)

def purity(density_matrix: np.ndarray) -> float:
    """
    Calculates the purity of a density matrix.
    
    Args:
        density_matrix: The density matrix to calculate the purity of.
    
    Returns:
        The purity of the density matrix.
    """

    return np.real(matrix_trace(density_matrix @ density_matrix))


# ================================================== 
# 3. MULTI-QUBIT TRANSFORMATIONS
# ================================================== 

def tensor(*operators: np.ndarray) -> np.ndarray:
    """
    Calculates the tensor product of multiple matrices or vectors.
    
    Args:
        *operators: A variable number of matrices or vectors.
    
    Returns:
        The tensor product of all provided matrices or vectors.
    """
    if not operators:
        raise ValueError("At least one operator must be provided.")
    return reduce(np.kron, operators)

def partial_trace(rho: np.ndarray, dims: list[int], subsystem: int) -> np.ndarray | float:
    """
    Calculates the partial trace of a multipartite density matrix.
    
    Args:
        rho: The density matrix.
        dims: A list specifying the dimensions of each subsystem (e.g. [2, 2] for two qubits).
        subsystem: The index (0-based) of the subsystem to trace out.
        
    Returns:
        The reduced density matrix.
    """
    n_subsystems = len(dims)
    if subsystem < 0 or subsystem >= n_subsystems:
        raise ValueError("Invalid subsystem index")
        
    # Create the reshape dimensions for the input matrix (d1, d2, ..., dn, d1, d2, ..., dn)
    reshape_dims = tuple(dims) + tuple(dims)
    rho_reshaped = rho.reshape(reshape_dims)
    
    # Trace out the specified subsystem using np.trace. 
    # For a tensor A_{i, j, k, l, m, n}, if we trace out the 2nd subsystem (index 1),
    # we trace over indices (1, 1+n_subsystems).
    reduced_rho = np.trace(rho_reshaped, axis1=subsystem, axis2=subsystem + n_subsystems)
    
    # Calculate the new dimension of the reduced matrix
    reduced_dims = dims[:subsystem] + dims[subsystem+1:]
    if not reduced_dims:
        # If all subsystems are traced out (e.g. subsystem=0 and len(dims)=1)
        return np.real(reduced_rho)
        
    new_dim = int(np.prod(reduced_dims))
    return reduced_rho.reshape((new_dim, new_dim))

def matrix_exp(matrix: np.ndarray) -> np.ndarray:
    """
    Calculates the matrix exponential e^M.
    Useful for generating unitary operators from Hamiltonians U = e^{-iHt}.
    
    Args:
        matrix: The matrix to exponentiate.
        
    Returns:
        The exponentiated matrix.
    """
    return scipy.linalg.expm(matrix)


# ================================================== 
# 4. INTEGRITY AND VALIDATION
# ================================================== 

def is_hermitian(matrix: np.ndarray, atol: float = ATOL) -> bool:
    """
    Checks if a matrix is Hermitian (M = M^\dagger).
    
    Args:
        matrix: The matrix to check.
        atol: Absolute tolerance for the numeric comparison.
        
    Returns:
        True if the matrix is Hermitian, False otherwise.
    """
    return np.allclose(matrix, hermitian_conjugate(matrix), atol=atol)

def is_positive_semidefinite(matrix: np.ndarray, atol: float = ATOL) -> bool:
    """
    Checks if a matrix is positive semi-definite (Hermitian and all eigenvalues >= 0).
    
    Args:
        matrix: The matrix to check.
        atol: Absolute tolerance to account for numerical errors (e.g., -1e-9 is considered 0).
        
    Returns:
        True if positive semi-definite, False otherwise.
    """
    if not is_hermitian(matrix, atol):
        return False
        
    eigenvalues = np.linalg.eigvalsh(matrix)
    return bool(np.all(eigenvalues >= -atol))

def is_unitary(matrix: np.ndarray, atol: float = ATOL) -> bool:
    """
    Checks if a matrix is unitary (U U^\dagger = I).
    
    Args:
        matrix: The matrix to check.
        atol: Absolute tolerance for the numeric comparison.
        
    Returns:
        True if unitary, False otherwise.
    """
    identity = np.eye(matrix.shape[0])
    return np.allclose(matrix @ hermitian_conjugate(matrix), identity, atol=atol)

def spectral_decomp(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the spectral decomposition of a Hermitian matrix.
    
    Args:
        matrix: A Hermitian matrix.
        
    Returns:
        A tuple (eigenvalues, eigenvectors).
        eigenvalues: 1D array of eigenvalues.
        eigenvectors: 2D array where the columns are the eigenvectors.
    """
    return np.linalg.eigh(matrix)


# ================================================== 
# 5. CRYPTOGRAPHY METRICS (VULNERABILITIES)
# ================================================== 

def expectation_value(state: np.ndarray, operator: np.ndarray) -> float:
    """
    Calculates the expectation value of an operator given a state.
    For pure states: <psi|O|psi>
    For mixed states: Tr(rho * O)
    
    Args:
        state: A pure state ket vector or a density matrix.
        operator: The observable operator.
    
    Returns:
        The expectation value (should be real for Hermitian operators).
    """
    state = np.asarray(state)
    if state.ndim == 1 or state.shape[1] == 1:
        # Pure state
        phi = state.flatten()
        val = np.vdot(phi, operator @ phi)
    else:
        # Mixed state
        val = matrix_trace(state @ operator)
    return np.real(val)

def fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    """
    Calculates the fidelity between two density matrices.
    Uses the convention F(rho, sigma) = (Tr(sqrt(sqrt(rho) * sigma * sqrt(rho))))^2.
    
    Args:
        rho: First density matrix.
        sigma: Second density matrix.
        
    Returns:
        The fidelity metric (0 to 1).
    """
    # Optimization for pure states: if both are pure, fidelity is simply Tr(rho * sigma)
    # which is computationally much faster than matrix square roots.
    if abs(purity(rho) - 1.0) < ATOL and abs(purity(sigma) - 1.0) < ATOL:
        return np.real(matrix_trace(rho @ sigma))

    sqrt_rho = scipy.linalg.sqrtm(rho)
    # The function might return complex outputs containing tiny imaginary parts
    f_matrix = scipy.linalg.sqrtm(sqrt_rho @ sigma @ sqrt_rho)
    f = matrix_trace(f_matrix)
    return np.real(f)**2

def trace_distance(rho: np.ndarray, sigma: np.ndarray) -> float:
    """
    Calculates the trace distance between two density matrices: 0.5 * ||rho - sigma||_1
    where ||X||_1 = Tr(sqrt(X^dagger * X)).
    
    Args:
        rho: First density matrix.
        sigma: Second density matrix.
        
    Returns:
        The trace distance (0 to 1).
    """
    diff = rho - sigma
    # For Hermitian matrices, the trace norm is the sum of absolute values of eigenvalues.
    eigenvalues = np.linalg.eigvalsh(diff)
    return 0.5 * np.sum(np.abs(eigenvalues))

def von_neumann_entropy(rho: np.ndarray) -> float:
    """
    Calculates the von Neumann entropy of a density matrix: S(rho) = -Tr(rho * log2(rho)).
    
    Args:
        rho: The density matrix.
        
    Returns:
        The von Neumann entropy.
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    entropy = 0.0
    for val in eigenvalues:
        # Ignore zero eigenvalues or small negative ones from numeric noise
        if val > ATOL:
            entropy -= val * np.log2(val)
    return np.real(entropy)
