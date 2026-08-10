"""Single-qubit Pauli noise channels."""

from dataclasses import dataclass, field

import numpy as np

from qkd.channel.base import QuantumChannel, _validate_probability
from qkd.channel.kraus import KrausChannel
from qkd.primitives.operations import X, Y, Z
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True)
class PauliChannel(QuantumChannel):
    """Apply an incoherent mixture of the single-qubit Pauli operators.

    The identity probability is ``p_i = 1 - px - py - pz``. Every
    probability must be non-negative, so ``px + py + pz <= 1``.
    """

    px: float
    py: float
    pz: float
    _kraus: KrausChannel = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        px = _validate_probability(self.px, name="px")
        py = _validate_probability(self.py, name="py")
        pz = _validate_probability(self.pz, name="pz")
        total_error_probability = px + py + pz
        if total_error_probability > 1.0:
            raise ValueError(
                "Pauli error probabilities must satisfy px + py + pz <= 1. "
                f"Got total={total_error_probability}."
            )

        object.__setattr__(self, "px", px)
        object.__setattr__(self, "py", py)
        object.__setattr__(self, "pz", pz)

        identity_probability = 1.0 - total_error_probability
        identity = np.eye(2, dtype=np.complex128)
        operators = (
            np.sqrt(identity_probability) * identity,
            np.sqrt(px) * X,
            np.sqrt(py) * Y,
            np.sqrt(pz) * Z,
        )
        object.__setattr__(self, "_kraus", KrausChannel(operators))

    @property
    def pi(self) -> float:
        """Return the implied identity probability."""

        return 1.0 - self.px - self.py - self.pz

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply Pauli noise to a single-qubit density matrix."""

        return self._kraus.apply(rho, validate_state=validate_state)


@dataclass(frozen=True, slots=True)
class BitFlipChannel(QuantumChannel):
    """Single-qubit channel that applies Pauli X with probability ``p``."""

    p: float
    _pauli: PauliChannel = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        channel = PauliChannel(px=self.p, py=0.0, pz=0.0)
        object.__setattr__(self, "p", channel.px)
        object.__setattr__(self, "_pauli", channel)

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply bit-flip noise to a single-qubit density matrix."""

        return self._pauli.apply(rho, validate_state=validate_state)


@dataclass(frozen=True, slots=True)
class PhaseFlipChannel(QuantumChannel):
    """Single-qubit channel that applies Pauli Z with probability ``p``."""

    p: float
    _pauli: PauliChannel = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        channel = PauliChannel(px=0.0, py=0.0, pz=self.p)
        object.__setattr__(self, "p", channel.pz)
        object.__setattr__(self, "_pauli", channel)

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply phase-flip noise to a single-qubit density matrix."""

        return self._pauli.apply(rho, validate_state=validate_state)
