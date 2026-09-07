"""Runtime-owned AES-256-GCM protected-session capability."""

from threading import Lock
from typing import Self

from data_protection.aes_gcm import AES_256_KEY_BYTES, decrypt_aes_256_gcm, encrypt_aes_256_gcm
from data_protection.context import (
    DATA_PLANE_ALGORITHM,
    DATA_PLANE_VERSION,
    MAX_SEQUENCE_NUMBER,
    DataPlaneContext,
    DataPlaneDirection,
    _require_bytes,
    canonical_data_plane_aad,
    nonce_for,
)
from data_protection.record import PROTECTED_RECORD_VERSION, ProtectedRecord


class ProtectedSession:
    """Own a 256-bit session key and issue unique direction-separated AES-GCM nonces."""

    __slots__ = ("_key", "_lock", "_next_sequences", "context")

    def __init__(self, key: bytes, context: DataPlaneContext) -> None:
        if not isinstance(context, DataPlaneContext):
            raise TypeError("context must be a DataPlaneContext.")
        self._key: bytes | None = _require_bytes(
            key,
            name="key",
            length=AES_256_KEY_BYTES,
        )
        self.context = context
        self._next_sequences = {direction: 0 for direction in DataPlaneDirection}
        self._lock = Lock()

    @property
    def is_closed(self) -> bool:
        with self._lock:
            return self._key is None

    def _live_key(self) -> bytes:
        if self._key is None:
            raise RuntimeError("Protected session is closed.")
        return bytes(self._key)

    def encrypt(
        self,
        plaintext: bytes,
        *,
        direction: DataPlaneDirection,
        aad: bytes = b"",
    ) -> ProtectedRecord:
        clean_plaintext = _require_bytes(plaintext, name="plaintext")
        clean_aad = _require_bytes(aad, name="aad")
        if not isinstance(direction, DataPlaneDirection):
            raise TypeError("direction must be a DataPlaneDirection.")

        with self._lock:
            key = self._live_key()
            sequence_number = self._next_sequences[direction]
            if sequence_number > MAX_SEQUENCE_NUMBER:
                raise RuntimeError(f"AES-GCM nonce space is exhausted for {direction.value}.")
            self._next_sequences[direction] = sequence_number + 1

        nonce = nonce_for(direction, sequence_number)
        internal_aad = canonical_data_plane_aad(
            self.context,
            direction,
            sequence_number,
            clean_aad,
        )
        ciphertext, tag = encrypt_aes_256_gcm(key, nonce, clean_plaintext, internal_aad)
        return ProtectedRecord(
            PROTECTED_RECORD_VERSION,
            self.context.session_id,
            self.context.profile,
            self.context.context_hash,
            DATA_PLANE_ALGORITHM,
            direction,
            sequence_number,
            nonce,
            ciphertext,
            tag,
            len(clean_aad),
        )

    def decrypt(self, record: ProtectedRecord, *, aad: bytes = b"") -> bytes:
        """Authenticate and decrypt without claiming network anti-replay protection.

        The caller or a future transport layer remains responsible for tracking received
        sequence numbers and rejecting duplicate records before application processing.
        """

        clean_aad = _require_bytes(aad, name="aad")
        with self._lock:
            key = self._live_key()
        if not isinstance(record, ProtectedRecord):
            raise TypeError("record must be a ProtectedRecord.")
        if (
            record.version != DATA_PLANE_VERSION
            or record.session_id != self.context.session_id
            or record.profile != self.context.profile
            or record.algorithm != DATA_PLANE_ALGORITHM
            or record.context_hash != self.context.context_hash
        ):
            raise ValueError("Protected record does not belong to this data-plane context.")
        if record.nonce != nonce_for(record.direction, record.sequence_number):
            raise ValueError("Protected record nonce is structurally invalid.")

        internal_aad = canonical_data_plane_aad(
            self.context,
            record.direction,
            record.sequence_number,
            clean_aad,
            declared_application_aad_bytes=record.application_aad_bytes,
        )
        return decrypt_aes_256_gcm(
            key,
            record.nonce,
            record.ciphertext,
            record.tag,
            internal_aad,
        )

    def close(self) -> None:
        """Release the Python key reference; this does not claim memory zeroization."""

        with self._lock:
            self._key = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"ProtectedSession(algorithm={DATA_PLANE_ALGORITHM!r}, profile={self.context.profile!r}, "
            f"context_hash={self.context.context_hash.hex()!r}, closed={self.is_closed})"
        )
