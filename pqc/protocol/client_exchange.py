"""Authenticated Alice-to-Bob KEM response processing for staged PQC handshakes."""

import hmac
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha384

from pqc.errors import UnknownTrustedPeerError
from pqc.kem import hqc_3_metadata, ml_kem_768_metadata
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.identity import _validated_identity_name
from pqc.protocol.initiator import ProcessedServerOffer
from pqc.protocol.messages import (
    CLIENT_KEY_EXCHANGE_PROTOCOL_VERSION,
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
    ClientKeyExchange,
    ServerKeyOffer,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
    _require_bytes,
)
from pqc.protocol.party import PQCParty
from pqc.protocol.server_offer import ResponderKEMState


class ClientKeyExchangeProcessingStatus(StrEnum):
    """Bob-side authentication, binding, and decapsulation outcome."""

    AUTHENTICATED_AND_DECAPSULATED = "authenticated_and_decapsulated"
    RESPONDER_STATE_CLOSED = "responder_state_closed"
    PROFILE_MISMATCH = "profile_mismatch"
    SESSION_MISMATCH = "session_mismatch"
    OFFER_BINDING_MISMATCH = "offer_binding_mismatch"
    ALGORITHM_MISMATCH = "algorithm_mismatch"
    UNTRUSTED_SIGNER = "untrusted_signer"
    INVALID_SIGNATURE = "invalid_signature"


@dataclass(slots=True, repr=False)
class ResponderSharedSecretState:
    """Bob-local KEM secrets recovered after authenticating Alice's response.

    Raw-secret export remains deliberately absent until the KDF phase defines a
    precise consumption contract. Call :meth:`close` on abort or expiry.
    """

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    _ml_kem_shared_secret: bytes | None = field(repr=False)
    _hqc_shared_secret: bytes | None = field(default=None, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        ml_kem_shared_secret = _require_bytes(
            self._ml_kem_shared_secret,
            name="ml_kem_shared_secret",
            length=ml_kem_768_metadata().shared_secret_length,
        )
        hqc_shared_secret: bytes | None = None
        if self.profile is PQCProfile.LOW:
            if self._hqc_shared_secret is not None:
                raise ValueError("LOW responder secret state must not contain an HQC shared secret.")
        else:
            if self._hqc_shared_secret is None:
                raise ValueError("HIGH responder secret state must contain an HQC shared secret.")
            hqc_shared_secret = _require_bytes(
                self._hqc_shared_secret,
                name="hqc_shared_secret",
                length=hqc_3_metadata().shared_secret_length,
            )

        self.session_id = session_id
        self._ml_kem_shared_secret = ml_kem_shared_secret
        self._hqc_shared_secret = hqc_shared_secret

    @property
    def is_closed(self) -> bool:
        """Return whether this private state's shared-secret references were released."""

        return self._closed

    def close(self) -> None:
        """Release secret references idempotently without claiming memory zeroization."""

        self._ml_kem_shared_secret = None
        self._hqc_shared_secret = None
        self._closed = True

    def __repr__(self) -> str:
        algorithms = profile_definition(self.profile).kem_algorithms
        return (
            f"ResponderSharedSecretState(profile={self.profile.value!r}, "
            f"algorithms={algorithms!r}, closed={self._closed!r})"
        )


@dataclass(frozen=True, slots=True, repr=False)
class ProcessedClientKeyExchange:
    """Bob-side result containing private KEM output only after successful authentication."""

    status: ClientKeyExchangeProcessingStatus
    signer: str
    profile: PQCProfile
    responder_state: ResponderSharedSecretState | None = field(default=None, repr=False)
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ClientKeyExchangeProcessingStatus):
            raise TypeError(
                f"status must be a ClientKeyExchangeProcessingStatus. Got {type(self.status).__name__}."
            )
        object.__setattr__(self, "signer", _validated_identity_name(self.signer))
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")

        if self.status is ClientKeyExchangeProcessingStatus.AUTHENTICATED_AND_DECAPSULATED:
            if not isinstance(self.responder_state, ResponderSharedSecretState):
                raise ValueError("Successful processing must contain Bob's private shared-secret state.")
            if self.failure_reason is not None:
                raise ValueError("Successful processing must not contain a failure reason.")
            if self.responder_state.profile is not self.profile:
                raise ValueError("Successful processing must preserve the negotiated profile.")
        else:
            if self.responder_state is not None:
                raise ValueError("Rejected processing must not contain shared-secret state.")
            if not isinstance(self.failure_reason, str) or not self.failure_reason.strip():
                raise ValueError("Rejected processing must contain a failure reason.")

    @property
    def authenticated(self) -> bool:
        """Return whether Alice was authenticated and all required KEMs were decapsulated."""

        return self.status is ClientKeyExchangeProcessingStatus.AUTHENTICATED_AND_DECAPSULATED

    def __repr__(self) -> str:
        return (
            f"ProcessedClientKeyExchange(status={self.status.value!r}, signer={self.signer!r}, "
            f"profile={self.profile.value!r}, shared_secret_state_ready={self.authenticated!r})"
        )


