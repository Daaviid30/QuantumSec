"""Web-facing laboratory service over orchestration and experiment contracts."""

from __future__ import annotations

import base64
from collections import OrderedDict
from dataclasses import replace
from threading import RLock

from cryptography.exceptions import InvalidTag

from data_protection import DataPlaneDirection, ProtectedSession
from experiments import (
    ExperimentConfig,
    ExperimentEnvironment,
    ExperimentKind,
    ExperimentRecord,
    ExperimentRuntimeFactory,
)
from orchestration import (
    EstablishedKeyType,
    QKDProfile,
    SessionConfig,
    SessionProfile,
    SessionStatus,
    open_data_plane,
    run_session,
)
from qkd.channel import ChannelPipeline, InterceptResendAttack, QKDChannelStageSpec
from qkd.postprocessing import CascadeConfig
from qkd.protocols import BB84PostprocessingConfig
from ui.backend.schemas import (
    AttackDiagnosticsSummary,
    CompareResponse,
    ComparisonCompatibility,
    ProtectedMessageRequest,
    ProtectedMessageResponse,
    RunListResponse,
    RunRecord,
    SessionRunRequest,
    SessionRunResponse,
)

_MAX_RETAINED_RUNS = 100
_PQC_ONLY_PROFILES = frozenset({SessionProfile.PQC_BASE, SessionProfile.PQC_DIVERSE})


class WebLaboratoryService:
    """Execute sessions and retain bounded, process-local public run evidence.

    Live data-plane capabilities are indexed only by opaque public run IDs. Key material remains
    inside ``ProtectedSession`` and is closed when a run is evicted.
    """

    def __init__(self, *, max_retained_runs: int = _MAX_RETAINED_RUNS) -> None:
        if max_retained_runs <= 0:
            raise ValueError("max_retained_runs must be positive.")
        self._max_retained_runs = max_retained_runs
        self._runtime_factory = ExperimentRuntimeFactory()
        self._runs: OrderedDict[str, SessionRunResponse] = OrderedDict()
        self._data_planes: dict[str, ProtectedSession] = {}
        self._lock = RLock()

    def run(self, request: SessionRunRequest) -> SessionRunResponse:
        """Run one normalized profile and retain its secret-free record."""

        if not isinstance(request, SessionRunRequest):
            raise TypeError("request must be a SessionRunRequest.")
        config = _experiment_config(request)
        with self._lock:
            environment = ExperimentEnvironment.capture()
            runtime = self._runtime_factory.build(config)
            result = run_session(config.session_config, runtime.context)
            data_plane: ProtectedSession | None = None
            try:
                record = ExperimentRecord.from_session_result(
                    config=config,
                    environment=environment,
                    provisioning=runtime.provisioning,
                    session_result=result,
                )
                diagnostics = _attack_diagnostics(runtime.context.qkd_protocol)
                if (
                    result.status is SessionStatus.ESTABLISHED
                    and result.established_key_type is EstablishedKeyType.SESSION_KEY
                ):
                    data_plane = open_data_plane(result)
                else:
                    result.close()
                response = SessionRunResponse(
                    record=RunRecord.model_validate(record.to_public_dict()),
                    attack_diagnostics=diagnostics,
                    data_plane_available=data_plane is not None,
                )
                self._retain(response, data_plane)
                return response
            except Exception:
                if data_plane is not None:
                    data_plane.close()
                result.close()
                raise

    def list_runs(self) -> RunListResponse:
        """Return newest-first public records."""

        with self._lock:
            return RunListResponse(runs=list(reversed(self._runs.values())))

    def get_run(self, run_id: str) -> SessionRunResponse:
        with self._lock:
            try:
                return self._runs[run_id]
            except KeyError as error:
                raise KeyError(f"Unknown run ID: {run_id}") from error

    def compare(self, left_id: str, right_id: str) -> CompareResponse:
        """Return two records with conservative metric-compatibility facts."""

        if left_id == right_id:
            raise ValueError("Comparison requires two distinct run IDs.")
        with self._lock:
            left = self.get_run(left_id)
            right = self.get_run(right_id)
            left_profile = SessionProfile(left.record.profile)
            right_profile = SessionProfile(right.record.profile)
            same_environment = _same_measurement_environment(left.record, right.record)
            qkd_metrics = (
                left.record.metrics.get("qkd") is not None and right.record.metrics.get("qkd") is not None
            )
            pqc_timing = (
                left_profile in _PQC_ONLY_PROFILES
                and right_profile in _PQC_ONLY_PROFILES
                and same_environment
            )
            notes = [
                "QKD simulator runtime is software provenance, never physical QKD latency or throughput.",
                "QKD and PQC timings are not ranked or placed on a common performance axis.",
            ]
            if qkd_metrics:
                notes.append("Both records expose compatible BB84 material and per-basis QBER metrics.")
            if pqc_timing:
                notes.append("Both records are PQC-only runs from the same reported software environment.")
            return CompareResponse(
                left=left,
                right=right,
                compatibility=ComparisonCompatibility(
                    qkd_metrics=qkd_metrics,
                    pqc_timing=pqc_timing,
                    same_environment=same_environment,
                    notes=notes,
                ),
            )

    def protect(self, run_id: str, request: ProtectedMessageRequest) -> ProtectedMessageResponse:
        """Protect and verify one payload without exporting the established session key."""

        with self._lock:
            self.get_run(run_id)
            try:
                protected = self._data_planes[run_id]
            except KeyError as error:
                raise ValueError("This run has no live 256-bit data-plane capability.") from error
            plaintext = request.plaintext.encode("utf-8")
            aad = request.aad.encode("utf-8")
            record = protected.encrypt(
                plaintext,
                direction=DataPlaneDirection.ALICE_TO_BOB,
                aad=aad,
            )
            round_trip_verified = protected.decrypt(record, aad=aad) == plaintext
            tampered = replace(
                record,
                ciphertext=bytes((record.ciphertext[0] ^ 1,)) + record.ciphertext[1:],
            )
            try:
                protected.decrypt(tampered, aad=aad)
            except InvalidTag:
                tamper_rejected = True
            else:
                tamper_rejected = False
            preview = base64.b64encode(record.ciphertext[:18]).decode("ascii")
            return ProtectedMessageResponse(
                algorithm="AES-256-GCM",
                plaintext_bytes=len(plaintext),
                ciphertext_bytes=len(record.ciphertext),
                nonce_bytes=len(record.nonce),
                tag_bytes=len(record.tag),
                application_aad_bytes=record.application_aad_bytes,
                round_trip_verified=round_trip_verified,
                tamper_rejected=tamper_rejected,
                ciphertext_preview=f"{preview}...",
            )

    def _retain(
        self,
        response: SessionRunResponse,
        data_plane: ProtectedSession | None,
    ) -> None:
        run_id = response.record.run_id
        self._runs[run_id] = response
        if data_plane is not None:
            self._data_planes[run_id] = data_plane
        while len(self._runs) > self._max_retained_runs:
            evicted_id, _response = self._runs.popitem(last=False)
            evicted_plane = self._data_planes.pop(evicted_id, None)
            if evicted_plane is not None:
                evicted_plane.close()


