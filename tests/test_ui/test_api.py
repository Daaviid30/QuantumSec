import pytest
from fastapi.testclient import TestClient

from ui.backend.main import app

client = TestClient(app)


def test_health_endpoint_reports_service_version():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "quantumsec-ui"


def test_capabilities_expose_real_and_planned_features_distinctly():
    response = client.get("/api/capabilities")

    assert response.status_code == 200
    body = response.json()
    protocols = {protocol["id"]: protocol for protocol in body["protocols"]}
    channels = {channel["id"]: channel for channel in body["channels"]}
    adversaries = {adversary["id"]: adversary for adversary in body["adversaries"]}
    features = {feature["id"]: feature for feature in body["features"]}

    assert protocols["bb84"]["implemented"] is True
    assert protocols["e91"]["implemented"] is False
    assert set(channels) == {
        "identity",
        "depolarizing",
        "bit_flip",
        "phase_flip",
        "amplitude_damping",
        "pauli",
    }
    assert set(adversaries) == {"intercept_resend"}
    assert adversaries["intercept_resend"]["implemented"] is True
    assert features["sifting"]["implemented"] is True
    assert features["parameter_estimation"]["implemented"] is True
    assert features["reconciliation"]["implemented"] is True
    assert features["verification"]["implemented"] is True
    assert features["privacy_amplification"]["implemented"] is True
    assert features["intercept_resend"]["implemented"] is True


def test_bb84_endpoint_is_reproducible_and_returns_real_result_data():
    payload = {
        "protocol": "bb84",
        "n_signals": 128,
        "seed": 88,
        "channels": [{"type": "depolarizing", "p": 0.12}],
    }

    first = client.post("/api/simulations/bb84", json=payload)
    second = client.post("/api/simulations/bb84", json=payload)

    assert first.status_code == second.status_code == 200
    first_body = first.json()
    second_body = second.json()
    assert first_body["metrics"] == second_body["metrics"]
    assert first_body["postprocessing"] == second_body["postprocessing"]
    assert first_body["alice_basis_counts"] == second_body["alice_basis_counts"]
    assert first_body["bob_basis_counts"] == second_body["bob_basis_counts"]
    assert first_body["bob_outcome_counts"] == second_body["bob_outcome_counts"]
    assert first_body["transmissions"] == second_body["transmissions"]
    assert first_body["metrics"]["n_raw"] == 128
    assert {"qber_z", "qber_x", "qber_aggregated"} <= first_body["metrics"].keys()
    assert first_body["postprocessing"]["n_disclosed"] > 0
    assert {
        "estimated_qber_z",
        "estimated_qber_x",
        "estimated_qber_aggregated",
        "phase_error_bound",
    } <= first_body["postprocessing"].keys()
    assert "n_final" in first_body["postprocessing"]
    assert first_body["channels"] == [
        {
            "stage_kind": "channel",
            "type": "depolarizing",
            "name": "Depolarizing",
            "parameters": {"p": 0.12},
        }
    ]
    assert first_body["attack_diagnostics"] == []


def test_completed_bb84_response_exposes_the_exact_final_simulator_key():
    response = client.post(
        "/api/simulations/bb84",
        json={"protocol": "bb84", "n_signals": 256, "seed": 2026, "channels": []},
    )

    assert response.status_code == 200
    postprocessing = response.json()["postprocessing"]
    assert postprocessing["status"] == "completed"
    assert len(postprocessing["final_key"]) == postprocessing["n_final"]
    assert set(postprocessing["final_key"]) <= {"0", "1"}


def test_aborted_bb84_response_exposes_reason_and_no_final_key():
    response = client.post(
        "/api/simulations/bb84",
        json={"protocol": "bb84", "n_signals": 1, "seed": 3, "channels": []},
    )

    assert response.status_code == 200
    postprocessing = response.json()["postprocessing"]
    assert postprocessing["status"] == "aborted"
    assert postprocessing["abort_reason"]
    assert postprocessing["final_key"] is None


def test_bb84_request_validation_rejects_invalid_signal_count():
    response = client.post(
        "/api/simulations/bb84",
        json={"protocol": "bb84", "n_signals": 0, "seed": 4, "channels": []},
    )

    assert response.status_code == 422


def test_channel_probability_validation_rejects_invalid_values():
    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 16,
            "seed": 4,
            "channels": [{"type": "amplitude_damping", "gamma": 1.1}],
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize("intercept_fraction", [-0.01, 1.01])
def test_intercept_resend_configuration_rejects_invalid_fraction(intercept_fraction):
    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 16,
            "seed": 4,
            "channels": [{"type": "intercept_resend", "intercept_fraction": intercept_fraction}],
        },
    )

    assert response.status_code == 422


def test_pauli_configuration_rejects_probability_sum_above_one():
    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 16,
            "seed": 4,
            "channels": [{"type": "pauli", "px": 0.5, "py": 0.4, "pz": 0.2}],
        },
    )

    assert response.status_code == 422


def test_channel_pipeline_order_is_preserved_in_response():
    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 32,
            "seed": 9,
            "channels": [
                {"type": "bit_flip", "p": 0.1},
                {"type": "phase_flip", "p": 0.2},
            ],
        },
    )

    assert response.status_code == 200
    assert [channel["type"] for channel in response.json()["channels"]] == ["bit_flip", "phase_flip"]


def test_intercept_resend_api_is_seeded_and_exposes_isolated_diagnostics():
    payload = {
        "protocol": "bb84",
        "n_signals": 512,
        "seed": 823,
        "channels": [{"type": "intercept_resend", "intercept_fraction": 0.6}],
    }

    first = client.post("/api/simulations/bb84", json=payload)
    second = client.post("/api/simulations/bb84", json=payload)

    assert first.status_code == second.status_code == 200
    first_body = first.json()
    second_body = second.json()
    assert first_body["metrics"] == second_body["metrics"]
    assert first_body["postprocessing"] == second_body["postprocessing"]
    assert first_body["transmissions"] == second_body["transmissions"]
    assert first_body["attack_diagnostics"] == second_body["attack_diagnostics"]
    assert first_body["channels"] == [
        {
            "stage_kind": "adversary",
            "type": "intercept_resend",
            "name": "Eve: intercept-resend",
            "parameters": {"intercept_fraction": 0.6},
        }
    ]
    diagnostics = first_body["attack_diagnostics"][0]
    assert diagnostics["stage_index"] == 0
    assert diagnostics["attack_type"] == "intercept_resend"
    assert diagnostics["intercept_fraction"] == 0.6
    assert diagnostics["n_signals_seen"] == 512
    assert 0 < diagnostics["n_intercepted"] < 512
    assert (
        diagnostics["eve_z_measurements"] + diagnostics["eve_x_measurements"] == diagnostics["n_intercepted"]
    )
    assert diagnostics["eve_zero_outcomes"] + diagnostics["eve_one_outcomes"] == diagnostics["n_intercepted"]


def test_attack_and_noise_order_is_preserved_in_response_and_diagnostics():
    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 64,
            "seed": 19,
            "channels": [
                {"type": "depolarizing", "p": 0.08},
                {"type": "intercept_resend", "intercept_fraction": 0.4},
                {"type": "phase_flip", "p": 0.05},
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert [stage["type"] for stage in body["channels"]] == [
        "depolarizing",
        "intercept_resend",
        "phase_flip",
    ]
    assert [stage["stage_kind"] for stage in body["channels"]] == [
        "channel",
        "adversary",
        "channel",
    ]
    assert body["attack_diagnostics"][0]["stage_index"] == 1
