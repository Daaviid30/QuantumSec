"""Internal validation helpers shared by QKD post-processing stages."""

import numpy as np
import numpy.typing as npt


def copy_binary_vector(values: npt.ArrayLike, *, name: str) -> npt.NDArray[np.uint8]:
    """Return a defensive, read-only copy of one-dimensional binary data."""

    try:
        vector = np.asarray(values)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be one-dimensional binary integer data.") from error
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional. Got shape={vector.shape}.")
    if vector.size > 0 and not np.issubdtype(vector.dtype, np.integer):
        raise ValueError(f"{name} must contain integer bits. Got dtype={vector.dtype}.")
    if np.any((vector != 0) & (vector != 1)):
        raise ValueError(f"{name} must contain only 0 and 1. Got {vector}.")

    result = np.array(vector, dtype=np.uint8, copy=True)
    result.flags.writeable = False
    return result


def copy_indices(values: npt.ArrayLike, *, name: str) -> npt.NDArray[np.intp]:
    """Return a defensive, read-only copy of one-dimensional integer indices."""

    try:
        indices = np.asarray(values)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{name} must be one-dimensional integer data.") from error
    if indices.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional. Got shape={indices.shape}.")
    if indices.size > 0 and not np.issubdtype(indices.dtype, np.integer):
        raise ValueError(f"{name} must contain integers. Got dtype={indices.dtype}.")

    result = np.array(indices, dtype=np.intp, copy=True)
    result.flags.writeable = False
    return result


def validate_aligned_keys(
    alice_key: npt.ArrayLike,
    bob_key: npt.ArrayLike,
    *,
    allow_empty: bool = False,
) -> tuple[npt.NDArray[np.uint8], npt.NDArray[np.uint8]]:
    """Validate and copy two aligned binary keys."""

    alice = copy_binary_vector(alice_key, name="alice_key")
    bob = copy_binary_vector(bob_key, name="bob_key")
    if alice.size != bob.size:
        raise ValueError(
            f"Alice and Bob keys must have equal lengths. Got alice={alice.size} and bob={bob.size}."
        )
    if not allow_empty and alice.size == 0:
        raise ValueError("Alice and Bob keys must be non-empty.")
    return alice, bob


def validate_non_negative_int(value: object, *, name: str) -> int:
    """Validate an integer while rejecting booleans."""

    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
    result = int(value)
    if result < 0:
        raise ValueError(f"{name} must be non-negative. Got {result}.")
    return result
