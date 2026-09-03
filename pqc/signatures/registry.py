"""Intentional dispatch registry for supported signature providers."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final

from pqc.errors import UnsupportedAlgorithmError
from pqc.signatures.base import SignatureMetadata, SignatureProvider
from pqc.signatures.ml_dsa import ML_DSA_65_METADATA, MLDSA65


@dataclass(frozen=True, slots=True)
class _RegisteredSignature:
    """Internal container pairing algorithm metadata with its corresponding signature provider class."""

    metadata: SignatureMetadata
    provider: type[SignatureProvider]


_SIGNATURES: Final[Mapping[str, _RegisteredSignature]] = MappingProxyType(
    {
        ML_DSA_65_METADATA.name: _RegisteredSignature(
            metadata=ML_DSA_65_METADATA,
            provider=MLDSA65,
        )
    }
)


def _metadata_for_algorithm(algorithm: str) -> SignatureMetadata | None:
    """Look up algorithm metadata from the registry, or return None if unsupported."""
    registration = _SIGNATURES.get(algorithm)
    return None if registration is None else registration.metadata


def verify_signature(algorithm: str, message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify a signature by dispatching to the registered provider for the specified algorithm name."""

    if not isinstance(algorithm, str):
        raise TypeError(f"algorithm must be a string. Got {type(algorithm).__name__}.")
    registration = _SIGNATURES.get(algorithm)
    if registration is None:
        raise UnsupportedAlgorithmError(f"No signature verifier is registered for {algorithm!r}.")
    return registration.provider.verify(message, signature, public_key)
