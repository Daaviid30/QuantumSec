"""Single-qubit depolarizing noise."""

from dataclasses import dataclass, field

import numpy as np

from qkd.channel.base import QuantumChannel, _validate_probability
from qkd.channel.kraus import KrausChannel
from qkd.primitives.operations import X, Y, Z
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True)
class DepolarizingChannel(QuantumChannel):
    """Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``.

    The parameter satisfies ``0 <= p <= 1``. Thus ``p=0`` is the identity
    and ``p=1`` maps every qubit state to the maximally mixed state.
    """

    p: float
    _kraus: KrausChannel = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        probability = _validate_probability(self.p, name="p")
        object.__setattr__(self, "p", probability)

        identity = np.eye(2, dtype=np.complex128)
        operators = (
            np.sqrt(1.0 - 3.0 * probability / 4.0) * identity,
            np.sqrt(probability / 4.0) * X,
            np.sqrt(probability / 4.0) * Y,
            np.sqrt(probability / 4.0) * Z,
        )
        object.__setattr__(self, "_kraus", KrausChannel(operators))

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply depolarizing noise to a single-qubit density matrix."""

        return self._kraus.apply(rho, validate_state=validate_state)
