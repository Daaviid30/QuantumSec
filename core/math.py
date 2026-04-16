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
# ================================================== 


# ================== FUNCTIONS ===================

def hermitian_conjugate(matrix: np.array) -> np.array:
    """
    Calculates the hermitian conjugate of a matrix or vector.
    
    Args:
        matrix: The matrix or vector to calculate the hermitian conjugate of.
    
    Returns:
        The hermitian conjugate of the matrix.
    """

    return np.conjugate(matrix.T)

def euclidean_norm(vector: np.array) -> float:
    """
    Calculates the euclidean norm of a vector.
    
    Args:
        vector: The vector to calculate the norm of.
    
    Returns:
        The euclidean norm of the vector.
    """

    return np.sqrt(hermitian_conjugate(vector) @ vector)[0,0]

def matrix_trace(matrix: np.array) -> float:
    """
    Calculates the trace of a matrix.
    
    Args:
        matrix: The matrix to calculate the trace of.
    
    Returns:
        The trace of the matrix.
    """

    return np.trace(matrix)

def purity(density_matrix: np.array) -> float:
    """
    Calculates the purity of a density matrix.
    
    Args:
        density_matrix: The density matrix to calculate the purity of.
    
    Returns:
        The purity of the density matrix.
    """

    return np.trace(density_matrix @ density_matrix)

def tensor_product(matrix_a: np.array, matrix_b: np.array) -> np.array:
    """
    Calculates the tensor product of two matrices or vectors.
    
    Args:
        matrix_a: The first matrix or vector.
        matrix_b: The second matrix or vector.
    
    Returns:
        The tensor product of the two matrices or vectors.
    """

    return np.kron(matrix_a, matrix_b)

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

def partial_trace(rho: np.ndarray, dims: list[int], subsystem: int) -> np.ndarray:
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
        return float(np.real(reduced_rho))
        
    new_dim = int(np.prod(reduced_dims))
    return reduced_rho.reshape((new_dim, new_dim))

def is_hermitian(matrix: np.ndarray, atol: float = 1e-8) -> bool:
    """
    Checks if a matrix is Hermitian (M = M^\dagger).
    
    Args:
        matrix: The matrix to check.
        atol: Absolute tolerance for the numeric comparison.
        
    Returns:
        True if the matrix is Hermitian, False otherwise.
    """
    return np.allclose(matrix, hermitian_conjugate(matrix), atol=atol)

def is_positive_semidefinite(matrix: np.ndarray, atol: float = 1e-8) -> bool:
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

def is_unitary(matrix: np.ndarray, atol: float = 1e-8) -> bool:
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
    sqrt_rho = scipy.linalg.sqrtm(rho)
    # The function might return complex outputs containing tiny imaginary parts
    f_matrix = scipy.linalg.sqrtm(sqrt_rho @ sigma @ sqrt_rho)
    f = matrix_trace(f_matrix)
    return float(np.real(f))**2

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
    return float(0.5 * np.sum(np.abs(eigenvalues)))

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
        if val > 1e-12:
            entropy -= val * np.log2(val)
    return float(np.real(entropy))
