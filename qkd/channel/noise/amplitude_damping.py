"""Single-qubit amplitude-damping noise."""

from dataclasses import dataclass, field

import numpy as np

from qkd.channel.base import QuantumChannel, _validate_probability
from qkd.channel.kraus import KrausChannel
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True)
class AmplitudeDampingChannel(QuantumChannel):
    """Standard single-qubit amplitude damping with ``0 <= gamma <= 1``.

    This CPTP model describes relaxation from ``|1>`` to ``|0>``. It is not a
    general model of optical fiber photon loss, which normally introduces a
    vacuum or no-detection outcome outside the logical qubit subspace.
    """

    gamma: float
    _kraus: KrausChannel = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        gamma = _validate_probability(self.gamma, name="gamma")
        object.__setattr__(self, "gamma", gamma)

        operators = (
            np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=np.complex128),
            np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128),
        )
        object.__setattr__(self, "_kraus", KrausChannel(operators))

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply amplitude damping to a single-qubit density matrix."""

        return self._kraus.apply(rho, validate_state=validate_state)
