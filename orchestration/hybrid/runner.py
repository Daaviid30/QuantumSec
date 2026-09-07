"""Orchestrate authenticated QKD and raw authenticated PQC contributions."""

from dataclasses import replace
from hashlib import sha384
from time import perf_counter_ns

import numpy as np

from orchestration.config import SessionConfig
from orchestration.context import SessionExecutionContext
from orchestration.hybrid.context import HybridPublicContext
from orchestration.hybrid.encoding import (
    QKD_COMPONENT_ALGORITHM,
    HybridSecretComponent,
    canonical_hybrid_secret_input,
    hybrid_component_metadata_bytes,
    hybrid_kem_label,
)
from orchestration.hybrid.finished import (
    HybridFinishedMessage,
    HybridFinishedRole,
    create_finished,
    verify_finished,
)
from orchestration.hybrid.key_schedule import (
    HybridDerivedKeys,
    derive_hybrid_confirmation_key,
    derive_hybrid_session_key,
)
from orchestration.metrics import HybridSessionMetrics, QKDSessionMetrics, SessionMetrics
from orchestration.pqc.exchange import PQCExchangeArtifacts, execute_authenticated_pqc_exchange
from orchestration.pqc.runner import _pqc_metrics
from orchestration.profiles import session_profile_definition
from orchestration.qkd.result import AuthenticatedQKDSessionResult, QKDOrchestrationStatus
from orchestration.qkd.runner import run_qkd_profile, validate_qkd_authentication_context
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
from pqc.protocol import (
    issue_initiator_hybrid_contributions,
    issue_responder_hybrid_contributions,
)


def _qkd_outcome(result: AuthenticatedQKDSessionResult) -> AuthenticationOutcome:
    authentication = result.authentication
    return AuthenticationOutcome(
        "QKD classical transcript authentication",
        authentication.metrics.mechanism.value,
        authentication.metrics.algorithm,
        authentication.executed,
        authentication.verified,
        authentication.metrics.trust_assumption,
    )


def _pqc_outcome(verified: bool) -> AuthenticationOutcome:
    return AuthenticationOutcome(
        "PQC contribution authentication",
        "mutual digital signatures",
        "ML-DSA-65",
        True,
        verified,
        "Peer ML-DSA public identities were pre-provisioned out of band.",
    )


def _hybrid_public_context_entries(
    context: HybridPublicContext | None,
) -> tuple[tuple[str, str | int], ...]:
    if context is None:
        return ()
    return (
        ("hybrid_context_hash_sha384", context.context_hash.hex()),
        ("qkd_transcript_hash_sha384", context.qkd_transcript_hash.hex()),
        ("pqc_transcript_hash_sha384", context.pqc_transcript_hash.hex()),
        ("hybrid_encoding_version", context.encoding_version),
        ("hybrid_context_version", context.version),
    )


