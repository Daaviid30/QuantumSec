from dataclasses import replace

import pytest

from orchestration.authentication import (
    AuthenticationFrame,
    AuthenticationMaterialExhaustedError,
    AuthenticationMaterialReuseError,
    MLDSADirectionalAuthenticator,
    PreSharedAuthenticationMaterial,
    WegmanCarterAuthenticationContext,
    WegmanCarterDirectionalAuthenticator,
)
from orchestration.profiles import ClassicalAuthenticationMode
from orchestration.qkd import QKDClassicalDirection
from pqc.protocol import MLDSAIdentity, PublicIdentity, TrustedIdentityStore


def _frame(
    *,
    session_id: bytes = b"s" * 16,
    direction: QKDClassicalDirection = QKDClassicalDirection.ALICE_TO_BOB,
    sequence_number: int = 7,
    message_type: str = "parameter_estimation",
    payload: bytes = b"canonical public payload",
) -> AuthenticationFrame:
    return AuthenticationFrame(
        session_id=session_id,
        direction=direction,
        sequence_number=sequence_number,
        message_type=message_type,
        payload=payload,
    )


@pytest.fixture(scope="module")
def ml_dsa_identities() -> tuple[MLDSAIdentity, MLDSAIdentity, MLDSAIdentity]:
    return (
        MLDSAIdentity.generate("alice"),
        MLDSAIdentity.generate("bob"),
        MLDSAIdentity.generate("mallory"),
    )


def _ml_dsa_authenticator(
    identities: tuple[MLDSAIdentity, MLDSAIdentity, MLDSAIdentity],
    *,
    trusted_identity: PublicIdentity | None,
) -> MLDSADirectionalAuthenticator:
    alice, bob, _ = identities
    store = TrustedIdentityStore()
    if trusted_identity is not None:
        store.trust(trusted_identity)
    return MLDSADirectionalAuthenticator(
        signer_identity=alice,
        verifier_name=bob.owner,
        verifier_trust_store=store,
        direction=QKDClassicalDirection.ALICE_TO_BOB,
    )


def test_ml_dsa_valid_signature_verifies(ml_dsa_identities) -> None:
    alice, _, _ = ml_dsa_identities
    authenticator = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=alice.public_identity,
    )
    frame = _frame()

    evidence = authenticator.generate_evidence(frame)

    assert evidence.mechanism is ClassicalAuthenticationMode.ML_DSA_65
    assert authenticator.verify_evidence(frame, evidence).verified


@pytest.mark.parametrize(
    "changed_frame",
    [
        _frame(payload=b"modified"),
        _frame(session_id=b"n" * 16),
        _frame(direction=QKDClassicalDirection.BOB_TO_ALICE),
        _frame(sequence_number=8),
        _frame(message_type="privacy_amplification_seed"),
    ],
    ids=["payload", "session", "direction", "sequence", "message-type"],
)
def test_ml_dsa_rejects_modified_or_cross_context_frame(
    ml_dsa_identities,
    changed_frame: AuthenticationFrame,
) -> None:
    alice, _, _ = ml_dsa_identities
    authenticator = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=alice.public_identity,
    )
    evidence = authenticator.generate_evidence(_frame())

    assert not authenticator.verify_evidence(changed_frame, evidence).verified


def test_ml_dsa_rejects_modified_signature(ml_dsa_identities) -> None:
    alice, _, _ = ml_dsa_identities
    authenticator = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=alice.public_identity,
    )
    frame = _frame()
    evidence = authenticator.generate_evidence(frame)
    modified = replace(evidence, value=evidence.value[:-1] + bytes((evidence.value[-1] ^ 1,)))

    assert not authenticator.verify_evidence(frame, modified).verified


def test_ml_dsa_rejects_wrong_public_identity(ml_dsa_identities) -> None:
    alice, _, _ = ml_dsa_identities
    wrong_key_same_owner = MLDSAIdentity.generate(alice.owner).public_identity
    authenticator = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=wrong_key_same_owner,
    )
    frame = _frame()
    evidence = authenticator.generate_evidence(frame)

    assert not authenticator.verify_evidence(frame, evidence).verified


def test_ml_dsa_rejects_unknown_identity(ml_dsa_identities) -> None:
    alice, _, _ = ml_dsa_identities
    signer = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=alice.public_identity,
    )
    unknown_verifier = _ml_dsa_authenticator(ml_dsa_identities, trusted_identity=None)
    frame = _frame()

    assert not unknown_verifier.verify_evidence(frame, signer.generate_evidence(frame)).verified


