"""Construction helpers for quantum density matrices."""

from collections.abc import Sequence

import numpy as np

from quantum import linalg
from quantum import validation as v
from quantum.types import ArrayLike, ComplexArray


def dm_from_ket(psi: ArrayLike) -> ComplexArray:
    """Construct the pure-state density matrix ``|psi><psi|``."""

    ket = linalg.as_ket(psi)
    v.validate_quantum_state(ket)
    return linalg.outer_product(ket, ket)


def dm_from_ensemble(states: Sequence[ArrayLike], probs: ArrayLike) -> ComplexArray:
    """Construct a density matrix from a finite ensemble of pure states.

    Parameters
    ----------
    states:
        Equal-dimensional normalized kets.
    probs:
        One probability per ket, forming a normalized distribution.
    """

    probabilities = linalg.as_ket(probs)
    v.validate_probability_state(probabilities)
    real_probabilities = np.real(probabilities)

    if len(states) != probabilities.size:
        raise ValueError(
            "An ensemble requires one probability per state. "
            f"Got {len(states)} states and {probabilities.size} probabilities."
        )
    if not states:
        raise ValueError("A density-matrix ensemble requires at least one state.")

    clean_states = tuple(linalg.as_ket(state) for state in states)
    expected_dimension = clean_states[0].size
    density = np.zeros((expected_dimension, expected_dimension), dtype=np.complex128)

    for index, state in enumerate(clean_states):
        v.validate_quantum_state(state)
        if state.size != expected_dimension:
            raise ValueError(
                "Ensemble states must have the same dimension. "
                f"Expected {expected_dimension}, got {state.size} at index {index}."
            )
        density += linalg.outer_product(state, state) * real_probabilities[index]

    return density
