"""Sampled QBER estimation with mandatory removal of disclosed key positions."""

from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG
from qkd.metrics.qber import qber
from qkd.postprocessing._validation import copy_binary_vector, copy_indices, validate_aligned_keys


@dataclass(frozen=True, slots=True, eq=False)
class ParameterEstimationResult:
    """Immutable transcript and remaining material from parameter estimation."""

    n_sifted: int
    disclosed_indices: npt.NDArray[np.intp] = field(repr=False)
    alice_disclosed_bits: npt.NDArray[np.uint8] = field(repr=False)
    bob_disclosed_bits: npt.NDArray[np.uint8] = field(repr=False)
    estimated_qber: float
    alice_candidate_key: npt.NDArray[np.uint8] = field(repr=False)
    bob_candidate_key: npt.NDArray[np.uint8] = field(repr=False)

    def __post_init__(self) -> None:
        if isinstance(self.n_sifted, (bool, np.bool_)) or not isinstance(self.n_sifted, (int, np.integer)):
            raise ValueError(f"n_sifted must be a positive integer. Got {self.n_sifted!r}.")
        n_sifted = int(self.n_sifted)
        if n_sifted <= 0:
            raise ValueError(f"n_sifted must be positive. Got {n_sifted}.")
        indices = copy_indices(self.disclosed_indices, name="disclosed_indices")
        alice_disclosed = copy_binary_vector(self.alice_disclosed_bits, name="alice_disclosed_bits")
        bob_disclosed = copy_binary_vector(self.bob_disclosed_bits, name="bob_disclosed_bits")
        alice_candidate, bob_candidate = validate_aligned_keys(
            self.alice_candidate_key, self.bob_candidate_key, allow_empty=True
        )
        if not (indices.size == alice_disclosed.size == bob_disclosed.size):
            raise ValueError("Disclosed indices and disclosed bit vectors must have equal lengths.")
        if indices.size == 0 or indices.size >= n_sifted:
            raise ValueError(
                "Parameter estimation must disclose at least one bit and retain at least one bit."
            )
        if np.any(indices < 0) or np.any(indices >= n_sifted) or np.unique(indices).size != indices.size:
            raise ValueError("disclosed_indices must be unique positions within the sifted key.")
        if alice_candidate.size + indices.size != n_sifted:
            raise ValueError("Candidate and disclosed lengths must reconstruct the sifted length.")
        if not isinstance(self.estimated_qber, (float, int, np.floating, np.integer)) or isinstance(
            self.estimated_qber, (bool, np.bool_)
        ):
            raise ValueError(f"estimated_qber must be a finite probability. Got {self.estimated_qber!r}.")
        estimated_qber = float(self.estimated_qber)
        if not np.isfinite(estimated_qber) or not 0.0 <= estimated_qber <= 1.0:
            raise ValueError(f"estimated_qber must lie in [0, 1]. Got {estimated_qber}.")
        if estimated_qber != qber(alice_disclosed, bob_disclosed):
            raise ValueError("estimated_qber must equal the QBER of the disclosed sample.")

        object.__setattr__(self, "n_sifted", n_sifted)
        object.__setattr__(self, "disclosed_indices", indices)
        object.__setattr__(self, "alice_disclosed_bits", alice_disclosed)
        object.__setattr__(self, "bob_disclosed_bits", bob_disclosed)
        object.__setattr__(self, "estimated_qber", estimated_qber)
        object.__setattr__(self, "alice_candidate_key", alice_candidate)
        object.__setattr__(self, "bob_candidate_key", bob_candidate)

    @property
    def sample_size(self) -> int:
        return int(self.disclosed_indices.size)

    @property
    def n_candidate(self) -> int:
        return int(self.alice_candidate_key.size)


def estimate_qber_from_sample(
    alice_sifted_key: npt.ArrayLike,
    bob_sifted_key: npt.ArrayLike,
    rng: BaseRNG,
    *,
    sample_fraction: float = 0.2,
    sample_size: int | None = None,
) -> ParameterEstimationResult:
    """Disclose a random sample without replacement and remove it from both keys.

    Exactly one of the derived fractional size or an explicit ``sample_size`` is
    used. Fractional sizes are rounded up so a valid positive fraction never
    silently discloses zero bits.
    """

    alice, bob = validate_aligned_keys(alice_sifted_key, bob_sifted_key)
    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    if isinstance(sample_fraction, (bool, np.bool_)) or not isinstance(
        sample_fraction, (float, int, np.floating, np.integer)
    ):
        raise ValueError(f"sample_fraction must lie strictly between 0 and 1. Got {sample_fraction!r}.")
    fraction = float(sample_fraction)
    if not np.isfinite(fraction) or not 0.0 < fraction < 1.0:
        raise ValueError(f"sample_fraction must lie strictly between 0 and 1. Got {fraction}.")
    if alice.size < 2:
        raise ValueError("Parameter estimation requires at least two sifted bits.")

    if sample_size is None:
        disclosure_count = int(np.ceil(alice.size * fraction))
    else:
        if isinstance(sample_size, (bool, np.bool_)) or not isinstance(sample_size, (int, np.integer)):
            raise ValueError(f"sample_size must be a positive integer. Got {sample_size!r}.")
        disclosure_count = int(sample_size)
    if disclosure_count <= 0 or disclosure_count >= alice.size:
        raise ValueError(
            "sample_size must disclose at least one bit and leave at least one candidate bit. "
            f"Got sample_size={disclosure_count} for {alice.size} sifted bits."
        )

    indices = np.sort(rng.gen.choice(alice.size, size=disclosure_count, replace=False))
    retain_mask = np.ones(alice.size, dtype=np.bool_)
    retain_mask[indices] = False
    return ParameterEstimationResult(
        n_sifted=int(alice.size),
        disclosed_indices=indices,
        alice_disclosed_bits=alice[indices],
        bob_disclosed_bits=bob[indices],
        estimated_qber=qber(alice[indices], bob[indices]),
        alice_candidate_key=alice[retain_mask],
        bob_candidate_key=bob[retain_mask],
    )
