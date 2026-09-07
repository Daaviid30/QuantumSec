"""Runtime-only capabilities kept separate from reproducible public configuration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orchestration.authentication import (
        AuthenticationTransportHook,
        MLDSAAuthenticationContext,
        WegmanCarterAuthenticationContext,
    )
    from pqc.protocol import (
        PQCFinishedMessage,
        PQCParty,
        SignedClientKeyExchange,
        SignedServerKeyOffer,
    )
    from qkd.protocols import BB84Protocol

type QKDAuthenticationContext = MLDSAAuthenticationContext | WegmanCarterAuthenticationContext
type ServerOfferTransportHook = Callable[[SignedServerKeyOffer], SignedServerKeyOffer]
type ClientExchangeTransportHook = Callable[[SignedClientKeyExchange], SignedClientKeyExchange]
type PQCFinishedTransportHook = Callable[[PQCFinishedMessage], PQCFinishedMessage]
type HybridContributionHook = Callable[[str, tuple[tuple[str, bytes], ...]], tuple[tuple[str, bytes], ...]]
type HybridQKDContributionHook = Callable[[str, bytes, int], bytes]
type HybridFinishedTransportHook = Callable[[object], object]


@dataclass(slots=True, repr=False)
class SessionExecutionContext:
    """Non-serializable provisioned parties, QKD engine, secrets, and test boundaries."""

    qkd_protocol: BB84Protocol | None = field(default=None, repr=False)
    qkd_authentication: QKDAuthenticationContext | None = field(default=None, repr=False)
    pqc_initiator: PQCParty | None = field(default=None, repr=False)
    pqc_responder: PQCParty | None = field(default=None, repr=False)
    qkd_transport_hook: AuthenticationTransportHook | None = field(default=None, repr=False)
    server_offer_transport_hook: ServerOfferTransportHook | None = field(default=None, repr=False)
    client_exchange_transport_hook: ClientExchangeTransportHook | None = field(default=None, repr=False)
    pqc_finished_transport_hook: PQCFinishedTransportHook | None = field(default=None, repr=False)
    hybrid_contribution_hook: HybridContributionHook | None = field(default=None, repr=False)
    hybrid_qkd_contribution_hook: HybridQKDContributionHook | None = field(default=None, repr=False)
    hybrid_finished_transport_hook: HybridFinishedTransportHook | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        for name in (
            "qkd_transport_hook",
            "server_offer_transport_hook",
            "client_exchange_transport_hook",
            "pqc_finished_transport_hook",
            "hybrid_contribution_hook",
            "hybrid_qkd_contribution_hook",
            "hybrid_finished_transport_hook",
        ):
            hook = getattr(self, name)
            if hook is not None and not callable(hook):
                raise TypeError(f"{name} must be callable or None.")

    def __repr__(self) -> str:
        authentication_name = type(self.qkd_authentication).__name__ if self.qkd_authentication else None
        hooks = (
            self.qkd_transport_hook,
            self.server_offer_transport_hook,
            self.client_exchange_transport_hook,
            self.pqc_finished_transport_hook,
            self.hybrid_contribution_hook,
            self.hybrid_qkd_contribution_hook,
            self.hybrid_finished_transport_hook,
        )
        return (
            "SessionExecutionContext("
            f"qkd_protocol={self.qkd_protocol is not None}, "
            f"qkd_authentication={authentication_name!r}, "
            f"pqc_initiator={self.pqc_initiator.name if self.pqc_initiator else None!r}, "
            f"pqc_responder={self.pqc_responder.name if self.pqc_responder else None!r}, "
            f"transport_hooks_configured={any(hooks)})"
        )
