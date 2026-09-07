"""ML-DSA-65 authentication of canonical QKD classical transcript checkpoints."""

from dataclasses import dataclass, field

from orchestration.authentication.base import (
    AuthenticationEvidence,
    AuthenticationFrame,
    AuthenticationSessionRegistry,
    AuthenticationVerification,
    AuthenticatorMetadata,
    DirectionalAuthenticator,
)
from orchestration.profiles import ClassicalAuthenticationMode
from orchestration.qkd.transcript import QKDClassicalDirection
from pqc.errors import PQCError, UnknownTrustedPeerError
from pqc.protocol import MLDSAIdentity, TrustedIdentityStore

ML_DSA_TRUST_ASSUMPTION = (
    "Peer ML-DSA-65 public identities are authenticated and pre-provisioned before the QKD session."
)


@dataclass(frozen=True, slots=True)
class MLDSADirectionalAuthenticator(DirectionalAuthenticator):
    """Sign as one provisioned party and verify through the receiver's trust store."""

    signer_identity: MLDSAIdentity = field(repr=False)
    verifier_name: str
    verifier_trust_store: TrustedIdentityStore = field(repr=False, compare=False)
    direction: QKDClassicalDirection

    def __post_init__(self) -> None:
        if not isinstance(self.signer_identity, MLDSAIdentity):
            raise TypeError("signer_identity must be an MLDSAIdentity.")
        if not isinstance(self.verifier_name, str) or not self.verifier_name.strip():
            raise ValueError("verifier_name must be a non-empty string.")
        if not isinstance(self.verifier_trust_store, TrustedIdentityStore):
            raise TypeError("verifier_trust_store must be a TrustedIdentityStore.")
        if not isinstance(self.direction, QKDClassicalDirection):
            raise TypeError("direction must be a QKDClassicalDirection.")
        object.__setattr__(self, "verifier_name", self.verifier_name.strip())

    @property
    def metadata(self) -> AuthenticatorMetadata:
        return AuthenticatorMetadata(
            mechanism=ClassicalAuthenticationMode.ML_DSA_65,
            algorithm=self.signer_identity.metadata.name,
            family="post-quantum digital signature",
            trust_assumption=ML_DSA_TRUST_ASSUMPTION,
            public_key_provisioning_bytes=self.signer_identity.metadata.public_key_length,
            forgery_bound=None,
        )

    def generate_evidence(self, frame: AuthenticationFrame) -> AuthenticationEvidence:
        if frame.direction is not self.direction:
            raise ValueError("Authentication frame direction does not match the ML-DSA signer direction.")
        signature = self.signer_identity.sign(frame.canonical_bytes())
        return AuthenticationEvidence(
            mechanism=ClassicalAuthenticationMode.ML_DSA_65,
            algorithm=self.signer_identity.metadata.name,
            signer=self.signer_identity.owner,
            verifier=self.verifier_name,
            session_id=frame.session_id,
            direction=frame.direction,
            sequence_number=frame.sequence_number,
            message_type=frame.message_type,
            value=signature,
            secret_bits_consumed=None,
        )

    def verify_evidence(
        self,
        frame: AuthenticationFrame,
        evidence: AuthenticationEvidence | None,
    ) -> AuthenticationVerification:
        if evidence is None:
            return AuthenticationVerification(False, "Missing ML-DSA authentication evidence.")
        if frame.direction is not self.direction or not evidence.matches_frame(frame):
            return AuthenticationVerification(False, "ML-DSA evidence context does not match the frame.")
        if (
            evidence.mechanism is not ClassicalAuthenticationMode.ML_DSA_65
            or evidence.algorithm != self.signer_identity.metadata.name
            or evidence.signer != self.signer_identity.owner
            or evidence.verifier != self.verifier_name
        ):
            return AuthenticationVerification(False, "ML-DSA evidence identity or algorithm is invalid.")
        try:
            trusted_identity = self.verifier_trust_store.lookup(evidence.signer)
            verified = trusted_identity.verify(frame.canonical_bytes(), evidence.value)
        except UnknownTrustedPeerError:
            return AuthenticationVerification(False, "The ML-DSA signer is not in the verifier trust store.")
        except PQCError, TypeError, ValueError:
            return AuthenticationVerification(False, "ML-DSA signature verification failed.")
        if not verified:
            return AuthenticationVerification(False, "ML-DSA signature verification failed.")
        return AuthenticationVerification(True)


@dataclass(frozen=True, slots=True)
class MLDSAAuthenticationContext:
    """Pre-provisioned bilateral ML-DSA identities and peer trust stores."""

    alice_identity: MLDSAIdentity = field(repr=False)
    bob_identity: MLDSAIdentity = field(repr=False)
    alice_trust_store: TrustedIdentityStore = field(repr=False, compare=False)
    bob_trust_store: TrustedIdentityStore = field(repr=False, compare=False)
    session_registry: AuthenticationSessionRegistry = field(
        default_factory=AuthenticationSessionRegistry,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        if not isinstance(self.alice_identity, MLDSAIdentity) or not isinstance(
            self.bob_identity, MLDSAIdentity
        ):
            raise TypeError("alice_identity and bob_identity must be MLDSAIdentity values.")
        if self.alice_identity.owner == self.bob_identity.owner:
            raise ValueError("Alice and Bob must have distinct ML-DSA identity names.")
        if not isinstance(self.alice_trust_store, TrustedIdentityStore) or not isinstance(
            self.bob_trust_store, TrustedIdentityStore
        ):
            raise TypeError("alice_trust_store and bob_trust_store must be TrustedIdentityStore values.")
        if not isinstance(self.session_registry, AuthenticationSessionRegistry):
            raise TypeError("session_registry must be an AuthenticationSessionRegistry.")

    def reserve_session_id(self, session_id: bytes) -> None:
        self.session_registry.reserve(session_id)

    def authenticators(
        self,
    ) -> tuple[MLDSADirectionalAuthenticator, MLDSADirectionalAuthenticator]:
        return (
            MLDSADirectionalAuthenticator(
                signer_identity=self.alice_identity,
                verifier_name=self.bob_identity.owner,
                verifier_trust_store=self.bob_trust_store,
                direction=QKDClassicalDirection.ALICE_TO_BOB,
            ),
            MLDSADirectionalAuthenticator(
                signer_identity=self.bob_identity,
                verifier_name=self.alice_identity.owner,
                verifier_trust_store=self.alice_trust_store,
                direction=QKDClassicalDirection.BOB_TO_ALICE,
            ),
        )
