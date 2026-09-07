import pytest

from pqc import (
    AuthenticatedKEMContributions,
    PQCProfile,
    issue_initiator_hybrid_contributions,
    issue_responder_hybrid_contributions,
)
from tests.test_pqc._handshake import create_phase5_flow, initiator_secret_state


def test_authenticated_contributions_are_single_use_and_close_source_states() -> None:
    flow = create_phase5_flow(PQCProfile.HIGH)
    initiator_state = initiator_secret_state(flow)
    responder_state = flow.processed_client_exchange.responder_state
    assert responder_state is not None
    alice = issue_initiator_hybrid_contributions(
        processed_server_offer=flow.processed_server_offer,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    bob = issue_responder_hybrid_contributions(
        processed_client_exchange=flow.processed_client_exchange,
        signed_server_offer=flow.signed_server_offer,
        signed_client_exchange=flow.signed_client_exchange,
    )
    assert initiator_state.is_closed and responder_state.is_closed
    assert tuple(item[0] for item in alice.consume()) == ("ML-KEM-768", "HQC-3")
    assert tuple(item[0] for item in bob.consume()) == ("ML-KEM-768", "HQC-3")
    with pytest.raises(RuntimeError, match="already consumed"):
        alice.consume()
    assert not hasattr(alice, "to_dict")
    assert "shared_secret" not in repr(alice)


def test_contribution_capability_cannot_be_claimed_without_protocol_proof() -> None:
    with pytest.raises(TypeError, match="authenticated PQC protocol"):
        AuthenticatedKEMContributions(b"0" * 16, PQCProfile.LOW, b"1" * 48, (), object())
