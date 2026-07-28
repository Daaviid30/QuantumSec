#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES ================

from collections.abc import Sequence

import numpy as np

from quantum import linalg

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== FUNCTIONS ===================

def _error_probability_state(probs: np.ndarray, tol: float = ATOL) -> str | None:
    """
    Inspect whether a vector defines a valid probability distribution.

    Parameters:
    -----------
    probs: np.ndarray
        Probability vector to inspect.
    tol: float
        Absolute tolerance for non-negativity and normalization checks.

    Returns:
    --------
    str | None
        Validation error message, or None when probs is valid.

    Raises:
    -------
    ValueError
        If probs is not a valid finite ket-shaped vector.
    """

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
    Check whether a vector defines a valid probability distribution.

    Parameters:
    -----------
    probs: np.ndarray
        Probability vector to check.
    tol: float
        Absolute tolerance for non-negativity and normalization checks.

    Returns:
    --------
    bool
        True when probs is a valid probability vector; otherwise False.

    Raises:
    -------
    ValueError
        If probs is not a valid finite ket-shaped vector.
    """

    return _error_probability_state(probs, tol) is None

def validate_probability_state(probs: np.ndarray, tol: float = ATOL) -> None:
    """
    Validate that a vector defines a probability distribution.

    Parameters:
    -----------
    probs: np.ndarray
        Probability vector to validate.
    tol: float
        Absolute tolerance for non-negativity and normalization checks.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If probs is malformed, complex, negative, or does not sum to one.
    """

    error = _error_probability_state(probs, tol)
    if error is not None:
        raise ValueError(error)

def _error_normalized_state(psi: np.ndarray, tol:float = ATOL) -> str | None:
    """
    Inspect whether a ket is normalized to unit norm.

    Parameters:
    -----------
    psi: np.ndarray
        Quantum-state ket to inspect.
    tol: float
        Absolute tolerance for the normalization check.

    Returns:
    --------
    str | None
        Validation error message, or None when psi is normalized.

    Raises:
    -------
    ValueError
        If psi is not a valid finite ket-shaped vector.
    """

    psi = linalg.as_ket(psi)
    
    modules_sum = np.sum(np.abs(psi) ** 2)

    if not np.isclose(modules_sum, 1, atol=tol, rtol=0.0):
        return "[!] The state is not normalized."

    return None

def is_normalized_state(psi: np.ndarray, tol:float = ATOL) -> bool:
    """
    Check whether a quantum-state ket has unit norm.

    Parameters:
    -----------
    psi: np.ndarray
        Quantum-state ket to check.
    tol: float
        Absolute tolerance for the normalization check.

    Returns:
    --------
    bool
        True when psi is normalized; otherwise False.

    Raises:
    -------
    ValueError
        If psi is not a valid finite ket-shaped vector.
    """

    return _error_normalized_state(psi, tol) is None

def validate_normalized_state(psi: np.ndarray, tol:float = ATOL) -> None:
    """
    Validate that a quantum-state ket has unit norm.

    Parameters:
    -----------
    psi: np.ndarray
        Quantum-state ket to validate.
    tol: float
        Absolute tolerance for the normalization check.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If psi is malformed, non-finite, or not normalized.
    """

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)

def is_quantum_state(psi: np.ndarray, tol:float = ATOL) -> bool:
    """
    Check whether a ket represents a valid pure quantum state.

    Parameters:
    -----------
    psi: np.ndarray
        Quantum-state ket to check.
    tol: float
        Absolute tolerance for the normalization check.

    Returns:
    --------
    bool
        True when psi is a normalized ket; otherwise False.

    Raises:
    -------
    ValueError
        If psi is not a valid finite ket-shaped vector.
    """

    return _error_normalized_state(psi, tol) is None

def validate_quantum_state(psi: np.ndarray, tol:float = ATOL) -> None:
    """
    Validate that a ket represents a pure quantum state.

    Parameters:
    -----------
    psi: np.ndarray
        Quantum-state ket to validate.
    tol: float
        Absolute tolerance for the normalization check.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If psi is malformed, non-finite, or not normalized.
    """

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)

def _error_unitary(U: np.ndarray, tol:float = ATOL) -> str | None:
    """
    Inspect whether a matrix is square, finite, and unitary.

    Parameters:
    -----------
    U: np.ndarray
        Operator matrix to inspect.
    tol: float
        Absolute tolerance for the unitarity check.

    Returns:
    --------
    str | None
        Validation error message, or None when U is unitary.

    Raises:
    -------
    ValueError
        If U cannot be converted to a complex NumPy array.
    """

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
    Check whether a matrix represents a unitary operator.

    Parameters:
    -----------
    U: np.ndarray
        Operator matrix to check.
    tol: float
        Absolute tolerance for the unitarity check.

    Returns:
    --------
    bool
        True when U is square, finite, and unitary; otherwise False.

    Raises:
    -------
    ValueError
        If U cannot be converted to a complex NumPy array.
    """

    return _error_unitary(U, tol) is None

