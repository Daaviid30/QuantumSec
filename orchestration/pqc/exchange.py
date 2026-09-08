"""Reusable execution of the existing mutually authenticated PQC phases 2--4."""

from dataclasses import dataclass
from time import perf_counter_ns

from orchestration.context import SessionExecutionContext
from orchestration.pqc.instrumentation import PQCOperationTimer
from orchestration.trace import SessionTraceBuilder, SessionTraceSource
from pqc import PQCProfile
from pqc.errors import PQCError
from pqc.protocol import (
    ClientKeyExchangeFactory,
    ClientKeyExchangeProcessor,
    PQCHandshakeTranscript,
    PQCParty,
    ProcessedClientKeyExchange,
    ProcessedServerOffer,
    ResponderSharedSecretState,
    ServerKeyOfferFactory,
    ServerKeyOfferProcessor,
    SignedClientKeyExchange,
    SignedServerKeyOffer,
)
from pqc.protocol.initiator import InitiatorKEMState
from pqc.protocol.instrumentation import PQCOperation


@dataclass(slots=True, repr=False)
class PQCExchangeArtifacts:
    signed_server_offer: SignedServerKeyOffer
    processed_server_offer: ProcessedServerOffer
    signed_client_exchange: SignedClientKeyExchange
    processed_client_exchange: ProcessedClientKeyExchange
    transcript: PQCHandshakeTranscript
    server_offer_time_ns: int
    server_processing_time_ns: int
    client_exchange_time_ns: int
    client_processing_time_ns: int
    operation_timer: PQCOperationTimer

    @property
    def initiator_state(self) -> InitiatorKEMState:
        state = self.processed_server_offer.initiator_state
        if state is None:
            raise RuntimeError("Authenticated exchange has no initiator KEM state.")
        return state

    @property
    def responder_state(self) -> ResponderSharedSecretState:
        state = self.processed_client_exchange.responder_state
        if state is None:
            raise RuntimeError("Authenticated exchange has no responder KEM state.")
        return state

    def close(self) -> None:
        self.initiator_state.close()
        self.responder_state.close()

    def __repr__(self) -> str:
        return (
            f"PQCExchangeArtifacts(profile={self.transcript.profile.value!r}, "
            f"session_id={self.transcript.session_id.hex()!r}, authenticated=True)"
        )


@dataclass(frozen=True, slots=True)
class PQCExchangeRejected:
    session_id: bytes
    reason: str
    server_offer_time_ns: int
    server_processing_time_ns: int
    client_exchange_time_ns: int = 0
    client_processing_time_ns: int = 0


