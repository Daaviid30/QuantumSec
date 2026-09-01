"""Parity-based Cascade information reconciliation for aligned QKD keys."""

from collections import deque
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG
from qkd._validation import copy_indices, validate_aligned_keys


@dataclass(frozen=True, slots=True)
class CascadeConfig:
    """Configuration for the original-style Cascade block-size strategy.

    The first block size is approximately ``initial_block_factor / QBER`` and
    doubles on each later pass. For a zero estimate, one full-key block is used.
    """

    passes: int = 4
    initial_block_factor: float = 0.73
    maximum_initial_block_size: int | None = None
    maximum_lookback_steps: int | None = None

    def __post_init__(self) -> None:
        if isinstance(self.passes, (bool, np.bool_)) or not isinstance(self.passes, (int, np.integer)):
            raise ValueError(f"passes must be a positive integer. Got {self.passes!r}.")
        if int(self.passes) <= 0:
            raise ValueError(f"passes must be positive. Got {self.passes}.")
        if isinstance(self.initial_block_factor, (bool, np.bool_)) or not isinstance(
            self.initial_block_factor, (float, int, np.floating, np.integer)
        ):
            raise ValueError("initial_block_factor must be a positive finite number.")
        factor = float(self.initial_block_factor)
        if not np.isfinite(factor) or factor <= 0.0:
            raise ValueError(f"initial_block_factor must be positive and finite. Got {factor}.")
        maximum = self.maximum_initial_block_size
        if maximum is not None:
            if isinstance(maximum, (bool, np.bool_)) or not isinstance(maximum, (int, np.integer)):
                raise ValueError("maximum_initial_block_size must be a positive integer or None.")
            if int(maximum) <= 0:
                raise ValueError("maximum_initial_block_size must be positive when provided.")
            object.__setattr__(self, "maximum_initial_block_size", int(maximum))
        lookback_maximum = self.maximum_lookback_steps
        if lookback_maximum is not None:
            if isinstance(lookback_maximum, (bool, np.bool_)) or not isinstance(
                lookback_maximum, (int, np.integer)
            ):
                raise ValueError("maximum_lookback_steps must be a positive integer or None.")
            if int(lookback_maximum) <= 0:
                raise ValueError("maximum_lookback_steps must be positive when provided.")
            object.__setattr__(self, "maximum_lookback_steps", int(lookback_maximum))
        object.__setattr__(self, "passes", int(self.passes))
        object.__setattr__(self, "initial_block_factor", factor)


@dataclass(frozen=True, slots=True, eq=False)
class CascadePassStatistics:
    """Immutable statistics and permutation for one Cascade pass."""

    pass_index: int
    block_size: int
    block_count: int
    corrected_errors: int
    parity_disclosures: int
    permutation: npt.NDArray[np.intp] = field(repr=False)

    def __post_init__(self) -> None:
        permutation = copy_indices(self.permutation, name="permutation")
        integer_fields = {
            "pass_index": self.pass_index,
            "block_size": self.block_size,
            "block_count": self.block_count,
            "corrected_errors": self.corrected_errors,
            "parity_disclosures": self.parity_disclosures,
        }
        for name, value in integer_fields.items():
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
            if int(value) < 0:
                raise ValueError(f"{name} must be non-negative. Got {value}.")
            object.__setattr__(self, name, int(value))
        if self.block_size <= 0 or self.block_count <= 0:
            raise ValueError("Cascade pass block_size and block_count must be positive.")
        if permutation.size > 0 and not np.array_equal(np.sort(permutation), np.arange(permutation.size)):
            raise ValueError("permutation must contain every key position exactly once.")
        object.__setattr__(self, "permutation", permutation)


