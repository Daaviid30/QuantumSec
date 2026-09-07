"""Ordered, bounded, public trace contracts shared by every session profile."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

SESSION_TRACE_VERSION: Final = 1


class SessionTraceSource(StrEnum):
    SESSION = "session"
    QKD = "qkd"
    PQC = "pqc"
    HYBRID = "hybrid"


@dataclass(frozen=True, slots=True)
class SessionTraceEvent:
    sequence: int
    source: SessionTraceSource
    stage: str
    state: str
    detail: str

    def __post_init__(self) -> None:
        if isinstance(self.sequence, bool) or not isinstance(self.sequence, int) or self.sequence < 0:
            raise ValueError("sequence must be a non-negative integer.")
        if not isinstance(self.source, SessionTraceSource):
            raise TypeError("source must be a SessionTraceSource.")
        for name in ("stage", "state", "detail"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class SessionTrace:
    events: tuple[SessionTraceEvent, ...]
    version: int = SESSION_TRACE_VERSION

    def __post_init__(self) -> None:
        if self.version != SESSION_TRACE_VERSION:
            raise ValueError(f"version must be {SESSION_TRACE_VERSION}.")
        events = tuple(self.events)
        if not events or not all(isinstance(event, SessionTraceEvent) for event in events):
            raise ValueError("events must contain at least one SessionTraceEvent.")
        if tuple(event.sequence for event in events) != tuple(range(len(events))):
            raise ValueError("Trace sequence numbers must be contiguous and start at zero.")
        object.__setattr__(self, "events", events)

    def to_public_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "events": tuple(
                {
                    "sequence": event.sequence,
                    "source": event.source.value,
                    "stage": event.stage,
                    "state": event.state,
                    "detail": event.detail,
                }
                for event in self.events
            ),
        }


class SessionTraceBuilder:
    """Execution-local append-only builder that produces an immutable trace."""

    __slots__ = ("_events",)

    def __init__(self) -> None:
        self._events: list[SessionTraceEvent] = []

    def append(self, source: SessionTraceSource, stage: str, state: str, detail: str) -> None:
        self._events.append(SessionTraceEvent(len(self._events), source, stage, state, detail))

    def freeze(self) -> SessionTrace:
        return SessionTrace(tuple(self._events))
