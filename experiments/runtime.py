"""Runtime-only provisioning for experiment configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from secrets import token_bytes
from time import perf_counter_ns

from core.rng import SeededRNG
from experiments.config import ExperimentConfig
from orchestration.authentication import (
    MLDSAAuthenticationContext,
    WegmanCarterAuthenticationContext,
)
from orchestration.context import SessionExecutionContext
from orchestration.profiles import ClassicalAuthenticationMode, qkd_profile_definition
from pqc import MLDSAIdentity, PQCParty, TrustedIdentityStore
from qkd.channel import build_channel_pipeline
from qkd.protocols import BB84Protocol

_WEGMAN_CARTER_BYTES_PER_SIGNAL_PER_PHASE = 128


@dataclass(frozen=True, slots=True)
class PQCIdentityProvisioning:
    """One-time ML-DSA identity-generation cost outside session timings."""

    alice_identity_generation_time_ns: int
    bob_identity_generation_time_ns: int
    public_identity_bytes: int

    @property
    def total_identity_generation_time_ns(self) -> int:
        return self.alice_identity_generation_time_ns + self.bob_identity_generation_time_ns

    def to_public_dict(self) -> dict[str, int]:
        return {
            "alice_identity_generation_time_ns": self.alice_identity_generation_time_ns,
            "bob_identity_generation_time_ns": self.bob_identity_generation_time_ns,
            "total_identity_generation_time_ns": self.total_identity_generation_time_ns,
            "public_identity_bytes": self.public_identity_bytes,
        }


@dataclass(frozen=True, slots=True)
class RuntimeProvisioning:
    """Public description of provisioning policy; it never contains key material."""

    pqc_identities: str | None
    qkd_authentication_material: str | None
    qkd_authentication_material_bytes_per_direction: int | None = None
    pqc_alice_identity_generation_time_ns: int | None = None
    pqc_bob_identity_generation_time_ns: int | None = None
    pqc_total_identity_generation_time_ns: int | None = None
    pqc_public_identity_bytes: int | None = None
    included_in_session_timings: bool = False

    def __post_init__(self) -> None:
        for name in ("pqc_identities", "qkd_authentication_material"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be a non-empty string or None.")
        capacity = self.qkd_authentication_material_bytes_per_direction
        if capacity is not None and (
            isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0
        ):
            raise ValueError("qkd_authentication_material_bytes_per_direction must be positive or None.")
        for name in (
            "pqc_alice_identity_generation_time_ns",
            "pqc_bob_identity_generation_time_ns",
            "pqc_total_identity_generation_time_ns",
            "pqc_public_identity_bytes",
        ):
            measurement = getattr(self, name)
            if measurement is not None and (
                isinstance(measurement, bool) or not isinstance(measurement, int) or measurement < 0
            ):
                raise ValueError(f"{name} must be a non-negative integer or None.")
        if not isinstance(self.included_in_session_timings, bool):
            raise TypeError("included_in_session_timings must be a bool.")

    def to_public_dict(self) -> dict[str, object]:
        return {
            "pqc_identities": self.pqc_identities,
            "qkd_authentication_material": self.qkd_authentication_material,
            "qkd_authentication_material_bytes_per_direction": (
                self.qkd_authentication_material_bytes_per_direction
            ),
            "pqc_alice_identity_generation_time_ns": self.pqc_alice_identity_generation_time_ns,
            "pqc_bob_identity_generation_time_ns": self.pqc_bob_identity_generation_time_ns,
            "pqc_total_identity_generation_time_ns": self.pqc_total_identity_generation_time_ns,
            "pqc_public_identity_bytes": self.pqc_public_identity_bytes,
            "included_in_session_timings": self.included_in_session_timings,
        }


@dataclass(slots=True, repr=False)
class ExperimentRuntime:
    context: SessionExecutionContext = field(repr=False)
    provisioning: RuntimeProvisioning


class ExperimentRuntimeFactory:
    """Create per-run contexts while retaining persistent laboratory identities.

    ML-DSA identities and PQC party trust are provisioned lazily once and reused.
    Wegman-Carter material is generated fresh for every run. All of this happens
    before ``run_session`` starts its profile-specific stopwatches.
    """

    __slots__ = (
        "_minimum_psk_bytes",
        "_pqc_parties",
        "_pqc_identity_provisioning",
        "_qkd_mldsa_material",
    )

    def __init__(self, *, minimum_psk_bytes: int = 65_536) -> None:
        if (
            isinstance(minimum_psk_bytes, bool)
            or not isinstance(minimum_psk_bytes, int)
            or minimum_psk_bytes <= 0
        ):
            raise ValueError("minimum_psk_bytes must be a positive integer.")
        self._minimum_psk_bytes = minimum_psk_bytes
        self._pqc_parties: tuple[PQCParty, PQCParty] | None = None
        self._pqc_identity_provisioning: PQCIdentityProvisioning | None = None
        self._qkd_mldsa_material: (
            tuple[MLDSAIdentity, MLDSAIdentity, TrustedIdentityStore, TrustedIdentityStore] | None
        ) = None

    def build(self, config: ExperimentConfig) -> ExperimentRuntime:
        if not isinstance(config, ExperimentConfig):
            raise TypeError("config must be an ExperimentConfig.")
        definition = config.session_config

        qkd_protocol = None
        qkd_authentication = None
        qkd_authentication_mode: str | None = None
        qkd_authentication_material_bytes: int | None = None
        if config.seed is not None:
            pipeline = build_channel_pipeline(config.qkd_stages, root_seed=config.seed)
            qkd_protocol = BB84Protocol(pipeline, SeededRNG(config.seed))
            assert definition.qkd_authentication_profile is not None
            auth_mode = qkd_profile_definition(definition.qkd_authentication_profile).classical_authentication
            if auth_mode is ClassicalAuthenticationMode.WEGMAN_CARTER:
                signal_count = definition.qkd_signal_count or 0
                postprocessing = definition.qkd_postprocessing
                assert postprocessing is not None
                phase_count = postprocessing.cascade.passes + 1
                material_bytes = max(
                    self._minimum_psk_bytes,
                    signal_count * _WEGMAN_CARTER_BYTES_PER_SIGNAL_PER_PHASE * phase_count,
                )
                qkd_authentication = WegmanCarterAuthenticationContext.from_shared_secrets(
                    alice_to_bob_secret=token_bytes(material_bytes),
                    bob_to_alice_secret=token_bytes(material_bytes),
                )
                qkd_authentication_mode = "fresh pre-shared authentication material per run"
                qkd_authentication_material_bytes = material_bytes
            elif auth_mode is ClassicalAuthenticationMode.ML_DSA_65:
                qkd_authentication = self._new_qkd_mldsa_context()
                qkd_authentication_mode = (
                    "persistent pre-provisioned ML-DSA identities; fresh anti-replay registry per run"
                )
            else:
                qkd_authentication_mode = "authentication explicitly assumed; no runtime material"

        pqc_initiator = pqc_responder = None
        pqc_identity_mode: str | None = None
        pqc_identity_provisioning: PQCIdentityProvisioning | None = None
        if definition.internal_pqc_profile is not None:
            pqc_initiator, pqc_responder = self._ensure_pqc_parties()
            pqc_identity_provisioning = self._pqc_identity_provisioning
            assert pqc_identity_provisioning is not None
            pqc_identity_mode = "persistent pre-provisioned ML-DSA identities and peer trust"

        return ExperimentRuntime(
            context=SessionExecutionContext(
                qkd_protocol=qkd_protocol,
                qkd_authentication=qkd_authentication,
                pqc_initiator=pqc_initiator,
                pqc_responder=pqc_responder,
            ),
            provisioning=RuntimeProvisioning(
                pqc_identities=pqc_identity_mode,
                qkd_authentication_material=qkd_authentication_mode,
                qkd_authentication_material_bytes_per_direction=(qkd_authentication_material_bytes),
                pqc_alice_identity_generation_time_ns=(
                    pqc_identity_provisioning.alice_identity_generation_time_ns
                    if pqc_identity_provisioning is not None
                    else None
                ),
                pqc_bob_identity_generation_time_ns=(
                    pqc_identity_provisioning.bob_identity_generation_time_ns
                    if pqc_identity_provisioning is not None
                    else None
                ),
                pqc_total_identity_generation_time_ns=(
                    pqc_identity_provisioning.total_identity_generation_time_ns
                    if pqc_identity_provisioning is not None
                    else None
                ),
                pqc_public_identity_bytes=(
                    pqc_identity_provisioning.public_identity_bytes
                    if pqc_identity_provisioning is not None
                    else None
                ),
            ),
        )

    def _ensure_pqc_parties(self) -> tuple[PQCParty, PQCParty]:
        if self._pqc_parties is None:
            self.provision_pqc_identities()
        assert self._pqc_parties is not None
        return self._pqc_parties

    def provision_pqc_identities(self) -> PQCIdentityProvisioning:
        """Provision and time persistent campaign identities exactly once."""

        if self._pqc_parties is None:
            started = perf_counter_ns()
            alice = PQCParty.create("experiment-pqc-alice")
            alice_time = perf_counter_ns() - started
            started = perf_counter_ns()
            bob = PQCParty.create("experiment-pqc-bob")
            bob_time = perf_counter_ns() - started
            alice.trust_peer(bob.public_identity)
            bob.trust_peer(alice.public_identity)
            self._pqc_parties = (alice, bob)
            self._pqc_identity_provisioning = PQCIdentityProvisioning(
                alice_identity_generation_time_ns=alice_time,
                bob_identity_generation_time_ns=bob_time,
                public_identity_bytes=(
                    len(alice.public_identity.public_key) + len(bob.public_identity.public_key)
                ),
            )
        assert self._pqc_identity_provisioning is not None
        return self._pqc_identity_provisioning

    def _new_qkd_mldsa_context(self) -> MLDSAAuthenticationContext:
        if self._qkd_mldsa_material is None:
            alice = MLDSAIdentity.generate("experiment-qkd-alice")
            bob = MLDSAIdentity.generate("experiment-qkd-bob")
            alice_trust = TrustedIdentityStore()
            bob_trust = TrustedIdentityStore()
            alice_trust.trust(bob.public_identity)
            bob_trust.trust(alice.public_identity)
            self._qkd_mldsa_material = (alice, bob, alice_trust, bob_trust)
        alice, bob, alice_trust, bob_trust = self._qkd_mldsa_material
        return MLDSAAuthenticationContext(alice, bob, alice_trust, bob_trust)
