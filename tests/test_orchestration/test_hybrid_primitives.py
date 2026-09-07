from dataclasses import replace

import pytest

from orchestration.hybrid.context import HybridPublicContext
from orchestration.hybrid.encoding import HybridSecretComponent, canonical_hybrid_secret_input
from orchestration.hybrid.key_schedule import (
    derive_hybrid_confirmation_key,
    derive_hybrid_session_key,
)
from orchestration.profiles import QKDProfile, SessionProfile, session_profile_definition
from pqc import PQCProfile
from pqc.kdf.combiner import canonical_kem_secret_input
from pqc.kdf.hkdf import derive_hkdf_sha384
from pqc.protocol.key_schedule import _session_key_info


def _component(
    position: int,
    label: str,
    source: str,
    algorithm: str,
    secret: bytes,
    *,
    bit_length: int | None = None,
) -> HybridSecretComponent:
    return HybridSecretComponent(
        position,
        label,
        source,
        algorithm,
        "packed-bits-big-endian" if source == "qkd" else "raw-bytes",
        bit_length if bit_length is not None else len(secret) * 8,
        secret,
    )


def _low_components() -> tuple[HybridSecretComponent, ...]:
    return (
        _component(1, "K_QKD", "qkd", "BB84-final-key", b"\xaa\xe0", bit_length=13),
        _component(2, "SS_ML_KEM", "pqc", "ML-KEM-768", b"m" * 32),
    )


def _high_components() -> tuple[HybridSecretComponent, ...]:
    return _low_components() + (_component(3, "SS_HQC", "pqc", "HQC-3", b"h" * 32),)


def _context(
    *,
    profile: SessionProfile = SessionProfile.HYBRID,
    session_id: bytes = b"session-context1",
    qkd_profile: QKDProfile = QKDProfile.QKD_ASSUMED,
) -> HybridPublicContext:
    pqc_profile = PQCProfile.LOW if profile is SessionProfile.HYBRID else PQCProfile.HIGH
    return HybridPublicContext(
        session_id,
        profile,
        qkd_profile,
        1,
        b"q" * 48,
        1,
        pqc_profile,
        b"p" * 48,
        session_profile_definition(profile).establishment_algorithms,
    )


def test_canonical_encoding_is_deterministic_and_order_sensitive() -> None:
    components = _low_components()
    first = canonical_hybrid_secret_input(profile=SessionProfile.HYBRID, components=components)
    second = canonical_hybrid_secret_input(profile=SessionProfile.HYBRID, components=components)
    assert first == second
    with pytest.raises(ValueError, match="positions|order"):
        canonical_hybrid_secret_input(
            profile=SessionProfile.HYBRID,
            components=(components[1], components[0]),
        )


@pytest.mark.parametrize(
    "components",
    [
        (),
        (_low_components()[0],),
        (_low_components()[1],),
        _high_components(),
        (_low_components()[0], _low_components()[1], _low_components()[1]),
        (_low_components()[0], replace(_low_components()[1], algorithm="wrong")),
    ],
)
def test_low_profile_rejects_missing_extra_duplicate_or_wrong_components(components) -> None:
    with pytest.raises(ValueError):
        canonical_hybrid_secret_input(profile=SessionProfile.HYBRID, components=components)


def test_diverse_requires_hqc_and_non_hybrid_profiles_are_rejected() -> None:
    with pytest.raises(ValueError):
        canonical_hybrid_secret_input(
            profile=SessionProfile.HYBRID_DIVERSE,
            components=_low_components(),
        )
    with pytest.raises(ValueError):
        canonical_hybrid_secret_input(
            profile=SessionProfile.PQC_BASE,
            components=_low_components(),
        )


def test_exact_bit_length_makes_padding_ambiguity_invalid() -> None:
    with pytest.raises(ValueError, match="Unused trailing bits"):
        _component(1, "K_QKD", "qkd", "BB84-final-key", b"\xaa\xe1", bit_length=13)
    with pytest.raises(ValueError, match="bit_length"):
        _component(1, "K_QKD", "qkd", "BB84-final-key", b"\xaa", bit_length=9)


def test_secret_component_repr_and_api_do_not_serialize_secret_bytes() -> None:
    component = _low_components()[1]
    assert component.secret.hex() not in repr(component)
    assert not hasattr(component, "to_dict")


def test_each_secret_component_changes_both_derived_keys() -> None:
    context = _context(profile=SessionProfile.HYBRID_DIVERSE)
    base = _high_components()
    base_input = canonical_hybrid_secret_input(
        profile=SessionProfile.HYBRID_DIVERSE,
        components=base,
    )
    base_pair = (
        derive_hybrid_session_key(base_input, context),
        derive_hybrid_confirmation_key(base_input, context),
    )
    for index in range(3):
        secret = base[index].secret
        changed_secret = bytes((secret[0] ^ 1,)) + secret[1:]
        changed = list(base)
        changed[index] = replace(base[index], secret=changed_secret)
        changed_input = canonical_hybrid_secret_input(
            profile=SessionProfile.HYBRID_DIVERSE,
            components=tuple(changed),
        )
        assert derive_hybrid_session_key(changed_input, context) != base_pair[0]
        assert derive_hybrid_confirmation_key(changed_input, context) != base_pair[1]


def test_context_changes_separate_keys_for_session_profile_and_qkd_policy() -> None:
    secret_input = canonical_hybrid_secret_input(
        profile=SessionProfile.HYBRID,
        components=_low_components(),
    )
    baseline = derive_hybrid_session_key(secret_input, _context())
    assert baseline != derive_hybrid_session_key(
        secret_input,
        _context(session_id=b"session-context2"),
    )
    assert baseline != derive_hybrid_session_key(
        secret_input,
        _context(qkd_profile=QKDProfile.QKD_PQC_AUTH),
    )
    high_input = canonical_hybrid_secret_input(
        profile=SessionProfile.HYBRID_DIVERSE,
        components=_high_components(),
    )
    assert baseline != derive_hybrid_session_key(
        high_input,
        _context(profile=SessionProfile.HYBRID_DIVERSE),
    )
    assert baseline != derive_hybrid_session_key(
        secret_input,
        _context(profile=SessionProfile.HYBRID_DIVERSE),
    )
    assert baseline != derive_hybrid_session_key(
        secret_input,
        replace(_context(), qkd_transcript_hash=b"x" * 48),
    )
    assert baseline != derive_hybrid_session_key(
        secret_input,
        replace(_context(), pqc_transcript_hash=b"y" * 48),
    )


def test_pure_pqc_and_hybrid_schedules_remain_domain_separated() -> None:
    ml_secret = b"m" * 32
    pqc_input = canonical_kem_secret_input(
        profile=PQCProfile.LOW,
        ml_kem_shared_secret=ml_secret,
    )
    pqc_key = derive_hkdf_sha384(
        key_material=pqc_input,
        salt=b"p" * 48,
        info=_session_key_info(protocol_version=1, profile=PQCProfile.LOW),
        length=32,
    )
    hybrid_input = canonical_hybrid_secret_input(
        profile=SessionProfile.HYBRID,
        components=_low_components(),
    )
    hybrid_key = derive_hybrid_session_key(hybrid_input, _context())
    assert pqc_input != hybrid_input
    assert pqc_key != hybrid_key
