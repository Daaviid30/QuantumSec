"""Reproducible prepare-and-measure simulation of the BB84 protocol."""

from collections.abc import Sequence
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG, random_basis, random_bit
from qkd.channel.base import QuantumChannel
from qkd.metrics.qber import qber as calculate_qber
from qkd.postprocessing.sifting import SiftingResult, sift_keys
from qkd.primitives.bases import Basis, bases_from_bits
from qkd.primitives.measurements import MEASUREMENTS_BY_BASIS
from qkd.primitives.states import KET0, KET1, MINUS, PLUS
from quantum.measures import sample_projective_outcome
from quantum.states import dm_from_ket
from quantum.types import ComplexArray


def _trusted_density_matrix(ket: npt.ArrayLike) -> ComplexArray:
    """Build an immutable density matrix for a validated named BB84 state."""

    density = dm_from_ket(ket)
    density.flags.writeable = False
    return density


_BB84_DENSITY_MATRICES = {
    (Basis.Z, 0): _trusted_density_matrix(KET0),
    (Basis.Z, 1): _trusted_density_matrix(KET1),
    (Basis.X, 0): _trusted_density_matrix(PLUS),
    (Basis.X, 1): _trusted_density_matrix(MINUS),
}


def _validate_bit(value: int | np.integer) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"A BB84 bit must be integer 0 or 1. Got {value!r}.")
    bit = int(value)
    if bit not in (0, 1):
        raise ValueError(f"A BB84 bit must be 0 or 1. Got {bit}.")
    return bit


def _validate_bb84_basis(basis: Basis) -> Basis:
    if not isinstance(basis, Basis) or basis not in (Basis.Z, Basis.X):
        raise ValueError(f"A BB84 basis must be Basis.Z or Basis.X. Got {basis!r}.")
    return basis


def encode_bb84_state(bit: int | np.integer, basis: Basis) -> ComplexArray:
    """Return an independent density matrix for one BB84 bit/basis symbol.

    The encoding convention is ``Z0 -> |0>``, ``Z1 -> |1>``, ``X0 -> |+>``,
    and ``X1 -> |->``.
    """

    clean_bit = _validate_bit(bit)
    clean_basis = _validate_bb84_basis(basis)
    return np.array(_BB84_DENSITY_MATRICES[(clean_basis, clean_bit)], copy=True)


def _copy_binary_vector(values: npt.ArrayLike, *, name: str) -> npt.NDArray[np.uint8]:
    vector = np.asarray(values)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional. Got shape={vector.shape}.")
    if vector.size > 0 and not np.issubdtype(vector.dtype, np.integer):
        raise ValueError(f"{name} must contain integer bits. Got dtype={vector.dtype}.")
    if np.any((vector != 0) & (vector != 1)):
        raise ValueError(f"{name} must contain only 0 and 1. Got {vector}.")

    result = np.array(vector, dtype=np.uint8, copy=True)
    result.flags.writeable = False
    return result


def _copy_bb84_bases(values: Sequence[Basis], *, name: str) -> tuple[Basis, ...]:
    bases = tuple(values)
    for index, basis in enumerate(bases):
        try:
            _validate_bb84_basis(basis)
        except ValueError as error:
            raise ValueError(f"Invalid {name} entry at index {index}: {error}") from error
    return bases


