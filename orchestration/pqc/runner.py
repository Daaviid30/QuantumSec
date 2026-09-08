"""Common-session adapter for the existing six-phase authenticated PQC protocol."""

from time import perf_counter_ns

from orchestration.config import SessionConfig
from orchestration.context import SessionExecutionContext
from orchestration.metrics import PQCAuthenticationMetrics, PQCSessionMetrics, SessionMetrics
from orchestration.pqc.exchange import PQCExchangeArtifacts, execute_authenticated_pqc_exchange
from orchestration.profiles import session_profile_definition
from orchestration.result import (
    SESSION_RESULT_VERSION,
    AuthenticationOutcome,
    EstablishedKeyCapability,
    EstablishedKeyType,
    SecretProvenance,
    SessionAuthentication,
    SessionResult,
    SessionStatus,
)
from orchestration.trace import SessionTraceBuilder, SessionTraceSource
from pqc.errors import PQCError
from pqc.profiles import profile_definition
from pqc.protocol import (
    PQCConfirmationKeyDeriver,
    PQCKeyConfirmation,
    PQCSessionKeyDeriver,
)


def _pqc_metrics(
    artifacts: PQCExchangeArtifacts,
    *,
    key_schedule_time_ns: int,
    confirmation_time_ns: int,
    public_key_provisioning_bytes: int,
    finished_bytes: int = 96,
) -> tuple[PQCSessionMetrics, PQCAuthenticationMetrics]:
    transcript = artifacts.transcript
    server = artifacts.signed_server_offer
    client = artifacts.signed_client_exchange
    definition = profile_definition(transcript.profile)
    operation = artifacts.operation_timer.snapshot()
    signature_bytes = len(server.signature) + len(client.signature)
    kem_public_key_bytes = len(server.offer.ml_kem_public_key) + (
        len(server.offer.hqc_public_key) if server.offer.hqc_public_key is not None else 0
    )
    kem_ciphertext_bytes = len(client.exchange.ml_kem_ciphertext) + (
        len(client.exchange.hqc_ciphertext) if client.exchange.hqc_ciphertext is not None else 0
    )
    canonical_protocol_bytes = len(server.offer.canonical_bytes()) + len(client.exchange.canonical_bytes())
    phase_total = (
        artifacts.server_offer_time_ns
        + artifacts.server_processing_time_ns
        + artifacts.client_exchange_time_ns
        + artifacts.client_processing_time_ns
        + key_schedule_time_ns
        + confirmation_time_ns
    )
    return (
        PQCSessionMetrics(
            internal_profile=transcript.profile.value,
            algorithms=definition.kem_algorithms
            + (definition.signature_algorithm, "HKDF-SHA-384", "HMAC-SHA-384"),
            server_offer_time_ns=artifacts.server_offer_time_ns,
            server_processing_time_ns=artifacts.server_processing_time_ns,
            client_exchange_time_ns=artifacts.client_exchange_time_ns,
            client_processing_time_ns=artifacts.client_processing_time_ns,
            key_schedule_time_ns=key_schedule_time_ns,
            confirmation_time_ns=confirmation_time_ns,
            crypto_software_time_ns=phase_total,
            ml_kem_keygen_time_ns=operation.ml_kem_keygen_time_ns,
            hqc_keygen_time_ns=operation.hqc_keygen_time_ns,
            server_offer_sign_time_ns=operation.server_offer_sign_time_ns,
            server_offer_verify_time_ns=operation.server_offer_verify_time_ns,
            ml_kem_encapsulate_time_ns=operation.ml_kem_encapsulate_time_ns,
            hqc_encapsulate_time_ns=operation.hqc_encapsulate_time_ns,
            client_exchange_sign_time_ns=operation.client_exchange_sign_time_ns,
            client_exchange_verify_time_ns=operation.client_exchange_verify_time_ns,
            ml_kem_decapsulate_time_ns=operation.ml_kem_decapsulate_time_ns,
            hqc_decapsulate_time_ns=operation.hqc_decapsulate_time_ns,
            transcript_construction_hash_time_ns=(operation.transcript_construction_hash_time_ns),
            kem_combiner_encoding_time_ns=operation.kem_combiner_encoding_time_ns,
            hkdf_session_time_ns=operation.hkdf_session_time_ns,
            hkdf_confirmation_time_ns=operation.hkdf_confirmation_time_ns,
            finished_generation_time_ns=operation.finished_generation_time_ns,
            finished_verification_time_ns=operation.finished_verification_time_ns,
            kem_public_key_bytes=kem_public_key_bytes,
            kem_ciphertext_bytes=kem_ciphertext_bytes,
            canonical_protocol_bytes=canonical_protocol_bytes,
            transcript_bytes=len(transcript.canonical_bytes()),
            signature_bytes=signature_bytes,
            finished_bytes=finished_bytes,
            public_key_provisioning_bytes=public_key_provisioning_bytes,
            serialized_transport_bytes=None,
        ),
        PQCAuthenticationMetrics(
            mechanism="mutual digital signatures",
            algorithm=definition.signature_algorithm,
            executed=True,
            verified=True,
            signatures_generated=2,
            signatures_verified=2,
            signature_bytes=signature_bytes,
            trust_assumption="Peer ML-DSA public identities were pre-provisioned out of band.",
        ),
    )


