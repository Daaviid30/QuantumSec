"""Runtime-only accumulation of exact PQC operation timings."""

from __future__ import annotations

from dataclasses import dataclass

from pqc.protocol.instrumentation import PQCOperation


@dataclass(frozen=True, slots=True)
class PQCOperationTimings:
    ml_kem_keygen_time_ns: int
    hqc_keygen_time_ns: int | None
    server_offer_sign_time_ns: int
    server_offer_verify_time_ns: int
    ml_kem_encapsulate_time_ns: int
    hqc_encapsulate_time_ns: int | None
    client_exchange_sign_time_ns: int
    client_exchange_verify_time_ns: int
    ml_kem_decapsulate_time_ns: int
    hqc_decapsulate_time_ns: int | None
    transcript_construction_hash_time_ns: int
    kem_combiner_encoding_time_ns: int
    hkdf_session_time_ns: int
    hkdf_confirmation_time_ns: int
    finished_generation_time_ns: int
    finished_verification_time_ns: int


class PQCOperationTimer:
    """Accumulate successful direct timings without observing secret values."""

    __slots__ = ("_hqc_enabled", "_values")

    def __init__(self, *, hqc_enabled: bool) -> None:
        if not isinstance(hqc_enabled, bool):
            raise TypeError("hqc_enabled must be a bool.")
        self._hqc_enabled = hqc_enabled
        self._values = {operation: 0 for operation in PQCOperation}

    def observe(self, operation: PQCOperation, elapsed_ns: int) -> None:
        if not isinstance(operation, PQCOperation):
            raise TypeError("operation must be a PQCOperation.")
        if isinstance(elapsed_ns, bool) or not isinstance(elapsed_ns, int) or elapsed_ns < 0:
            raise ValueError("elapsed_ns must be a non-negative integer.")
        self._values[operation] += elapsed_ns

    def snapshot(self) -> PQCOperationTimings:
        value = self._values

        def optional(operation: PQCOperation) -> int | None:
            return value[operation] if self._hqc_enabled else None

        return PQCOperationTimings(
            ml_kem_keygen_time_ns=value[PQCOperation.ML_KEM_KEYGEN],
            hqc_keygen_time_ns=optional(PQCOperation.HQC_KEYGEN),
            server_offer_sign_time_ns=value[PQCOperation.SERVER_OFFER_SIGN],
            server_offer_verify_time_ns=value[PQCOperation.SERVER_OFFER_VERIFY],
            ml_kem_encapsulate_time_ns=value[PQCOperation.ML_KEM_ENCAPSULATE],
            hqc_encapsulate_time_ns=optional(PQCOperation.HQC_ENCAPSULATE),
            client_exchange_sign_time_ns=value[PQCOperation.CLIENT_EXCHANGE_SIGN],
            client_exchange_verify_time_ns=value[PQCOperation.CLIENT_EXCHANGE_VERIFY],
            ml_kem_decapsulate_time_ns=value[PQCOperation.ML_KEM_DECAPSULATE],
            hqc_decapsulate_time_ns=optional(PQCOperation.HQC_DECAPSULATE),
            transcript_construction_hash_time_ns=value[PQCOperation.TRANSCRIPT_CONSTRUCTION_HASH],
            kem_combiner_encoding_time_ns=value[PQCOperation.KEM_COMBINER_ENCODING],
            hkdf_session_time_ns=value[PQCOperation.HKDF_SESSION],
            hkdf_confirmation_time_ns=value[PQCOperation.HKDF_CONFIRMATION],
            finished_generation_time_ns=value[PQCOperation.FINISHED_GENERATION],
            finished_verification_time_ns=value[PQCOperation.FINISHED_VERIFICATION],
        )
