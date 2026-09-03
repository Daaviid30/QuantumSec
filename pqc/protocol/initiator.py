"""Alice-side authentication and encapsulation for staged PQC handshakes."""

from dataclasses import dataclass, field
from enum import StrEnum

from pqc.errors import UnknownTrustedPeerError
from pqc.kem import (
    HQC3,
    HQC_3_ALGORITHM,
    ML_KEM_768_ALGORITHM,
    MLKEM768,
    hqc_3_metadata,
    ml_kem_768_metadata,
)
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.identity import _validated_identity_name
from pqc.protocol.messages import (
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
    ServerKeyOffer,
    SignedServerKeyOffer,
)
from pqc.protocol.party import PQCParty


def _require_exact_bytes(value: object, *, name: str, length: int) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    if len(value) != length:
        raise ValueError(f"{name} must contain {length} bytes. Got {len(value)}.")
    return bytes(value)


class ServerOfferProcessingStatus(StrEnum):
    """Authentication outcome produced before any Alice-side response is sent."""

    AUTHENTICATED = "authenticated"
    UNTRUSTED_SIGNER = "untrusted_signer"
    ALGORITHM_MISMATCH = "algorithm_mismatch"
    INVALID_SIGNATURE = "invalid_signature"


@dataclass(frozen=True, slots=True, repr=False)
class InitiatorKEMState:
    """Alice-local KEM secrets created only after authenticating the responder."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    _ml_kem_shared_secret: bytes = field(repr=False)
    _hqc_shared_secret: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_exact_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        ml_kem_shared_secret = _require_exact_bytes(
            self._ml_kem_shared_secret,
            name="ml_kem_shared_secret",
            length=ml_kem_768_metadata().shared_secret_length,
        )
        hqc_shared_secret: bytes | None = None
        if self.profile is PQCProfile.LOW:
            if self._hqc_shared_secret is not None:
                raise ValueError("LOW initiator state must not contain an HQC shared secret.")
        else:
            if self._hqc_shared_secret is None:
                raise ValueError("HIGH initiator state must contain an HQC shared secret.")
            hqc_shared_secret = _require_exact_bytes(
                self._hqc_shared_secret,
                name="hqc_shared_secret",
                length=hqc_3_metadata().shared_secret_length,
            )
        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "_ml_kem_shared_secret", ml_kem_shared_secret)
        object.__setattr__(self, "_hqc_shared_secret", hqc_shared_secret)

    def __repr__(self) -> str:
        algorithms = profile_definition(self.profile).kem_algorithms
        return f"InitiatorKEMState(profile={self.profile.value!r}, algorithms={algorithms!r})"


@dataclass(frozen=True, slots=True, repr=False)
class EncapsulationResponse:
    """Unsigned public KEM ciphertext material prepared for the next phase."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    ml_kem_algorithm: str
    ml_kem_ciphertext: bytes = field(repr=False)
    hqc_algorithm: str | None = None
    hqc_ciphertext: bytes | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_exact_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        definition = profile_definition(self.profile)
        if self.ml_kem_algorithm != definition.kem_algorithms[0]:
            raise ValueError(f"ml_kem_algorithm must be {ML_KEM_768_ALGORITHM!r}.")
        ml_kem_ciphertext = _require_exact_bytes(
            self.ml_kem_ciphertext,
            name="ml_kem_ciphertext",
            length=ml_kem_768_metadata().ciphertext_length,
        )

        hqc_fields_present = self.hqc_algorithm is not None or self.hqc_ciphertext is not None
        hqc_ciphertext: bytes | None = None
        if self.profile is PQCProfile.LOW:
            if hqc_fields_present:
                raise ValueError("LOW encapsulation response must not contain HQC fields.")
        else:
            if self.hqc_algorithm != HQC_3_ALGORITHM or self.hqc_ciphertext is None:
                raise ValueError("HIGH encapsulation response must contain an HQC-3 ciphertext.")
            hqc_ciphertext = _require_exact_bytes(
                self.hqc_ciphertext,
                name="hqc_ciphertext",
                length=hqc_3_metadata().ciphertext_length,
            )

        object.__setattr__(self, "session_id", session_id)
        object.__setattr__(self, "ml_kem_ciphertext", ml_kem_ciphertext)
        object.__setattr__(self, "hqc_ciphertext", hqc_ciphertext)

    def __repr__(self) -> str:
        hqc_length = None if self.hqc_ciphertext is None else len(self.hqc_ciphertext)
        return (
            f"EncapsulationResponse(profile={self.profile.value!r}, "
            f"ml_kem_algorithm={self.ml_kem_algorithm!r}, "
            f"ml_kem_ciphertext_length={len(self.ml_kem_ciphertext)}, "
            f"hqc_algorithm={self.hqc_algorithm!r}, hqc_ciphertext_length={hqc_length!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class ProcessedServerOffer:
    """Alice-side authentication outcome and optional private/public KEM outputs."""

    status: ServerOfferProcessingStatus
    signer: str
    profile: PQCProfile
    initiator_state: InitiatorKEMState | None = field(default=None, repr=False)
    public_encapsulation: EncapsulationResponse | None = field(default=None, repr=False)
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ServerOfferProcessingStatus):
            raise TypeError(
                f"status must be a ServerOfferProcessingStatus. Got {type(self.status).__name__}."
            )
        object.__setattr__(self, "signer", _validated_identity_name(self.signer))
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")

        if self.status is ServerOfferProcessingStatus.AUTHENTICATED:
            if not isinstance(self.initiator_state, InitiatorKEMState) or not isinstance(
                self.public_encapsulation,
                EncapsulationResponse,
            ):
                raise ValueError("Authenticated processing must contain private and public KEM outputs.")
            if self.failure_reason is not None:
                raise ValueError("Authenticated processing must not contain a failure reason.")
            if (
                self.initiator_state.profile is not self.profile
                or self.public_encapsulation.profile is not self.profile
                or self.initiator_state.session_id != self.public_encapsulation.session_id
            ):
                raise ValueError("Authenticated KEM outputs must preserve the same profile and session.")
        else:
            if self.initiator_state is not None or self.public_encapsulation is not None:
                raise ValueError("Rejected processing must not contain KEM outputs.")
            if not isinstance(self.failure_reason, str) or not self.failure_reason.strip():
                raise ValueError("Rejected processing must contain a failure reason.")

    @property
    def authenticated(self) -> bool:
        """Return whether Bob was authenticated and encapsulation completed."""

        return self.status is ServerOfferProcessingStatus.AUTHENTICATED

    def __repr__(self) -> str:
        return (
            f"ProcessedServerOffer(status={self.status.value!r}, signer={self.signer!r}, "
            f"profile={self.profile.value!r}, encapsulation_ready={self.authenticated!r})"
        )


