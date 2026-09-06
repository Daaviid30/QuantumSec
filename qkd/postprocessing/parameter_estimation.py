"""Sampled QBER estimation with mandatory removal of disclosed key positions."""

from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.constants import DEFAULT_ATOL
from core.rng import BaseRNG
from qkd._validation import copy_binary_vector, copy_indices, validate_aligned_keys
from qkd.metrics.qber import qber_by_basis
from qkd.primitives.bases import Basis


def _copy_bb84_bases(
    values: Sequence[Basis] | np.ndarray,
    *,
    name: str,
) -> tuple[Basis, ...]:
    array = np.asarray(values, dtype=object)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional. Got shape={array.shape}.")
    bases = tuple(array.tolist())
    if any(basis not in (Basis.Z, Basis.X) for basis in bases):
        raise ValueError(f"{name} must contain only the BB84 Z and X bases.")
    return bases


def _explicit_stratified_counts(n_z: int, n_x: int, sample_size: int) -> tuple[int, int]:
    if sample_size < 2 or sample_size > n_z + n_x - 2:
        raise ValueError(
            "sample_size must disclose at least one bit from each BB84 basis and leave "
            f"at least one candidate bit in each basis. Got sample_size={sample_size}."
        )
    disclose_z = int(round(sample_size * n_z / (n_z + n_x)))
    disclose_z = min(max(disclose_z, 1), n_z - 1)
    disclose_x = sample_size - disclose_z
    if disclose_x < 1:
        disclose_x = 1
        disclose_z = sample_size - 1
    elif disclose_x > n_x - 1:
        disclose_x = n_x - 1
        disclose_z = sample_size - disclose_x
    return disclose_z, disclose_x


@dataclass(frozen=True, slots=True, eq=False)
class ParameterEstimationResult:
    """Immutable basis-aware transcript and remaining candidate material."""

    n_sifted: int
    disclosed_indices: npt.NDArray[np.intp] = field(repr=False)
    disclosed_bases: tuple[Basis, ...] = field(repr=False)
    alice_disclosed_bits: npt.NDArray[np.uint8] = field(repr=False)
    bob_disclosed_bits: npt.NDArray[np.uint8] = field(repr=False)
    estimated_qber_z: float
    estimated_qber_x: float
    estimated_qber_aggregated: float
    candidate_bases: tuple[Basis, ...] = field(repr=False)
    alice_candidate_key: npt.NDArray[np.uint8] = field(repr=False)
    bob_candidate_key: npt.NDArray[np.uint8] = field(repr=False)

    def __post_init__(self) -> None:
        if isinstance(self.n_sifted, (bool, np.bool_)) or not isinstance(self.n_sifted, (int, np.integer)):
            raise ValueError(f"n_sifted must be a positive integer. Got {self.n_sifted!r}.")
        n_sifted = int(self.n_sifted)
        if n_sifted <= 0:
            raise ValueError(f"n_sifted must be positive. Got {n_sifted}.")
        indices = copy_indices(self.disclosed_indices, name="disclosed_indices")
        disclosed_bases = _copy_bb84_bases(self.disclosed_bases, name="disclosed_bases")
        candidate_bases = _copy_bb84_bases(self.candidate_bases, name="candidate_bases")
        alice_disclosed = copy_binary_vector(self.alice_disclosed_bits, name="alice_disclosed_bits")
        bob_disclosed = copy_binary_vector(self.bob_disclosed_bits, name="bob_disclosed_bits")
        alice_candidate, bob_candidate = validate_aligned_keys(
            self.alice_candidate_key, self.bob_candidate_key, allow_empty=True
        )
        if not (indices.size == len(disclosed_bases) == alice_disclosed.size == bob_disclosed.size):
            raise ValueError("Disclosed indices, bases, and bit vectors must have equal lengths.")
        if indices.size == 0 or indices.size >= n_sifted:
            raise ValueError(
                "Parameter estimation must disclose at least one bit and retain at least one bit."
            )
        if np.any(indices < 0) or np.any(indices >= n_sifted) or np.unique(indices).size != indices.size:
            raise ValueError("disclosed_indices must be unique positions within the sifted key.")
        if alice_candidate.size != len(candidate_bases):
            raise ValueError("Candidate bases and candidate bit vectors must have equal lengths.")
        if alice_candidate.size + indices.size != n_sifted:
            raise ValueError("Candidate and disclosed lengths must reconstruct the sifted length.")
        if set(disclosed_bases) != {Basis.Z, Basis.X}:
            raise ValueError("The disclosed sample must contain both BB84 bases.")
        if set(candidate_bases) != {Basis.Z, Basis.X}:
            raise ValueError("The candidate material must retain both BB84 bases.")

        metrics = qber_by_basis(alice_disclosed, bob_disclosed, disclosed_bases)
        expected = {
            "estimated_qber_z": metrics.qber_z,
            "estimated_qber_x": metrics.qber_x,
            "estimated_qber_aggregated": metrics.qber_aggregated,
        }
        cleaned: dict[str, float] = {}
        for name, expected_value in expected.items():
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(
                value, (float, int, np.floating, np.integer)
            ):
                raise ValueError(f"{name} must be a finite probability. Got {value!r}.")
            clean = float(value)
            if not np.isfinite(clean) or not 0.0 <= clean <= 1.0:
                raise ValueError(f"{name} must lie in [0, 1]. Got {clean}.")
            if expected_value is None or not np.isclose(clean, expected_value, atol=DEFAULT_ATOL, rtol=0.0):
                raise ValueError(f"{name} must equal the corresponding QBER of the disclosed sample.")
            cleaned[name] = clean

        object.__setattr__(self, "n_sifted", n_sifted)
        object.__setattr__(self, "disclosed_indices", indices)
        object.__setattr__(self, "disclosed_bases", disclosed_bases)
        object.__setattr__(self, "alice_disclosed_bits", alice_disclosed)
        object.__setattr__(self, "bob_disclosed_bits", bob_disclosed)
        for name, value in cleaned.items():
            object.__setattr__(self, name, value)
        object.__setattr__(self, "candidate_bases", candidate_bases)
        object.__setattr__(self, "alice_candidate_key", alice_candidate)
        object.__setattr__(self, "bob_candidate_key", bob_candidate)

    @property
    def sample_size(self) -> int:
        return int(self.disclosed_indices.size)

    @property
    def n_candidate(self) -> int:
        return int(self.alice_candidate_key.size)

    @property
    def estimated_qber(self) -> float:
        """Return aggregate sampled QBER as a backwards-compatible alias."""

        return self.estimated_qber_aggregated

    @property
    def bit_error_rate(self) -> float:
        """Return the aggregate sampled bit-error rate used to configure Cascade."""

        return self.estimated_qber_aggregated

    @property
    def phase_error_bound(self) -> float:
        """Return the common asymptotic bound used for mixed-basis candidates.

        In the BB84/CSS reduction, sampled X bit errors bound Z-candidate phase
        errors and sampled Z bit errors bound X-candidate phase errors. Because
        this implementation mixes both candidate subsets, their maximum is a
        single conservative upper bound for every retained bit.
        """

        return max(self.estimated_qber_z, self.estimated_qber_x)

    @property
    def sample_size_z(self) -> int:
        return self.disclosed_bases.count(Basis.Z)

    @property
    def sample_size_x(self) -> int:
        return self.disclosed_bases.count(Basis.X)

    @property
    def n_candidate_z(self) -> int:
        return self.candidate_bases.count(Basis.Z)

    @property
    def n_candidate_x(self) -> int:
        return self.candidate_bases.count(Basis.X)


