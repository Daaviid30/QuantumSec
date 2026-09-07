"""Domain-owned, one-time release of authenticated raw KEM contributions."""

from dataclasses import dataclass, field

from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.client_exchange import ProcessedClientKeyExchange
from pqc.protocol.initiator import ProcessedServerOffer
from pqc.protocol.key_schedule import (
    _validated_initiator_secret_state,
    _validated_responder_secret_state,
)
from pqc.protocol.messages import SignedClientKeyExchange, SignedServerKeyOffer
from pqc.protocol.transcript import PQCHandshakeTranscript

_AUTHENTICATED_CONTRIBUTIONS_PROOF = object()


@dataclass(slots=True, repr=False)
class AuthenticatedKEMContributions:
    """Consumable capability issued only for an authenticated exact PQC transcript."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    transcript_hash: bytes
    _components: tuple[tuple[str, bytes], ...] | None = field(repr=False)
    _proof: object = field(repr=False)

    def __post_init__(self) -> None:
        if self._proof is not _AUTHENTICATED_CONTRIBUTIONS_PROOF:
            raise TypeError("AuthenticatedKEMContributions must be issued by the authenticated PQC protocol.")

    @property
    def is_consumed(self) -> bool:
        return self._components is None

    def consume(self) -> tuple[tuple[str, bytes], ...]:
        """Return defensive secret copies once and retire the capability."""

        if self._components is None:
            raise RuntimeError("Authenticated KEM contributions were already consumed.")
        components = tuple((algorithm, bytes(secret)) for algorithm, secret in self._components)
        self._components = None
        return components

    def close(self) -> None:
        self._components = None

    def __repr__(self) -> str:
        return (
            f"AuthenticatedKEMContributions(profile={self.profile.value!r}, "
            f"algorithms={profile_definition(self.profile).kem_algorithms!r}, "
            f"consumed={self.is_consumed})"
        )


def _transcript(
    signed_server_offer: SignedServerKeyOffer,
    signed_client_exchange: SignedClientKeyExchange,
) -> PQCHandshakeTranscript:
    return PQCHandshakeTranscript.from_messages(signed_server_offer, signed_client_exchange)


def issue_initiator_hybrid_contributions(
    *,
    processed_server_offer: ProcessedServerOffer,
    signed_server_offer: SignedServerKeyOffer,
    signed_client_exchange: SignedClientKeyExchange,
) -> AuthenticatedKEMContributions:
    """Consume Alice's state only after its authenticated transcript binding validates."""

    transcript = _transcript(signed_server_offer, signed_client_exchange)
    state = _validated_initiator_secret_state(processed_server_offer, transcript)
    return AuthenticatedKEMContributions(
        transcript.session_id,
        transcript.profile,
        transcript.transcript_hash,
        state._consume_hybrid_components(),
        _AUTHENTICATED_CONTRIBUTIONS_PROOF,
    )


def issue_responder_hybrid_contributions(
    *,
    processed_client_exchange: ProcessedClientKeyExchange,
    signed_server_offer: SignedServerKeyOffer,
    signed_client_exchange: SignedClientKeyExchange,
) -> AuthenticatedKEMContributions:
    """Consume Bob's state only after its authenticated transcript binding validates."""

    transcript = _transcript(signed_server_offer, signed_client_exchange)
    state = _validated_responder_secret_state(processed_client_exchange, transcript)
    return AuthenticatedKEMContributions(
        transcript.session_id,
        transcript.profile,
        transcript.transcript_hash,
        state._consume_hybrid_components(),
        _AUTHENTICATED_CONTRIBUTIONS_PROOF,
    )
