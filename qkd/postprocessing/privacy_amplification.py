"""Toeplitz-universal privacy amplification for reconciled QKD keys."""

from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from core.rng import BaseRNG
from qkd.postprocessing._validation import copy_binary_vector, validate_aligned_keys
from qkd.postprocessing.universal_hashing import generate_toeplitz_seed, toeplitz_hash


@dataclass(frozen=True, slots=True, eq=False)
class PrivacyAmplificationResult:
    """Immutable final keys and public Toeplitz seed metadata."""

    input_length: int
    output_length: int
    public_seed: npt.NDArray[np.uint8] = field(repr=False)
    alice_final_key: npt.NDArray[np.uint8] = field(repr=False)
    bob_final_key: npt.NDArray[np.uint8] = field(repr=False)

    def __post_init__(self) -> None:
        for name in ("input_length", "output_length"):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
            if int(value) < 0:
                raise ValueError(f"{name} must be non-negative. Got {value}.")
            object.__setattr__(self, name, int(value))
        if self.output_length > self.input_length:
            raise ValueError("output_length cannot exceed input_length.")
        seed = copy_binary_vector(self.public_seed, name="public_seed")
        alice = copy_binary_vector(self.alice_final_key, name="alice_final_key")
        bob = copy_binary_vector(self.bob_final_key, name="bob_final_key")
        if alice.size != self.output_length or bob.size != self.output_length:
            raise ValueError("Final key lengths must equal output_length.")
        expected_seed = 0 if self.output_length == 0 else self.input_length + self.output_length - 1
        if seed.size != expected_seed:
            raise ValueError(f"public_seed must contain {expected_seed} bits. Got {seed.size}.")
        object.__setattr__(self, "public_seed", seed)
        object.__setattr__(self, "alice_final_key", alice)
        object.__setattr__(self, "bob_final_key", bob)

    @property
    def compression_ratio(self) -> float:
        if self.input_length == 0:
            return 0.0
        return self.output_length / self.input_length


def amplify_privacy(
    alice_key: npt.ArrayLike,
    bob_key: npt.ArrayLike,
    target_length: int,
    rng: BaseRNG,
) -> PrivacyAmplificationResult:
    """Hash both reconciled keys to an explicitly derived target length."""

    alice, bob = validate_aligned_keys(alice_key, bob_key, allow_empty=True)
    if not isinstance(rng, BaseRNG):
        raise TypeError(f"rng must implement BaseRNG. Got {type(rng).__name__}.")
    if isinstance(target_length, (bool, np.bool_)) or not isinstance(target_length, (int, np.integer)):
        raise ValueError(f"target_length must be a non-negative integer. Got {target_length!r}.")
    output_length = int(target_length)
    if output_length < 0 or output_length > alice.size:
        raise ValueError(f"target_length must lie in [0, {alice.size}]. Got {output_length}.")
    seed = generate_toeplitz_seed(int(alice.size), output_length, rng)
    return PrivacyAmplificationResult(
        input_length=int(alice.size),
        output_length=output_length,
        public_seed=seed,
        alice_final_key=toeplitz_hash(alice, output_length, seed),
        bob_final_key=toeplitz_hash(bob, output_length, seed),
    )
