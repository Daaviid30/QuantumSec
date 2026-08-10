"""Ideal quantum channel."""

from dataclasses import dataclass

import numpy as np

from qkd.channel.base import QuantumChannel, _prepare_density_matrix
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True)
class IdentityChannel(QuantumChannel):
    """Channel that returns an independent copy of the input state."""

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Return the same physical state without aliasing the input array."""

        matrix = _prepare_density_matrix(rho, validate_state=validate_state)
        return np.array(matrix, dtype=np.complex128, copy=True)
