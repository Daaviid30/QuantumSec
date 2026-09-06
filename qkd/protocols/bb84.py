"""Reproducible prepare-and-measure simulation of the BB84 protocol."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG, random_basis, random_bit
from qkd._validation import copy_binary_vector
from qkd.channel.base import QuantumChannel
from qkd.metrics.qber import QBERByBasis
from qkd.metrics.qber import qber_by_basis as calculate_qber_by_basis
from qkd.metrics.security import asymptotic_bb84_secret_length
from qkd.postprocessing.parameter_estimation import (
    ParameterEstimationResult,
    estimate_qber_from_sample,
)
from qkd.postprocessing.privacy_amplification import PrivacyAmplificationResult, amplify_privacy
from qkd.postprocessing.reconciliation import CascadeConfig, ReconciliationResult, reconcile_cascade
from qkd.postprocessing.sifting import SiftingResult, sift_keys
from qkd.postprocessing.verification import VerificationResult, verify_reconciled_keys
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
        alice_bits = copy_binary_vector(self.alice_raw_bits, name="alice_raw_bits")
        bob_bits = copy_binary_vector(self.bob_measured_bits, name="bob_measured_bits")
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
    def sifted_bases(self) -> tuple[Basis, ...]:
        """Return Alice's BB84 bases aligned with the sifted key."""

        return tuple(self.alice_bases[int(index)] for index in self.matching_indices)

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
        """Return aggregate simulator-diagnostic QBER over the complete sifted key.

        This value is retained for backwards compatibility and inspection. A
        secure session never uses it for a protocol decision: ``run_session``
        estimates QBER from disclosed random positions and removes them.

        Raises
        ------
        ValueError
            If no positions survived sifting and QBER is therefore undefined.
        """

        return self.qber_by_basis.qber_aggregated

    @property
    def qber_by_basis(self) -> QBERByBasis:
        """Return simulator-only Z, X, and aggregate full-sifted QBER."""

        return calculate_qber_by_basis(
            self.alice_sifted_key,
            self.bob_sifted_key,
            self.sifted_bases,
        )

    @property
    def qber_z(self) -> float | None:
        return self.qber_by_basis.qber_z

    @property
    def qber_x(self) -> float | None:
        return self.qber_by_basis.qber_x

    @property
    def qber_aggregated(self) -> float:
        return self.qber_by_basis.qber_aggregated


class BB84SessionStatus(StrEnum):
    """Terminal state of a complete BB84 session."""

    COMPLETED = "completed"
    ABORTED = "aborted"


@dataclass(frozen=True, slots=True)
class BB84PostprocessingConfig:
    """Configuration for BB84 post-processing under assumed channel authentication.

    The legacy-named ``qber_abort_threshold`` is applied to the explicit common
    phase-error bound. Its 11% default is the familiar ideal/asymptotic BB84
    boundary under this simulator's assumptions, not a universal practical
    finite-key threshold.
    """

    sample_fraction: float = 0.2
    qber_abort_threshold: float = 0.11
    cascade: CascadeConfig = field(default_factory=CascadeConfig)
    verification_tag_length: int = 32
    security_margin_bits: int = 0

    def __post_init__(self) -> None:
        for name in ("sample_fraction", "qber_abort_threshold"):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(
                value, (float, int, np.floating, np.integer)
            ):
                raise ValueError(f"{name} must be a finite probability. Got {value!r}.")
            clean = float(value)
            valid = 0.0 < clean < 1.0 if name == "sample_fraction" else 0.0 <= clean <= 1.0
            if not np.isfinite(clean) or not valid:
                interval = "strictly between 0 and 1" if name == "sample_fraction" else "in [0, 1]"
                raise ValueError(f"{name} must lie {interval}. Got {clean}.")
            object.__setattr__(self, name, clean)
        if not isinstance(self.cascade, CascadeConfig):
            raise TypeError(f"cascade must be a CascadeConfig. Got {type(self.cascade).__name__}.")
        for name in ("verification_tag_length", "security_margin_bits"):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be an integer. Got {value!r}.")
            clean = int(value)
            if name == "verification_tag_length" and clean <= 0:
                raise ValueError("verification_tag_length must be positive.")
            if name == "security_margin_bits" and clean < 0:
                raise ValueError("security_margin_bits must be non-negative.")
            object.__setattr__(self, name, clean)

    @property
    def phase_error_abort_threshold(self) -> float:
        """Return the phase-error threshold stored under the legacy QBER name."""

        return self.qber_abort_threshold