@dataclass(frozen=True, slots=True, eq=False)
class ReconciliationResult:
    """Immutable corrected key and conservative public parity transcript size."""

    alice_key: npt.NDArray[np.uint8] = field(repr=False)
    bob_corrected_key: npt.NDArray[np.uint8] = field(repr=False)
    corrected_errors: int
    parity_disclosures: int
    pass_statistics: tuple[CascadePassStatistics, ...]
    residual_mismatch_count: int

    def __post_init__(self) -> None:
        alice, bob = validate_aligned_keys(self.alice_key, self.bob_corrected_key)
        stats = tuple(self.pass_statistics)
        if not stats or not all(isinstance(item, CascadePassStatistics) for item in stats):
            raise ValueError("pass_statistics must contain at least one CascadePassStatistics value.")
        for name in ("corrected_errors", "parity_disclosures", "residual_mismatch_count"):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
            if int(value) < 0:
                raise ValueError(f"{name} must be non-negative. Got {value}.")
            object.__setattr__(self, name, int(value))
        if self.corrected_errors != sum(item.corrected_errors for item in stats):
            raise ValueError("corrected_errors must equal the sum of per-pass corrections.")
        if self.parity_disclosures != sum(item.parity_disclosures for item in stats):
            raise ValueError("parity_disclosures must equal the sum of per-pass disclosures.")
        actual_residual = int(np.count_nonzero(alice != bob))
        if self.residual_mismatch_count != actual_residual:
            raise ValueError("residual_mismatch_count must match the simulator-only exact diagnostic.")
        object.__setattr__(self, "alice_key", alice)
        object.__setattr__(self, "bob_corrected_key", bob)
        object.__setattr__(self, "pass_statistics", stats)

    @property
    def input_length(self) -> int:
        return int(self.alice_key.size)

    @property
    def leak_ec(self) -> int:
        """Return the conservative leakage: one bit per disclosed Alice parity."""

        return self.parity_disclosures

    @property
    def passes(self) -> int:
        return len(self.pass_statistics)


@dataclass(slots=True)
class _PassLayout:
    permutation: npt.NDArray[np.intp]
    block_size: int
    blocks: tuple[npt.NDArray[np.intp], ...]
    inverse: npt.NDArray[np.intp]


def _parity(key: npt.NDArray[np.uint8], indices: npt.NDArray[np.intp]) -> int:
    return int(np.bitwise_xor.reduce(key[indices], initial=np.uint8(0)))


def _initial_block_size(n_bits: int, estimated_qber: float, config: CascadeConfig) -> int:
    if estimated_qber == 0.0:
        size = n_bits
    else:
        size = max(1, int(round(config.initial_block_factor / estimated_qber)))
    if config.maximum_initial_block_size is not None:
        size = min(size, config.maximum_initial_block_size)
    return min(size, n_bits)


