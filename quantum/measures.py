#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from core.rng import BaseRNG
from quantum import validation as v

#=================== CONSTANTS ===================

ATOL = 1e-10

#=================== CLASSES ===================

@dataclass(frozen=True, slots=True)
class MeasurementResult:
    outcome: int
    probability: float
    post_state: np.ndarray

#=================== FUNCTIONS ===================

def dm_purity(
        rho: np.ndarray
    ) -> float:
    """
    Calculate the purity Tr(rho²) of a quantum state.

    Parameters:
    -----------
    rho: np.ndarray
        Density matrix representing the quantum state.

    Returns:
    --------
    float
        Real purity value of rho.

    Raises:
    -------
    ValueError
        If rho is not a valid density matrix.
    """

    rho = np.asarray(rho, dtype = complex)
    v.validate_density_matrix(rho)

    purity = np.trace(rho @ rho)

    return float(purity.real)

def measure_projective(
        rho: np.ndarray, 
        projectors: Sequence[np.ndarray], 
        rng: BaseRNG, 
        tol: float = ATOL
    ) -> MeasurementResult:
    """
    Perform a projective measurement on a density matrix.

    Parameters:
    -----------
    rho: np.ndarray
        Density matrix representing the state before measurement.
    projectors: Sequence[np.ndarray]
        Projectors associated with the possible measurement outcomes.
    rng: BaseRNG
        Random source used to sample an outcome.
    tol: float
        Absolute tolerance used for probability checks.

    Returns:
    --------
    MeasurementResult
        Sampled outcome, its probability, and the normalized post-measurement state.

    Raises:
    -------
    ValueError
        If rho or a projector is invalid, dimensions differ, or probabilities are inconsistent.
    """

    rho = np.asarray(rho, dtype=complex)
    v.validate_density_matrix(rho)

    if len(projectors) == 0:
        raise ValueError("[!] At least one projector is required.")

    clean_projectors: list[np.ndarray] = []
    probabilities = np.empty(len(projectors), dtype=float)

    for index, projector in enumerate(projectors):
        projector = np.asarray(projector, dtype = complex)

        if projector.shape != rho.shape:
            raise ValueError("[!] Projector and state dimensions must match. "
                f"Got projector.shape={projector.shape} "
                f"and rho.shape={rho.shape}.")

        v.validate_projector(projector)

        probability = np.trace(projector @ rho)

        if not np.isclose(probability.imag, 0.0, atol=tol, rtol=0.0):
            raise ValueError("[!] The probability must not have an imaginary part.")

        probabilities[index] = probability.real
        clean_projectors.append(projector)

    total_probability = float(np.sum(probabilities))

    if not np.isclose(total_probability, 1.0, atol=tol, rtol=0.0):
        raise ValueError(f"[!] The probability sum must be equal to 1. Got {total_probability}")

    # Clean little variantions (ex: 1e-10)
    probabilities = np.clip(probabilities, 0.0, 1.0)

    # Erase minimal variations
    probabilities /= total_probability

    outcome = int(rng.gen.choice(
        len(projectors),
        p=probabilities
    ))

    probability = float(probabilities[outcome])
    projector = clean_projectors[outcome]

    post_state = projector @ rho @ projector
    post_state /= probability

    return MeasurementResult(
        outcome=outcome,
        probability=probability,
        post_state=post_state
    )

