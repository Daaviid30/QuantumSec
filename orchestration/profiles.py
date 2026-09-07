"""Public session profiles with orthogonal establishment and authentication dimensions."""

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from pqc.profiles import PQCProfile


class QKDProfile(StrEnum):
    QKD_ASSUMED = "QKD-ASSUMED"
    QKD_CLASSICAL_AUTH = "QKD-CLASSICAL-AUTH"
    QKD_PQC_AUTH = "QKD-PQC-AUTH"


class EstablishmentSource(StrEnum):
    BB84 = "bb84"
    ML_KEM_768 = "ml_kem_768"
    HQC_3 = "hqc_3"


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


class SessionProfile(StrEnum):
    QKD_ASSUMED = "QKD-ASSUMED"
    QKD_CLASSICAL_AUTH = "QKD-CLASSICAL-AUTH"
    QKD_PQC_AUTH = "QKD-PQC-AUTH"
    PQC_BASE = "PQC-BASE"
    PQC_DIVERSE = "PQC-DIVERSE"
    HYBRID = "HYBRID"
    HYBRID_DIVERSE = "HYBRID-DIVERSE"


class CapabilityStatus(StrEnum):
    CURRENT = "current"


@dataclass(frozen=True, slots=True)
class SessionProfileDefinition:
    profile: SessionProfile
    establishment_sources: tuple[EstablishmentSource, ...]
    qkd_profile: QKDProfile | None
    internal_pqc_profile: PQCProfile | None
    algorithms: tuple[str, ...]
    hybrid: bool
    diversified: bool
    status: CapabilityStatus = CapabilityStatus.CURRENT

    @property
    def establishment_algorithms(self) -> tuple[str, ...]:
        names = {
            EstablishmentSource.BB84: "BB84",
            EstablishmentSource.ML_KEM_768: "ML-KEM-768",
            EstablishmentSource.HQC_3: "HQC-3",
        }
        return tuple(names[source] for source in self.establishment_sources)

    @property
    def authentication_policy(self) -> tuple[str, ...]:
        """Return explicit, public authentication duties for capability discovery."""

        policies: list[str] = []
        if self.hybrid:
            policies.append("QKD classical authentication selected explicitly in SessionConfig")
        elif self.qkd_profile is not None:
            policies.append(
                f"QKD classical authentication: "
                f"{qkd_profile_definition(self.qkd_profile).classical_authentication.value}"
            )
        if self.internal_pqc_profile is not None:
            policies.append("PQC mutual authentication: ML-DSA-65 with pre-provisioned trust")
        return tuple(policies)

    @property
    def supported(self) -> bool:
        return self.status is CapabilityStatus.CURRENT

    def to_public_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile.value,
            "status": self.status.value,
            "supported": self.supported,
            "establishment_sources": tuple(source.value for source in self.establishment_sources),
            "establishment_algorithms": self.establishment_algorithms,
            "authentication_policy": self.authentication_policy,
            "internal_pqc_profile": (
                self.internal_pqc_profile.value if self.internal_pqc_profile is not None else None
            ),
            "algorithms": self.algorithms,
            "hybrid": self.hybrid,
            "diversified": self.diversified,
        }


SESSION_PROFILE_DEFINITIONS: Final = MappingProxyType(
    {
        SessionProfile.QKD_ASSUMED: SessionProfileDefinition(
            SessionProfile.QKD_ASSUMED,
            (EstablishmentSource.BB84,),
            QKDProfile.QKD_ASSUMED,
            None,
            ("BB84",),
            False,
            False,
        ),
        SessionProfile.QKD_CLASSICAL_AUTH: SessionProfileDefinition(
            SessionProfile.QKD_CLASSICAL_AUTH,
            (EstablishmentSource.BB84,),
            QKDProfile.QKD_CLASSICAL_AUTH,
            None,
            ("BB84", "Toeplitz-U2+one-time-mask-128"),
            False,
            False,
        ),
        SessionProfile.QKD_PQC_AUTH: SessionProfileDefinition(
            SessionProfile.QKD_PQC_AUTH,
            (EstablishmentSource.BB84,),
            QKDProfile.QKD_PQC_AUTH,
            None,
            ("BB84", "ML-DSA-65"),
            False,
            False,
        ),
        SessionProfile.PQC_BASE: SessionProfileDefinition(
            SessionProfile.PQC_BASE,
            (EstablishmentSource.ML_KEM_768,),
            None,
            PQCProfile.LOW,
            ("ML-KEM-768", "ML-DSA-65", "HKDF-SHA-384", "HMAC-SHA-384"),
            False,
            False,
        ),
        SessionProfile.PQC_DIVERSE: SessionProfileDefinition(
            SessionProfile.PQC_DIVERSE,
            (EstablishmentSource.ML_KEM_768, EstablishmentSource.HQC_3),
            None,
            PQCProfile.HIGH,
            ("ML-KEM-768", "HQC-3", "ML-DSA-65", "HKDF-SHA-384", "HMAC-SHA-384"),
            False,
            True,
        ),
        SessionProfile.HYBRID: SessionProfileDefinition(
            SessionProfile.HYBRID,
            (EstablishmentSource.BB84, EstablishmentSource.ML_KEM_768),
            None,
            PQCProfile.LOW,
            ("BB84", "ML-KEM-768", "ML-DSA-65", "HKDF-SHA-384", "HMAC-SHA-384"),
            True,
            False,
        ),
        SessionProfile.HYBRID_DIVERSE: SessionProfileDefinition(
            SessionProfile.HYBRID_DIVERSE,
            (EstablishmentSource.BB84, EstablishmentSource.ML_KEM_768, EstablishmentSource.HQC_3),
            None,
            PQCProfile.HIGH,
            ("BB84", "ML-KEM-768", "HQC-3", "ML-DSA-65", "HKDF-SHA-384", "HMAC-SHA-384"),
            True,
            True,
        ),
    }
)


def session_profile_definition(profile: SessionProfile) -> SessionProfileDefinition:
    if not isinstance(profile, SessionProfile):
        raise TypeError(f"profile must be a SessionProfile. Got {type(profile).__name__}.")
    return SESSION_PROFILE_DEFINITIONS[profile]


def session_capabilities() -> tuple[SessionProfileDefinition, ...]:
    """Return all executable profiles in stable public-enum order."""

    return tuple(SESSION_PROFILE_DEFINITIONS[profile] for profile in SessionProfile)
