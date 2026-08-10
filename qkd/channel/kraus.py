"""Reusable operator-sum representation of CPTP quantum channels."""

from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np

from core.constants import DEFAULT_ATOL
from qkd.channel.base import QuantumChannel, _prepare_density_matrix
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True, eq=False, init=False)
class KrausChannel(QuantumChannel):
    """A completely positive trace-preserving map validated at construction."""

    operators: tuple[ComplexArray, ...] = field(repr=False)

    def __init__(self, operators: Sequence[ArrayLike]) -> None:
        """Build a channel from a non-empty complete set of Kraus operators."""

        if len(operators) == 0:
            raise ValueError("A Kraus channel requires at least one operator.")

        clean_operators: list[ComplexArray] = []
        expected_shape: tuple[int, int] | None = None

        for index, operator in enumerate(operators):
            matrix = np.array(operator, dtype=np.complex128, copy=True)
            if matrix.size == 0:
                raise ValueError(f"Kraus operator at index {index} must not be empty.")
            if matrix.ndim != 2:
                raise ValueError(
                    f"Kraus operator at index {index} must be two-dimensional. Got ndim={matrix.ndim}."
                )
            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError(f"Kraus operator at index {index} must be square. Got shape={matrix.shape}.")
            if not np.all(np.isfinite(matrix)):
                raise ValueError(f"Kraus operator entries must be finite. Invalid index={index}.")

            if expected_shape is None:
                expected_shape = matrix.shape
            elif matrix.shape != expected_shape:
                raise ValueError(
                    "All Kraus operators must have the same shape. "
                    f"Expected {expected_shape}, got {matrix.shape} at index {index}."
                )
            clean_operators.append(matrix)

        assert expected_shape is not None
        completeness = np.zeros(expected_shape, dtype=np.complex128)
        for operator in clean_operators:
            completeness += operator.conj().T @ operator

        identity = np.eye(expected_shape[0], dtype=np.complex128)
        if not np.allclose(completeness, identity, atol=DEFAULT_ATOL, rtol=0.0):
            deviation = float(np.max(np.abs(completeness - identity)))
            raise ValueError(
                f"Kraus operators must satisfy sum(K_i^dagger K_i) = I. Maximum deviation={deviation}."
            )

        for operator in clean_operators:
            operator.flags.writeable = False
        object.__setattr__(self, "operators", tuple(clean_operators))

    @property
    def dimension(self) -> int:
        """Return the Hilbert-space dimension acted on by the channel."""

        return self.operators[0].shape[0]

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Evaluate ``sum_i K_i rho K_i^dagger``."""

        matrix = _prepare_density_matrix(
            rho,
            dimension=self.dimension,
            validate_state=validate_state,
        )
        output = np.zeros_like(matrix, dtype=np.complex128)
        for operator in self.operators:
            output += operator @ matrix @ operator.conj().T
        return output
