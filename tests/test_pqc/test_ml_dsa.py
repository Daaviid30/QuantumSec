"""Real-backend tests for ML-DSA-65 signatures."""

import pytest

from pqc.backends.oqs_backend import OQSSignatureBackend
from pqc.errors import UnsupportedAlgorithmError
from pqc.signatures import ML_DSA_65_METADATA, MLDSA65


@pytest.fixture(scope="module")
def signer() -> MLDSA65:
    return MLDSA65.generate()


def test_real_ml_dsa_65_keygen_sign_and_verify(signer: MLDSA65) -> None:
    message = b"QuantumSec Phase 1"

    signature = signer.sign(message)

    assert isinstance(signer.public_key, bytes)
    assert signer.public_key
    assert isinstance(signature, bytes)
    assert signature
    assert signer.verify(message, signature, signer.public_key)


def test_ml_dsa_65_metadata_is_precise(signer: MLDSA65) -> None:
    assert signer.metadata is ML_DSA_65_METADATA
    assert signer.metadata.name == "ML-DSA-65"
    assert signer.metadata.algorithm_type == "digital signature"
    assert signer.metadata.family == "module-lattice based"
    assert signer.metadata.nist_security_category == 3
    assert signer.metadata.standardization == "NIST FIPS 204"


def test_modified_message_and_signature_are_invalid(signer: MLDSA65) -> None:
    message = b"hello"
    signature = signer.sign(message)
    corrupted_signature = bytes([signature[0] ^ 1]) + signature[1:]

    assert not signer.verify(b"hello!", signature, signer.public_key)
    assert not signer.verify(message, corrupted_signature, signer.public_key)


def test_wrong_public_key_is_invalid(signer: MLDSA65) -> None:
    other_signer = MLDSA65.generate()
    message = b"signed by the fixture identity"

    assert not signer.verify(message, signer.sign(message), other_signer.public_key)


def test_malformed_public_key_is_rejected_before_backend_call(signer: MLDSA65) -> None:
    with pytest.raises(ValueError, match="must contain 1952 bytes"):
        signer.verify(b"message", b"signature", b"too short")


def test_private_key_is_not_exposed_by_normal_representation(signer: MLDSA65) -> None:
    secret_key = object.__getattribute__(signer, "_secret_key")

    assert not hasattr(signer, "secret_key")
    assert repr(secret_key) not in repr(signer)
    assert "public_key_length=" in repr(signer)


def test_unsupported_backend_algorithm_has_domain_error() -> None:
    with pytest.raises(UnsupportedAlgorithmError, match="not enabled"):
        OQSSignatureBackend().generate_keypair("NOT-A-SIGNATURE-ALGORITHM")
