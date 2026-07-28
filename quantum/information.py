"""Quantum-information metrics for density matrices."""

import numpy as np

from core.constants import DEFAULT_ATOL
from quantum import validation as v
from quantum.types import ArrayLike, ComplexArray


def _as_square_matrix(matrix: ArrayLike, name: str) -> ComplexArray:
    result = np.asarray(matrix, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1] or result.size == 0:
        raise ValueError(f"{name} must be a non-empty square matrix. Got shape={result.shape}.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} entries must be finite.")
    return result


def _prepare_pair(
    rho: ArrayLike,
    sigma: ArrayLike,
    tol: float,
    validate_state: bool,
) -> tuple[ComplexArray, ComplexArray]:
    clean_rho = _as_square_matrix(rho, "rho")
    clean_sigma = _as_square_matrix(sigma, "sigma")

    if clean_rho.shape != clean_sigma.shape:
        raise ValueError(
            "Quantum states must have the same shape. "
            f"Got rho.shape={clean_rho.shape} and sigma.shape={clean_sigma.shape}."
        )

    if validate_state:
        v.validate_density_matrix(clean_rho, tol)
        v.validate_density_matrix(clean_sigma, tol)

    return clean_rho, clean_sigma


def _psd_matrix_sqrt(matrix: ComplexArray, tol: float) -> ComplexArray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    if not np.allclose(matrix, hermitian, atol=tol, rtol=0.0):
        raise ValueError("A positive-semidefinite square root requires a Hermitian matrix.")

    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    minimum = float(np.min(eigenvalues))
    if minimum < -tol:
        raise ValueError(
            "A positive-semidefinite square root received significant negativity. "
            f"Minimum eigenvalue={minimum}."
        )

    eigenvalues = np.clip(eigenvalues, 0.0, None)
    result = (eigenvectors * np.sqrt(eigenvalues)) @ eigenvectors.conj().T
    return np.asarray((result + result.conj().T) / 2.0, dtype=np.complex128)


def _unit_interval(value: float, name: str, tol: float) -> float:
    if value < -tol or value > 1.0 + tol:
        raise ValueError(f"{name} must lie in [0, 1]. Got {value}.")
    return float(np.clip(value, 0.0, 1.0))


def purity(
    rho: ArrayLike,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> float:
    """Return ``Tr(rho^2)``, equal to one exactly for pure states."""

    clean_rho = _as_square_matrix(rho, "rho")
    if validate_state:
        v.validate_density_matrix(clean_rho, tol)

    value = complex(np.trace(clean_rho @ clean_rho))
    if not np.isclose(value.imag, 0.0, atol=tol, rtol=0.0):
        raise ValueError(f"Purity must be real. Got {value}.")
    return _unit_interval(float(value.real), "Purity", tol)


def trace_distance(
    rho: ArrayLike,
    sigma: ArrayLike,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> float:
    """Return half the trace norm of ``rho - sigma``."""

    clean_rho, clean_sigma = _prepare_pair(rho, sigma, tol, validate_state)
    difference = clean_rho - clean_sigma
    hermitian = (difference + difference.conj().T) / 2.0
    if not np.allclose(difference, hermitian, atol=tol, rtol=0.0):
        raise ValueError("Trace distance requires Hermitian density matrices.")

    eigenvalues = np.linalg.eigvalsh(hermitian)
    value = 0.5 * float(np.sum(np.abs(eigenvalues)))
    return _unit_interval(value, "Trace distance", tol)


def fidelity(
    rho: ArrayLike,
    sigma: ArrayLike,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> float:
    """Return squared Uhlmann fidelity between two density matrices.

    This project consistently uses
    ``F(rho, sigma) = (Tr(sqrt(sqrt(rho) sigma sqrt(rho))))^2``.
    """

    clean_rho, clean_sigma = _prepare_pair(rho, sigma, tol, validate_state)
    sqrt_rho = _psd_matrix_sqrt(clean_rho, tol)
    middle = sqrt_rho @ clean_sigma @ sqrt_rho
    middle = np.asarray((middle + middle.conj().T) / 2.0, dtype=np.complex128)
    sqrt_middle = _psd_matrix_sqrt(middle, tol)
    trace_value = complex(np.trace(sqrt_middle))
    if not np.isclose(trace_value.imag, 0.0, atol=tol, rtol=0.0):
        raise ValueError(f"Fidelity square-root trace must be real. Got {trace_value}.")

    value = float(trace_value.real**2)
    return _unit_interval(value, "Fidelity", tol)


def von_neumann_entropy(
    rho: ArrayLike,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> float:
    """Return the von Neumann entropy of ``rho`` in bits."""

    clean_rho = _as_square_matrix(rho, "rho")
    if validate_state:
        v.validate_density_matrix(clean_rho, tol)

    hermitian = (clean_rho + clean_rho.conj().T) / 2.0
    if not np.allclose(clean_rho, hermitian, atol=tol, rtol=0.0):
        raise ValueError("Von Neumann entropy requires a Hermitian density matrix.")

    eigenvalues = np.linalg.eigvalsh(hermitian)
    minimum = float(np.min(eigenvalues))
    if minimum < -tol:
        raise ValueError(
            f"Von Neumann entropy received significant negativity. Minimum eigenvalue={minimum}."
        )

    eigenvalues = np.clip(eigenvalues, 0.0, None)
    positive = eigenvalues[eigenvalues > tol]
    entropy = -float(np.sum(positive * np.log2(positive)))
    if entropy < -tol:
        raise ValueError(f"Von Neumann entropy cannot be negative. Got {entropy}.")
    return max(0.0, entropy)