def estimate_qber_from_sample(
    alice_sifted_key: npt.ArrayLike,
    bob_sifted_key: npt.ArrayLike,
    sifted_bases: Sequence[Basis] | np.ndarray,
    rng: BaseRNG,
    *,
    sample_fraction: float = 0.2,
    sample_size: int | None = None,
) -> ParameterEstimationResult:
    """Disclose a stratified BB84 sample and remove it from both keys.

    Sampling is random without replacement inside each basis. Both bases must
    contribute at least one disclosed bit and retain at least one candidate bit;
    otherwise the mixed-basis asymptotic phase-error model has no justified
    bound and estimation fails closed.
    """

    alice, bob = validate_aligned_keys(alice_sifted_key, bob_sifted_key)
    bases = _copy_bb84_bases(sifted_bases, name="sifted_bases")
    if len(bases) != alice.size:
        raise ValueError(
            "sifted_bases must contain one basis per aligned sifted bit. "
            f"Got bases={len(bases)} and bits={alice.size}."
        )
    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    if isinstance(sample_fraction, (bool, np.bool_)) or not isinstance(
        sample_fraction, (float, int, np.floating, np.integer)
    ):
        raise ValueError(f"sample_fraction must lie strictly between 0 and 1. Got {sample_fraction!r}.")
    fraction = float(sample_fraction)
    if not np.isfinite(fraction) or not 0.0 < fraction < 1.0:
        raise ValueError(f"sample_fraction must lie strictly between 0 and 1. Got {fraction}.")
    basis_array = np.asarray(bases, dtype=object)
    z_indices = np.flatnonzero(basis_array == Basis.Z)
    x_indices = np.flatnonzero(basis_array == Basis.X)
    if z_indices.size < 2 or x_indices.size < 2:
        raise ValueError("Parameter estimation requires at least two sifted positions from each BB84 basis.")

    if sample_size is None:
        disclose_z = int(np.ceil(z_indices.size * fraction))
        disclose_x = int(np.ceil(x_indices.size * fraction))
        if disclose_z >= z_indices.size or disclose_x >= x_indices.size:
            raise ValueError("sample_fraction must leave at least one candidate bit in each BB84 basis.")
    else:
        if isinstance(sample_size, (bool, np.bool_)) or not isinstance(sample_size, (int, np.integer)):
            raise ValueError(f"sample_size must be a positive integer. Got {sample_size!r}.")
        disclose_z, disclose_x = _explicit_stratified_counts(
            int(z_indices.size), int(x_indices.size), int(sample_size)
        )

    indices = np.sort(
        np.concatenate(
            (
                rng.gen.choice(z_indices, size=disclose_z, replace=False),
                rng.gen.choice(x_indices, size=disclose_x, replace=False),
            )
        )
    )
    retain_mask = np.ones(alice.size, dtype=np.bool_)
    retain_mask[indices] = False
    disclosed_bases = tuple(bases[int(index)] for index in indices)
    candidate_bases = tuple(basis for index, basis in enumerate(bases) if retain_mask[index])
    metrics = qber_by_basis(alice[indices], bob[indices], disclosed_bases)
    if metrics.qber_z is None or metrics.qber_x is None:
        raise RuntimeError("Stratified sampling failed to disclose both BB84 bases.")
    return ParameterEstimationResult(
        n_sifted=int(alice.size),
        disclosed_indices=indices,
        disclosed_bases=disclosed_bases,
        alice_disclosed_bits=alice[indices],
        bob_disclosed_bits=bob[indices],
        estimated_qber_z=metrics.qber_z,
        estimated_qber_x=metrics.qber_x,
        estimated_qber_aggregated=metrics.qber_aggregated,
        candidate_bases=candidate_bases,
        alice_candidate_key=alice[retain_mask],
        bob_candidate_key=bob[retain_mask],
    )