def run_hybrid_session(config: SessionConfig, context: SessionExecutionContext) -> SessionResult:
    """Establish a hybrid key only after both source protocols and hybrid Finished succeed."""

    definition = session_profile_definition(config.profile)
    if not definition.hybrid or definition.internal_pqc_profile is None:
        raise ValueError("run_hybrid_session requires a hybrid session profile.")
    if context.qkd_protocol is None:
        raise ValueError("Hybrid execution requires context.qkd_protocol.")
    if context.pqc_initiator is None or context.pqc_responder is None:
        raise ValueError("Hybrid execution requires pre-provisioned PQC parties.")
    if config.qkd_signal_count is None:
        raise ValueError("Hybrid execution requires a positive qkd_signal_count.")
    if config.qkd_authentication_profile is None:
        raise ValueError("Hybrid execution requires an explicit qkd_authentication_profile.")
    validate_qkd_authentication_context(
        config.qkd_authentication_profile,
        context.qkd_authentication,
        transport_hook=context.qkd_transport_hook,
    )

    trace = SessionTraceBuilder()
    trace.append(SessionTraceSource.SESSION, "session", "started", config.profile.value)
    wall_start = perf_counter_ns()
    exchange = execute_authenticated_pqc_exchange(
        context,
        definition.internal_pqc_profile,
        trace,
    )
    if not isinstance(exchange, PQCExchangeArtifacts):
        trace.append(SessionTraceSource.SESSION, "session", "aborted", exchange.reason)
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.session_id,
            config.profile,
            SessionStatus.ABORTED,
            exchange.reason,
            (),
            SessionAuthentication(pqc_exchange=_pqc_outcome(False)),
            trace.freeze(),
            SessionMetrics(orchestration_software_wall_time_ns=perf_counter_ns() - wall_start),
        )

    alice_keys = bob_keys = None
    alice_capability = bob_capability = None
    qkd_result = None
    pqc_auth_metrics = None
    pqc_metrics = None
    qkd_metrics = None
    qkd_auth = None
    hybrid_metrics = None
    public_context = None
    try:
        qkd_start = perf_counter_ns()
        qkd_result = run_qkd_profile(
            context.qkd_protocol,
            config.qkd_signal_count,
            config.qkd_authentication_profile,
            config=config.qkd_postprocessing,
            authentication_context=context.qkd_authentication,
            session_id=exchange.transcript.session_id,
            transport_hook=context.qkd_transport_hook,
        )
        qkd_elapsed = perf_counter_ns() - qkd_start
        for event in qkd_result.trace:
            trace.append(SessionTraceSource.QKD, event.stage, event.state, event.detail)
        if qkd_result.session_id != exchange.transcript.session_id:
            raise ValueError("QKD and PQC contribution session identifiers do not match.")
        qkd_auth = _qkd_outcome(qkd_result)
        transcript_bytes = qkd_result.transcript.canonical_bytes()
        qkd_metrics = QKDSessionMetrics(
            simulation_time_ns=max(0, qkd_elapsed - qkd_result.authentication.metrics.total_time_ns),
            n_raw=qkd_result.qkd.n_raw,
            n_sifted=qkd_result.qkd.n_sifted,
            n_disclosed=qkd_result.qkd.n_disclosed,
            n_candidate=qkd_result.qkd.n_candidate,
            n_reconciled=qkd_result.qkd.n_reconciled,
            n_final=qkd_result.qkd.n_final,
            sifting_efficiency=qkd_result.qkd.sifting_efficiency,
            final_secret_fraction=qkd_result.qkd.final_secret_fraction,
            estimated_qber_z=qkd_result.qkd.estimated_qber_z,
            estimated_qber_x=qkd_result.qkd.estimated_qber_x,
            estimated_qber_aggregated=qkd_result.qkd.estimated_qber_aggregated,
            phase_error_bound=qkd_result.qkd.phase_error_bound,
            diagnostic_full_sifted_qber=qkd_result.qkd.diagnostic_full_sifted_qber,
            diagnostic_qber_z=qkd_result.qkd.diagnostic_qber_z,
            diagnostic_qber_x=qkd_result.qkd.diagnostic_qber_x,
            diagnostic_qber_aggregated=qkd_result.qkd.diagnostic_qber_aggregated,
            transcript_bytes=len(transcript_bytes),
        )
        pqc_metrics, pqc_auth_metrics = _pqc_metrics(
            exchange,
            key_schedule_time_ns=0,
            confirmation_time_ns=0,
            public_key_provisioning_bytes=(
                len(context.pqc_initiator.public_identity.public_key)
                + len(context.pqc_responder.public_identity.public_key)
            ),
            finished_bytes=0,
        )
        if qkd_result.status is QKDOrchestrationStatus.ABORTED:
            reason = qkd_result.abort_reason or "QKD contribution was not accepted."
            trace.append(SessionTraceSource.SESSION, "session", "aborted", reason)
            return SessionResult(
                SESSION_RESULT_VERSION,
                exchange.transcript.session_id,
                config.profile,
                SessionStatus.ABORTED,
                reason,
                (),
                SessionAuthentication(qkd_auth, _pqc_outcome(True)),
                trace.freeze(),
                SessionMetrics(
                    qkd=qkd_metrics,
                    pqc=pqc_metrics,
                    qkd_authentication=qkd_result.authentication.metrics,
                    pqc_authentication=pqc_auth_metrics,
                    orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
                ),
            )

        alice_bits, bob_bits = qkd_result.release_final_keys()
        qkd_bit_length = int(alice_bits.size)
        alice_qkd = np.packbits(alice_bits, bitorder="big").tobytes()
        bob_qkd = np.packbits(bob_bits, bitorder="big").tobytes()
        if context.hybrid_qkd_contribution_hook is not None:
            alice_qkd = context.hybrid_qkd_contribution_hook("initiator", alice_qkd, qkd_bit_length)
            bob_qkd = context.hybrid_qkd_contribution_hook("responder", bob_qkd, qkd_bit_length)
        alice_capability = issue_initiator_hybrid_contributions(
            processed_server_offer=exchange.processed_server_offer,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
        )
        bob_capability = issue_responder_hybrid_contributions(
            processed_client_exchange=exchange.processed_client_exchange,
            signed_server_offer=exchange.signed_server_offer,
            signed_client_exchange=exchange.signed_client_exchange,
        )
        alice_kems = alice_capability.consume()
        bob_kems = bob_capability.consume()
        if context.hybrid_contribution_hook is not None:
            alice_kems = context.hybrid_contribution_hook("initiator", alice_kems)
            bob_kems = context.hybrid_contribution_hook("responder", bob_kems)

        def components(qkd: bytes, kems: tuple[tuple[str, bytes], ...]) -> tuple[HybridSecretComponent, ...]:
            values = [
                HybridSecretComponent(
                    1,
                    "K_QKD",
                    "qkd",
                    QKD_COMPONENT_ALGORITHM,
                    "packed-bits-big-endian",
                    qkd_bit_length,
                    qkd,
                )
            ]
            values.extend(
                HybridSecretComponent(
                    index,
                    hybrid_kem_label(algorithm),
                    "pqc",
                    algorithm,
                    "raw-bytes",
                    len(secret) * 8,
                    secret,
                )
                for index, (algorithm, secret) in enumerate(kems, 2)
            )
            return tuple(values)

        alice_components = components(alice_qkd, alice_kems)
        bob_components = components(bob_qkd, bob_kems)
        encode_start = perf_counter_ns()
        alice_input = canonical_hybrid_secret_input(profile=config.profile, components=alice_components)
        bob_input = canonical_hybrid_secret_input(profile=config.profile, components=bob_components)
        encoding_time = perf_counter_ns() - encode_start
        public_context = HybridPublicContext(
            exchange.transcript.session_id,
            config.profile,
            config.qkd_authentication_profile,
            qkd_result.transcript.version,
            sha384(transcript_bytes).digest(),
            exchange.transcript.protocol_version,
            exchange.transcript.profile,
            exchange.transcript.transcript_hash,
            definition.establishment_algorithms,
        )
        trace.append(
            SessionTraceSource.HYBRID, "combiner_input", "encoded", "Canonical ordered contributions encoded."
        )

        start = perf_counter_ns()
        alice_session_key = derive_hybrid_session_key(alice_input, public_context)
        bob_session_key = derive_hybrid_session_key(bob_input, public_context)
        hkdf_session_time = perf_counter_ns() - start
        start = perf_counter_ns()
        alice_confirmation_key = derive_hybrid_confirmation_key(alice_input, public_context)
        bob_confirmation_key = derive_hybrid_confirmation_key(bob_input, public_context)
        hkdf_confirmation_time = perf_counter_ns() - start
        alice_keys = HybridDerivedKeys(public_context.context_hash, alice_session_key, alice_confirmation_key)
        bob_keys = HybridDerivedKeys(public_context.context_hash, bob_session_key, bob_confirmation_key)

        raw_bytes = sum(len(component.secret) for component in alice_components)
        ml_bytes = len(alice_components[1].secret)
        hqc_bytes = len(alice_components[2].secret) if len(alice_components) == 3 else None
        hybrid_metrics = HybridSessionMetrics(
            component_count=len(alice_components),
            component_metadata_bytes=tuple(
                hybrid_component_metadata_bytes(component) for component in alice_components
            ),
            qkd_contribution_bits=qkd_bit_length,
            ml_kem_contribution_bytes=ml_bytes,
            hqc_contribution_bytes=hqc_bytes,
            canonical_combiner_input_bytes=len(alice_input),
            encoding_overhead_bytes=len(alice_input) - raw_bytes,
            public_context_bytes=len(public_context.canonical_bytes()),
            encoding_time_ns=encoding_time,
            hkdf_session_time_ns=hkdf_session_time,
            hkdf_confirmation_time_ns=hkdf_confirmation_time,
            finished_generation_time_ns=0,
            finished_verification_time_ns=0,
            finished_responder_bytes=0,
            finished_initiator_bytes=0,
            derived_session_key_bits=256,
        )

        generation_start = perf_counter_ns()
        responder_finished = create_finished(
            bob_keys.confirmation_key(), public_context, HybridFinishedRole.RESPONDER
        )
        generation_time = perf_counter_ns() - generation_start
        hybrid_metrics = replace(
            hybrid_metrics,
            finished_generation_time_ns=generation_time,
            finished_responder_bytes=len(responder_finished.canonical_bytes()),
        )
        if context.hybrid_finished_transport_hook is not None:
            transported = context.hybrid_finished_transport_hook(responder_finished)
            if not isinstance(transported, HybridFinishedMessage):
                raise TypeError("Hybrid Finished hook must return HybridFinishedMessage.")
            responder_finished = transported
        verification_start = perf_counter_ns()
        responder_verified = verify_finished(
            alice_keys.confirmation_key(),
            public_context,
            responder_finished,
            HybridFinishedRole.RESPONDER,
        )
        verification_time = perf_counter_ns() - verification_start
        hybrid_metrics = replace(
            hybrid_metrics,
            finished_verification_time_ns=verification_time,
        )
        if not responder_verified:
            raise ValueError("Responder hybrid Finished verification failed.")
        trace.append(
            SessionTraceSource.HYBRID,
            "finished_b",
            "verified",
            "Alice verified Bob's hybrid Finished.",
        )

        generation_start = perf_counter_ns()
        initiator_finished = create_finished(
            alice_keys.confirmation_key(),
            public_context,
            HybridFinishedRole.INITIATOR,
            previous=responder_finished.verify_data,
        )
        generation_time += perf_counter_ns() - generation_start
        hybrid_metrics = replace(
            hybrid_metrics,
            finished_generation_time_ns=generation_time,
            finished_initiator_bytes=len(initiator_finished.canonical_bytes()),
        )
        if context.hybrid_finished_transport_hook is not None:
            transported = context.hybrid_finished_transport_hook(initiator_finished)
            if not isinstance(transported, HybridFinishedMessage):
                raise TypeError("Hybrid Finished hook must return HybridFinishedMessage.")
            initiator_finished = transported
        verification_start = perf_counter_ns()
        initiator_verified = verify_finished(
            bob_keys.confirmation_key(),
            public_context,
            initiator_finished,
            HybridFinishedRole.INITIATOR,
            previous=responder_finished.verify_data,
        )
        verification_time += perf_counter_ns() - verification_start
        hybrid_metrics = replace(
            hybrid_metrics,
            finished_verification_time_ns=verification_time,
        )
        if not initiator_verified:
            raise ValueError("Initiator hybrid Finished verification failed.")
        alice_keys.retire_confirmation_key()
        bob_keys.retire_confirmation_key()
        trace.append(
            SessionTraceSource.HYBRID,
            "finished_a",
            "verified",
            "Bob verified Alice's chained hybrid Finished.",
        )

        key = alice_keys.session_key()
        trace.append(
            SessionTraceSource.SESSION,
            "session",
            "established",
            "Mutually confirmed hybrid session key released.",
        )
        provenance = tuple(
            SecretProvenance(
                component.position,
                component.source,
                "BB84" if component.source == "qkd" else "authenticated KEM handshake",
                component.algorithm,
                component.encoding,
                component.bit_length,
                len(component.secret),
            )
            for component in alice_components
        )
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.ESTABLISHED,
            None,
            provenance,
            SessionAuthentication(qkd_auth, _pqc_outcome(True)),
            trace.freeze(),
            SessionMetrics(
                qkd=qkd_metrics,
                pqc=pqc_metrics,
                qkd_authentication=qkd_result.authentication.metrics,
                pqc_authentication=pqc_auth_metrics,
                hybrid=hybrid_metrics,
                orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
            ),
            _hybrid_public_context_entries(public_context),
            EstablishedKeyCapability(key, bit_length=256, key_type=EstablishedKeyType.SESSION_KEY),
        )
    except ValueError as exc:
        reason = str(exc)
        trace.append(SessionTraceSource.HYBRID, "confirmation", "failed", reason)
        trace.append(SessionTraceSource.SESSION, "session", "aborted", reason)
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.ABORTED,
            reason,
            (),
            SessionAuthentication(qkd_auth, _pqc_outcome(True)),
            trace.freeze(),
            SessionMetrics(
                qkd=qkd_metrics,
                pqc=pqc_metrics,
                qkd_authentication=(qkd_result.authentication.metrics if qkd_result else None),
                pqc_authentication=pqc_auth_metrics,
                hybrid=hybrid_metrics,
                orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
            ),
            _hybrid_public_context_entries(public_context),
        )
    except (PQCError, RuntimeError, TypeError) as exc:
        reason = f"Operational execution failure: {exc}"
        trace.append(SessionTraceSource.HYBRID, "execution", "failed", reason)
        trace.append(SessionTraceSource.SESSION, "session", "failed", reason)
        return SessionResult(
            SESSION_RESULT_VERSION,
            exchange.transcript.session_id,
            config.profile,
            SessionStatus.FAILED,
            reason,
            (),
            SessionAuthentication(qkd_auth, _pqc_outcome(True)),
            trace.freeze(),
            SessionMetrics(
                qkd=qkd_metrics,
                pqc=pqc_metrics,
                qkd_authentication=(qkd_result.authentication.metrics if qkd_result else None),
                pqc_authentication=pqc_auth_metrics,
                hybrid=hybrid_metrics,
                orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
            ),
            _hybrid_public_context_entries(public_context),
        )
    finally:
        if alice_keys is not None:
            alice_keys.close()
        if bob_keys is not None:
            bob_keys.close()
        if alice_capability is not None:
            alice_capability.close()
        if bob_capability is not None:
            bob_capability.close()
        exchange.close()
