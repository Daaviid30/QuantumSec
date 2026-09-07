"""Runtime-only provisioning for experiment configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from secrets import token_bytes

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


@dataclass(frozen=True, slots=True)
class RuntimeProvisioning:
    """Public description of provisioning policy; it never contains key material."""

    pqc_identities: str | None
    qkd_authentication_material: str | None
    included_in_session_timings: bool = False

    def to_public_dict(self) -> dict[str, object]:
        return {
            "pqc_identities": self.pqc_identities,
            "qkd_authentication_material": self.qkd_authentication_material,
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
        self._qkd_mldsa_material: (
            tuple[MLDSAIdentity, MLDSAIdentity, TrustedIdentityStore, TrustedIdentityStore]
            | None
        ) = None

    def build(self, config: ExperimentConfig) -> ExperimentRuntime:
        if not isinstance(config, ExperimentConfig):
            raise TypeError("config must be an ExperimentConfig.")
        definition = config.session_config

        qkd_protocol = None
        qkd_authentication = None
        qkd_authentication_mode: str | None = None
        if config.seed is not None:
            pipeline = build_channel_pipeline(config.qkd_stages, root_seed=config.seed)
            qkd_protocol = BB84Protocol(pipeline, SeededRNG(config.seed))
            assert definition.qkd_authentication_profile is not None
            auth_mode = qkd_profile_definition(
                definition.qkd_authentication_profile
            ).classical_authentication
            if auth_mode is ClassicalAuthenticationMode.WEGMAN_CARTER:
                signal_count = definition.qkd_signal_count or 0
                material_bytes = max(self._minimum_psk_bytes, signal_count * 32)
                qkd_authentication = WegmanCarterAuthenticationContext.from_shared_secrets(
                    alice_to_bob_secret=token_bytes(material_bytes),
                    bob_to_alice_secret=token_bytes(material_bytes),
                )
                qkd_authentication_mode = "fresh pre-shared authentication material per run"
            elif auth_mode is ClassicalAuthenticationMode.ML_DSA_65:
                qkd_authentication = self._new_qkd_mldsa_context()
                qkd_authentication_mode = (
                    "persistent pre-provisioned ML-DSA identities; fresh anti-replay registry per run"
                )
            else:
                qkd_authentication_mode = "authentication explicitly assumed; no runtime material"

        pqc_initiator = pqc_responder = None
        pqc_identity_mode: str | None = None
        if definition.internal_pqc_profile is not None:
            pqc_initiator, pqc_responder = self._ensure_pqc_parties()
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
            ),
        )

    def _ensure_pqc_parties(self) -> tuple[PQCParty, PQCParty]:
        if self._pqc_parties is None:
            alice = PQCParty.create("experiment-pqc-alice")
            bob = PQCParty.create("experiment-pqc-bob")
            alice.trust_peer(bob.public_identity)
            bob.trust_peer(alice.public_identity)
            self._pqc_parties = (alice, bob)
        return self._pqc_parties

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
