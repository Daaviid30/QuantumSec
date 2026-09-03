"""Central QuantumSec deployment profiles for PQC handshakes."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from pqc.kem import HQC_3_ALGORITHM, ML_KEM_768_ALGORITHM
from pqc.signatures import ML_DSA_65_METADATA


class PQCProfile(StrEnum):
    """Enumeration of QuantumSec handshake profiles defining selected algorithm suites."""

    LOW = "low"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class PQCProfileDefinition:
    """Immutable algorithm suite specification for a QuantumSec PQC profile."""

    profile: PQCProfile
    kem_algorithms: tuple[str, ...]
    signature_algorithm: str


PQC_PROFILE_DEFINITIONS: Final[Mapping[PQCProfile, PQCProfileDefinition]] = MappingProxyType(
    {
        PQCProfile.LOW: PQCProfileDefinition(
            profile=PQCProfile.LOW,
            kem_algorithms=(ML_KEM_768_ALGORITHM,),
            signature_algorithm=ML_DSA_65_METADATA.name,
        ),
        PQCProfile.HIGH: PQCProfileDefinition(
            profile=PQCProfile.HIGH,
            kem_algorithms=(ML_KEM_768_ALGORITHM, HQC_3_ALGORITHM),
            signature_algorithm=ML_DSA_65_METADATA.name,
        ),
    }
)


def profile_definition(profile: PQCProfile) -> PQCProfileDefinition:
    """Retrieve the immutable algorithm suite definition for the specified QuantumSec PQC profile."""

    if not isinstance(profile, PQCProfile):
        raise TypeError(f"profile must be a PQCProfile. Got {type(profile).__name__}.")
    return PQC_PROFILE_DEFINITIONS[profile]