def execute_authenticated_pqc_exchange(
    context: SessionExecutionContext,
    profile: PQCProfile,
    trace: SessionTraceBuilder,
) -> PQCExchangeArtifacts | PQCExchangeRejected:
    """Execute signed offer/encapsulation/exchange/decapsulation without deriving keys."""

    alice = context.pqc_initiator
    bob = context.pqc_responder
    if alice is None or bob is None:
        raise ValueError("PQC execution requires pre-provisioned initiator and responder parties.")
    if not isinstance(alice, PQCParty) or not isinstance(bob, PQCParty):
        raise TypeError("PQC initiator and responder must be PQCParty instances.")
    if alice.name == bob.name:
        raise ValueError("PQC initiator and responder identities must be distinct.")
    operation_timer = PQCOperationTimer(hqc_enabled=profile is PQCProfile.HIGH)

    start = perf_counter_ns()
    responder_kem_state, signed_offer = ServerKeyOfferFactory().create(
        responder=bob,
        profile=profile,
        operation_observer=operation_timer.observe,
    )
    offer_time = perf_counter_ns() - start
    trace.append(SessionTraceSource.PQC, "server_offer", "created", "Responder KEM offer signed.")
    try:
        transported_offer = (
            context.server_offer_transport_hook(signed_offer)
            if context.server_offer_transport_hook is not None
            else signed_offer
        )
    except Exception:
        responder_kem_state.close()
        raise
    if not isinstance(transported_offer, SignedServerKeyOffer):
        responder_kem_state.close()
        raise TypeError("Server-offer transport hook must return SignedServerKeyOffer.")

    start = perf_counter_ns()
    try:
        processed_offer = ServerKeyOfferProcessor().process(
            initiator=alice,
            signed_offer=transported_offer,
            operation_observer=operation_timer.observe,
        )
    except PQCError as exc:
        offer_processing_time = perf_counter_ns() - start
        responder_kem_state.close()
        reason = f"PQC server-offer processing failed: {exc}"
        trace.append(SessionTraceSource.PQC, "server_offer_processing", "failed", reason)
        return PQCExchangeRejected(
            signed_offer.offer.session_id,
            reason,
            offer_time,
            offer_processing_time,
        )
    except Exception:
        responder_kem_state.close()
        raise
    offer_processing_time = perf_counter_ns() - start
    if not processed_offer.authenticated:
        responder_kem_state.close()
        reason = processed_offer.failure_reason or "Server offer authentication failed."
        trace.append(SessionTraceSource.PQC, "server_offer_authentication", "rejected", reason)
        return PQCExchangeRejected(
            signed_offer.offer.session_id,
            reason,
            offer_time,
            offer_processing_time,
        )
    trace.append(
        SessionTraceSource.PQC, "server_offer_authentication", "verified", "Responder identity verified."
    )

    start = perf_counter_ns()
    try:
        signed_exchange = ClientKeyExchangeFactory().create(
            initiator=alice,
            signed_server_offer=transported_offer,
            processed_offer=processed_offer,
            operation_observer=operation_timer.observe,
        )
    except PQCError as exc:
        exchange_time = perf_counter_ns() - start
        responder_kem_state.close()
        assert processed_offer.initiator_state is not None
        processed_offer.initiator_state.close()
        reason = f"PQC client-exchange creation failed: {exc}"
        trace.append(SessionTraceSource.PQC, "client_exchange", "failed", reason)
        return PQCExchangeRejected(
            signed_offer.offer.session_id,
            reason,
            offer_time,
            offer_processing_time,
            exchange_time,
        )
    except Exception:
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        raise
    exchange_time = perf_counter_ns() - start
    trace.append(SessionTraceSource.PQC, "client_exchange", "created", "Initiator encapsulations signed.")
    try:
        transported_exchange = (
            context.client_exchange_transport_hook(signed_exchange)
            if context.client_exchange_transport_hook is not None
            else signed_exchange
        )
    except Exception:
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        raise
    if not isinstance(transported_exchange, SignedClientKeyExchange):
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        raise TypeError("Client-exchange transport hook must return SignedClientKeyExchange.")

    start = perf_counter_ns()
    try:
        processed_exchange = ClientKeyExchangeProcessor().process(
            responder=bob,
            responder_state=responder_kem_state,
            server_offer=transported_offer,
            signed_exchange=transported_exchange,
            operation_observer=operation_timer.observe,
        )
    except PQCError as exc:
        processing_time = perf_counter_ns() - start
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        reason = f"PQC client-exchange processing failed: {exc}"
        trace.append(SessionTraceSource.PQC, "client_exchange_processing", "failed", reason)
        return PQCExchangeRejected(
            signed_offer.offer.session_id,
            reason,
            offer_time,
            offer_processing_time,
            exchange_time,
            processing_time,
        )
    except Exception:
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        raise
    processing_time = perf_counter_ns() - start
    if not processed_exchange.authenticated:
        responder_kem_state.close()
        if processed_offer.initiator_state is not None:
            processed_offer.initiator_state.close()
        reason = processed_exchange.failure_reason or "Client exchange authentication failed."
        trace.append(SessionTraceSource.PQC, "client_exchange_authentication", "rejected", reason)
        return PQCExchangeRejected(
            signed_offer.offer.session_id,
            reason,
            offer_time,
            offer_processing_time,
            exchange_time,
            processing_time,
        )
    trace.append(
        SessionTraceSource.PQC, "client_exchange_authentication", "verified", "Initiator identity verified."
    )
    start = perf_counter_ns()
    transcript = PQCHandshakeTranscript.from_messages(transported_offer, transported_exchange)
    _ = transcript.transcript_hash
    operation_timer.observe(PQCOperation.TRANSCRIPT_CONSTRUCTION_HASH, perf_counter_ns() - start)
    return PQCExchangeArtifacts(
        transported_offer,
        processed_offer,
        transported_exchange,
        processed_exchange,
        transcript,
        offer_time,
        offer_processing_time,
        exchange_time,
        processing_time,
        operation_timer,
    )
