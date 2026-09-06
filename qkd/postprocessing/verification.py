"""Universal-hash verification of key agreement after information reconciliation."""

from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG
from qkd._validation import copy_binary_vector, validate_aligned_keys
from qkd.postprocessing.universal_hashing import generate_toeplitz_seed, toeplitz_hash


@dataclass(frozen=True, slots=True, eq=False)
class VerificationResult:
    """Immutable public key-agreement verification data and protocol decision."""

    verified: bool
    tag_length: int
    public_seed: npt.NDArray[np.uint8] = field(repr=False)
    alice_tag: npt.NDArray[np.uint8] = field(repr=False)
    bob_tag: npt.NDArray[np.uint8] = field(repr=False)
    residual_mismatch_count: int

    def __post_init__(self) -> None:
        if not isinstance(self.verified, (bool, np.bool_)):
            raise TypeError(f"verified must be a bool. Got {type(self.verified).__name__}.")
        if isinstance(self.tag_length, (bool, np.bool_)) or not isinstance(
            self.tag_length, (int, np.integer)
        ):
            raise ValueError(f"tag_length must be a positive integer. Got {self.tag_length!r}.")
        tag_length = int(self.tag_length)
        if tag_length <= 0:
            raise ValueError(f"tag_length must be positive. Got {tag_length}.")
        seed = copy_binary_vector(self.public_seed, name="public_seed")
        alice_tag = copy_binary_vector(self.alice_tag, name="alice_tag")
        bob_tag = copy_binary_vector(self.bob_tag, name="bob_tag")
        if alice_tag.size != tag_length or bob_tag.size != tag_length:
            raise ValueError("Verification tags must match tag_length.")
        decision = bool(np.array_equal(alice_tag, bob_tag))
        if bool(self.verified) != decision:
            raise ValueError("verified must be determined solely by the public tag comparison.")
        if isinstance(self.residual_mismatch_count, (bool, np.bool_)) or not isinstance(
            self.residual_mismatch_count, (int, np.integer)
        ):
            raise ValueError("residual_mismatch_count must be a non-negative integer.")
        residual = int(self.residual_mismatch_count)
        if residual < 0:
            raise ValueError("residual_mismatch_count must be non-negative.")
        object.__setattr__(self, "verified", decision)
        object.__setattr__(self, "tag_length", tag_length)
        object.__setattr__(self, "public_seed", seed)
        object.__setattr__(self, "alice_tag", alice_tag)
        object.__setattr__(self, "bob_tag", bob_tag)
        object.__setattr__(self, "residual_mismatch_count", residual)

    @property
    def leakage(self) -> int:
        """Return the number of public Alice tag bits."""

        return self.tag_length


def verify_reconciled_keys(
    alice_key: npt.ArrayLike,
    bob_key: npt.ArrayLike,
    rng: BaseRNG,
    *,
    tag_length: int = 32,
) -> VerificationResult:
    """Verify reconciled-key agreement using public Toeplitz-universal hash tags.

    The exact mismatch count is retained only as a simulator diagnostic. The
    protocol decision is exclusively the comparison of the two public tags.
    This step does not authenticate the classical channel.
    """

    alice, bob = validate_aligned_keys(alice_key, bob_key)
    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    if isinstance(tag_length, (bool, np.bool_)) or not isinstance(tag_length, (int, np.integer)):
        raise ValueError(f"tag_length must be a positive integer. Got {tag_length!r}.")
    clean_tag_length = int(tag_length)
    if clean_tag_length <= 0 or clean_tag_length > alice.size:
        raise ValueError(
            "tag_length must be positive and cannot exceed the reconciled key length. "
            f"Got {clean_tag_length} for {alice.size} bits."
        )
    seed = generate_toeplitz_seed(int(alice.size), clean_tag_length, rng)
    alice_tag = toeplitz_hash(alice, clean_tag_length, seed)
    bob_tag = toeplitz_hash(bob, clean_tag_length, seed)
    return VerificationResult(
        verified=bool(np.array_equal(alice_tag, bob_tag)),
        tag_length=clean_tag_length,
        public_seed=seed,
        alice_tag=alice_tag,
        bob_tag=bob_tag,
        residual_mismatch_count=int(np.count_nonzero(alice != bob)),
    )
