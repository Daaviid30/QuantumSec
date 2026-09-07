"""Purpose-separated HKDF-SHA-384 schedule for hybrid sessions."""

from dataclasses import dataclass, field
from typing import Final

from orchestration._encoding import length_prefixed
from orchestration.hybrid.context import HybridPublicContext
from pqc.kdf.hkdf import derive_hkdf_sha384

HYBRID_SESSION_KEY_DOMAIN: Final = b"QuantumSec/HybridSession/v1/SessionKey"
HYBRID_CONFIRMATION_KEY_DOMAIN: Final = b"QuantumSec/HybridSession/v1/ConfirmationKey"
HYBRID_KEY_LENGTH: Final = 32


@dataclass(slots=True, repr=False)
class HybridDerivedKeys:
    context_hash: bytes
    _session_key: bytes | None = field(repr=False)
    _confirmation_key: bytes | None = field(repr=False)

    def __post_init__(self) -> None:
        if len(self.context_hash) != 48:
            raise ValueError("context_hash must be a SHA-384 digest.")
        if self._session_key is None or len(self._session_key) != HYBRID_KEY_LENGTH:
            raise ValueError(f"session_key must contain {HYBRID_KEY_LENGTH} bytes.")
        if self._confirmation_key is None or len(self._confirmation_key) != HYBRID_KEY_LENGTH:
            raise ValueError(f"confirmation_key must contain {HYBRID_KEY_LENGTH} bytes.")
        self.context_hash = bytes(self.context_hash)
        self._session_key = bytes(self._session_key)
        self._confirmation_key = bytes(self._confirmation_key)

    def session_key(self) -> bytes:
        if self._session_key is None:
            raise RuntimeError("Hybrid derived-key state is closed.")
        return bytes(self._session_key)

    def confirmation_key(self) -> bytes:
        if self._confirmation_key is None:
            raise RuntimeError("Hybrid derived-key state is closed.")
        return bytes(self._confirmation_key)

    def retire_confirmation_key(self) -> None:
        self._confirmation_key = None

    def close(self) -> None:
        self._session_key = None
        self._confirmation_key = None

    def __repr__(self) -> str:
        return (
            f"HybridDerivedKeys(context_hash={self.context_hash.hex()!r}, closed={self._session_key is None})"
        )


def _info(domain: bytes, context: HybridPublicContext) -> bytes:
    return length_prefixed(domain) + length_prefixed(context.context_hash)


def derive_hybrid_keys(secret_input: bytes, context: HybridPublicContext) -> HybridDerivedKeys:
    """Derive session and confirmation keys independently from the same canonical input."""

    return HybridDerivedKeys(
        context_hash=context.context_hash,
        _session_key=derive_hybrid_session_key(secret_input, context),
        _confirmation_key=derive_hybrid_confirmation_key(secret_input, context),
    )


def derive_hybrid_session_key(secret_input: bytes, context: HybridPublicContext) -> bytes:
    return derive_hkdf_sha384(
        key_material=secret_input,
        salt=context.context_hash,
        info=_info(HYBRID_SESSION_KEY_DOMAIN, context),
        length=HYBRID_KEY_LENGTH,
    )


def derive_hybrid_confirmation_key(secret_input: bytes, context: HybridPublicContext) -> bytes:
    return derive_hkdf_sha384(
        key_material=secret_input,
        salt=context.context_hash,
        info=_info(HYBRID_CONFIRMATION_KEY_DOMAIN, context),
        length=HYBRID_KEY_LENGTH,
    )