@dataclass(frozen=True, slots=True, eq=False)
class BB84Result:
    """Immutable raw and sifted material produced by one complete BB84 run."""

    alice_raw_bits: npt.NDArray[np.uint8] = field(repr=False)
    alice_bases: tuple[Basis, ...] = field(repr=False)
    bob_bases: tuple[Basis, ...] = field(repr=False)
    bob_measured_bits: npt.NDArray[np.uint8] = field(repr=False)
    sifting: SiftingResult = field(repr=False)

    def __post_init__(self) -> None:
        alice_bits = _copy_binary_vector(self.alice_raw_bits, name="alice_raw_bits")
        bob_bits = _copy_binary_vector(self.bob_measured_bits, name="bob_measured_bits")
        alice_bases = _copy_bb84_bases(self.alice_bases, name="alice_bases")
        bob_bases = _copy_bb84_bases(self.bob_bases, name="bob_bases")

        lengths = (alice_bits.size, bob_bits.size, len(alice_bases), len(bob_bases))
        if len(set(lengths)) != 1:
            raise ValueError(
                "BB84 raw bits and bases must have equal lengths. "
                f"Got alice_bits={lengths[0]}, bob_bits={lengths[1]}, "
                f"alice_bases={lengths[2]}, bob_bases={lengths[3]}."
            )
        if not isinstance(self.sifting, SiftingResult):
            raise TypeError(f"sifting must be a SiftingResult. Got {type(self.sifting).__name__}.")
        if self.sifting.n_raw != lengths[0]:
            raise ValueError(
                "Sifting metadata must describe the BB84 raw material. "
                f"Got sifting.n_raw={self.sifting.n_raw} and n_raw={lengths[0]}."
            )

        expected_mask = np.fromiter(
            (alice_basis is bob_basis for alice_basis, bob_basis in zip(alice_bases, bob_bases, strict=True)),
            dtype=np.bool_,
            count=lengths[0],
        )
        expected_indices = np.flatnonzero(expected_mask)
        if not np.array_equal(self.sifting.matching_indices, expected_indices):
            raise ValueError("Sifting indices must correspond exactly to matching BB84 bases.")
        if not np.array_equal(self.sifting.alice_sifted_key, alice_bits[expected_indices]):
            raise ValueError("Alice's sifted key must preserve her bits at the matching positions.")
        if not np.array_equal(self.sifting.bob_sifted_key, bob_bits[expected_indices]):
            raise ValueError("Bob's sifted key must preserve his bits at the matching positions.")

        object.__setattr__(self, "alice_raw_bits", alice_bits)
        object.__setattr__(self, "bob_measured_bits", bob_bits)
        object.__setattr__(self, "alice_bases", alice_bases)
        object.__setattr__(self, "bob_bases", bob_bases)

    @property
    def bob_raw_bits(self) -> npt.NDArray[np.uint8]:
        """Return Bob's measured outcomes under the raw-key naming convention."""

        return self.bob_measured_bits

    @property
    def matching_indices(self) -> npt.NDArray[np.intp]:
        """Return raw positions where Alice and Bob selected the same basis."""

        return self.sifting.matching_indices

    @property
    def alice_sifted_key(self) -> npt.NDArray[np.uint8]:
        """Return Alice's key after basis reconciliation."""

        return self.sifting.alice_sifted_key

    @property
    def bob_sifted_key(self) -> npt.NDArray[np.uint8]:
        """Return Bob's key after basis reconciliation."""

        return self.sifting.bob_sifted_key

    @property
    def n_raw(self) -> int:
        """Return the number of quantum signals sent by Alice."""

        return int(self.alice_raw_bits.size)

    @property
    def n_sifted(self) -> int:
        """Return the number of positions retained after sifting."""

        return self.sifting.n_sifted

    @property
    def sifting_efficiency(self) -> float:
        """Return the fraction of raw positions retained after sifting."""

        return self.sifting.sifting_efficiency

    @property
    def qber(self) -> float:
        """Return QBER over the complete sifted key.

        Raises
        ------
        ValueError
            If no positions survived sifting and QBER is therefore undefined.
        """

        return calculate_qber(self.alice_sifted_key, self.bob_sifted_key)


@dataclass(frozen=True, slots=True, eq=False)
class BB84Protocol:
    """Run BB84 with an injected random source and density-matrix channel.

    Alice's named states are trusted immutable constants, so their repeated
    spectral validation is skipped at the channel input. By default the state
    returned by the injected channel is fully validated before Bob samples it;
    ``validate_channel_output=False`` enables the existing tested fast path.
    """

    channel: QuantumChannel
    rng: BaseRNG = field(repr=False)
    validate_channel_output: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.channel, QuantumChannel):
            raise TypeError(f"channel must implement QuantumChannel. Got {type(self.channel).__name__}.")
        if not isinstance(self.rng, BaseRNG):
            raise TypeError(f"rng must implement BaseRNG. Got {type(self.rng).__name__}.")
        if not isinstance(self.validate_channel_output, bool):
            raise TypeError(
                f"validate_channel_output must be a bool. Got {type(self.validate_channel_output).__name__}."
            )

    def run(self, n_signals: int) -> BB84Result:
        """Simulate preparation, transmission, measurement, sifting, and QBER data."""

        if isinstance(n_signals, (bool, np.bool_)) or not isinstance(n_signals, (int, np.integer)):
            raise ValueError(f"n_signals must be a positive integer. Got {n_signals!r}.")
        signal_count = int(n_signals)
        if signal_count <= 0:
            raise ValueError(f"n_signals must be positive. Got {signal_count}.")

        alice_raw_bits = np.asarray(random_bit(self.rng, size=signal_count), dtype=np.uint8)
        alice_bases = bases_from_bits(np.asarray(random_basis(self.rng, size=signal_count)))
        bob_bases = bases_from_bits(np.asarray(random_basis(self.rng, size=signal_count)))
        bob_measured_bits = np.empty(signal_count, dtype=np.uint8)

        for index, (alice_bit, alice_basis, bob_basis) in enumerate(
            zip(alice_raw_bits, alice_bases, bob_bases, strict=True)
        ):
            prepared_state = _BB84_DENSITY_MATRICES[(alice_basis, int(alice_bit))]
            received_state = self.channel.apply(prepared_state, validate_state=False)
            sample = sample_projective_outcome(
                received_state,
                MEASUREMENTS_BY_BASIS[bob_basis],
                self.rng,
                validate_state=self.validate_channel_output,
            )
            bob_measured_bits[index] = sample.outcome

        sifting = sift_keys(
            alice_bases,
            bob_bases,
            alice_raw_bits,
            bob_measured_bits,
        )
        return BB84Result(
            alice_raw_bits=alice_raw_bits,
            alice_bases=alice_bases,
            bob_bases=bob_bases,
            bob_measured_bits=bob_measured_bits,
            sifting=sifting,
        )
