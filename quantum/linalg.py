"""Linear-algebra helpers for finite-dimensional quantum systems."""

import numpy as np

from core.constants import DEFAULT_ATOL
from quantum.types import ArrayLike, ComplexArray, RealArray


def as_ket(psi: ArrayLike) -> ComplexArray:
    """Convert an array-like vector to a finite one-dimensional complex ket.

    Accepted shapes are ``(n,)`` and the column-vector form ``(n, 1)``.
    """

    ket = np.asarray(psi, dtype=np.complex128)
    if not np.all(np.isfinite(ket)):
        raise ValueError("Ket amplitudes must be finite.")
    if ket.ndim == 1:
        if ket.size == 0:
            raise ValueError("A ket must not be empty.")
        return ket
    if ket.ndim == 2 and ket.shape[1] == 1:
        if ket.size == 0:
            raise ValueError("A ket must not be empty.")
        return ket[:, 0]
    raise ValueError(f"A ket must have shape (n,) or (n, 1). Got shape={ket.shape}.")


def inner_product(phi: ArrayLike, psi: ArrayLike) -> complex:
    """Return the complex inner product ``<phi|psi>`` between equal-size kets."""

    clean_phi = as_ket(phi)
    clean_psi = as_ket(psi)
    if clean_phi.size != clean_psi.size:
        raise ValueError(
            "Inner-product kets must have the same dimension. "
            f"Got phi.size={clean_phi.size} and psi.size={clean_psi.size}."
        )
    return complex(np.vdot(clean_phi, clean_psi))


def outer_product(phi: ArrayLike, psi: ArrayLike) -> ComplexArray:
    """Return the outer product ``|phi><psi|`` between equal-size kets."""

    clean_phi = as_ket(phi)
    clean_psi = as_ket(psi)
    if clean_phi.size != clean_psi.size:
        raise ValueError(
            "Outer-product kets must have the same dimension. "
            f"Got phi.size={clean_phi.size} and psi.size={clean_psi.size}."
        )
    return np.asarray(np.outer(clean_phi, clean_psi.conj()), dtype=np.complex128)


def normalize(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> ComplexArray:
    """Return a ket normalized to unit Euclidean norm."""

    ket = as_ket(psi)
    norm = float(np.linalg.norm(ket))
    if np.isclose(norm, 0.0, atol=tol, rtol=0.0):
        raise ValueError(f"A ket cannot be normalized from zero norm. Got norm={norm}.")
    return np.asarray(ket / norm, dtype=np.complex128)


def probabilities_from_ket(
    psi: ArrayLike,
    tol: float = DEFAULT_ATOL,
) -> RealArray:
    """Return computational-basis probabilities for a normalized ket."""

    ket = as_ket(psi)
    norm_squared = float(np.vdot(ket, ket).real)
    if not np.isclose(norm_squared, 1.0, atol=tol, rtol=0.0):
        raise ValueError(f"A probability ket must have unit norm. Got norm_squared={norm_squared}.")
    return np.asarray(np.abs(ket) ** 2, dtype=np.float64)