def test_ml_dsa_rejects_missing_signature(ml_dsa_identities) -> None:
    alice, _, _ = ml_dsa_identities
    authenticator = _ml_dsa_authenticator(
        ml_dsa_identities,
        trusted_identity=alice.public_identity,
    )

    result = authenticator.verify_evidence(_frame(), None)

    assert not result.verified
    assert "Missing" in (result.failure_reason or "")


def _wegman_carter_authenticator(
    *,
    sender_secret: bytes = b"a" * 1024,
    verifier_secret: bytes = b"a" * 1024,
) -> WegmanCarterDirectionalAuthenticator:
    return WegmanCarterDirectionalAuthenticator(
        sender_material=PreSharedAuthenticationMaterial(sender_secret),
        verifier_material=PreSharedAuthenticationMaterial(verifier_secret),
        sender_name="alice",
        verifier_name="bob",
        direction=QKDClassicalDirection.ALICE_TO_BOB,
    )


def test_wegman_carter_valid_tag_verifies_and_accounts_for_consumption() -> None:
    authenticator = _wegman_carter_authenticator()
    frame = _frame()

    evidence = authenticator.generate_evidence(frame)
    verification = authenticator.verify_evidence(frame, evidence)

    expected = len(frame.canonical_bytes()) * 8 + 2 * 128 - 1
    assert verification.verified
    assert evidence.secret_bits_consumed == expected
    assert authenticator.sender_material.consumed_bits == expected
    assert authenticator.verifier_material.consumed_bits == expected


def test_wegman_carter_rejects_modified_payload_and_tag() -> None:
    payload_authenticator = _wegman_carter_authenticator()
    frame = _frame()
    evidence = payload_authenticator.generate_evidence(frame)
    assert not payload_authenticator.verify_evidence(
        replace(frame, payload=b"tampered"),
        evidence,
    ).verified

    tag_authenticator = _wegman_carter_authenticator()
    evidence = tag_authenticator.generate_evidence(frame)
    modified_tag = replace(evidence, value=evidence.value[:-1] + bytes((evidence.value[-1] ^ 1,)))
    assert not tag_authenticator.verify_evidence(frame, modified_tag).verified


def test_wegman_carter_rejects_wrong_psk() -> None:
    authenticator = _wegman_carter_authenticator(verifier_secret=b"b" * 1024)
    frame = _frame()

    assert not authenticator.verify_evidence(frame, authenticator.generate_evidence(frame)).verified


@pytest.mark.parametrize(
    "changed_frame",
    [
        _frame(session_id=b"r" * 16),
        _frame(direction=QKDClassicalDirection.BOB_TO_ALICE),
        _frame(sequence_number=11),
    ],
    ids=["replayed-new-session", "direction", "sequence"],
)
def test_wegman_carter_rejects_replay_or_context_mismatch(changed_frame) -> None:
    authenticator = _wegman_carter_authenticator()
    evidence = authenticator.generate_evidence(_frame())

    assert not authenticator.verify_evidence(changed_frame, evidence).verified


def test_pre_shared_material_prevents_same_context_reuse() -> None:
    authenticator = _wegman_carter_authenticator()
    frame = _frame()
    authenticator.generate_evidence(frame)

    with pytest.raises(AuthenticationMaterialReuseError, match="cannot be reused"):
        authenticator.generate_evidence(frame)


def test_pre_shared_material_fails_closed_when_exhausted() -> None:
    authenticator = _wegman_carter_authenticator(
        sender_secret=b"short",
        verifier_secret=b"short",
    )

    with pytest.raises(AuthenticationMaterialExhaustedError, match="Insufficient"):
        authenticator.generate_evidence(_frame())


def test_psk_representation_never_contains_secret() -> None:
    secret = b"DO-NOT-EXPOSE-THIS-PSK"
    material = PreSharedAuthenticationMaterial(secret)

    assert secret.decode("ascii") not in repr(material)
    assert not hasattr(material, "secret")
    assert not hasattr(material, "to_dict")


def test_wegman_carter_context_enforces_directional_key_separation() -> None:
    with pytest.raises(ValueError, match="must be distinct"):
        WegmanCarterAuthenticationContext.from_shared_secrets(
            alice_to_bob_secret=b"same-secret",
            bob_to_alice_secret=b"same-secret",
        )
