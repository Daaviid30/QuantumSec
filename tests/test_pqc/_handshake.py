"""Shared real PQC handshake setup for Phase 5/6 tests."""

from dataclasses import dataclass

from pqc import (
    ClientKeyExchangeFactory,
    ClientKeyExchangeProcessor,
    DerivedSessionKeyState,
    PQCParty,
    PQCProfile,
    PQCSessionKeyDeriver,
    ProcessedClientKeyExchange,
    ProcessedServerOffer,
    ServerKeyOfferFactory,
    ServerKeyOfferProcessor,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
)
from pqc.protocol import InitiatorKEMState, ResponderKEMState, ResponderSharedSecretState


@dataclass(slots=True)
class Phase5Flow:
    """Complete authenticated flow retaining both parties' private Phase 4 states."""

    alice: PQCParty
    bob: PQCParty
    responder_kem_state: ResponderKEMState
    signed_server_offer: SignedServerKeyOffer
    processed_server_offer: ProcessedServerOffer
    signed_client_exchange: SignedClientKeyExchange
    processed_client_exchange: ProcessedClientKeyExchange


def create_phase5_flow(profile: PQCProfile) -> Phase5Flow:
    """Execute the real mutually authenticated PQC flow through Phase 4."""

    alice = PQCParty.create("Alice")
    bob = PQCParty.create("Bob")
    alice.trust_peer(bob.public_identity)
    bob.trust_peer(alice.public_identity)

    responder_kem_state, signed_server_offer = ServerKeyOfferFactory().create(
        responder=bob,
        profile=profile,
    )
    processed_server_offer = ServerKeyOfferProcessor().process(
        initiator=alice,
        signed_offer=signed_server_offer,
    )
    signed_client_exchange = ClientKeyExchangeFactory().create(
        initiator=alice,
        signed_server_offer=signed_server_offer,
        processed_offer=processed_server_offer,
    )
    processed_client_exchange = ClientKeyExchangeProcessor().process(
        responder=bob,
        responder_state=responder_kem_state,
        server_offer=signed_server_offer,
        signed_exchange=signed_client_exchange,
    )
    assert processed_server_offer.authenticated
    assert processed_client_exchange.authenticated
    return Phase5Flow(
        alice=alice,
        bob=bob,
        responder_kem_state=responder_kem_state,
        signed_server_offer=signed_server_offer,
        processed_server_offer=processed_server_offer,
        signed_client_exchange=signed_client_exchange,
        processed_client_exchange=processed_client_exchange,
    )


def initiator_secret_state(flow: Phase5Flow) -> InitiatorKEMState:
    """Return Alice's authenticated private KEM state for tests."""

    state = flow.processed_server_offer.initiator_state
    assert state is not None
    return state


def responder_secret_state(flow: Phase5Flow) -> ResponderSharedSecretState:
    """Return Bob's authenticated private KEM state for tests."""

    state = flow.processed_client_exchange.responder_state
    assert state is not None
    return state


def derive_session_keys(
    flow: Phase5Flow,
) -> tuple[DerivedSessionKeyState, DerivedSessionKeyState]:
    """Derive the two independent Phase 5 role-local session-key states."""

    deriver = PQCSessionKeyDeriver()
    alice_key = deriver.derive_initiator(
        processed_server_offer=flow.processed_server_offer,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    bob_key = deriver.derive_responder(
        processed_client_exchange=flow.processed_client_exchange,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    return alice_key, bob_key
