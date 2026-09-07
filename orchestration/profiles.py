"""Public session profiles with orthogonal establishment and authentication dimensions."""

from dataclasses import dataclass
from enum import StrEnum


class QKDProfile(StrEnum):
    QKD_ASSUMED = "QKD-ASSUMED"
    QKD_CLASSICAL_AUTH = "QKD-CLASSICAL-AUTH"
    QKD_PQC_AUTH = "QKD-PQC-AUTH"


class EstablishmentSource(StrEnum):
    BB84 = "bb84"


class ClassicalAuthenticationMode(StrEnum):
    ASSUMED = "assumed"
    WEGMAN_CARTER = "wegman_carter"
    ML_DSA_65 = "ml_dsa_65"


@dataclass(frozen=True, slots=True)
class QKDProfileDefinition:
    profile: QKDProfile
    establishment_source: EstablishmentSource
    classical_authentication: ClassicalAuthenticationMode


_DEFINITIONS = {
    QKDProfile.QKD_ASSUMED: QKDProfileDefinition(
        profile=QKDProfile.QKD_ASSUMED,
        establishment_source=EstablishmentSource.BB84,
        classical_authentication=ClassicalAuthenticationMode.ASSUMED,
    ),
    QKDProfile.QKD_CLASSICAL_AUTH: QKDProfileDefinition(
        profile=QKDProfile.QKD_CLASSICAL_AUTH,
        establishment_source=EstablishmentSource.BB84,
        classical_authentication=ClassicalAuthenticationMode.WEGMAN_CARTER,
    ),
    QKDProfile.QKD_PQC_AUTH: QKDProfileDefinition(
        profile=QKDProfile.QKD_PQC_AUTH,
        establishment_source=EstablishmentSource.BB84,
        classical_authentication=ClassicalAuthenticationMode.ML_DSA_65,
    ),
}


def qkd_profile_definition(profile: QKDProfile) -> QKDProfileDefinition:
    if not isinstance(profile, QKDProfile):
        raise TypeError(f"profile must be a QKDProfile. Got {type(profile).__name__}.")
    return _DEFINITIONS[profile]
