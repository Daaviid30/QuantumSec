"""Establishment-to-data-plane adapter with explicit session-key ownership transfer."""

from data_protection import DATA_PLANE_KEY_BITS, DataPlaneContext, ProtectedSession
from orchestration.result import EstablishedKeyType, SessionResult, SessionStatus


def open_data_plane(session: SessionResult) -> ProtectedSession:
    """Transfer one established 256-bit session key into an AES-GCM runtime capability."""

    if not isinstance(session, SessionResult):
        raise TypeError("session must be a SessionResult.")
    if session.status is not SessionStatus.ESTABLISHED:
        raise RuntimeError("Data plane requires an established session.")
    if session.is_closed:
        raise RuntimeError("Session key capability is already closed.")
    if session.established_key_type is not EstablishedKeyType.SESSION_KEY:
        raise ValueError(
            "AES-256-GCM data plane requires EstablishedKeyType.SESSION_KEY; "
            "QKD_BITSTRING needs an explicit application-key schedule."
        )
    if session.established_key_bits != DATA_PLANE_KEY_BITS:
        raise ValueError(f"AES-256-GCM data plane requires exactly {DATA_PLANE_KEY_BITS} key bits.")

    context = DataPlaneContext(
        session_id=session.session_id,
        profile=session.profile.value,
        session_result_version=session.version,
        key_type=session.established_key_type.value,
        key_bits=session.established_key_bits,
        public_context=session.public_context,
    )
    key = session.export_session_key()
    protected = ProtectedSession(key, context)
    session.close()
    return protected
