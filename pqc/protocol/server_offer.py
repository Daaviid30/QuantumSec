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


@dataclass(frozen=True, slots=True, repr=False)
class ResponderKEMState:
    """Private ephemeral KEM capabilities retained by one responder session."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    _ml_kem: MLKEM768 = field(repr=False)
    _hqc: HQC3 | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
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
        object.__setattr__(self, "session_id", bytes(self.session_id))

    @property
    def ml_kem_public_key(self) -> bytes:
        """Return the public ML-KEM key for the associated offer."""

        return self._ml_kem.public_key

    @property
    def hqc_public_key(self) -> bytes | None:
        """Return the public HQC key when the HIGH profile is active."""

        return None if self._hqc is None else self._hqc.public_key

    def __repr__(self) -> str:
        algorithms = profile_definition(self.profile).kem_algorithms
        return f"ResponderKEMState(profile={self.profile.value!r}, algorithms={algorithms!r})"


class ServerKeyOfferFactory:
    """Create fresh KEM state, canonical offers, and responder signatures."""

    def create(
        self,
        *,
        responder: PQCParty,
        profile: PQCProfile,
    ) -> tuple[ResponderKEMState, SignedServerKeyOffer]:
        """Create and sign one fresh server offer without establishing a secret."""

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
            ml_kem_algorithm=definition.kem_algorithms[0],
            ml_kem_public_key=state.ml_kem_public_key,
            hqc_algorithm=definition.kem_algorithms[1] if profile is PQCProfile.HIGH else None,
            hqc_public_key=state.hqc_public_key,
        )
        signed_offer = SignedServerKeyOffer(
            offer=offer,
            signer=responder.name,
            signature_algorithm=definition.signature_algorithm,
            signature=responder.sign(offer.canonical_bytes()),
        )
        return state, signed_offer
