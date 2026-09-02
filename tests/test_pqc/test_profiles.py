"""Tests for centralized QuantumSec PQC profile definitions."""

import pytest

from pqc.kem import HQC_3_ALGORITHM, ML_KEM_768_ALGORITHM
from pqc.profiles import PQC_PROFILE_DEFINITIONS, PQCProfile, profile_definition


def test_low_profile_uses_one_kem_assumption() -> None:
    definition = profile_definition(PQCProfile.LOW)

    assert definition.kem_algorithms == (ML_KEM_768_ALGORITHM,)
    assert definition.signature_algorithm == "ML-DSA-65"


def test_high_profile_uses_two_diverse_kem_assumptions() -> None:
    definition = profile_definition(PQCProfile.HIGH)

    assert definition.kem_algorithms == (ML_KEM_768_ALGORITHM, HQC_3_ALGORITHM)
    assert definition.signature_algorithm == "ML-DSA-65"


def test_profile_definitions_are_centralized_and_immutable() -> None:
    assert set(PQC_PROFILE_DEFINITIONS) == {PQCProfile.LOW, PQCProfile.HIGH}
    assert "HYBRID" not in PQCProfile.__members__

    with pytest.raises(TypeError):
        PQC_PROFILE_DEFINITIONS[PQCProfile.LOW] = profile_definition(PQCProfile.HIGH)  # type: ignore[index]
