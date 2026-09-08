"""Optional timing observer for exact PQC protocol operations."""

from collections.abc import Callable
from enum import StrEnum


class PQCOperation(StrEnum):
    """Stable names for directly surrounded protocol operations."""

    ML_KEM_KEYGEN = "ml_kem_keygen_time_ns"
    HQC_KEYGEN = "hqc_keygen_time_ns"
    SERVER_OFFER_SIGN = "server_offer_sign_time_ns"
    SERVER_OFFER_VERIFY = "server_offer_verify_time_ns"
    ML_KEM_ENCAPSULATE = "ml_kem_encapsulate_time_ns"
    HQC_ENCAPSULATE = "hqc_encapsulate_time_ns"
    CLIENT_EXCHANGE_SIGN = "client_exchange_sign_time_ns"
    CLIENT_EXCHANGE_VERIFY = "client_exchange_verify_time_ns"
    ML_KEM_DECAPSULATE = "ml_kem_decapsulate_time_ns"
    HQC_DECAPSULATE = "hqc_decapsulate_time_ns"
    TRANSCRIPT_CONSTRUCTION_HASH = "transcript_construction_hash_time_ns"
    KEM_COMBINER_ENCODING = "kem_combiner_encoding_time_ns"
    HKDF_SESSION = "hkdf_session_time_ns"
    HKDF_CONFIRMATION = "hkdf_confirmation_time_ns"
    FINISHED_GENERATION = "finished_generation_time_ns"
    FINISHED_VERIFICATION = "finished_verification_time_ns"


type PQCOperationObserver = Callable[[PQCOperation, int], None]


def validate_operation_observer(observer: PQCOperationObserver | None) -> None:
    if observer is not None and not callable(observer):
        raise TypeError("operation_observer must be callable or None.")
