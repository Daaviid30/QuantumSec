"""Real-backend tests for Phase 2 KEM providers."""

import pytest

from pqc.backends.oqs_kem_backend import OQSKEMBackend
from pqc.errors import UnsupportedAlgorithmError
from pqc.kem import HQC3, MLKEM768, KEMProvider


@pytest.fixture(scope="module")
def ml_kem() -> MLKEM768:
    return MLKEM768.generate()


@pytest.fixture(scope="module")
def hqc() -> HQC3:
    return HQC3.generate()


def test_ml_kem_768_real_key_generation_and_metadata(ml_kem: MLKEM768) -> None:
    assert isinstance(ml_kem, KEMProvider)
    assert ml_kem.metadata.name == "ML-KEM-768"
    assert ml_kem.metadata.algorithm_type == "key encapsulation mechanism"
    assert ml_kem.metadata.family == "module-lattice based"
    assert ml_kem.metadata.nist_security_category == 3
    assert ml_kem.metadata.standardization == "NIST FIPS 203"
    assert ml_kem.metadata.public_key_length == 1184
    assert ml_kem.metadata.secret_key_length == 2400
    assert ml_kem.metadata.ciphertext_length == 1088
    assert ml_kem.metadata.shared_secret_length == 32
    assert isinstance(ml_kem.public_key, bytes)
    assert len(ml_kem.public_key) == ml_kem.metadata.public_key_length


def test_hqc_3_real_key_generation_and_metadata(hqc: HQC3) -> None:
    assert isinstance(hqc, KEMProvider)
    assert hqc.metadata.name == "HQC-3"
    assert hqc.metadata.algorithm_type == "key encapsulation mechanism"
    assert hqc.metadata.family == "code based"
    assert hqc.metadata.nist_security_category == 3
    assert "selected for standardization" in hqc.metadata.standardization
    assert "FIPS not yet finalized" in hqc.metadata.standardization
    assert hqc.metadata.public_key_length == 4514
    assert hqc.metadata.secret_key_length == 4602
    assert hqc.metadata.ciphertext_length == 8978
    assert hqc.metadata.shared_secret_length == 32
    assert isinstance(hqc.public_key, bytes)
    assert len(hqc.public_key) == hqc.metadata.public_key_length


@pytest.mark.parametrize("provider_name", ["ml_kem", "hqc"])
def test_kem_private_material_is_not_exposed(
    provider_name: str,
    request: pytest.FixtureRequest,
) -> None:
    provider = request.getfixturevalue(provider_name)
    secret_key = object.__getattribute__(provider, "_secret_key")

    assert not hasattr(provider, "secret_key")
    assert repr(secret_key) not in repr(provider)
    assert "public_key_length=" in repr(provider)


def test_ml_kem_768_primitive_round_trip(ml_kem: MLKEM768) -> None:
    encapsulation = MLKEM768.encapsulate(ml_kem.public_key)

    assert ml_kem.decapsulate(encapsulation.ciphertext) == encapsulation.shared_secret
    assert repr(encapsulation.shared_secret) not in repr(encapsulation)


def test_hqc_3_primitive_round_trip(hqc: HQC3) -> None:
    encapsulation = HQC3.encapsulate(hqc.public_key)

    assert hqc.decapsulate(encapsulation.ciphertext) == encapsulation.shared_secret
    assert repr(encapsulation.shared_secret) not in repr(encapsulation)


def test_kem_rejects_malformed_public_key_before_backend() -> None:
    with pytest.raises(ValueError, match="must contain 1184 bytes"):
        MLKEM768.encapsulate(b"truncated")


def test_unsupported_kem_algorithm_has_domain_error() -> None:
    with pytest.raises(UnsupportedAlgorithmError, match="not enabled"):
        OQSKEMBackend().generate_keypair("NOT-A-KEM")
