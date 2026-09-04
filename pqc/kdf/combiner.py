"""Unambiguous profile-aware encoding of independently established KEM secrets."""

from struct import pack
from typing import Final

from pqc._encoding import _length_prefixed
from pqc.kem import hqc_3_metadata, ml_kem_768_metadata
from pqc.profiles import PQCProfile, profile_definition

KEM_SECRET_INPUT_DOMAIN: Final = b"QuantumSec/PQCHandshake/v1/KEMSecretInput"


def _validated_secret(value: object, *, name: str, length: int) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes. Got {type(value).__name__}.")
    if len(value) != length:
        raise ValueError(f"{name} must contain {length} bytes. Got {len(value)}.")
    return bytes(value)


def canonical_kem_secret_input(
    *,
    profile: PQCProfile,
    ml_kem_shared_secret: bytes,
    hqc_shared_secret: bytes | None = None,
) -> bytes:
    """Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.

    HIGH is a QuantumSec research diversity construction, not a standardized
    multi-KEM combiner. ML-KEM-768 is always encoded first and HQC-3 second.
    """

    definition = profile_definition(profile)
    ml_secret = _validated_secret(
        ml_kem_shared_secret,
        name="ml_kem_shared_secret",
        length=ml_kem_768_metadata().shared_secret_length,
    )
    components = [(definition.ml_kem_algorithm.encode("ascii"), ml_secret)]

    if profile is PQCProfile.LOW:
        if hqc_shared_secret is not None:
            raise ValueError("LOW KEM secret input must not contain an HQC shared secret.")
    else:
        if definition.hqc_algorithm is None or hqc_shared_secret is None:
            raise ValueError("HIGH KEM secret input requires an HQC shared secret.")
        hqc_secret = _validated_secret(
            hqc_shared_secret,
            name="hqc_shared_secret",
            length=hqc_3_metadata().shared_secret_length,
        )
        components.append((definition.hqc_algorithm.encode("ascii"), hqc_secret))

    fields = [_length_prefixed(KEM_SECRET_INPUT_DOMAIN), pack(">B", len(components))]
    for algorithm, secret in components:
        fields.extend((_length_prefixed(algorithm), _length_prefixed(secret)))
    return b"".join(fields)