class ClientKeyExchangeFactory:
    """Package and sign Alice's already-created Phase 3 public encapsulation response."""

    def create(
        self,
        *,
        initiator: PQCParty,
        signed_server_offer: SignedServerKeyOffer,
        processed_offer: ProcessedServerOffer,
    ) -> SignedClientKeyExchange:
        """Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice."""

        if not isinstance(initiator, PQCParty):
            raise TypeError(f"initiator must be a PQCParty. Got {type(initiator).__name__}.")
        if not isinstance(signed_server_offer, SignedServerKeyOffer):
            raise TypeError(
                "signed_server_offer must be a SignedServerKeyOffer. "
                f"Got {type(signed_server_offer).__name__}."
            )
        if not isinstance(processed_offer, ProcessedServerOffer):
            raise TypeError(
                f"processed_offer must be a ProcessedServerOffer. Got {type(processed_offer).__name__}."
            )
        if not processed_offer.authenticated:
            raise ValueError("ClientKeyExchange requires an authenticated Phase 3 result.")
        if processed_offer.initiator_state is None or processed_offer.public_encapsulation is None:
            raise ValueError("Authenticated Phase 3 result is missing its KEM outputs.")
        if processed_offer.initiator_state.is_closed:
            raise ValueError("ClientKeyExchange cannot use a closed initiator KEM state.")

        offer = signed_server_offer.offer
        response = processed_offer.public_encapsulation
        if processed_offer.signer != signed_server_offer.signer:
            raise ValueError("Processed responder identity does not match the signed server offer.")
        if (
            processed_offer.profile is not offer.profile
            or response.profile is not offer.profile
            or processed_offer.initiator_state.profile is not offer.profile
        ):
            raise ValueError("Processed offer profile does not match the signed server offer.")
        if (
            response.session_id != offer.session_id
            or processed_offer.initiator_state.session_id != offer.session_id
        ):
            raise ValueError("Processed offer session does not match the signed server offer.")
        if (
            response.ml_kem_algorithm != offer.ml_kem_algorithm
            or response.hqc_algorithm != offer.hqc_algorithm
            or (response.hqc_ciphertext is None) != (offer.hqc_public_key is None)
        ):
            raise ValueError("Encapsulation algorithms do not match the signed server offer.")

        definition = profile_definition(offer.profile)
        exchange = ClientKeyExchange(
            protocol_version=CLIENT_KEY_EXCHANGE_PROTOCOL_VERSION,
            session_id=response.session_id,
            profile=response.profile,
            server_offer_hash=sha384(offer.canonical_bytes()).digest(),
            ml_kem_algorithm=response.ml_kem_algorithm,
            ml_kem_ciphertext=response.ml_kem_ciphertext,
            hqc_algorithm=response.hqc_algorithm,
            hqc_ciphertext=response.hqc_ciphertext,
        )
        return SignedClientKeyExchange(
            exchange=exchange,
            signer=initiator.name,
            signature_algorithm=definition.signature_algorithm,
            signature=initiator.sign(exchange.canonical_bytes()),
        )