def validate_unitary(U: np.ndarray, tol:float = ATOL) -> None:
    """
    Validate that a matrix represents a unitary operator.

    Parameters:
    -----------
    U: np.ndarray
        Operator matrix to validate.
    tol: float
        Absolute tolerance for the unitarity check.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If U is malformed, non-finite, non-square, or not unitary.
    """

    error = _error_unitary(U, tol)
    if error is not None:
        raise ValueError(error)

def _error_density_matrix(rho: np.ndarray, tol:float = ATOL) -> str | None:
    """
    Inspect whether a matrix satisfies the density-matrix conditions.

    Parameters:
    -----------
    rho: np.ndarray
        Candidate density matrix to inspect.
    tol: float
        Absolute tolerance for physical-validity checks.

    Returns:
    --------
    str | None
        Validation error message, or None when rho is a density matrix.

    Raises:
    -------
    ValueError
        If rho cannot be converted to a complex NumPy array.
    """

    rho = np.asarray(rho, dtype=complex)

    if rho.size == 0:
        return "[!] The input matrix could not be empty"
    
    if rho.ndim != 2:
        return "[!] rho must be a two-dimensional matrix."
    
    if rho.shape[0] != rho.shape[1]:
        return "[!] rho is not a square matrix."

    if not np.all(np.isfinite(rho)):
        return "[!] Matrix entries must be finite."
    
    hermitian = rho.conj().T

    if not np.allclose(hermitian, rho, atol=tol, rtol=0.0):
        return "[!] rho is not a hermitian matrix."

    trace = np.trace(rho)

    if not np.isclose(trace, 1, atol=tol, rtol=0.0):
        return f"[!] rho trace must be 1. rho trace value is: {trace}"

    eigenvalues = np.linalg.eigvalsh(rho)

    if not np.all(eigenvalues >= -tol):
        return "[!] The matrix is not positive semi-definite."

    return None

def is_density_matrix(rho: np.ndarray, tol:float = ATOL) -> bool:
    """
    Check whether a matrix represents a physical quantum state.

    Parameters:
    -----------
    rho: np.ndarray
        Candidate density matrix to check.
    tol: float
        Absolute tolerance for physical-validity checks.

    Returns:
    --------
    bool
        True when rho is Hermitian, positive semidefinite, and has unit trace.

    Raises:
    -------
    ValueError
        If rho cannot be converted to a complex NumPy array.
    """

    return _error_density_matrix(rho, tol) is None

def validate_density_matrix(rho: np.ndarray, tol:float = ATOL) -> None:
    """
    Validate that a matrix represents a physical quantum state.

    Parameters:
    -----------
    rho: np.ndarray
        Candidate density matrix to validate.
    tol: float
        Absolute tolerance for physical-validity checks.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If rho is malformed, non-Hermitian, not positive semidefinite, or lacks unit trace.
    """

    error = _error_density_matrix(rho, tol)
    if error is not None:
        raise ValueError(error)

def _error_projector(projector: np.ndarray, tol: float = ATOL) -> str | None:
    """
    Inspect whether a matrix is an orthogonal projector.

    Parameters:
    -----------
    projector: np.ndarray
        Candidate projector matrix to inspect.
    tol: float
        Absolute tolerance for Hermiticity and idempotence checks.

    Returns:
    --------
    str | None
        Validation error message, or None when projector is valid.

    Raises:
    -------
    ValueError
        If projector cannot be converted to a complex NumPy array.
    """

    projector = np.asarray(projector, dtype=complex)

    if projector.size == 0:
        return "[!] The proyector must not be empty"

    if projector.ndim != 2:
        return f"[!] The projector should be a bi-dimensional matrix.\
            Projector dimensions: {projector.ndim}"

    if projector.shape[0] != projector.shape[1]:
        return f"[!] The projector must be a square matrix\
            Projector shape: {projector.shape}"

    if not np.all(np.isfinite(projector)):
        return "[!] The projector entries must be finite."

    hermitian = projector.conj().T

    if not np.allclose(hermitian, projector, atol=tol, rtol=0.0):
        return "[!] The projector must be a hermitian matrix."

    square = projector @ projector

    if not np.allclose(square, projector, atol=tol, rtol=0.0):
        return "[!] The projecctor must be idempotent."

    return None

