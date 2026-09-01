"""Quantum bit error rate for aligned QKD key material."""

import numpy as np
import numpy.typing as npt

from qkd._validation import copy_binary_vector


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
