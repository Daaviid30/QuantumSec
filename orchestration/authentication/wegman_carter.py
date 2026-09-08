"""One-time universal-hash authentication for QKD classical checkpoints.

The construction uses a fresh secret Toeplitz hash selector and a fresh secret
one-time pad for every tag.  It deliberately does not implement key recycling:
consumed pre-shared bits can never be selected again by the same material
instance.
"""

from dataclasses import dataclass, field
from hmac import compare_digest
from threading import Lock
from typing import Self

import numpy as np
import numpy.typing as npt

from orchestration.authentication.base import (
    AuthenticationEvidence,
    AuthenticationFrame,
    AuthenticationSessionRegistry,
    AuthenticationVerification,
    AuthenticatorMetadata,
    DirectionalAuthenticator,
)
from orchestration.profiles import ClassicalAuthenticationMode
from orchestration.qkd.transcript import QKDClassicalDirection
from qkd.postprocessing.universal_hashing import toeplitz_hash, toeplitz_seed_length

WEGMAN_CARTER_DEFAULT_TAG_BITS = 128
WEGMAN_CARTER_TRUST_ASSUMPTION = (
    "Alice and Bob hold identical, uniformly random, pre-shared authentication material; "
    "every Toeplitz selector and one-time tag mask is fresh and never reused."
)


class AuthenticationMaterialError(RuntimeError):
    """Base error for unsafe or unavailable authentication material."""


class AuthenticationMaterialExhaustedError(AuthenticationMaterialError):
    """Raised before a tag operation that would exceed the provisioned PSK."""


class AuthenticationMaterialReuseError(AuthenticationMaterialError):
    """Raised when a frame context attempts to consume authentication bits twice."""


class PreSharedAuthenticationMaterial:
    """Consumable PSK bit stream whose contents are never exposed or serialized."""

    __slots__ = ("_secret", "_consumed_bits", "_lock", "_usage_ids")

    def __init__(self, secret: bytes) -> None:
        if not isinstance(secret, bytes):
            raise TypeError(f"secret must be bytes. Got {type(secret).__name__}.")
        if not secret:
            raise ValueError("Pre-shared authentication material must not be empty.")
        self._secret = bytes(secret)
        self._consumed_bits = 0
        self._usage_ids: set[bytes] = set()
        self._lock = Lock()

    @property
    def total_bits(self) -> int:
        return len(self._secret) * 8

    @property
    def consumed_bits(self) -> int:
        with self._lock:
            return self._consumed_bits

    @property
    def remaining_bits(self) -> int:
        with self._lock:
            return self.total_bits - self._consumed_bits

    def consume(self, bit_count: int, *, usage_id: bytes) -> npt.NDArray[np.uint8]:
        """Atomically reserve fresh bits for one unique authenticated frame context."""

        if isinstance(bit_count, bool) or not isinstance(bit_count, int) or bit_count <= 0:
            raise ValueError("bit_count must be a positive integer.")
        if not isinstance(usage_id, bytes) or not usage_id:
            raise ValueError("usage_id must be non-empty bytes.")
        clean_usage_id = bytes(usage_id)
        with self._lock:
            if clean_usage_id in self._usage_ids:
                raise AuthenticationMaterialReuseError(
                    "Pre-shared authentication material cannot be reused for the same frame context."
                )
            end = self._consumed_bits + bit_count
            if end > self.total_bits:
                raise AuthenticationMaterialExhaustedError(
                    "Insufficient fresh pre-shared authentication material: "
                    f"required={bit_count}, remaining={self.total_bits - self._consumed_bits} bits."
                )
            byte_start = self._consumed_bits // 8
            byte_end = (end + 7) // 8
            packed = np.frombuffer(self._secret[byte_start:byte_end], dtype=np.uint8)
            unpacked = np.unpackbits(packed, bitorder="big")
            bit_offset = self._consumed_bits - byte_start * 8
            selected = np.array(
                unpacked[bit_offset : bit_offset + bit_count],
                dtype=np.uint8,
                copy=True,
            )
            selected.flags.writeable = False
            self._consumed_bits = end
            self._usage_ids.add(clean_usage_id)
            return selected

    def _same_secret_as(self, other: PreSharedAuthenticationMaterial) -> bool:
        return compare_digest(self._secret, other._secret)

    def __repr__(self) -> str:
        return (
            "PreSharedAuthenticationMaterial("
            f"total_bits={self.total_bits}, consumed_bits={self.consumed_bits}, "
            f"remaining_bits={self.remaining_bits})"
        )


