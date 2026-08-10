"""Named basis conventions used by QKD protocols."""

from collections.abc import Sequence
from enum import Enum

import numpy as np


class Basis(Enum):
    """Standard single-qubit measurement bases."""

    Z = "Z"
    X = "X"
    Y = "Y"


def basis_from_bit(value: int | np.integer) -> Basis:
    """Map the QKD random-bit convention 0/1 to the Z/X basis."""

    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"A basis bit must be integer 0 or 1. Got {value!r}.")
    if value == 0:
        return Basis.Z
    if value == 1:
        return Basis.X
    raise ValueError(f"A basis bit must be 0 or 1. Got {value}.")


def bases_from_bits(values: Sequence[int] | np.ndarray) -> tuple[Basis, ...]:
    """Map a one-dimensional sequence of random bits to QKD bases."""

    bits = np.asarray(values)
    if bits.ndim != 1:
        raise ValueError(f"Basis bits must be one-dimensional. Got shape={bits.shape}.")
    return tuple(basis_from_bit(value) for value in bits)
