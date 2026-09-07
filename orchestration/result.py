"""Safe common terminal result and established-key capability."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final, Self

from orchestration.metrics import SessionMetrics
from orchestration.profiles import SessionProfile
from orchestration.qkd.transcript import QKD_CLASSICAL_SESSION_ID_LENGTH
from orchestration.trace import SessionTrace

SESSION_RESULT_VERSION: Final = 1


class SessionStatus(StrEnum):
    ESTABLISHED = "established"
    ABORTED = "aborted"
    FAILED = "failed"


class EstablishedKeyType(StrEnum):
    QKD_BITSTRING = "qkd_bitstring"
    SESSION_KEY = "session_key"


class EstablishedKeyCapability:
    """Private export boundary for accepted key bytes with exact bit-length metadata."""

    __slots__ = ("_closed", "_key", "bit_length", "key_type")

    def __init__(self, key: bytes, *, bit_length: int, key_type: EstablishedKeyType) -> None:
        if not isinstance(key, bytes) or not key:
            raise ValueError("key must be non-empty bytes.")
        if isinstance(bit_length, bool) or not isinstance(bit_length, int) or bit_length <= 0:
            raise ValueError("bit_length must be a positive integer.")
        if bit_length > len(key) * 8 or bit_length <= (len(key) - 1) * 8:
            raise ValueError("bit_length is inconsistent with the packed key byte length.")
        if not isinstance(key_type, EstablishedKeyType):
            raise TypeError("key_type must be an EstablishedKeyType.")
        self._key: bytes | None = bytes(key)
        self.bit_length = bit_length
        self.key_type = key_type
        self._closed = False

    @property
    def is_closed(self) -> bool:
        return self._closed

    def export(self) -> bytes:
        if self._closed or self._key is None:
            raise RuntimeError("Established key capability is closed.")
        return bytes(self._key)

    def close(self) -> None:
        self._key = None
        self._closed = True

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"EstablishedKeyCapability(key_type={self.key_type.value!r}, "
            f"bit_length={self.bit_length}, closed={self._closed})"
        )


@dataclass(frozen=True, slots=True)
class SecretProvenance:
    position: int
    source: str
    protocol: str
    algorithm: str
    encoding: str
    bit_length: int
    byte_length: int

    def __post_init__(self) -> None:
        if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position <= 0:
            raise ValueError("position must be a positive integer.")
        for name in ("source", "protocol", "algorithm", "encoding"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")
        if self.bit_length <= 0 or self.byte_length <= 0:
            raise ValueError("Provenance lengths must be positive.")


@dataclass(frozen=True, slots=True)
class AuthenticationOutcome:
    purpose: str
    mechanism: str
    algorithm: str
    executed: bool
    verified: bool | None
    trust_assumption: str

    def __post_init__(self) -> None:
        for name in ("purpose", "mechanism", "algorithm", "trust_assumption"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must be a non-empty string.")
        if not isinstance(self.executed, bool):
            raise TypeError("executed must be a bool.")
        if self.verified is not None and not isinstance(self.verified, bool):
            raise TypeError("verified must be bool or None.")
        if not self.executed and self.verified is not None:
            raise ValueError("Authentication not executed cannot claim a verification result.")


@dataclass(frozen=True, slots=True)
class SessionAuthentication:
    qkd_classical: AuthenticationOutcome | None = None
    pqc_exchange: AuthenticationOutcome | None = None

    def __post_init__(self) -> None:
        for value in (self.qkd_classical, self.pqc_exchange):
            if value is not None and not isinstance(value, AuthenticationOutcome):
                raise TypeError("Authentication summaries must contain AuthenticationOutcome values.")


@dataclass(frozen=True, slots=True, repr=False)
class SessionResult:
    version: int
    session_id: bytes = field(repr=False)
    profile: SessionProfile
    status: SessionStatus
    abort_reason: str | None
    provenance: tuple[SecretProvenance, ...]
    authentication: SessionAuthentication
    trace: SessionTrace
    metrics: SessionMetrics
    public_context: tuple[tuple[str, str | int], ...] = ()
    _key_capability: EstablishedKeyCapability | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.version != SESSION_RESULT_VERSION:
            raise ValueError(f"version must be {SESSION_RESULT_VERSION}.")
        if not isinstance(self.session_id, bytes) or len(self.session_id) != QKD_CLASSICAL_SESSION_ID_LENGTH:
            raise ValueError(f"session_id must contain {QKD_CLASSICAL_SESSION_ID_LENGTH} bytes.")
        if not isinstance(self.profile, SessionProfile):
            raise TypeError("profile must be a SessionProfile.")
        if not isinstance(self.status, SessionStatus):
            raise TypeError("status must be a SessionStatus.")
        if not isinstance(self.authentication, SessionAuthentication):
            raise TypeError("authentication must be a SessionAuthentication.")
        if not isinstance(self.trace, SessionTrace):
            raise TypeError("trace must be a SessionTrace.")
        if not isinstance(self.metrics, SessionMetrics):
            raise TypeError("metrics must be SessionMetrics.")
        provenance = tuple(self.provenance)
        if tuple(item.position for item in provenance) != tuple(range(1, len(provenance) + 1)):
            raise ValueError("Provenance positions must be contiguous and start at one.")
        if self.status is SessionStatus.ESTABLISHED:
            if self.abort_reason is not None or self._key_capability is None:
                raise ValueError("Established sessions require live key capability and no abort reason.")
        elif not self.abort_reason or self._key_capability is not None:
            raise ValueError("Non-established sessions must withhold key material and give a reason.")
        object.__setattr__(self, "session_id", bytes(self.session_id))
        object.__setattr__(self, "provenance", provenance)
        public_context = tuple(self.public_context)
        if len({key for key, _value in public_context}) != len(public_context):
            raise ValueError("public_context keys must be unique.")
        if not all(
            isinstance(key, str)
            and key.strip()
            and isinstance(value, (str, int))
            and not isinstance(value, bool)
            for key, value in public_context
        ):
            raise ValueError("public_context must contain non-empty string keys and string/int values.")
        object.__setattr__(self, "public_context", public_context)

    @property
    def established_key_bits(self) -> int:
        return self._key_capability.bit_length if self._key_capability is not None else 0

    @property
    def established_key_type(self) -> EstablishedKeyType | None:
        return self._key_capability.key_type if self._key_capability is not None else None

    def export_session_key(self) -> bytes:
        """Export accepted key bytes; QKD exact bit length remains in result metadata."""

        if self.status is not SessionStatus.ESTABLISHED or self._key_capability is None:
            raise RuntimeError("Session key material is withheld because the session is not established.")
        return self._key_capability.export()

    def close(self) -> None:
        if self._key_capability is not None:
            self._key_capability.close()

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "session_id": self.session_id.hex(),
            "profile": self.profile.value,
            "status": self.status.value,
            "abort_reason": self.abort_reason,
            "established_key": {
                "type": self.established_key_type.value if self.established_key_type else None,
                "bit_length": self.established_key_bits,
            },
            "provenance": tuple(
                {
                    "position": item.position,
                    "source": item.source,
                    "protocol": item.protocol,
                    "algorithm": item.algorithm,
                    "encoding": item.encoding,
                    "bit_length": item.bit_length,
                    "byte_length": item.byte_length,
                }
                for item in self.provenance
            ),
            "authentication": {
                "qkd_classical": _authentication_dict(self.authentication.qkd_classical),
                "pqc_exchange": _authentication_dict(self.authentication.pqc_exchange),
            },
            "public_context": dict(self.public_context),
            "trace": self.trace.to_public_dict(),
            "metrics": self.metrics.to_public_dict(),
        }

    def __repr__(self) -> str:
        return (
            f"SessionResult(version={self.version}, session_id={self.session_id.hex()!r}, "
            f"profile={self.profile.value!r}, status={self.status.value!r}, "
            f"abort_reason={self.abort_reason!r}, provenance_count={len(self.provenance)}, "
            f"established_key_type={self.established_key_type!r}, "
            f"established_key_bits={self.established_key_bits})"
        )


def _authentication_dict(outcome: AuthenticationOutcome | None) -> dict[str, object] | None:
    if outcome is None:
        return None
    return {
        "purpose": outcome.purpose,
        "mechanism": outcome.mechanism,
        "algorithm": outcome.algorithm,
        "executed": outcome.executed,
        "verified": outcome.verified,
        "trust_assumption": outcome.trust_assumption,
    }