class ClientKeyExchangeProcessor:
    """Authenticate Alice and validate session binding before Bob decapsulates."""

    def process(
        self,
        *,
        responder: PQCParty,
        responder_state: ResponderKEMState,
        server_offer: SignedServerKeyOffer,
        signed_exchange: SignedClientKeyExchange,
    ) -> ProcessedClientKeyExchange:
        """Verify Alice's response and only then recover Bob's matching KEM secrets."""

        if not isinstance(responder, PQCParty):
            raise TypeError(f"responder must be a PQCParty. Got {type(responder).__name__}.")
        if not isinstance(responder_state, ResponderKEMState):
            raise TypeError(
                f"responder_state must be a ResponderKEMState. Got {type(responder_state).__name__}."
            )
        if not isinstance(server_offer, SignedServerKeyOffer):
            raise TypeError(
                f"server_offer must be a SignedServerKeyOffer. Got {type(server_offer).__name__}."
            )
        if not isinstance(signed_exchange, SignedClientKeyExchange):
            raise TypeError(
                f"signed_exchange must be a SignedClientKeyExchange. Got {type(signed_exchange).__name__}."
            )

        exchange = signed_exchange.exchange
        offer = server_offer.offer
        if responder_state.is_closed:
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.RESPONDER_STATE_CLOSED,
                reason="The responder KEM state is closed and cannot be reused.",
            )
        if offer.profile is not responder_state.profile or exchange.profile is not responder_state.profile:
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.PROFILE_MISMATCH,
                reason="The client exchange profile does not match Bob's local session.",
            )
        if (
            offer.session_id != responder_state.session_id
            or exchange.session_id != responder_state.session_id
        ):
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.SESSION_MISMATCH,
                reason="The client exchange session does not match Bob's local session.",
            )
        if not self._server_offer_matches_state(responder, responder_state, server_offer):
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.OFFER_BINDING_MISMATCH,
                reason="The original server offer does not match Bob's local responder state.",
            )

        expected_offer_hash = sha384(offer.canonical_bytes()).digest()
        if not hmac.compare_digest(expected_offer_hash, exchange.server_offer_hash):
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.OFFER_BINDING_MISMATCH,
                reason="The client exchange does not reference Bob's exact server offer.",
            )
        if not self._algorithms_match(exchange, offer):
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.ALGORITHM_MISMATCH,
                reason="The client exchange algorithms do not match the selected profile and offer.",
            )

        definition = profile_definition(exchange.profile)
        if signed_exchange.signature_algorithm != definition.signature_algorithm:
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.ALGORITHM_MISMATCH,
                reason="The declared signature algorithm does not match the selected profile.",
            )
        try:
            trusted_initiator = responder.trusted_peers.lookup(signed_exchange.signer)
        except UnknownTrustedPeerError:
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.UNTRUSTED_SIGNER,
                reason=f"Signer {signed_exchange.signer!r} is not provisioned in the trust store.",
            )
        if trusted_initiator.algorithm != signed_exchange.signature_algorithm:
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.ALGORITHM_MISMATCH,
                reason="The trusted identity algorithm does not match the signed client exchange.",
            )
        if not trusted_initiator.verify(exchange.canonical_bytes(), signed_exchange.signature):
            return self._rejected(
                signed_exchange,
                status=ClientKeyExchangeProcessingStatus.INVALID_SIGNATURE,
                reason="The client exchange signature is invalid for the trusted initiator identity.",
            )

        ml_kem_shared_secret = responder_state.decapsulate_ml_kem(exchange.ml_kem_ciphertext)
        hqc_shared_secret = None
        if exchange.profile is PQCProfile.HIGH:
            if exchange.hqc_ciphertext is None:
                raise ValueError("Authenticated HIGH client exchange is missing its HQC-3 ciphertext.")
            hqc_shared_secret = responder_state.decapsulate_hqc(exchange.hqc_ciphertext)

        shared_secret_state = ResponderSharedSecretState(
            session_id=exchange.session_id,
            profile=exchange.profile,
            _ml_kem_shared_secret=ml_kem_shared_secret,
            _hqc_shared_secret=hqc_shared_secret,
        )
        responder_state.close()
        return ProcessedClientKeyExchange(
            status=ClientKeyExchangeProcessingStatus.AUTHENTICATED_AND_DECAPSULATED,
            signer=signed_exchange.signer,
            profile=exchange.profile,
            responder_state=shared_secret_state,
        )

    @staticmethod
    def _server_offer_matches_state(
        responder: PQCParty,
        responder_state: ResponderKEMState,
        server_offer: SignedServerKeyOffer,
    ) -> bool:
        offer = server_offer.offer
        state_hqc_public_key = responder_state.hqc_public_key
        hqc_public_key_matches = (state_hqc_public_key is None and offer.hqc_public_key is None) or (
            state_hqc_public_key is not None
            and offer.hqc_public_key is not None
            and hmac.compare_digest(state_hqc_public_key, offer.hqc_public_key)
        )
        return (
            server_offer.signer == responder.name
            and hmac.compare_digest(responder_state.ml_kem_public_key, offer.ml_kem_public_key)
            and hqc_public_key_matches
        )

    @staticmethod
    def _algorithms_match(exchange: ClientKeyExchange, offer: ServerKeyOffer) -> bool:
        definition = profile_definition(exchange.profile)
        return (
            exchange.ml_kem_algorithm == definition.ml_kem_algorithm == offer.ml_kem_algorithm
            and exchange.hqc_algorithm == definition.hqc_algorithm == offer.hqc_algorithm
            and (exchange.hqc_ciphertext is None) == (definition.hqc_algorithm is None)
        )

    @staticmethod
    def _rejected(
        signed_exchange: SignedClientKeyExchange,
        *,
        status: ClientKeyExchangeProcessingStatus,
        reason: str,
    ) -> ProcessedClientKeyExchange:
        return ProcessedClientKeyExchange(
            status=status,
            signer=signed_exchange.signer,
            profile=signed_exchange.exchange.profile,
            failure_reason=reason,
        )
