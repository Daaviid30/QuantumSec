"""Secret-free executable D1 protected-session demonstration."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Final

from cryptography.exceptions import InvalidTag

from data_protection import DataPlaneDirection
from experiments.config import ExperimentConfig, ExperimentKind
from experiments.environment import ExperimentEnvironment
from experiments.runtime import ExperimentRuntimeFactory
from orchestration.data_plane import open_data_plane
from orchestration.result import SessionStatus
from orchestration.runner import run_session

D1_RECORD_VERSION: Final = 1
_PLAINTEXT = b"QuantumSec thesis D1 authenticated payload"
_AAD = b"QuantumSec/D1/v1"


@dataclass(frozen=True, slots=True)
class TamperOutcome:
    scenario: str
    rejected: bool
    exception: str | None

    def to_public_dict(self) -> dict[str, object]:
        return {"scenario": self.scenario, "rejected": self.rejected, "exception": self.exception}


@dataclass(frozen=True, slots=True)
class D1Record:
    timestamp_utc: str
    environment: dict[str, object]
    config: dict[str, object]
    provisioning: dict[str, object]
    session: dict[str, object]
    algorithm: str
    key_bits: int
    plaintext_bytes: int
    ciphertext_bytes: int
    nonce_bytes: int
    tag_bytes: int
    application_aad_bytes: int
    round_trip_verified: bool
    tamper_matrix: tuple[TamperOutcome, ...]
    version: int = D1_RECORD_VERSION

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "timestamp_utc": self.timestamp_utc,
            "environment": self.environment,
            "config": self.config,
            "provisioning": self.provisioning,
            "session": self.session,
            "algorithm": self.algorithm,
            "key_bits": self.key_bits,
            "sizes": {
                "plaintext_bytes": self.plaintext_bytes,
                "ciphertext_bytes": self.ciphertext_bytes,
                "nonce_bytes": self.nonce_bytes,
                "tag_bytes": self.tag_bytes,
                "application_aad_bytes": self.application_aad_bytes,
            },
            "round_trip_verified": self.round_trip_verified,
            "tamper_matrix": tuple(item.to_public_dict() for item in self.tamper_matrix),
        }


def run_d1(config: ExperimentConfig, runtime_factory: ExperimentRuntimeFactory) -> D1Record:
    """Establish HYBRID-DIVERSE, transfer its key, and test AES-GCM rejection."""

    if (
        not isinstance(config, ExperimentConfig)
        or config.experiment_kind is not ExperimentKind.D1_PROTECTED_SESSION
    ):
        raise ValueError("D1 requires an ExperimentKind.D1_PROTECTED_SESSION configuration.")
    if not isinstance(runtime_factory, ExperimentRuntimeFactory):
        raise TypeError("runtime_factory must be an ExperimentRuntimeFactory.")
    environment = ExperimentEnvironment.capture()
    runtime = runtime_factory.build(config)
    session = run_session(config.session_config, runtime.context)
    session_public = session.to_public_dict()
    session_public.pop("trace", None)
    session_public.pop("metrics", None)
    if session.status is not SessionStatus.ESTABLISHED:
        session.close()
        raise RuntimeError(f"D1 session did not establish: {session.abort_reason}")

    protected = open_data_plane(session)
    try:
        record = protected.encrypt(_PLAINTEXT, direction=DataPlaneDirection.ALICE_TO_BOB, aad=_AAD)
        round_trip = protected.decrypt(record, aad=_AAD) == _PLAINTEXT
        tampered_ciphertext = replace(record, ciphertext=_flip_first(record.ciphertext))
        tampered_tag = replace(record, tag=_flip_first(record.tag))
        outcomes = (
            _expect_invalid_tag(protected, tampered_ciphertext, _AAD, "ciphertext_bit_flip"),
            _expect_invalid_tag(protected, tampered_tag, _AAD, "tag_bit_flip"),
            _expect_invalid_tag(protected, record, _AAD + b"!", "aad_change"),
        )
        return D1Record(
            timestamp_utc=datetime.now(UTC).isoformat(),
            environment=environment.to_public_dict(),
            config=config.to_public_dict(),
            provisioning=runtime.provisioning.to_public_dict(),
            session=session_public,
            algorithm=record.algorithm,
            key_bits=256,
            plaintext_bytes=len(_PLAINTEXT),
            ciphertext_bytes=len(record.ciphertext),
            nonce_bytes=len(record.nonce),
            tag_bytes=len(record.tag),
            application_aad_bytes=record.application_aad_bytes,
            round_trip_verified=round_trip,
            tamper_matrix=outcomes,
        )
    finally:
        protected.close()


def _flip_first(value: bytes) -> bytes:
    if not value:
        raise ValueError("Cannot tamper with an empty value.")
    return bytes((value[0] ^ 1,)) + value[1:]


def _expect_invalid_tag(protected: object, record: object, aad: bytes, scenario: str) -> TamperOutcome:
    from data_protection import ProtectedRecord, ProtectedSession

    if not isinstance(protected, ProtectedSession) or not isinstance(record, ProtectedRecord):
        raise TypeError("D1 tamper helpers require protected-session values.")
    try:
        protected.decrypt(record, aad=aad)
    except InvalidTag:
        return TamperOutcome(scenario, True, "InvalidTag")
    return TamperOutcome(scenario, False, None)