def reconcile_cascade(
    alice_key: npt.ArrayLike,
    bob_key: npt.ArrayLike,
    estimated_qber: float,
    rng: BaseRNG,
    *,
    config: CascadeConfig | None = None,
) -> ReconciliationResult:
    """Correct Bob through disclosed block parities, binary searches, and look-back.

    No mismatch-position oracle is used by the reconciliation decisions. Exact
    residual mismatches are counted only after the public-protocol simulation as
    a diagnostic that cannot affect correction or verification.
    """

    alice, initial_bob = validate_aligned_keys(alice_key, bob_key)
    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    if isinstance(estimated_qber, (bool, np.bool_)) or not isinstance(
        estimated_qber, (float, int, np.floating, np.integer)
    ):
        raise ValueError(f"estimated_qber must be a finite probability. Got {estimated_qber!r}.")
    qber = float(estimated_qber)
    if not np.isfinite(qber) or not 0.0 <= qber <= 1.0:
        raise ValueError(f"estimated_qber must lie in [0, 1]. Got {qber}.")
    clean_config = CascadeConfig() if config is None else config
    if not isinstance(clean_config, CascadeConfig):
        raise TypeError(f"config must be a CascadeConfig. Got {type(clean_config).__name__}.")

    bob = np.array(initial_bob, dtype=np.uint8, copy=True)
    n_bits = int(alice.size)
    first_block_size = _initial_block_size(n_bits, qber, clean_config)
    layouts: list[_PassLayout] = []
    statistics: list[CascadePassStatistics] = []

    for pass_index in range(clean_config.passes):
        permutation = (
            np.arange(n_bits, dtype=np.intp)
            if pass_index == 0
            else np.asarray(rng.gen.permutation(n_bits), dtype=np.intp)
        )
        block_size = min(n_bits, first_block_size * (2**pass_index))
        blocks = tuple(permutation[start : start + block_size] for start in range(0, n_bits, block_size))
        inverse = np.empty(n_bits, dtype=np.intp)
        inverse[permutation] = np.arange(n_bits, dtype=np.intp)
        layouts.append(_PassLayout(permutation, block_size, blocks, inverse))

        disclosure_counts = [0] * (pass_index + 1)
        correction_counts = [0] * (pass_index + 1)
        # Every block's Alice parity is publicly disclosed once at pass start.
        disclosure_counts[pass_index] += len(blocks)
        pending: deque[tuple[int, int]] = deque()
        queued: set[tuple[int, int]] = set()
        for block_index, indices in enumerate(blocks):
            if _parity(alice, indices) != _parity(bob, indices):
                item = (pass_index, block_index)
                pending.append(item)
                queued.add(item)

        lookback_steps = 0
        derived_lookback_limit = len(blocks) + n_bits * pass_index
        lookback_limit = clean_config.maximum_lookback_steps or derived_lookback_limit
        while pending:
            lookback_steps += 1
            if lookback_steps > lookback_limit:
                raise RuntimeError(
                    "Cascade look-back exceeded its maximum step limit. "
                    f"Got limit={lookback_limit} in pass={pass_index}."
                )
            source_pass, block_index = pending.popleft()
            queued.discard((source_pass, block_index))
            indices = layouts[source_pass].blocks[block_index]
            if _parity(alice, indices) == _parity(bob, indices):
                continue

            search_indices = indices
            while search_indices.size > 1:
                midpoint = search_indices.size // 2
                left = search_indices[:midpoint]
                disclosure_counts[source_pass] += 1
                search_indices = (
                    left if _parity(alice, left) != _parity(bob, left) else search_indices[midpoint:]
                )
            corrected_position = int(search_indices[0])
            bob[corrected_position] ^= np.uint8(1)
            correction_counts[source_pass] += 1

            # A correction can expose a previously hidden error pair in every
            # other pass whose root block parity was already disclosed.
            for affected_pass, layout in enumerate(layouts):
                if affected_pass == source_pass:
                    continue
                affected_block = int(layout.inverse[corrected_position]) // layout.block_size
                item = (affected_pass, affected_block)
                if item not in queued:
                    pending.append(item)
                    queued.add(item)

        # Look-back corrections are attributed to the pass whose parity tree was queried.
        for prior_index, old_stat in enumerate(statistics):
            if correction_counts[prior_index] or disclosure_counts[prior_index]:
                statistics[prior_index] = CascadePassStatistics(
                    pass_index=old_stat.pass_index,
                    block_size=old_stat.block_size,
                    block_count=old_stat.block_count,
                    corrected_errors=old_stat.corrected_errors + correction_counts[prior_index],
                    parity_disclosures=old_stat.parity_disclosures + disclosure_counts[prior_index],
                    permutation=old_stat.permutation,
                )
        statistics.append(
            CascadePassStatistics(
                pass_index=pass_index,
                block_size=block_size,
                block_count=len(blocks),
                corrected_errors=correction_counts[pass_index],
                parity_disclosures=disclosure_counts[pass_index],
                permutation=permutation,
            )
        )

    bob.flags.writeable = False
    return ReconciliationResult(
        alice_key=alice,
        bob_corrected_key=bob,
        corrected_errors=sum(item.corrected_errors for item in statistics),
        parity_disclosures=sum(item.parity_disclosures for item in statistics),
        pass_statistics=tuple(statistics),
        residual_mismatch_count=int(np.count_nonzero(alice != bob)),
    )
