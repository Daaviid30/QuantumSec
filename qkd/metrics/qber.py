"""Aggregate and per-basis quantum bit error rate metrics."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from core.constants import DEFAULT_ATOL
from qkd._validation import copy_binary_vector
from qkd.primitives.bases import Basis


def _optional_probability(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (float, int, np.floating, np.integer)):
        raise ValueError(f"{name} must be a finite probability or None. Got {value!r}.")
    result = float(value)
    if not np.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]. Got {result}.")
    return result


@dataclass(frozen=True, slots=True)
class QBERByBasis:
    """Immutable aggregate and BB84 basis-conditioned error metrics."""

    qber_z: float | None
    qber_x: float | None
    qber_aggregated: float
    n_z: int
    n_x: int

    def __post_init__(self) -> None:
        qber_z = _optional_probability(self.qber_z, name="qber_z")
        qber_x = _optional_probability(self.qber_x, name="qber_x")
        aggregate = _optional_probability(self.qber_aggregated, name="qber_aggregated")
        if aggregate is None:
            raise ValueError("qber_aggregated cannot be None.")
        for name in ("n_z", "n_x"):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
            clean = int(value)
            if clean < 0:
                raise ValueError(f"{name} must be non-negative. Got {clean}.")
            object.__setattr__(self, name, clean)
        if self.n_z + self.n_x == 0:
            raise ValueError("Per-basis QBER requires at least one compared BB84 bit.")
        if (qber_z is None) != (self.n_z == 0) or (qber_x is None) != (self.n_x == 0):
            raise ValueError("A basis QBER is defined exactly when that basis has compared bits.")
        weighted_errors = (qber_z or 0.0) * self.n_z + (qber_x or 0.0) * self.n_x
        expected_aggregate = weighted_errors / (self.n_z + self.n_x)
        if not np.isclose(aggregate, expected_aggregate, atol=DEFAULT_ATOL, rtol=0.0):
            raise ValueError("qber_aggregated must be the count-weighted per-basis QBER.")
        object.__setattr__(self, "qber_z", qber_z)
        object.__setattr__(self, "qber_x", qber_x)
        object.__setattr__(self, "qber_aggregated", aggregate)


def qber(alice_key: npt.ArrayLike, bob_key: npt.ArrayLike) -> float:
    """Return the differing-bit fraction for two aligned non-empty binary keys.

    An empty comparison has no defined QBER and raises ``ValueError`` instead of
    producing a numerical placeholder such as ``NaN``.
    """

    clean_alice_key = copy_binary_vector(alice_key, name="alice_key")
    clean_bob_key = copy_binary_vector(bob_key, name="bob_key")

    if clean_alice_key.size != clean_bob_key.size:
        raise ValueError(
            "QBER requires aligned keys with equal lengths. "
            f"Got alice={clean_alice_key.size} and bob={clean_bob_key.size}."
        )
    if clean_alice_key.size == 0:
        raise ValueError("QBER is undefined for empty compared keys.")

    differing_bits = int(np.count_nonzero(clean_alice_key != clean_bob_key))
    return differing_bits / int(clean_alice_key.size)


def qber_by_basis(
    alice_key: npt.ArrayLike,
    bob_key: npt.ArrayLike,
    bases: Sequence[Basis] | np.ndarray,
) -> QBERByBasis:
    """Return Z, X, and aggregate QBER without inventing absent-basis values."""

    alice = copy_binary_vector(alice_key, name="alice_key")
    bob = copy_binary_vector(bob_key, name="bob_key")
    if alice.size != bob.size:
        raise ValueError(
            "Per-basis QBER requires aligned keys with equal lengths. "
            f"Got alice={alice.size} and bob={bob.size}."
        )
    basis_array = np.asarray(bases, dtype=object)
    if basis_array.ndim != 1:
        raise ValueError(f"bases must be one-dimensional. Got shape={basis_array.shape}.")
    if basis_array.size != alice.size:
        raise ValueError(
            "Per-basis QBER requires one basis per aligned bit. "
            f"Got bases={basis_array.size} and bits={alice.size}."
        )
    if alice.size == 0:
        raise ValueError("Per-basis QBER is undefined for empty compared keys.")
    if any(basis not in (Basis.Z, Basis.X) for basis in basis_array):
        raise ValueError("bases must contain only the BB84 Z and X bases.")

    z_mask = basis_array == Basis.Z
    x_mask = basis_array == Basis.X
    n_z = int(np.count_nonzero(z_mask))
    n_x = int(np.count_nonzero(x_mask))
    return QBERByBasis(
        qber_z=qber(alice[z_mask], bob[z_mask]) if n_z else None,
        qber_x=qber(alice[x_mask], bob[x_mask]) if n_x else None,
        qber_aggregated=qber(alice, bob),
        n_z=n_z,
        n_x=n_x,
    )
