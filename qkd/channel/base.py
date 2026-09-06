"""Base interface and shared input handling for quantum channels."""

from abc import ABC, abstractmethod
from numbers import Real

import numpy as np

from quantum import validation as v
from quantum.types import ArrayLike, ComplexArray


class QuantumChannel(ABC):
    """Interface for composable channel stages acting on density matrices.

    A stage may be deterministic or may own an explicitly injected random
    source. The call contract intentionally exposes no Alice/Bob protocol data.
    """

    @abstractmethod
    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply the channel to a density matrix."""


def _validate_probability(value: float, *, name: str) -> float:
    """Return a finite scalar probability in the closed unit interval."""

    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a real scalar probability. Got {value!r}.")
    probability = float(value)
    if not np.isfinite(probability) or probability < 0.0 or probability > 1.0:
        raise ValueError(f"{name} must satisfy 0 <= {name} <= 1. Got {probability}.")
    return probability


def _prepare_density_matrix(
    rho: ArrayLike,
    *,
    dimension: int | None = None,
    validate_state: bool,
) -> ComplexArray:
    """Convert a channel input and enforce cheap structural invariants."""

    matrix = np.asarray(rho, dtype=np.complex128)
    if matrix.size == 0:
        raise ValueError("A channel input density matrix must not be empty.")
    if matrix.ndim != 2:
        raise ValueError(f"A channel input density matrix must be two-dimensional. Got ndim={matrix.ndim}.")
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"A channel input density matrix must be square. Got shape={matrix.shape}.")
    if dimension is not None and matrix.shape != (dimension, dimension):
        raise ValueError(
            "Channel and state dimensions must match. "
            f"Got channel dimension={dimension} and rho.shape={matrix.shape}."
        )
    if not np.all(np.isfinite(matrix)):
        raise ValueError("Channel input density-matrix entries must be finite.")
    if validate_state:
        v.validate_density_matrix(matrix)
    return matrix
