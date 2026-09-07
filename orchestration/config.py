"""Versioned public configuration for common QuantumSec session execution."""

from dataclasses import dataclass
from typing import Final

from orchestration.profiles import QKDProfile, SessionProfile, session_profile_definition
from pqc.profiles import PQCProfile
from qkd.protocols import BB84PostprocessingConfig

SESSION_CONFIG_VERSION: Final = 1


@dataclass(frozen=True, slots=True)
class SessionConfig:
    """Normalized public configuration; runtime secrets belong in a separate context."""

    profile: SessionProfile
    qkd_authentication_profile: QKDProfile | None = None
    qkd_signal_count: int | None = None
    qkd_postprocessing: BB84PostprocessingConfig | None = None
    internal_pqc_profile: PQCProfile | None = None
    version: int = SESSION_CONFIG_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.profile, SessionProfile):
            raise TypeError("profile must be a SessionProfile.")
        if self.version != SESSION_CONFIG_VERSION:
            raise ValueError(f"version must be {SESSION_CONFIG_VERSION}.")
        definition = session_profile_definition(self.profile)
        expected_pqc = definition.internal_pqc_profile
        if self.internal_pqc_profile is not None and self.internal_pqc_profile is not expected_pqc:
            raise ValueError("internal_pqc_profile conflicts with the selected public profile.")
        object.__setattr__(self, "internal_pqc_profile", expected_pqc)

        if definition.hybrid:
            if not isinstance(self.qkd_authentication_profile, QKDProfile):
                raise ValueError("Hybrid profiles require an explicit qkd_authentication_profile.")
        elif definition.qkd_profile is not None:
            supplied_qkd = self.qkd_authentication_profile
            if supplied_qkd is not None and supplied_qkd is not definition.qkd_profile:
                raise ValueError("qkd_authentication_profile conflicts with the QKD public profile.")
            object.__setattr__(self, "qkd_authentication_profile", definition.qkd_profile)
        elif self.qkd_authentication_profile is not None:
            raise ValueError("PQC-only profiles cannot configure QKD authentication.")

        uses_qkd = definition.qkd_profile is not None or definition.hybrid
        if uses_qkd:
            count = self.qkd_signal_count
            if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
                raise ValueError("QKD profiles require a positive qkd_signal_count.")
            postprocessing = self.qkd_postprocessing or BB84PostprocessingConfig()
            if not isinstance(postprocessing, BB84PostprocessingConfig):
                raise TypeError("qkd_postprocessing must be a BB84PostprocessingConfig.")
            object.__setattr__(self, "qkd_postprocessing", postprocessing)
        elif self.qkd_signal_count is not None or self.qkd_postprocessing is not None:
            raise ValueError("PQC-only profiles cannot configure QKD execution.")

    def to_public_dict(self) -> dict[str, object]:
        postprocessing = self.qkd_postprocessing
        return {
            "version": self.version,
            "profile": self.profile.value,
            "qkd_authentication_profile": (
                self.qkd_authentication_profile.value if self.qkd_authentication_profile is not None else None
            ),
            "qkd_signal_count": self.qkd_signal_count,
            "qkd_postprocessing": (
                None
                if postprocessing is None
                else {
                    "sample_fraction": postprocessing.sample_fraction,
                    "phase_error_abort_threshold": postprocessing.phase_error_abort_threshold,
                    "cascade_passes": postprocessing.cascade.passes,
                    "cascade_initial_block_factor": postprocessing.cascade.initial_block_factor,
                    "cascade_maximum_initial_block_size": (postprocessing.cascade.maximum_initial_block_size),
                    "cascade_maximum_lookback_steps": postprocessing.cascade.maximum_lookback_steps,
                    "verification_tag_length": postprocessing.verification_tag_length,
                    "security_margin_bits": postprocessing.security_margin_bits,
                }
            ),
            "internal_pqc_profile": (
                self.internal_pqc_profile.value if self.internal_pqc_profile is not None else None
            ),
        }