def _frame_bits(frame: AuthenticationFrame) -> npt.NDArray[np.uint8]:
    bits = np.unpackbits(
        np.frombuffer(frame.canonical_bytes(), dtype=np.uint8),
        bitorder="big",
    )
    bits.flags.writeable = False
    return bits


@dataclass(frozen=True, slots=True)
class WegmanCarterDirectionalAuthenticator(DirectionalAuthenticator):
    """Authenticate one direction with fresh Toeplitz-selector and mask bits."""

    sender_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    verifier_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    sender_name: str
    verifier_name: str
    direction: QKDClassicalDirection
    tag_bits: int = WEGMAN_CARTER_DEFAULT_TAG_BITS

    def __post_init__(self) -> None:
        if not isinstance(self.sender_material, PreSharedAuthenticationMaterial) or not isinstance(
            self.verifier_material, PreSharedAuthenticationMaterial
        ):
            raise TypeError("sender_material and verifier_material must be PSK material instances.")
        if self.sender_material is self.verifier_material:
            raise ValueError("Sender and verifier require independent synchronized PSK copies.")
        for name in ("sender_name", "verifier_name"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")
            object.__setattr__(self, name, value.strip())
        if self.sender_name == self.verifier_name:
            raise ValueError("Sender and verifier names must be distinct.")
        if not isinstance(self.direction, QKDClassicalDirection):
            raise TypeError("direction must be a QKDClassicalDirection.")
        if isinstance(self.tag_bits, bool) or not isinstance(self.tag_bits, int):
            raise ValueError("tag_bits must be a positive byte-aligned integer.")
        if self.tag_bits <= 0 or self.tag_bits % 8 != 0:
            raise ValueError("tag_bits must be a positive multiple of eight.")

    @property
    def algorithm(self) -> str:
        return f"Toeplitz-U2+one-time-mask-{self.tag_bits}"

    @property
    def metadata(self) -> AuthenticatorMetadata:
        return AuthenticatorMetadata(
            mechanism=ClassicalAuthenticationMode.WEGMAN_CARTER,
            algorithm=self.algorithm,
            family="information-theoretic universal-hash authentication",
            trust_assumption=WEGMAN_CARTER_TRUST_ASSUMPTION,
            public_key_provisioning_bytes=None,
            forgery_bound=f"<= 2^-{self.tag_bits} per fresh-key checkpoint",
        )

    def _required_material_bits(self, frame: AuthenticationFrame) -> int:
        message_bits = len(frame.canonical_bytes()) * 8
        return toeplitz_seed_length(message_bits, self.tag_bits) + self.tag_bits

    def _tag(
        self,
        frame: AuthenticationFrame,
        material: npt.NDArray[np.uint8],
    ) -> bytes:
        message = _frame_bits(frame)
        seed_length = toeplitz_seed_length(int(message.size), self.tag_bits)
        selector = material[:seed_length]
        mask = material[seed_length:]
        tag = np.bitwise_xor(toeplitz_hash(message, self.tag_bits, selector), mask)
        return np.packbits(tag, bitorder="big").tobytes()

    def generate_evidence(self, frame: AuthenticationFrame) -> AuthenticationEvidence:
        if frame.direction is not self.direction:
            raise ValueError("Authentication frame direction does not match the PSK direction.")
        required = self._required_material_bits(frame)
        material = self.sender_material.consume(
            required,
            usage_id=frame.canonical_context_bytes(),
        )
        return AuthenticationEvidence(
            mechanism=ClassicalAuthenticationMode.WEGMAN_CARTER,
            algorithm=self.algorithm,
            signer=self.sender_name,
            verifier=self.verifier_name,
            session_id=frame.session_id,
            direction=frame.direction,
            sequence_number=frame.sequence_number,
            message_type=frame.message_type,
            value=self._tag(frame, material),
            secret_bits_consumed=required,
        )

    def verify_evidence(
        self,
        frame: AuthenticationFrame,
        evidence: AuthenticationEvidence | None,
    ) -> AuthenticationVerification:
        if evidence is None:
            return AuthenticationVerification(False, "Missing Wegman-Carter authentication tag.")
        if frame.direction is not self.direction or not evidence.matches_frame(frame):
            return AuthenticationVerification(False, "Wegman-Carter tag context does not match the frame.")
        if (
            evidence.mechanism is not ClassicalAuthenticationMode.WEGMAN_CARTER
            or evidence.algorithm != self.algorithm
            or evidence.signer != self.sender_name
            or evidence.verifier != self.verifier_name
            or len(evidence.value) * 8 != self.tag_bits
        ):
            return AuthenticationVerification(False, "Wegman-Carter tag identity or algorithm is invalid.")
        required = self._required_material_bits(frame)
        try:
            material = self.verifier_material.consume(
                required,
                usage_id=frame.canonical_context_bytes(),
            )
        except AuthenticationMaterialError as exc:
            return AuthenticationVerification(False, str(exc))
        expected = self._tag(frame, material)
        if not compare_digest(expected, evidence.value):
            return AuthenticationVerification(False, "Wegman-Carter tag verification failed.")
        return AuthenticationVerification(True)


@dataclass(frozen=True, slots=True)
class WegmanCarterAuthenticationContext:
    """Bilateral, direction-separated PSK material for one or more QKD sessions."""

    alice_sender_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    bob_verifier_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    bob_sender_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    alice_verifier_material: PreSharedAuthenticationMaterial = field(repr=False, compare=False)
    alice_name: str = "alice"
    bob_name: str = "bob"
    tag_bits: int = WEGMAN_CARTER_DEFAULT_TAG_BITS
    session_registry: AuthenticationSessionRegistry = field(
        default_factory=AuthenticationSessionRegistry,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        materials = (
            self.alice_sender_material,
            self.bob_verifier_material,
            self.bob_sender_material,
            self.alice_verifier_material,
        )
        if not all(isinstance(item, PreSharedAuthenticationMaterial) for item in materials):
            raise TypeError("All Wegman-Carter context materials must be PSK material instances.")
        if len({id(item) for item in materials}) != len(materials):
            raise ValueError("Every sender and verifier must hold an independent PSK copy.")
        if not self.alice_sender_material._same_secret_as(self.bob_verifier_material):
            raise ValueError("Alice-to-Bob sender and verifier PSK copies must match.")
        if not self.bob_sender_material._same_secret_as(self.alice_verifier_material):
            raise ValueError("Bob-to-Alice sender and verifier PSK copies must match.")
        if self.alice_sender_material._same_secret_as(self.bob_sender_material):
            raise ValueError("Alice-to-Bob and Bob-to-Alice PSKs must be distinct.")
        if not isinstance(self.session_registry, AuthenticationSessionRegistry):
            raise TypeError("session_registry must be an AuthenticationSessionRegistry.")

    def reserve_session_id(self, session_id: bytes) -> None:
        self.session_registry.reserve(session_id)

    @classmethod
    def from_shared_secrets(
        cls,
        *,
        alice_to_bob_secret: bytes,
        bob_to_alice_secret: bytes,
        alice_name: str = "alice",
        bob_name: str = "bob",
        tag_bits: int = WEGMAN_CARTER_DEFAULT_TAG_BITS,
    ) -> Self:
        """Provision matching but independent copies for each communication direction."""

        return cls(
            alice_sender_material=PreSharedAuthenticationMaterial(alice_to_bob_secret),
            bob_verifier_material=PreSharedAuthenticationMaterial(alice_to_bob_secret),
            bob_sender_material=PreSharedAuthenticationMaterial(bob_to_alice_secret),
            alice_verifier_material=PreSharedAuthenticationMaterial(bob_to_alice_secret),
            alice_name=alice_name,
            bob_name=bob_name,
            tag_bits=tag_bits,
        )

    def authenticators(
        self,
    ) -> tuple[WegmanCarterDirectionalAuthenticator, WegmanCarterDirectionalAuthenticator]:
        return (
            WegmanCarterDirectionalAuthenticator(
                sender_material=self.alice_sender_material,
                verifier_material=self.bob_verifier_material,
                sender_name=self.alice_name,
                verifier_name=self.bob_name,
                direction=QKDClassicalDirection.ALICE_TO_BOB,
                tag_bits=self.tag_bits,
            ),
            WegmanCarterDirectionalAuthenticator(
                sender_material=self.bob_sender_material,
                verifier_material=self.alice_verifier_material,
                sender_name=self.bob_name,
                verifier_name=self.alice_name,
                direction=QKDClassicalDirection.BOB_TO_ALICE,
                tag_bits=self.tag_bits,
            ),
        )