def run_pqc_session(config: SessionConfig, context: SessionExecutionContext) -> SessionResult:
    """Run the unchanged PQC handshake and adapt its established capability."""

    definition = session_profile_definition(config.profile)
    if definition.internal_pqc_profile is None or definition.hybrid or definition.qkd_profile is not None:
        raise ValueError("run_pqc_session requires a PQC-only session profile.")
    if context.pqc_initiator is None or context.pqc_responder is None:
        raise ValueError("PQC execution requires pre-provisioned initiator and responder parties.")
    trace = SessionTraceBuilder()
    trace.append(SessionTraceSource.SESSION, "session", "started", config.profile.value)
    wall_start = perf_counter_ns()
    exchange = execute_authenticated_pqc_exchange(context, definition.internal_pqc_profile, trace)
    if not isinstance(exchange, PQCExchangeArtifacts):
        elapsed = perf_counter_ns() - wall_start
        trace.append(SessionTraceSource.SESSION, "session", "aborted", exchange.reason)
        auth = AuthenticationOutcome(
            "PQC handshake authentication",
            "mutual digital signatures",
            "ML-DSA-65",
            True,
            False,
            "Peer public identities must be pre-provisioned out of band.",
        )
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.session_id,
            config.profile,
            SessionStatus.ABORTED,
            exchange.reason,
            (),
            SessionAuthentication(pqc_exchange=auth),
            trace.freeze(),
            SessionMetrics(orchestration_software_wall_time_ns=elapsed),
        )

    alice_key = bob_key = None
    alice_session = bob_session = None
    alice_confirmation = bob_confirmation = None
    key_time = 0
    confirmation_time = 0
    try:
        start = perf_counter_ns()
        key_deriver = PQCSessionKeyDeriver()
        alice_key = key_deriver.derive_initiator(
            processed_server_offer=exchange.processed_server_offer,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
            operation_observer=exchange.operation_timer.observe,
        )
        bob_key = key_deriver.derive_responder(
            processed_client_exchange=exchange.processed_client_exchange,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
            operation_observer=exchange.operation_timer.observe,
        )
        key_time = perf_counter_ns() - start
        trace.append(
            SessionTraceSource.PQC,
            "key_schedule",
            "derived",
            "Role-local session and confirmation schedules started.",
        )

        start = perf_counter_ns()
        confirmation_deriver = PQCConfirmationKeyDeriver()
        alice_confirmation = confirmation_deriver.derive_initiator(
            processed_server_offer=exchange.processed_server_offer,
            session_key_state=alice_key,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
            operation_observer=exchange.operation_timer.observe,
        )
        bob_confirmation = confirmation_deriver.derive_responder(
            processed_client_exchange=exchange.processed_client_exchange,
            session_key_state=bob_key,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
            operation_observer=exchange.operation_timer.observe,
        )
        responder_finished = PQCKeyConfirmation.create_responder_finished(
            bob_confirmation,
            operation_observer=exchange.operation_timer.observe,
        )
        if context.pqc_finished_transport_hook is not None:
            responder_finished = context.pqc_finished_transport_hook(responder_finished)
        initiator_finished = PQCKeyConfirmation.verify_responder_and_create_initiator(
            alice_confirmation,
            responder_finished,
            operation_observer=exchange.operation_timer.observe,
        )
        if context.pqc_finished_transport_hook is not None:
            initiator_finished = context.pqc_finished_transport_hook(initiator_finished)
        confirmed = PQCKeyConfirmation.verify_initiator_and_confirm(
            bob_confirmation,
            initiator_finished,
            operation_observer=exchange.operation_timer.observe,
        )
        alice_session = PQCKeyConfirmation.establish_local_session(confirmed, alice_confirmation)
        bob_session = PQCKeyConfirmation.establish_local_session(confirmed, bob_confirmation)
        confirmation_time = perf_counter_ns() - start
        key = alice_session.export_session_key()
        # The authenticated Finished state machine guarantees agreement; equality does not decide acceptance.
        trace.append(
            SessionTraceSource.PQC, "finished", "verified", "Both role-separated Finished messages verified."
        )
        pqc_metrics, auth_metrics = _pqc_metrics(
            exchange,
            key_schedule_time_ns=key_time,
            confirmation_time_ns=confirmation_time,
            public_key_provisioning_bytes=(
                len(context.pqc_initiator.public_identity.public_key)
                + len(context.pqc_responder.public_identity.public_key)
            ),
        )
        trace.append(
            SessionTraceSource.SESSION, "session", "established", "Confirmed PQC session key released."
        )
        elapsed = perf_counter_ns() - wall_start
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.ESTABLISHED,
            None,
            tuple(
                SecretProvenance(
                    index,
                    "pqc",
                    "authenticated KEM handshake",
                    algorithm,
                    "raw KEM secret via canonical PQC KDF input",
                    256,
                    32,
                )
                for index, algorithm in enumerate(
                    profile_definition(exchange.transcript.profile).kem_algorithms, 1
                )
            ),
            SessionAuthentication(
                pqc_exchange=AuthenticationOutcome(
                    "PQC handshake authentication",
                    auth_metrics.mechanism,
                    auth_metrics.algorithm,
                    True,
                    True,
                    auth_metrics.trust_assumption,
                )
            ),
            trace.freeze(),
            SessionMetrics(
                pqc=pqc_metrics,
                pqc_authentication=auth_metrics,
                orchestration_software_wall_time_ns=elapsed,
            ),
            (
                ("pqc_protocol_version", exchange.transcript.protocol_version),
                ("pqc_transcript_hash_sha384", exchange.transcript.transcript_hash.hex()),
            ),
            EstablishedKeyCapability(key, bit_length=256, key_type=EstablishedKeyType.SESSION_KEY),
        )
    except ValueError as exc:
        pqc_metrics, auth_metrics = _pqc_metrics(
            exchange,
            key_schedule_time_ns=key_time,
            confirmation_time_ns=confirmation_time,
            public_key_provisioning_bytes=(
                len(context.pqc_initiator.public_identity.public_key)
                + len(context.pqc_responder.public_identity.public_key)
            ),
        )
        reason = str(exc)
        trace.append(SessionTraceSource.PQC, "finished", "failed", reason)
        trace.append(SessionTraceSource.SESSION, "session", "aborted", reason)
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.ABORTED,
            reason,
            (),
            SessionAuthentication(
                pqc_exchange=AuthenticationOutcome(
                    "PQC handshake authentication",
                    auth_metrics.mechanism,
                    auth_metrics.algorithm,
                    True,
                    True,
                    auth_metrics.trust_assumption,
                )
            ),
            trace.freeze(),
            SessionMetrics(
                pqc=pqc_metrics,
                pqc_authentication=auth_metrics,
                orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
            ),
            (
                ("pqc_protocol_version", exchange.transcript.protocol_version),
                ("pqc_transcript_hash_sha384", exchange.transcript.transcript_hash.hex()),
            ),
        )
    except (PQCError, RuntimeError, TypeError) as exc:
        pqc_metrics, auth_metrics = _pqc_metrics(
            exchange,
            key_schedule_time_ns=key_time,
            confirmation_time_ns=confirmation_time,
            public_key_provisioning_bytes=(
                len(context.pqc_initiator.public_identity.public_key)
                + len(context.pqc_responder.public_identity.public_key)
            ),
        )
        reason = f"Operational execution failure: {exc}"
        trace.append(SessionTraceSource.PQC, "execution", "failed", reason)
        trace.append(SessionTraceSource.SESSION, "session", "failed", reason)
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.FAILED,
            reason,
            (),
            SessionAuthentication(
                pqc_exchange=AuthenticationOutcome(
                    "PQC handshake authentication",
                    auth_metrics.mechanism,
                    auth_metrics.algorithm,
                    True,
                    True,
                    auth_metrics.trust_assumption,
                )
            ),
            trace.freeze(),
            SessionMetrics(
                pqc=pqc_metrics,
                pqc_authentication=auth_metrics,
                orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
            ),
            (
                ("pqc_protocol_version", exchange.transcript.protocol_version),
                ("pqc_transcript_hash_sha384", exchange.transcript.transcript_hash.hex()),
            ),
        )
    finally:
        if alice_session is not None:
            alice_session.close()
        if bob_session is not None:
            bob_session.close()
        if alice_confirmation is not None:
            alice_confirmation.close()
        if bob_confirmation is not None:
            bob_confirmation.close()
        if alice_key is not None:
            alice_key.close()
        if bob_key is not None:
            bob_key.close()
        # KEM states are already retired by confirmation derivation; close is idempotent.
        exchange.close()
