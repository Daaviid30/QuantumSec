"""Quantum bit error rate for aligned QKD key material."""

import numpy as np
import numpy.typing as npt


def _binary_vector(values: npt.ArrayLike, *, name: str) -> np.ndarray:
    """Return a validated one-dimensional binary integer vector."""

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
    return vector


def qber(alice_key: npt.ArrayLike, bob_key: npt.ArrayLike) -> float:
    """Return the differing-bit fraction for two aligned non-empty binary keys.

    An empty comparison has no defined QBER and raises ``ValueError`` instead of
    producing a numerical placeholder such as ``NaN``.
    """

    clean_alice_key = _binary_vector(alice_key, name="alice_key")
    clean_bob_key = _binary_vector(bob_key, name="bob_key")

    if clean_alice_key.size != clean_bob_key.size:
        raise ValueError(
            "QBER requires aligned keys with equal lengths. "
            f"Got alice={clean_alice_key.size} and bob={clean_bob_key.size}."
        )
    if clean_alice_key.size == 0:
        raise ValueError("QBER is undefined for empty compared keys.")

    differing_bits = int(np.count_nonzero(clean_alice_key != clean_bob_key))
    return differing_bits / int(clean_alice_key.size)
