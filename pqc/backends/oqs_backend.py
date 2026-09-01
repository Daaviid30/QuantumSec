"""Adapter isolating the liboqs-python signature API."""

from dataclasses import dataclass, field
from functools import cache, lru_cache
from importlib import import_module
from types import ModuleType, TracebackType
from typing import Protocol, Self, cast

from pqc.errors import BackendOperationError, BackendUnavailableError, UnsupportedAlgorithmError


class _OQSSignature(Protocol):
    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def generate_keypair(self) -> bytes: ...

    def export_secret_key(self) -> bytes: ...

    def sign(self, message: bytes) -> bytes: ...

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool: ...


class _SignatureFactory(Protocol):
    def __call__(self, alg_name: str, secret_key: bytes | None = None) -> _OQSSignature: ...


class _OQSModule(Protocol):
    Signature: _SignatureFactory
    MechanismNotEnabledError: type[Exception]
    MechanismNotSupportedError: type[Exception]

    def is_sig_enabled(self, alg_name: str) -> int: ...


@dataclass(frozen=True, slots=True)
class OQSKeyPair:
    """Private transfer object used only across the OQS adapter boundary."""

    public_key: bytes = field(repr=False)
    secret_key: bytes = field(repr=False)


@lru_cache(maxsize=1)
def _load_oqs() -> _OQSModule:
    try:
        module: ModuleType = import_module("oqs")
    except (ImportError, OSError, RuntimeError) as exc:
        raise BackendUnavailableError("The liboqs-python backend could not be loaded.") from exc
    return cast(_OQSModule, module)


@cache
def _ensure_signature_algorithm_enabled(algorithm: str) -> None:
    module = _load_oqs()
    try:
        algorithm_enabled = bool(module.is_sig_enabled(algorithm))
    except Exception as exc:
        raise BackendUnavailableError("The liboqs backend could not query enabled algorithms.") from exc
    if not algorithm_enabled:
        raise UnsupportedAlgorithmError(f"Signature algorithm {algorithm!r} is not enabled by liboqs.")


def _new_signature(algorithm: str, *, secret_key: bytes | None = None) -> _OQSSignature:
    module = _load_oqs()
    _ensure_signature_algorithm_enabled(algorithm)
    try:
        return module.Signature(algorithm, secret_key=secret_key)
    except (module.MechanismNotEnabledError, module.MechanismNotSupportedError) as exc:
        raise UnsupportedAlgorithmError(f"Signature algorithm {algorithm!r} is unavailable.") from exc
    except Exception as exc:
        raise BackendUnavailableError(f"The liboqs backend could not initialize {algorithm!r}.") from exc


class OQSSignatureBackend:
    """Execute signature operations through liboqs without leaking its lifecycle."""

    def generate_keypair(self, algorithm: str) -> OQSKeyPair:
        signer = _new_signature(algorithm)
        try:
            with signer:
                public_key = bytes(signer.generate_keypair())
                secret_key = bytes(signer.export_secret_key())
        except Exception as exc:
            raise BackendOperationError(f"liboqs key generation failed for {algorithm!r}.") from exc
        return OQSKeyPair(public_key=public_key, secret_key=secret_key)

    def sign(self, algorithm: str, message: bytes, secret_key: bytes) -> bytes:
        signer = _new_signature(algorithm, secret_key=secret_key)
        try:
            with signer:
                return bytes(signer.sign(message))
        except Exception as exc:
            raise BackendOperationError(f"liboqs signing failed for {algorithm!r}.") from exc

    def verify(self, algorithm: str, message: bytes, signature: bytes, public_key: bytes) -> bool:
        verifier = _new_signature(algorithm)
        try:
            with verifier:
                return bool(verifier.verify(message, signature, public_key))
        except Exception as exc:
            raise BackendOperationError(f"liboqs verification failed for {algorithm!r}.") from exc