def is_projector(projector: np.ndarray, tol:float = ATOL) -> bool:
    """
    Check whether a matrix is an orthogonal projector.

    Parameters:
    -----------
    projector: np.ndarray
        Candidate projector matrix to check.
    tol: float
        Absolute tolerance for Hermiticity and idempotence checks.

    Returns:
    --------
    bool
        True when projector is square, finite, Hermitian, and idempotent.

    Raises:
    -------
    ValueError
        If projector cannot be converted to a complex NumPy array.
    """

    return _error_projector(projector, tol) is None

def validate_projector(projector: np.ndarray, tol:float = ATOL) -> None:
    """
    Validate that a matrix is an orthogonal projector.

    Parameters:
    -----------
    projector: np.ndarray
        Candidate projector matrix to validate.
    tol: float
        Absolute tolerance for Hermiticity and idempotence checks.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If projector is malformed, non-finite, non-Hermitian, or not idempotent.
    """

    error = _error_projector(projector, tol)
    if error is not None:
        raise ValueError(error)

def _error_projective_measurement(projectors: Sequence[np.ndarray], tol: float = ATOL) -> str | None:
    """
    Inspect whether a sequence forms a complete projective measurement.

    Parameters:
    -----------
    projectors: Sequence[np.ndarray]
        Candidate orthogonal projectors with a common dimension.
    tol: float
        Absolute tolerance for projector and completeness checks.

    Returns:
    --------
    str | None
        Validation error message, or None when the measurement is valid.

    Raises:
    -------
    ValueError
        If a projector cannot be converted to a complex NumPy array.
    """
    if len(projectors) == 0:
        return "[!] A projective measurement requires at least one projector."

    clean_projectors: list[np.ndarray] = []
    expected_shape: tuple[int, int] | None = None

    for index, projector in enumerate(projectors):
        projector = np.asarray(
            projector,
            dtype=np.complex128,
        )

        try:
            validate_projector(projector, tol)
        except ValueError as exc:
            return f"Invalid projector at index {index}: {exc}"

        if expected_shape is None:
            expected_shape = projector.shape
        elif projector.shape != expected_shape:
            return (
                "All projectors must have the same shape. "
                f"Expected {expected_shape}, got {projector.shape} "
                f"at index {index}."
            )

        clean_projectors.append(projector)

    assert expected_shape is not None

    projector_sum = np.zeros(
        expected_shape,
        dtype=np.complex128,
    )

    for projector in clean_projectors:
        projector_sum += projector

    identity = np.eye(
        expected_shape[0],
        dtype=np.complex128,
    )

    if not np.allclose(
        projector_sum,
        identity,
        atol=tol,
        rtol=0.0,
    ):
        return "[!] Projective measurement must satisfy sum(P_i) = I."

    return None

def is_projective_measurement(projectors: Sequence[np.ndarray], tol: float = ATOL) -> bool:
    """
    Check whether a sequence forms a complete projective measurement.

    Parameters:
    -----------
    projectors: Sequence[np.ndarray]
        Candidate orthogonal projectors with a common dimension.
    tol: float
        Absolute tolerance for projector and completeness checks.

    Returns:
    --------
    bool
        True when all projectors are valid and their sum is the identity.

    Raises:
    -------
    ValueError
        If a projector cannot be converted to a complex NumPy array.
    """

    return _error_projective_measurement is None

def validate_projective_measurement(projectors: Sequence[np.ndarray], tol: float = ATOL) -> None:
    """
    Validate that a sequence forms a complete projective measurement.

    Parameters:
    -----------
    projectors: Sequence[np.ndarray]
        Candidate orthogonal projectors with a common dimension.
    tol: float
        Absolute tolerance for projector and completeness checks.

    Returns:
    --------
    None.

    Raises:
    -------
    ValueError
        If a projector is invalid, dimensions differ, or the projectors are incomplete.
    """

    error = _error_projective_measurement(projectors, tol)
    if error is not None:
        raise ValueError(error)
