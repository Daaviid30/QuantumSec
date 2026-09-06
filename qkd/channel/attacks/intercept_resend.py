"""Seeded stochastic intercept-resend attack for logical-qubit BB84 signals."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Literal

import numpy as np

from core.rng import BaseRNG, random_basis
from qkd.channel.base import QuantumChannel, _prepare_density_matrix, _validate_probability
from qkd.primitives.bases import Basis, basis_from_bit
from qkd.primitives.measurements import MEASUREMENTS_BY_BASIS
from qkd.primitives.states import KET0, KET1, MINUS, PLUS
from quantum.measures import sample_projective_outcome
from quantum.states import dm_from_ket
from quantum.types import ArrayLike, ComplexArray


def _immutable_density(ket: ArrayLike) -> ComplexArray:
    density = dm_from_ket(ket)
    density.flags.writeable = False
    return density


_RESENT_STATES = MappingProxyType(
    {
        (Basis.Z, 0): _immutable_density(KET0),
        (Basis.Z, 1): _immutable_density(KET1),
        (Basis.X, 0): _immutable_density(PLUS),
        (Basis.X, 1): _immutable_density(MINUS),
    }
)


@dataclass(frozen=True, slots=True)
class AttackDiagnostics:
    """Small immutable snapshot of simulator-only attack observations."""

    intercept_fraction: float
    n_signals_seen: int
    n_intercepted: int
    eve_z_measurements: int
    eve_x_measurements: int
    eve_zero_outcomes: int
    eve_one_outcomes: int
    attack_type: Literal["intercept_resend"] = field(default="intercept_resend", init=False)

    def __post_init__(self) -> None:
        fraction = _validate_probability(self.intercept_fraction, name="intercept_fraction")
        names = (
            "n_signals_seen",
            "n_intercepted",
            "eve_z_measurements",
            "eve_x_measurements",
            "eve_zero_outcomes",
            "eve_one_outcomes",
        )
        counts: dict[str, int] = {}
        for name in names:
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
            clean = int(value)
            if clean < 0:
                raise ValueError(f"{name} must be non-negative. Got {clean}.")
            counts[name] = clean
        if counts["n_intercepted"] > counts["n_signals_seen"]:
            raise ValueError("n_intercepted cannot exceed n_signals_seen.")
        if counts["eve_z_measurements"] + counts["eve_x_measurements"] != counts["n_intercepted"]:
            raise ValueError("Eve basis counts must sum to n_intercepted.")
        if counts["eve_zero_outcomes"] + counts["eve_one_outcomes"] != counts["n_intercepted"]:
            raise ValueError("Eve outcome counts must sum to n_intercepted.")
        object.__setattr__(self, "intercept_fraction", fraction)
        for name, value in counts.items():
            object.__setattr__(self, name, value)


class InterceptResendAttack(QuantumChannel):
    """Measure selected signals in a random BB84 basis and resend fresh states.

    The stage receives only a density matrix. It has no access to Alice's bit or
    basis, Bob's future basis, parameter estimation, or abort decisions.
    Diagnostics are cumulative for the lifetime of this attack instance.
    """

    __slots__ = (
        "intercept_fraction",
        "_rng",
        "_n_signals_seen",
        "_n_intercepted",
        "_eve_z_measurements",
        "_eve_x_measurements",
        "_eve_zero_outcomes",
        "_eve_one_outcomes",
    )

    def __init__(self, intercept_fraction: float, rng: BaseRNG) -> None:
        self.intercept_fraction = _validate_probability(
            intercept_fraction,
            name="intercept_fraction",
        )
        if not isinstance(rng, BaseRNG):
            raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
        self._rng = rng
        self._n_signals_seen = 0
        self._n_intercepted = 0
        self._eve_z_measurements = 0
        self._eve_x_measurements = 0
        self._eve_zero_outcomes = 0
        self._eve_one_outcomes = 0

    @property
    def diagnostics(self) -> AttackDiagnostics:
        """Return an immutable simulator-only snapshot of cumulative counters."""

        return AttackDiagnostics(
            intercept_fraction=self.intercept_fraction,
            n_signals_seen=self._n_signals_seen,
            n_intercepted=self._n_intercepted,
            eve_z_measurements=self._eve_z_measurements,
            eve_x_measurements=self._eve_x_measurements,
            eve_zero_outcomes=self._eve_zero_outcomes,
            eve_one_outcomes=self._eve_one_outcomes,
        )

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Possibly intercept one qubit, then return a fresh transmitted state."""

        matrix = _prepare_density_matrix(
            rho,
            dimension=2,
            validate_state=validate_state,
        )
        self._n_signals_seen += 1

        if self.intercept_fraction == 0.0:
            return np.array(matrix, dtype=np.complex128, copy=True)
        if self.intercept_fraction < 1.0 and float(self._rng.gen.random()) >= self.intercept_fraction:
            return np.array(matrix, dtype=np.complex128, copy=True)

        basis_bit = random_basis(self._rng)
        if isinstance(basis_bit, np.ndarray):
            raise RuntimeError("Scalar Eve basis sampling unexpectedly returned an array.")
        eve_basis = basis_from_bit(basis_bit)
        measurement = sample_projective_outcome(
            matrix,
            MEASUREMENTS_BY_BASIS[eve_basis],
            self._rng,
            validate_state=False,
        )
        outcome = int(measurement.outcome)
        resent_state = np.array(_RESENT_STATES[(eve_basis, outcome)], dtype=np.complex128, copy=True)

        self._n_intercepted += 1
        if eve_basis is Basis.Z:
            self._eve_z_measurements += 1
        else:
            self._eve_x_measurements += 1
        if outcome == 0:
            self._eve_zero_outcomes += 1
        else:
            self._eve_one_outcomes += 1
        return resent_state
