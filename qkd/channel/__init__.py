"""Public quantum-channel API for QKD simulations."""

from qkd.channel.attacks import AttackDiagnostics, InterceptResendAttack
from qkd.channel.base import QuantumChannel
from qkd.channel.ideal import IdentityChannel
from qkd.channel.kraus import KrausChannel
from qkd.channel.noise import (
    AmplitudeDampingChannel,
    BitFlipChannel,
    DepolarizingChannel,
    PauliChannel,
    PhaseFlipChannel,
)
from qkd.channel.pipeline import ChannelPipeline

__all__ = [
    "AmplitudeDampingChannel",
    "AttackDiagnostics",
    "BitFlipChannel",
    "ChannelPipeline",
    "DepolarizingChannel",
    "IdentityChannel",
    "InterceptResendAttack",
    "KrausChannel",
    "PauliChannel",
    "PhaseFlipChannel",
    "QuantumChannel",
]