@dataclass(frozen=True, slots=True, eq=False)
class BB84SessionResult:
    """Stage-by-stage immutable result of a complete BB84 session."""

    raw: BB84Result = field(repr=False)
    config: BB84PostprocessingConfig
    status: BB84SessionStatus
    abort_reason: str | None = None
    parameter_estimation: ParameterEstimationResult | None = field(default=None, repr=False)
    reconciliation: ReconciliationResult | None = field(default=None, repr=False)
    verification: VerificationResult | None = field(default=None, repr=False)
    privacy_amplification: PrivacyAmplificationResult | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.raw, BB84Result):
            raise TypeError(f"raw must be a BB84Result. Got {type(self.raw).__name__}.")
        if not isinstance(self.config, BB84PostprocessingConfig):
            raise TypeError(f"config must be a BB84PostprocessingConfig. Got {type(self.config).__name__}.")
        if not isinstance(self.status, BB84SessionStatus):
            raise TypeError(f"status must be a BB84SessionStatus. Got {type(self.status).__name__}.")
        if self.status is BB84SessionStatus.COMPLETED:
            stages = (
                self.parameter_estimation,
                self.reconciliation,
                self.verification,
                self.privacy_amplification,
            )
            if self.abort_reason is not None or any(stage is None for stage in stages):
                raise ValueError(
                    "A completed session requires every post-processing stage and no abort reason."
                )
        elif not self.abort_reason:
            raise ValueError("An aborted session requires a non-empty abort reason.")

    @property
    def n_raw(self) -> int:
        return self.raw.n_raw

    @property
    def n_sifted(self) -> int:
        return self.raw.n_sifted

    @property
    def diagnostic_full_sifted_qber(self) -> float | None:
        """Return aggregate full-key QBER as a backwards-compatible alias."""

        return self.diagnostic_qber_aggregated

    @property
    def diagnostic_qber_z(self) -> float | None:
        return self.raw.qber_z if self.raw.n_sifted > 0 else None

    @property
    def diagnostic_qber_x(self) -> float | None:
        return self.raw.qber_x if self.raw.n_sifted > 0 else None

    @property
    def diagnostic_qber_aggregated(self) -> float | None:
        return self.raw.qber_aggregated if self.raw.n_sifted > 0 else None

    @property
    def n_disclosed(self) -> int:
        return self.parameter_estimation.sample_size if self.parameter_estimation is not None else 0

    @property
    def estimated_qber(self) -> float | None:
        """Return aggregate sampled QBER as a backwards-compatible alias."""

        return self.estimated_qber_aggregated

    @property
    def estimated_qber_z(self) -> float | None:
        return self.parameter_estimation.estimated_qber_z if self.parameter_estimation is not None else None

    @property
    def estimated_qber_x(self) -> float | None:
        return self.parameter_estimation.estimated_qber_x if self.parameter_estimation is not None else None

    @property
    def estimated_qber_aggregated(self) -> float | None:
        return (
            self.parameter_estimation.estimated_qber_aggregated
            if self.parameter_estimation is not None
            else None
        )

    @property
    def phase_error_bound(self) -> float | None:
        return self.parameter_estimation.phase_error_bound if self.parameter_estimation is not None else None

    @property
    def n_candidate(self) -> int:
        return self.parameter_estimation.n_candidate if self.parameter_estimation is not None else 0

    @property
    def leak_ec(self) -> int:
        return self.reconciliation.leak_ec if self.reconciliation is not None else 0

    @property
    def verification_leakage(self) -> int:
        return self.verification.leakage if self.verification is not None else 0

    @property
    def total_public_leakage(self) -> int:
        """Return disclosed sample, reconciliation parities, and confirmation tag bits.

        Sampled bits are removed before extraction, so the secret-length formula
        subtracts only reconciliation and verification leakage from ``n_candidate``.
        """

        return self.n_disclosed + self.leak_ec + self.verification_leakage

    @property
    def n_reconciled(self) -> int:
        return self.reconciliation.input_length if self.reconciliation is not None else 0

    @property
    def n_final(self) -> int:
        return self.privacy_amplification.output_length if self.privacy_amplification is not None else 0

    @property
    def final_secret_fraction(self) -> float:
        return self.n_final / self.n_raw

    @property
    def alice_final_key(self) -> npt.NDArray[np.uint8] | None:
        return self.privacy_amplification.alice_final_key if self.privacy_amplification is not None else None

    @property
    def bob_final_key(self) -> npt.NDArray[np.uint8] | None:
        return self.privacy_amplification.bob_final_key if self.privacy_amplification is not None else None


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

    def run_session(
        self,
        n_signals: int,
        config: BB84PostprocessingConfig | None = None,
    ) -> BB84SessionResult:
        """Run BB84 through estimation, Cascade, verification, and extraction.

        Legitimate security aborts are represented in the returned session.
        Invalid inputs and invalid configurations still raise validation errors.
        The classical transcript is assumed to be authenticated.
        """

        clean_config = BB84PostprocessingConfig() if config is None else config
        if not isinstance(clean_config, BB84PostprocessingConfig):
            raise TypeError(f"config must be a BB84PostprocessingConfig. Got {type(clean_config).__name__}.")
        raw = self.run(n_signals)
        if raw.n_sifted < 4:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason="Insufficient sifted material for basis-aware parameter estimation.",
            )
        sifted_bases = raw.sifted_bases
        basis_counts = {basis: sifted_bases.count(basis) for basis in (Basis.Z, Basis.X)}
        if any(count < 2 for count in basis_counts.values()):
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason=(
                    "Basis-aware parameter estimation requires at least two sifted positions "
                    "from each BB84 basis."
                ),
            )
        if any(
            int(np.ceil(count * clean_config.sample_fraction)) >= count for count in basis_counts.values()
        ):
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason="Parameter estimation would leave a BB84 basis without candidate material.",
            )

        estimation = estimate_qber_from_sample(
            raw.alice_sifted_key,
            raw.bob_sifted_key,
            sifted_bases,
            self.rng,
            sample_fraction=clean_config.sample_fraction,
        )
        if estimation.phase_error_bound > 0.5:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason=(
                    f"Phase-error bound {estimation.phase_error_bound:.6f} lies outside the "
                    "asymptotic entropy estimator's domain [0, 0.5]."
                ),
                parameter_estimation=estimation,
            )
        if estimation.phase_error_bound > clean_config.phase_error_abort_threshold:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason=(
                    f"Per-basis errors Z={estimation.estimated_qber_z:.6f}, "
                    f"X={estimation.estimated_qber_x:.6f} give phase-error bound "
                    f"{estimation.phase_error_bound:.6f}, above the configured asymptotic "
                    f"threshold {clean_config.phase_error_abort_threshold:.6f}; aggregate QBER "
                    f"{estimation.estimated_qber_aggregated:.6f} is not the phase-error bound."
                ),
                parameter_estimation=estimation,
            )
        if estimation.n_candidate < clean_config.verification_tag_length:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason="Insufficient candidate material for the configured verification tag.",
                parameter_estimation=estimation,
            )

        reconciliation = reconcile_cascade(
            estimation.alice_candidate_key,
            estimation.bob_candidate_key,
            estimation.bit_error_rate,
            self.rng,
            config=clean_config.cascade,
        )
        verification = verify_reconciled_keys(
            reconciliation.alice_key,
            reconciliation.bob_corrected_key,
            self.rng,
            tag_length=clean_config.verification_tag_length,
        )
        if not verification.verified:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason="Universal-hash key confirmation failed after reconciliation.",
                parameter_estimation=estimation,
                reconciliation=reconciliation,
                verification=verification,
            )

        target_length = asymptotic_bb84_secret_length(
            estimation.n_candidate,
            phase_error_bound=estimation.phase_error_bound,
            reconciliation_leakage=reconciliation.leak_ec,
            verification_leakage=verification.leakage,
            security_margin_bits=clean_config.security_margin_bits,
        )
        if target_length <= 0:
            return BB84SessionResult(
                raw=raw,
                config=clean_config,
                status=BB84SessionStatus.ABORTED,
                abort_reason="The asymptotic security estimator produced no extractable secret bits.",
                parameter_estimation=estimation,
                reconciliation=reconciliation,
                verification=verification,
            )
        amplification = amplify_privacy(
            reconciliation.alice_key,
            reconciliation.bob_corrected_key,
            target_length,
            self.rng,
        )
        return BB84SessionResult(
            raw=raw,
            config=clean_config,
            status=BB84SessionStatus.COMPLETED,
            parameter_estimation=estimation,
            reconciliation=reconciliation,
            verification=verification,
            privacy_amplification=amplification,
        )
