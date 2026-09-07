"""Unambiguous encoding of independently established QKD and KEM contributions."""

from dataclasses import dataclass, field
from typing import Final

from orchestration._encoding import length_prefixed, unsigned
from orchestration.profiles import SessionProfile
from pqc.kem import HQC_3_ALGORITHM, ML_KEM_768_ALGORITHM

HYBRID_SECRET_INPUT_DOMAIN: Final = b"QuantumSec/HybridSession/v1/SecretInput"
HYBRID_ENCODING_VERSION: Final = 1
QKD_COMPONENT_ALGORITHM: Final = "BB84-final-key"


@dataclass(frozen=True, slots=True, repr=False)
class HybridSecretComponent:
    position: int
    label: str
    source: str
    algorithm: str
    encoding: str
    bit_length: int
    secret: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if self.position <= 0:
            raise ValueError("position must be positive.")
        if not self.label or not self.source or not self.algorithm or not self.encoding:
            raise ValueError("label, source, algorithm, and encoding must be non-empty.")
        if not isinstance(self.secret, bytes) or not self.secret:
            raise ValueError("secret must be non-empty bytes.")
        if self.bit_length <= (len(self.secret) - 1) * 8 or self.bit_length > len(self.secret) * 8:
            raise ValueError("bit_length does not match the packed secret length.")
        if self.bit_length % 8:
            unused_mask = (1 << (8 - self.bit_length % 8)) - 1
            if self.secret[-1] & unused_mask:
                raise ValueError("Unused trailing bits of a packed component must be zero.")
        object.__setattr__(self, "secret", bytes(self.secret))

    def __repr__(self) -> str:
        return (
            f"HybridSecretComponent(position={self.position}, label={self.label!r}, "
            f"source={self.source!r}, algorithm={self.algorithm!r}, "
            f"encoding={self.encoding!r}, bit_length={self.bit_length}, "
            f"byte_length={len(self.secret)})"
        )


def _expected_algorithms(profile: SessionProfile) -> tuple[str, ...]:
    if profile is SessionProfile.HYBRID:
        return (QKD_COMPONENT_ALGORITHM, ML_KEM_768_ALGORITHM)
    if profile is SessionProfile.HYBRID_DIVERSE:
        return (QKD_COMPONENT_ALGORITHM, ML_KEM_768_ALGORITHM, HQC_3_ALGORITHM)
    raise ValueError("Canonical hybrid input requires a hybrid public profile.")


def canonical_hybrid_secret_input(
    *, profile: SessionProfile, components: tuple[HybridSecretComponent, ...]
) -> bytes:
    """Encode secret contributions in mandatory QKD, ML-KEM, optional HQC order."""

    clean = tuple(components)
    expected = _expected_algorithms(profile)
    if tuple(item.position for item in clean) != tuple(range(1, len(clean) + 1)):
        raise ValueError("Hybrid component positions must be contiguous and start at one.")
    if tuple(item.algorithm for item in clean) != expected:
        raise ValueError("Hybrid components do not match the profile's canonical algorithm order.")
    if not clean or clean[0].source != "qkd" or any(item.source != "pqc" for item in clean[1:]):
        raise ValueError("Hybrid components must contain QKD first and PQC KEMs after it.")
    expected_labels = ("K_QKD", "SS_ML_KEM", "SS_HQC")[: len(expected)]
    if tuple(item.label for item in clean) != expected_labels:
        raise ValueError("Hybrid component labels do not match the canonical profile policy.")
    if clean[0].encoding != "packed-bits-big-endian" or any(
        item.encoding != "raw-bytes" for item in clean[1:]
    ):
        raise ValueError("Hybrid component encoding labels do not match the canonical policy.")

    encoded = [
        length_prefixed(HYBRID_SECRET_INPUT_DOMAIN),
        unsigned(HYBRID_ENCODING_VERSION, width=2),
        length_prefixed(profile.value.encode("ascii")),
        unsigned(len(clean), width=2),
    ]
    for item in clean:
        encoded.extend(
            (
                unsigned(item.position, width=2),
                length_prefixed(item.label.encode("ascii")),
                length_prefixed(item.source.encode("ascii")),
                length_prefixed(item.algorithm.encode("ascii")),
                length_prefixed(item.encoding.encode("ascii")),
                unsigned(item.bit_length),
                unsigned(len(item.secret)),
                length_prefixed(item.secret),
            )
        )
    return b"".join(encoded)


def hybrid_component_metadata_bytes(component: HybridSecretComponent) -> int:
    """Return encoded bytes attributable to one component's non-secret framing/metadata."""

    return (
        2
        + 8
        + len(component.label.encode("ascii"))
        + 8
        + len(component.source.encode("ascii"))
        + 8
        + len(component.algorithm.encode("ascii"))
        + 8
        + len(component.encoding.encode("ascii"))
        + 8
        + 8
        + 8
    )
