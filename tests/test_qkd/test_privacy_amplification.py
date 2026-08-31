import numpy as np
import pytest
from numpy.testing import assert_array_equal

from core.rng import SeededRNG
from qkd.postprocessing import amplify_privacy


def test_privacy_amplification_agrees_and_respects_target_length():
    key = np.arange(64, dtype=np.uint8) % 2
    result = amplify_privacy(key, key, 23, SeededRNG(18))

    assert result.input_length == 64
    assert result.output_length == 23
    assert result.compression_ratio == pytest.approx(23 / 64)
    assert_array_equal(result.alice_final_key, result.bob_final_key)
    assert not result.alice_final_key.flags.writeable
    assert result.public_seed.size == 64 + 23 - 1


def test_privacy_amplification_reproduces_public_seed_and_final_key():
    key = np.arange(40, dtype=np.uint8) % 2
    first = amplify_privacy(key, key, 10, SeededRNG(3))
    second = amplify_privacy(key, key, 10, SeededRNG(3))

    assert_array_equal(first.public_seed, second.public_seed)
    assert_array_equal(first.alice_final_key, second.alice_final_key)


def test_privacy_amplification_handles_zero_target_explicitly():
    result = amplify_privacy([0, 1], [0, 1], 0, SeededRNG(1))
    assert result.output_length == 0
    assert result.public_seed.size == 0
    assert result.alice_final_key.size == 0


@pytest.mark.parametrize("target", [-1, 4, True])
def test_privacy_amplification_rejects_invalid_target(target):
    with pytest.raises(ValueError, match="target_length"):
        amplify_privacy([0, 1, 0], [0, 1, 0], target, SeededRNG(1))
