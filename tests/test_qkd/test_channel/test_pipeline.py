import numpy as np
import pytest
from numpy.testing import assert_allclose

from qkd.channel import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    ChannelPipeline,
    DepolarizingChannel,
    IdentityChannel,
    PhaseFlipChannel,
)
from qkd.primitives.states import KET0, MINUS, PLUS
from quantum.states import dm_from_ket


def test_empty_pipeline_is_an_identity_without_aliasing_input():
    rho = dm_from_ket(PLUS)

    output = ChannelPipeline(()).apply(rho)

    assert_allclose(output, rho)
    assert not np.shares_memory(output, rho)


def test_pipeline_composes_identity_channels():
    rho = dm_from_ket(PLUS)
    pipeline = ChannelPipeline((IdentityChannel(), IdentityChannel()))

    assert_allclose(pipeline.apply(rho), rho)


def test_pipeline_composes_bit_and_phase_flips_in_order():
    rho = dm_from_ket(PLUS)
    pipeline = ChannelPipeline((BitFlipChannel(p=1.0), PhaseFlipChannel(p=1.0)))

    assert_allclose(pipeline.apply(rho), dm_from_ket(MINUS))


def test_pipeline_matches_manual_sequential_application():
    rho = dm_from_ket(KET0)
    first = DepolarizingChannel(p=0.23)
    second = AmplitudeDampingChannel(gamma=0.41)
    pipeline = ChannelPipeline((first, second))

    expected = second.apply(first.apply(rho), validate_state=False)

    assert_allclose(pipeline.apply(rho), expected)


def test_pipeline_copies_channel_collection_and_does_not_mutate_input():
    channels = [BitFlipChannel(p=0.2)]
    pipeline = ChannelPipeline(channels)
    channels.clear()
    rho = dm_from_ket(PLUS)
    original = rho.copy()

    pipeline.apply(rho)

    assert len(pipeline.channels) == 1
    assert_allclose(rho, original)


def test_pipeline_rejects_non_channel_components():
    with pytest.raises(TypeError, match="index 1"):
        ChannelPipeline((IdentityChannel(), object()))  # pyright: ignore[reportArgumentType]


def test_pipeline_validates_input_state_at_its_boundary():
    invalid_state = np.diag([0.6, 0.6])

    with pytest.raises(ValueError, match="unit trace"):
        ChannelPipeline((IdentityChannel(),)).apply(invalid_state)
