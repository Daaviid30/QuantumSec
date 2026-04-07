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



