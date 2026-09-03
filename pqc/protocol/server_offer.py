"""Creation of responder KEM state and authenticated server offers."""

import secrets
from dataclasses import dataclass, field

from pqc.kem import HQC3, MLKEM768
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.messages import (
    SERVER_KEY_OFFER_NONCE_LENGTH,
    SERVER_KEY_OFFER_PROTOCOL_VERSION,
    SERVER_KEY_OFFER_SESSION_ID_LENGTH,
    ServerKeyOffer,
    SignedServerKeyOffer,
)
from pqc.protocol.party import PQCParty


@dataclass(slots=True, repr=False)
class ResponderKEMState:
    """Maintains ephemeral private KEM key pairs for an active handshake responder session."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    _ml_kem: MLKEM768 | None = field(repr=False)
    _hqc: HQC3 | None = field(default=None, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate session ID length, profile compatibility, and presence of required KEM instances."""
        if not isinstance(self.session_id, bytes):
            raise TypeError(f"session_id must be bytes. Got {type(self.session_id).__name__}.")
        if len(self.session_id) != SERVER_KEY_OFFER_SESSION_ID_LENGTH:
            raise ValueError(
                f"session_id must contain {SERVER_KEY_OFFER_SESSION_ID_LENGTH} bytes. "
                f"Got {len(self.session_id)}."
            )
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        if not isinstance(self._ml_kem, MLKEM768):
            raise TypeError(f"ml_kem must be MLKEM768. Got {type(self._ml_kem).__name__}.")
        if self.profile is PQCProfile.LOW and self._hqc is not None:
            raise ValueError("LOW responder state must not contain HQC material.")
        if self.profile is PQCProfile.HIGH and not isinstance(self._hqc, HQC3):
            raise ValueError("HIGH responder state must contain HQC3 material.")
        self.session_id = bytes(self.session_id)

    def _active_ml_kem(self) -> MLKEM768:
        """Return the active ML-KEM provider instance or raise RuntimeError if state is closed."""
        if self._closed or self._ml_kem is None:
            raise RuntimeError("Responder KEM state is closed.")
        return self._ml_kem

    def _active_hqc(self) -> HQC3:
        """Return the active HQC provider instance required by a HIGH-profile session."""

        if self._closed:
            raise RuntimeError("Responder KEM state is closed.")
        if self._hqc is None:
            raise RuntimeError("Responder KEM state does not contain an HQC key pair.")
        return self._hqc

    @property
    def ml_kem_public_key(self) -> bytes:
        """Return the public ML-KEM encapsulation key associated with this responder session."""

        return self._active_ml_kem().public_key

    @property
    def hqc_public_key(self) -> bytes | None:
        """Return the public HQC encapsulation key if the session uses the HIGH profile, or None otherwise."""

        if self._closed:
            raise RuntimeError("Responder KEM state is closed.")
        return None if self._hqc is None else self._hqc.public_key

    def decapsulate_ml_kem(self, ciphertext: bytes) -> bytes:
        """Decapsulate an ML-KEM ciphertext with this session's private key."""

        return self._active_ml_kem().decapsulate(ciphertext)

    def decapsulate_hqc(self, ciphertext: bytes) -> bytes:
        """Decapsulate an HQC ciphertext with this HIGH-profile session's private key."""

        return self._active_hqc().decapsulate(ciphertext)

    @property
    def is_closed(self) -> bool:
        """Return whether this responder KEM state has been closed and its private keys released."""

        return self._closed

    def close(self) -> None:
        """Release references to ephemeral private KEM instances to prevent subsequent reuse."""

        self._ml_kem = None
        self._hqc = None
        self._closed = True

    def __repr__(self) -> str:
        """Return a safe string representation showing profile and closed status."""
        algorithms = profile_definition(self.profile).kem_algorithms
        return (
            f"ResponderKEMState(profile={self.profile.value!r}, algorithms={algorithms!r}, "
            f"closed={self._closed!r})"
        )


class ServerKeyOfferFactory:
    """Factory creating responder ephemeral KEM states and authenticated SignedServerKeyOffers."""

    def create(
        self,
        *,
        responder: PQCParty,
        profile: PQCProfile,
    ) -> tuple[ResponderKEMState, SignedServerKeyOffer]:
        """Generate fresh ephemeral KEM keys and create a signed server offer for a new session."""

        if not isinstance(responder, PQCParty):
            raise TypeError(f"responder must be a PQCParty. Got {type(responder).__name__}.")
        definition = profile_definition(profile)

        session_id = secrets.token_bytes(SERVER_KEY_OFFER_SESSION_ID_LENGTH)
        ml_kem = MLKEM768.generate()
        hqc = HQC3.generate() if profile is PQCProfile.HIGH else None
        state = ResponderKEMState(session_id=session_id, profile=profile, _ml_kem=ml_kem, _hqc=hqc)
        offer = ServerKeyOffer(
            protocol_version=SERVER_KEY_OFFER_PROTOCOL_VERSION,
            session_id=session_id,
            profile=profile,
            nonce=secrets.token_bytes(SERVER_KEY_OFFER_NONCE_LENGTH),
            ml_kem_algorithm=definition.ml_kem_algorithm,
            ml_kem_public_key=state.ml_kem_public_key,
            hqc_algorithm=definition.hqc_algorithm,
            hqc_public_key=state.hqc_public_key,
        )
        signed_offer = SignedServerKeyOffer(
            offer=offer,
            signer=responder.name,
            signature_algorithm=definition.signature_algorithm,
            signature=responder.sign(offer.canonical_bytes()),
        )
        return state, signed_offer
