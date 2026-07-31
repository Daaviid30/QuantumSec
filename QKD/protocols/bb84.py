"""BB84-protocol definition"""

from dataclasses import dataclass

import numpy

from core import rng
from qkd.primitives import measurements
from quantum import measures

# Parties involved in the protocol

@dataclass(frozen=True, slots=True)
class BB84Alice:
    """A sampled logical outcome and its normalized post-measurement state."""

    rng: rng.BaseRNG
    bitstring: str
    bases: str
    key: str

@dataclass(frozen=True, slots=True)
class BB84Bob:
    """A sampled logical outcome and its normalized post-measurement state."""

    rng: rng.BaseRNG
    bases: str
    key: str