def _experiment_config(request: SessionRunRequest) -> ExperimentConfig:
    profile = SessionProfile(request.profile)
    uses_qkd = profile.name.startswith("QKD_") or profile.name.startswith("HYBRID")
    is_hybrid = profile.name.startswith("HYBRID")
    if is_hybrid:
        kind = ExperimentKind.E5_HYBRID_OVERHEAD
    elif uses_qkd:
        kind = ExperimentKind.E4_QKD_AUTHENTICATION
    else:
        kind = ExperimentKind.E1_PQC_COST

    postprocessing = request.postprocessing
    qkd_config = (
        BB84PostprocessingConfig(
            sample_fraction=postprocessing.sample_fraction,
            phase_error_abort_threshold=postprocessing.phase_error_abort_threshold,
            cascade=CascadeConfig(
                passes=postprocessing.cascade_passes,
                initial_block_factor=postprocessing.cascade_initial_block_factor,
            ),
            verification_tag_length=postprocessing.verification_tag_length,
            security_margin_bits=postprocessing.security_margin_bits,
        )
        if uses_qkd
        else None
    )
    session = SessionConfig(
        profile=profile,
        qkd_authentication_profile=(
            QKDProfile(request.qkd_authentication_profile)
            if request.qkd_authentication_profile is not None
            else None
        ),
        qkd_signal_count=request.n_signals if uses_qkd else None,
        qkd_postprocessing=qkd_config,
    )
    stages = tuple(
        QKDChannelStageSpec.from_public_dict(configuration.model_dump()) for configuration in request.channels
    )
    return ExperimentConfig(
        experiment_kind=kind,
        condition_id=f"web-{profile.value}",
        replicate_index=0,
        session_config=session,
        seed=request.seed if uses_qkd else None,
        qkd_stages=stages,
        tags=("web-ui",),
    )


def _attack_diagnostics(protocol: object) -> list[AttackDiagnosticsSummary]:
    channel = getattr(protocol, "channel", None)
    if not isinstance(channel, ChannelPipeline):
        return []
    summaries: list[AttackDiagnosticsSummary] = []
    for stage_index, stage in enumerate(channel.channels):
        if not isinstance(stage, InterceptResendAttack):
            continue
        diagnostics = stage.diagnostics
        summaries.append(
            AttackDiagnosticsSummary(
                stage_index=stage_index,
                attack_type=diagnostics.attack_type,
                intercept_fraction=diagnostics.intercept_fraction,
                n_signals_seen=diagnostics.n_signals_seen,
                n_intercepted=diagnostics.n_intercepted,
                eve_z_measurements=diagnostics.eve_z_measurements,
                eve_x_measurements=diagnostics.eve_x_measurements,
                eve_zero_outcomes=diagnostics.eve_zero_outcomes,
                eve_one_outcomes=diagnostics.eve_one_outcomes,
            )
        )
    return summaries


def _same_measurement_environment(left: RunRecord, right: RunRecord) -> bool:
    fields = ("cpu_identifier", "os", "python_version", "liboqs_version", "liboqs_python_version")
    return all(left.environment.get(field) == right.environment.get(field) for field in fields)
