"""Sequential composition of quantum channels."""

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

from qkd.channel.base import QuantumChannel, _prepare_density_matrix
from quantum.types import ArrayLike, ComplexArray


@dataclass(frozen=True, slots=True, init=False)
class ChannelPipeline(QuantumChannel):
    """Apply an immutable sequence of channels in order.

    An empty pipeline is defined as the identity channel. Full state validation
    occurs once at the pipeline boundary; component channels retain their cheap
    dimension and finiteness checks.
    """

    channels: tuple[QuantumChannel, ...]

    def __init__(self, channels: Iterable[QuantumChannel]) -> None:
        clean_channels = tuple(channels)
        for index, channel in enumerate(clean_channels):
            if not isinstance(channel, QuantumChannel):
                raise TypeError(
                    "A channel pipeline accepts only QuantumChannel instances. "
                    f"Got {type(channel).__name__} at index {index}."
                )
        object.__setattr__(self, "channels", clean_channels)

    def apply(
        self,
        rho: ArrayLike,
        *,
        validate_state: bool = True,
    ) -> ComplexArray:
        """Apply each component from first to last without mutating the input."""

        input_state = _prepare_density_matrix(rho, validate_state=validate_state)
        state = np.array(input_state, dtype=np.complex128, copy=True)
        for channel in self.channels:
            state = channel.apply(state, validate_state=False)
        return state
