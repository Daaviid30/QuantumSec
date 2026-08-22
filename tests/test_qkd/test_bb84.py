import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from core.rng import SeededRNG
from qkd.channel import DepolarizingChannel, IdentityChannel, QuantumChannel
from qkd.primitives import Basis
from qkd.primitives.states import KET0, KET1, MINUS, PLUS
from qkd.protocols import BB84Protocol, BB84Result, encode_bb84_state
from quantum.states import dm_from_ket
from quantum.types import ArrayLike, ComplexArray


class _InvalidOutputChannel(QuantumChannel):
    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        return np.diag([1.1, -0.1]).astype(np.complex128)


@pytest.mark.parametrize(
    ("basis", "bit", "expected_ket"),
    [
        (Basis.Z, 0, KET0),
        (Basis.Z, 1, KET1),
        (Basis.X, 0, PLUS),
        (Basis.X, 1, MINUS),
    ],
)
def test_bb84_encoding_convention_returns_expected_density_matrix(basis, bit, expected_ket):
    assert_allclose(encode_bb84_state(bit, basis), dm_from_ket(expected_ket))


def test_bb84_encoding_returns_independent_state_copies():
    first = encode_bb84_state(0, Basis.Z)
    second = encode_bb84_state(0, Basis.Z)

    first[0, 0] = 0.0

    assert_allclose(second, dm_from_ket(KET0))
    assert not np.shares_memory(first, second)


@pytest.mark.parametrize(
    ("bit", "basis"),
    [(-1, Basis.Z), (2, Basis.X), (True, Basis.Z), (0, Basis.Y), (0, "Z")],
)
def test_bb84_encoding_rejects_invalid_symbols(bit, basis):
    with pytest.raises(ValueError):
        encode_bb84_state(bit, basis)


def test_ideal_bb84_is_correct_end_to_end():
    n_signals = 256
    result = BB84Protocol(IdentityChannel(), SeededRNG(2026)).run(n_signals)
    expected_indices = np.flatnonzero(
        np.fromiter(
            (alice is bob for alice, bob in zip(result.alice_bases, result.bob_bases, strict=True)),
            dtype=np.bool_,
            count=n_signals,
        )
    )

    assert isinstance(result, BB84Result)
    assert result.n_raw == n_signals
    assert result.alice_raw_bits.shape == (n_signals,)
    assert result.bob_measured_bits.shape == (n_signals,)
    assert len(result.alice_bases) == n_signals
    assert len(result.bob_bases) == n_signals
    assert set(result.alice_bases) <= {Basis.Z, Basis.X}
    assert set(result.bob_bases) <= {Basis.Z, Basis.X}
    assert_array_equal(result.matching_indices, expected_indices)
    assert_array_equal(result.alice_sifted_key, result.bob_sifted_key)
    assert result.n_sifted == expected_indices.size
    assert result.sifting_efficiency == pytest.approx(result.n_sifted / n_signals)
    assert result.qber == 0.0


def test_ideal_bb84_reproduces_the_complete_run_with_equal_seeds():
    first = BB84Protocol(IdentityChannel(), SeededRNG(88)).run(128)
    second = BB84Protocol(IdentityChannel(), SeededRNG(88)).run(128)

    assert first.alice_bases == second.alice_bases
    assert first.bob_bases == second.bob_bases
    assert_array_equal(first.alice_raw_bits, second.alice_raw_bits)
    assert_array_equal(first.bob_measured_bits, second.bob_measured_bits)
    assert_array_equal(first.matching_indices, second.matching_indices)
    assert_array_equal(first.alice_sifted_key, second.alice_sifted_key)
    assert_array_equal(first.bob_sifted_key, second.bob_sifted_key)
    assert first.qber == second.qber == 0.0


def test_different_seeds_can_produce_different_bb84_runs():
    first = BB84Protocol(IdentityChannel(), SeededRNG(1)).run(128)
    second = BB84Protocol(IdentityChannel(), SeededRNG(2)).run(128)

    assert not (
        np.array_equal(first.alice_raw_bits, second.alice_raw_bits)
        and first.alice_bases == second.alice_bases
        and first.bob_bases == second.bob_bases
    )


def test_bb84_result_protects_all_stored_key_arrays():
    result = BB84Protocol(IdentityChannel(), SeededRNG(12)).run(64)

    assert BB84Result.__eq__ is object.__eq__
    assert result.bob_raw_bits is result.bob_measured_bits
    assert not result.alice_raw_bits.flags.writeable
    assert not result.bob_measured_bits.flags.writeable
    assert not result.alice_sifted_key.flags.writeable
    assert not result.bob_sifted_key.flags.writeable
    with pytest.raises(ValueError):
        result.alice_raw_bits[0] = 1 - result.alice_raw_bits[0]


def test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness():
    result = BB84Protocol(
        DepolarizingChannel(p=0.4),
        SeededRNG(41),
        validate_channel_output=False,
    ).run(512)

    assert result.n_raw == 512
    assert result.n_sifted > 0
    assert 0.0 <= result.qber <= 1.0


def test_bb84_validates_the_injected_channels_output_by_default():
    protocol = BB84Protocol(_InvalidOutputChannel(), SeededRNG(9))

    with pytest.raises(ValueError, match="positive semidefinite"):
        protocol.run(1)


@pytest.mark.parametrize("n_signals", [0, -1, 1.0, True])
def test_bb84_rejects_non_positive_or_non_integer_signal_counts(n_signals):
    protocol = BB84Protocol(IdentityChannel(), SeededRNG(5))

    with pytest.raises(ValueError, match="n_signals"):
        protocol.run(n_signals)