class ServerKeyOfferProcessor:
    """Authenticate Bob's offer before producing Alice's KEM encapsulations."""

    def process(
        self,
        *,
        initiator: PQCParty,
        signed_offer: SignedServerKeyOffer,
    ) -> ProcessedServerOffer:
        """Verify a trusted responder and encapsulate only after authentication."""

        if not isinstance(initiator, PQCParty):
            raise TypeError(f"initiator must be a PQCParty. Got {type(initiator).__name__}.")
        if not isinstance(signed_offer, SignedServerKeyOffer):
            raise TypeError(
                f"signed_offer must be a SignedServerKeyOffer. Got {type(signed_offer).__name__}."
            )

        offer = signed_offer.offer
        definition = profile_definition(offer.profile)
        if signed_offer.signature_algorithm != definition.signature_algorithm:
            return self._rejected(
                signed_offer,
                status=ServerOfferProcessingStatus.ALGORITHM_MISMATCH,
                reason="The declared signature algorithm does not match the selected profile.",
            )
        if not self._offer_algorithms_match_profile(offer):
            return self._rejected(
                signed_offer,
                status=ServerOfferProcessingStatus.ALGORITHM_MISMATCH,
                reason="The offered KEM algorithms do not match the selected profile.",
            )

        try:
            trusted_responder = initiator.trusted_peers.lookup(signed_offer.signer)
        except UnknownTrustedPeerError:
            return self._rejected(
                signed_offer,
                status=ServerOfferProcessingStatus.UNTRUSTED_SIGNER,
                reason=f"Signer {signed_offer.signer!r} is not provisioned in the trust store.",
            )
        if trusted_responder.algorithm != signed_offer.signature_algorithm:
            return self._rejected(
                signed_offer,
                status=ServerOfferProcessingStatus.ALGORITHM_MISMATCH,
                reason="The trusted identity algorithm does not match the signed offer.",
            )
        if not trusted_responder.verify(offer.canonical_bytes(), signed_offer.signature):
            return self._rejected(
                signed_offer,
                status=ServerOfferProcessingStatus.INVALID_SIGNATURE,
                reason="The server offer signature is invalid for the trusted responder identity.",
            )

        return self._encapsulate_authenticated(signed_offer)

    @staticmethod
    def _offer_algorithms_match_profile(offer: ServerKeyOffer) -> bool:
        definition = profile_definition(offer.profile)
        if offer.ml_kem_algorithm != definition.kem_algorithms[0]:
            return False
        if offer.profile is PQCProfile.LOW:
            return offer.hqc_algorithm is None and offer.hqc_public_key is None
        return (
            len(definition.kem_algorithms) == 2
            and offer.hqc_algorithm == definition.kem_algorithms[1]
            and offer.hqc_public_key is not None
        )

    @staticmethod
    def _rejected(
        signed_offer: SignedServerKeyOffer,
        *,
        status: ServerOfferProcessingStatus,
        reason: str,
    ) -> ProcessedServerOffer:
        return ProcessedServerOffer(
            status=status,
            signer=signed_offer.signer,
            profile=signed_offer.offer.profile,
            failure_reason=reason,
        )

    @staticmethod
    def _encapsulate_authenticated(signed_offer: SignedServerKeyOffer) -> ProcessedServerOffer:
        offer = signed_offer.offer
        ml_kem = MLKEM768.encapsulate(offer.ml_kem_public_key)
        hqc = None
        if offer.profile is PQCProfile.HIGH:
            if offer.hqc_public_key is None:
                raise ValueError("Authenticated HIGH offer is missing its HQC-3 public key.")
            hqc = HQC3.encapsulate(offer.hqc_public_key)

        initiator_state = InitiatorKEMState(
            session_id=offer.session_id,
            profile=offer.profile,
            _ml_kem_shared_secret=ml_kem.shared_secret,
            _hqc_shared_secret=None if hqc is None else hqc.shared_secret,
        )
        public_encapsulation = EncapsulationResponse(
            session_id=offer.session_id,
            profile=offer.profile,
            ml_kem_algorithm=offer.ml_kem_algorithm,
            ml_kem_ciphertext=ml_kem.ciphertext,
            hqc_algorithm=offer.hqc_algorithm,
            hqc_ciphertext=None if hqc is None else hqc.ciphertext,
        )
        return ProcessedServerOffer(
            status=ServerOfferProcessingStatus.AUTHENTICATED,
            signer=signed_offer.signer,
            profile=offer.profile,
            initiator_state=initiator_state,
            public_encapsulation=public_encapsulation,
        )
