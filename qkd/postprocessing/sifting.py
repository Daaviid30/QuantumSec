"""Deterministic basis reconciliation for QKD raw keys."""

from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from qkd._validation import copy_binary_vector, copy_indices
from qkd.primitives.bases import Basis


def _basis_vector(values: Sequence[Basis] | np.ndarray, *, name: str) -> tuple[Basis, ...]:
    """Validate a one-dimensional sequence of named QKD bases."""

    array = np.asarray(values, dtype=object)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional. Got shape={array.shape}.")

    bases = tuple(array.tolist())
    for index, basis in enumerate(bases):
        if not isinstance(basis, Basis):
            raise ValueError(f"{name} must contain Basis values. Got {basis!r} at index {index}.")
    return bases


@dataclass(frozen=True, slots=True, eq=False)
class SiftingResult:
    """Aligned sifted keys and the raw positions retained by reconciliation."""

    n_raw: int
    matching_indices: npt.NDArray[np.intp] = field(repr=False)
    alice_sifted_key: npt.NDArray[np.uint8] = field(repr=False)
    bob_sifted_key: npt.NDArray[np.uint8] = field(repr=False)

    def __post_init__(self) -> None:
        if isinstance(self.n_raw, (bool, np.bool_)) or not isinstance(self.n_raw, (int, np.integer)):
            raise ValueError(f"n_raw must be a non-negative integer. Got {self.n_raw!r}.")
        n_raw = int(self.n_raw)
        if n_raw < 0:
            raise ValueError(f"n_raw must be non-negative. Got {n_raw}.")

        indices = copy_indices(self.matching_indices, name="matching_indices")
        alice_key = copy_binary_vector(self.alice_sifted_key, name="alice_sifted_key")
        bob_key = copy_binary_vector(self.bob_sifted_key, name="bob_sifted_key")

        if indices.size != alice_key.size or alice_key.size != bob_key.size:
            raise ValueError(
                "Sifted keys and matching indices must have equal lengths. "
                f"Got indices={indices.size}, alice={alice_key.size}, bob={bob_key.size}."
            )
        if np.any(indices < 0) or np.any(indices >= n_raw):
            raise ValueError(f"matching_indices must lie in [0, {n_raw}). Got {indices}.")
        if indices.size > 1 and np.any(np.diff(indices) <= 0):
            raise ValueError("matching_indices must be strictly increasing.")

        object.__setattr__(self, "n_raw", n_raw)
        object.__setattr__(self, "matching_indices", indices)
        object.__setattr__(self, "alice_sifted_key", alice_key)
        object.__setattr__(self, "bob_sifted_key", bob_key)

    @property
    def n_sifted(self) -> int:
        """Return the number of positions retained after basis reconciliation."""

        return int(self.matching_indices.size)

    @property
    def sifting_efficiency(self) -> float:
        """Return the fraction of raw positions retained after sifting."""

        if self.n_raw == 0:
            raise ValueError("Sifting efficiency is undefined for zero raw bits.")
        return self.n_sifted / self.n_raw


def sift_keys(
    alice_bases: Sequence[Basis] | np.ndarray,
    bob_bases: Sequence[Basis] | np.ndarray,
    alice_raw_bits: npt.ArrayLike,
    bob_measured_bits: npt.ArrayLike,
) -> SiftingResult:
    """Keep aligned raw bits whose named preparation and measurement bases match."""

    clean_alice_bases = _basis_vector(alice_bases, name="alice_bases")
    clean_bob_bases = _basis_vector(bob_bases, name="bob_bases")
    clean_alice_bits = copy_binary_vector(alice_raw_bits, name="alice_raw_bits")
    clean_bob_bits = copy_binary_vector(bob_measured_bits, name="bob_measured_bits")

    lengths = (
        len(clean_alice_bases),
        len(clean_bob_bases),
        clean_alice_bits.size,
        clean_bob_bits.size,
    )
    if len(set(lengths)) != 1:
        raise ValueError(
            "Sifting inputs must have equal lengths. "
            f"Got alice_bases={lengths[0]}, bob_bases={lengths[1]}, "
            f"alice_raw_bits={lengths[2]}, bob_measured_bits={lengths[3]}."
        )

    matching_mask = np.fromiter(
        (
            alice_basis is bob_basis
            for alice_basis, bob_basis in zip(
                clean_alice_bases,
                clean_bob_bases,
                strict=True,
            )
        ),
        dtype=np.bool_,
        count=lengths[0],
    )
    matching_indices = np.flatnonzero(matching_mask)

    return SiftingResult(
        n_raw=lengths[0],
        matching_indices=matching_indices,
        alice_sifted_key=clean_alice_bits[matching_indices],
        bob_sifted_key=clean_bob_bits[matching_indices],
    )
