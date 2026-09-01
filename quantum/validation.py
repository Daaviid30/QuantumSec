"""Validation helpers for quantum states, operators, and measurements."""

from collections.abc import Sequence

import numpy as np

from core.constants import DEFAULT_ATOL
from quantum import linalg
from quantum.types import ArrayLike


def _error_probability_state(probs: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
    try:
        probabilities = linalg.as_ket(probs)
    except (TypeError, ValueError) as error:
        return str(error)
    if np.any(np.abs(np.imag(probabilities)) > tol):
        return f"Probability entries must be real. Got {probabilities}."

    real_probabilities = np.real(probabilities)
    if np.any(real_probabilities < -tol):
        return f"Probability entries must be non-negative. Got {real_probabilities}."

    total = float(np.sum(real_probabilities))
    if not np.isclose(total, 1.0, atol=tol, rtol=0.0):
        return f"Probabilities must sum to one. Got total={total}."
    return None


def is_probability_state(probs: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an input is a finite probability distribution."""

    return _error_probability_state(probs, tol) is None


def validate_probability_state(probs: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate a finite, real, non-negative probability distribution."""

    error = _error_probability_state(probs, tol)
    if error is not None:
        raise ValueError(error)


def _error_normalized_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
    try:
        state = linalg.as_ket(psi)
    except (TypeError, ValueError) as error:
        return str(error)
    norm_squared = float(np.sum(np.abs(state) ** 2))
    if not np.isclose(norm_squared, 1.0, atol=tol, rtol=0.0):
        return f"A quantum-state ket must have unit norm. Got norm_squared={norm_squared}."
    return None


def is_normalized_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an input is a finite ket with unit norm."""

    return _error_normalized_state(psi, tol) is None


def validate_normalized_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate that a well-formed ket has unit norm."""

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)


def is_quantum_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an input represents a normalized pure state."""

    return _error_normalized_state(psi, tol) is None


def validate_quantum_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate that a ket represents a normalized pure quantum state."""

    error = _error_normalized_state(psi, tol)
    if error is not None:
        raise ValueError(error)


def _error_unitary(operator: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
    matrix = np.asarray(operator, dtype=np.complex128)
    if matrix.size == 0:
        return "A unitary operator must not be empty."
    if matrix.ndim != 2:
        return f"A unitary operator must be two-dimensional. Got ndim={matrix.ndim}."
    if matrix.shape[0] != matrix.shape[1]:
        return f"A unitary operator must be square. Got shape={matrix.shape}."
    if not np.all(np.isfinite(matrix)):
        return "Unitary-operator entries must be finite."

    product = matrix.conj().T @ matrix
    identity = np.eye(matrix.shape[0], dtype=np.complex128)
    if not np.allclose(product, identity, atol=tol, rtol=0.0):
        deviation = float(np.max(np.abs(product - identity)))
        return f"The operator is not unitary: U^dagger U differs from I by up to {deviation}."
    return None


def is_unitary(operator: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an array is a finite square unitary operator.

    Structurally malformed numerical arrays return ``False``. Conversion failures
    from incompatible Python objects may raise ``TypeError`` or ``ValueError``.
    """

    return _error_unitary(operator, tol) is None


def validate_unitary(operator: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate that an array is a finite square unitary operator."""

    error = _error_unitary(operator, tol)
    if error is not None:
        raise ValueError(error)


def _error_density_matrix(rho: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
    matrix = np.asarray(rho, dtype=np.complex128)
    if matrix.size == 0:
        return "A density matrix must not be empty."
    if matrix.ndim != 2:
        return f"A density matrix must be two-dimensional. Got ndim={matrix.ndim}."
    if matrix.shape[0] != matrix.shape[1]:
        return f"A density matrix must be square. Got shape={matrix.shape}."
    if not np.all(np.isfinite(matrix)):
        return "Density-matrix entries must be finite."
    if not np.allclose(matrix, matrix.conj().T, atol=tol, rtol=0.0):
        deviation = float(np.max(np.abs(matrix - matrix.conj().T)))
        return f"A density matrix must be Hermitian. Maximum deviation={deviation}."

    trace = complex(np.trace(matrix))
    if not np.isclose(trace, 1.0, atol=tol, rtol=0.0):
        return f"A density matrix must have unit trace. Got trace={trace}."

    eigenvalues = np.linalg.eigvalsh(matrix)
    minimum = float(np.min(eigenvalues))
    if minimum < -tol:
        return f"A density matrix must be positive semidefinite. Minimum eigenvalue={minimum}."
    return None


def is_density_matrix(rho: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an array is a physical density matrix.

    Structurally malformed numerical arrays return ``False``. Conversion failures
    from incompatible Python objects may raise ``TypeError`` or ``ValueError``.
    """

    return _error_density_matrix(rho, tol) is None


def validate_density_matrix(rho: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate Hermiticity, unit trace, and positive semidefiniteness."""

    error = _error_density_matrix(rho, tol)
    if error is not None:
        raise ValueError(error)


def _error_projector(projector: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
    matrix = np.asarray(projector, dtype=np.complex128)
    if matrix.size == 0:
        return "A projector must not be empty."
    if matrix.ndim != 2:
        return f"A projector must be two-dimensional. Got ndim={matrix.ndim}."
    if matrix.shape[0] != matrix.shape[1]:
        return f"A projector must be square. Got shape={matrix.shape}."
    if not np.all(np.isfinite(matrix)):
        return "Projector entries must be finite."
    if not np.allclose(matrix, matrix.conj().T, atol=tol, rtol=0.0):
        deviation = float(np.max(np.abs(matrix - matrix.conj().T)))
        return f"A projector must be Hermitian. Maximum deviation={deviation}."

    square = matrix @ matrix
    if not np.allclose(square, matrix, atol=tol, rtol=0.0):
        deviation = float(np.max(np.abs(square - matrix)))
        return f"A projector must be idempotent. Maximum deviation={deviation}."
    return None


def is_projector(projector: ArrayLike, tol: float = DEFAULT_ATOL) -> bool:
    """Return whether an array is a finite square orthogonal projector.

    Structurally malformed numerical arrays return ``False``. Conversion failures
    from incompatible Python objects may raise ``TypeError`` or ``ValueError``.
    """

    return _error_projector(projector, tol) is None


def validate_projector(projector: ArrayLike, tol: float = DEFAULT_ATOL) -> None:
    """Validate that an array is a finite Hermitian idempotent projector."""

    error = _error_projector(projector, tol)
    if error is not None:
        raise ValueError(error)


def _error_projective_measurement(
    projectors: Sequence[ArrayLike],
    tol: float = DEFAULT_ATOL,
) -> str | None:
    if len(projectors) == 0:
        return "A projective measurement requires at least one projector."

    clean_projectors: list[np.ndarray] = []
    expected_shape: tuple[int, int] | None = None

    for index, projector in enumerate(projectors):
        matrix = np.asarray(projector, dtype=np.complex128)
        error = _error_projector(matrix, tol)
        if error is not None:
            return f"Invalid projector at index {index}: {error}"

        if expected_shape is None:
            expected_shape = matrix.shape
        elif matrix.shape != expected_shape:
            return (
                "All projectors must have the same shape. "
                f"Expected {expected_shape}, got {matrix.shape} at index {index}."
            )
        clean_projectors.append(matrix)

    assert expected_shape is not None
    projector_sum = np.sum(clean_projectors, axis=0, dtype=np.complex128)
    identity = np.eye(expected_shape[0], dtype=np.complex128)
    if not np.allclose(projector_sum, identity, atol=tol, rtol=0.0):
        deviation = float(np.max(np.abs(projector_sum - identity)))
        return (
            "A complete projective measurement must satisfy sum(P_i) = I. "
            f"Dimension={expected_shape[0]}, maximum deviation={deviation}."
        )
    return None


def is_projective_measurement(
    projectors: Sequence[ArrayLike],
    tol: float = DEFAULT_ATOL,
) -> bool:
    """Return whether a sequence is a complete projective measurement.

    Invalid numerical projectors return ``False``. Conversion failures from
    incompatible Python objects may raise ``TypeError`` or ``ValueError``.
    """

    return _error_projective_measurement(projectors, tol) is None


def validate_projective_measurement(
    projectors: Sequence[ArrayLike],
    tol: float = DEFAULT_ATOL,
) -> None:
    """Validate individual projectors, common dimension, and completeness."""

    error = _error_projective_measurement(projectors, tol)
    if error is not None:
        raise ValueError(error)
