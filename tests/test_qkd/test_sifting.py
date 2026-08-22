import numpy as np
import pytest
from numpy.testing import assert_array_equal

from qkd.postprocessing import SiftingResult, sift_keys
from qkd.primitives import Basis


def test_sifting_keeps_every_position_when_all_bases_match():
    alice_bases = (Basis.Z, Basis.X, Basis.Y, Basis.Z)
    bob_bases = (Basis.Z, Basis.X, Basis.Y, Basis.Z)
    alice_bits = np.array([0, 1, 1, 0])
    bob_bits = np.array([0, 1, 0, 0])

    result = sift_keys(alice_bases, bob_bases, alice_bits, bob_bits)

    assert_array_equal(result.matching_indices, [0, 1, 2, 3])
    assert_array_equal(result.alice_sifted_key, alice_bits)
    assert_array_equal(result.bob_sifted_key, bob_bits)
    assert result.n_raw == 4
    assert result.n_sifted == 4
    assert result.sifting_efficiency == 1.0


def test_sifting_returns_empty_keys_when_no_bases_match():
    result = sift_keys(
        (Basis.Z, Basis.X, Basis.Z),
        (Basis.X, Basis.Z, Basis.X),
        np.array([0, 1, 1]),
        np.array([1, 0, 1]),
    )

    assert_array_equal(result.matching_indices, np.array([], dtype=np.intp))
    assert_array_equal(result.alice_sifted_key, np.array([], dtype=np.uint8))
    assert_array_equal(result.bob_sifted_key, np.array([], dtype=np.uint8))
    assert result.n_sifted == 0
    assert result.sifting_efficiency == 0.0


def test_sifting_known_mixed_example_preserves_each_partys_bits():
    alice_bits = np.array([0, 1, 0, 1, 1, 0])
    bob_bits = np.array([1, 1, 1, 1, 0, 0])
    result = sift_keys(
        (Basis.Z, Basis.X, Basis.X, Basis.Z, Basis.X, Basis.Z),
        (Basis.Z, Basis.Z, Basis.X, Basis.X, Basis.X, Basis.Z),
        alice_bits,
        bob_bits,
    )

    assert_array_equal(result.matching_indices, [0, 2, 4, 5])
    assert_array_equal(result.alice_sifted_key, [0, 0, 1, 0])
    assert_array_equal(result.bob_sifted_key, [1, 1, 0, 0])
    assert result.sifting_efficiency == pytest.approx(4 / 6)


@pytest.mark.parametrize(
    ("alice_bases", "bob_bases", "alice_bits", "bob_bits"),
    [
        ((Basis.Z,), (Basis.Z, Basis.X), np.array([0]), np.array([0])),
        ((Basis.Z,), (Basis.Z,), np.array([0, 1]), np.array([0])),
        ((Basis.Z,), (Basis.Z,), np.array([0]), np.array([0, 1])),
    ],
)
def test_sifting_rejects_mismatched_input_lengths(alice_bases, bob_bases, alice_bits, bob_bits):
    with pytest.raises(ValueError, match="equal lengths"):
        sift_keys(alice_bases, bob_bases, alice_bits, bob_bits)


@pytest.mark.parametrize(
    ("alice_bases", "bob_bases", "alice_bits", "bob_bits", "message"),
    [
        (np.array([[Basis.Z]]), (Basis.Z,), np.array([0]), np.array([0]), "one-dimensional"),
        ((Basis.Z,), np.array([[Basis.Z]]), np.array([0]), np.array([0]), "one-dimensional"),
        ((Basis.Z,), (Basis.Z,), np.array([[0]]), np.array([0]), "one-dimensional"),
        ((Basis.Z,), (Basis.Z,), np.array([0]), np.array([[0]]), "one-dimensional"),
        (("Z",), (Basis.Z,), np.array([0]), np.array([0]), "Basis values"),
        ((Basis.Z,), (Basis.Z,), np.array([2]), np.array([0]), "only 0 and 1"),
        ((Basis.Z,), (Basis.Z,), np.array([0.0]), np.array([0]), "integer bits"),
    ],
)
def test_sifting_rejects_malformed_vectors(alice_bases, bob_bases, alice_bits, bob_bits, message):
    with pytest.raises(ValueError, match=message):
        sift_keys(alice_bases, bob_bases, alice_bits, bob_bits)


def test_sifting_does_not_mutate_or_alias_inputs_and_returns_protected_arrays():
    alice_bits = np.array([0, 1, 0])
    bob_bits = np.array([0, 0, 0])
    original_alice = alice_bits.copy()
    original_bob = bob_bits.copy()

    result = sift_keys(
        (Basis.Z, Basis.X, Basis.Z),
        (Basis.Z, Basis.X, Basis.X),
        alice_bits,
        bob_bits,
    )

    assert SiftingResult.__eq__ is object.__eq__
    assert_array_equal(alice_bits, original_alice)
    assert_array_equal(bob_bits, original_bob)
    assert not np.shares_memory(result.alice_sifted_key, alice_bits)
    assert not np.shares_memory(result.bob_sifted_key, bob_bits)
    assert not result.matching_indices.flags.writeable
    assert not result.alice_sifted_key.flags.writeable
    assert not result.bob_sifted_key.flags.writeable
    with pytest.raises(ValueError):
        result.alice_sifted_key[0] = 1


def test_empty_sifting_is_valid_but_efficiency_is_undefined():
    result = sift_keys((), (), np.array([], dtype=int), np.array([], dtype=int))

    with pytest.raises(ValueError, match="undefined"):
        _ = result.sifting_efficiency
