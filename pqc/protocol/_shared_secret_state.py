"""Private shared lifecycle and validation for staged-handshake KEM secret states."""

from dataclasses import dataclass, field
from types import TracebackType
from typing import Self

from pqc.kem import hqc_3_metadata, ml_kem_768_metadata
from pqc.profiles import PQCProfile, profile_definition
from pqc.protocol.messages import SERVER_KEY_OFFER_SESSION_ID_LENGTH, _require_bytes


@dataclass(slots=True, repr=False)
class _KEMSharedSecretStateBase:
    """Internal validated storage shared by initiator and responder secret states."""

    session_id: bytes = field(repr=False)
    profile: PQCProfile
    _ml_kem_shared_secret: bytes | None = field(repr=False)
    _hqc_shared_secret: bytes | None = field(default=None, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.profile, PQCProfile):
            raise TypeError(f"profile must be a PQCProfile. Got {type(self.profile).__name__}.")
        session_id = _require_bytes(
            self.session_id,
            name="session_id",
            length=SERVER_KEY_OFFER_SESSION_ID_LENGTH,
        )
        ml_kem_shared_secret = _require_bytes(
            self._ml_kem_shared_secret,
            name="ml_kem_shared_secret",
            length=ml_kem_768_metadata().shared_secret_length,
        )
        hqc_shared_secret: bytes | None = None
        if self.profile is PQCProfile.LOW:
            if self._hqc_shared_secret is not None:
                raise ValueError("LOW shared-secret state must not contain an HQC shared secret.")
        else:
            if self._hqc_shared_secret is None:
                raise ValueError("HIGH shared-secret state must contain an HQC shared secret.")
            hqc_shared_secret = _require_bytes(
                self._hqc_shared_secret,
                name="hqc_shared_secret",
                length=hqc_3_metadata().shared_secret_length,
            )

        self.session_id = session_id
        self._ml_kem_shared_secret = ml_kem_shared_secret
        self._hqc_shared_secret = hqc_shared_secret

    @property
    def is_closed(self) -> bool:
        """Return whether the private shared-secret references were released."""

        return self._closed

    def close(self) -> None:
        """Release secret references idempotently without claiming memory zeroization."""

        self._ml_kem_shared_secret = None
        self._hqc_shared_secret = None
        self._closed = True

    def __enter__(self) -> Self:
        """Enter a managed lifetime for this private state."""

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release secret references when leaving a managed lifetime."""

        self.close()

    def __repr__(self) -> str:
        algorithms = profile_definition(self.profile).kem_algorithms
        return (
            f"{type(self).__name__}(profile={self.profile.value!r}, "
            f"algorithms={algorithms!r}, closed={self._closed!r})"
        )
