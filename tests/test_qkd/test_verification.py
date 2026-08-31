import numpy as np
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import verify_reconciled_keys


def test_equal_keys_verify_and_tag_leakage_is_tracked():
    key = np.arange(32, dtype=np.uint8) % 2
    result = verify_reconciled_keys(key, key, SeededRNG(14), tag_length=12)

    assert result.verified
    assert result.leakage == 12
    assert result.residual_mismatch_count == 0
    assert_array_equal(result.alice_tag, result.bob_tag)


def test_different_keys_fail_for_deterministic_hash_setup():
    alice = np.zeros(32, dtype=np.uint8)
    bob = alice.copy()
    bob[7] = 1
    result = verify_reconciled_keys(alice, bob, SeededRNG(31), tag_length=16)

    assert not result.verified
    assert result.residual_mismatch_count == 1


def test_verification_seed_and_tags_reproduce_with_equal_rng_state():
    key = np.arange(24, dtype=np.uint8) % 2
    first = verify_reconciled_keys(key, key, SeededRNG(22), tag_length=8)
    second = verify_reconciled_keys(key, key, SeededRNG(22), tag_length=8)

    assert_array_equal(first.public_seed, second.public_seed)
    assert_array_equal(first.alice_tag, second.alice_tag)
