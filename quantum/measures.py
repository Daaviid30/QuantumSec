"""General projective-measurement domain objects and operations."""

from dataclasses import dataclass, field

import numpy as np

from core.constants import DEFAULT_ATOL
from core.rng import BaseRNG
from quantum import validation as v
from quantum.types import ArrayLike, ComplexArray, RealArray


@dataclass(frozen=True, slots=True, eq=False)
class MeasurementResult:
    """A sampled logical outcome and its normalized post-measurement state."""

    outcome: int
    probability: float
    post_state: ComplexArray = field(repr=False)


@dataclass(frozen=True, slots=True)
class MeasurementSample:
    """A sampled projector index and logical outcome, without state collapse."""

    index: int
    outcome: int
    probability: float


@dataclass(frozen=True, slots=True, eq=False)
class ProjectiveMeasurement:
    """A complete projective measurement validated once at construction time."""

    projectors: tuple[ComplexArray, ...]
    outcomes: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.projectors:
            raise ValueError("A projective measurement requires at least one projector.")

        if len(self.projectors) != len(self.outcomes):
            raise ValueError(
                "Each projector must have one associated outcome. "
                f"Got {len(self.projectors)} projectors and {len(self.outcomes)} outcomes."
            )

        clean_projectors = tuple(
            np.array(projector, dtype=np.complex128, copy=True) for projector in self.projectors
        )
        v.validate_projective_measurement(clean_projectors)

        for projector in clean_projectors:
            projector.flags.writeable = False

        object.__setattr__(self, "projectors", clean_projectors)
        object.__setattr__(self, "outcomes", tuple(int(outcome) for outcome in self.outcomes))

    @property
    def dimension(self) -> int:
        """Return the Hilbert-space dimension measured by the projectors."""

        return self.projectors[0].shape[0]

    @property
    def number_of_outcomes(self) -> int:
        """Return the number of projector/outcome pairs."""

        return len(self.projectors)


def _born_probabilities(
    rho: ComplexArray,
    measurement: ProjectiveMeasurement,
    tol: float,
) -> RealArray:
    """Calculate and validate the Born probability vector."""

    complex_probabilities = np.array(
        [np.trace(projector @ rho) for projector in measurement.projectors],
        dtype=np.complex128,
    )

    imaginary_parts = np.abs(complex_probabilities.imag)
    if np.any(imaginary_parts > tol):
        raise ValueError(
            f"Measurement probabilities must be real. Got imaginary parts {complex_probabilities.imag}."
        )

    probabilities = np.asarray(complex_probabilities.real, dtype=np.float64)

    if not np.all(np.isfinite(probabilities)):
        raise ValueError(f"Measurement probabilities must be finite. Got {probabilities}.")

    if np.any(probabilities < -tol):
        raise ValueError(f"Measurement probabilities must be non-negative. Got {probabilities}.")

    if np.any(probabilities > 1.0 + tol):
        raise ValueError(f"Measurement probabilities cannot exceed one. Got {probabilities}.")

    probabilities = np.clip(probabilities, 0.0, 1.0)
    total_probability = float(np.sum(probabilities))

    if not np.isclose(total_probability, 1.0, atol=tol, rtol=0.0):
        raise ValueError(
            f"Measurement probabilities must sum to one. Got total={total_probability} from {probabilities}."
        )

    probabilities /= total_probability
    return probabilities


def sample_projective_outcome(
    rho: ArrayLike,
    measurement: ProjectiveMeasurement,
    rng: BaseRNG,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> MeasurementSample:
    """Sample a projective outcome without constructing a collapsed state.

    Parameters
    ----------
    rho:
        Density matrix representing the state before measurement.
    measurement:
        Prevalidated complete projective measurement.
    rng:
        Injected random source used to select an outcome.
    tol:
        Absolute tolerance for physical probability checks.
    validate_state:
        Whether to perform full density-matrix validation, including a spectral check.

    Returns
    -------
    MeasurementSample
        Selected projector index, logical outcome, and Born probability.

    Raises
    ------
    ValueError
        If the state is invalid or incompatible, or its probabilities are unphysical.
    """

    clean_rho = np.asarray(rho, dtype=np.complex128)
    if validate_state:
        v.validate_density_matrix(clean_rho, tol)

    expected_shape = (measurement.dimension, measurement.dimension)
    if clean_rho.shape != expected_shape:
        raise ValueError(
            "Measurement and state dimensions must match. "
            f"Got measurement dimension={measurement.dimension} and rho.shape={clean_rho.shape}."
        )

    probabilities = _born_probabilities(clean_rho, measurement, tol)
    index = int(rng.gen.choice(measurement.number_of_outcomes, p=probabilities))

    return MeasurementSample(
        index=index,
        outcome=measurement.outcomes[index],
        probability=float(probabilities[index]),
    )


def measure_projective(
    rho: ArrayLike,
    measurement: ProjectiveMeasurement,
    rng: BaseRNG,
    tol: float = DEFAULT_ATOL,
    validate_state: bool = True,
) -> MeasurementResult:
    """Sample a projective outcome and apply the Lueders state update.

    Parameters
    ----------
    rho:
        Density matrix representing the state before measurement.
    measurement:
        Prevalidated complete projective measurement.
    rng:
        Injected random source used to select an outcome.
    tol:
        Absolute tolerance for physical probability checks.
    validate_state:
        Whether to perform full density-matrix validation before sampling.

    Returns
    -------
    MeasurementResult
        Logical outcome, Born probability, and normalized post-measurement state.
    """

    clean_rho = np.asarray(rho, dtype=np.complex128)
    sample = sample_projective_outcome(
        clean_rho,
        measurement,
        rng,
        tol=tol,
        validate_state=validate_state,
    )

    if sample.probability <= tol:
        raise RuntimeError("Sampled an outcome with numerically zero probability.")

    projector = measurement.projectors[sample.index]
    post_state = np.asarray(projector @ clean_rho @ projector, dtype=np.complex128)
    post_state /= sample.probability

    return MeasurementResult(
        outcome=sample.outcome,
        probability=sample.probability,
        post_state=post_state,
    )
