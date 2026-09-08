import pytest
from fastapi.testclient import TestClient

from core.rng import BaseRNG, SeededRNG
from qkd.channel import InterceptResendAttack, QuantumChannel
from qkd.protocols import BB84Protocol
from ui.backend import adapters
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
    profiles = {profile["id"]: profile for profile in body["profiles"]}

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
    assert set(profiles) == {
        "QKD-ASSUMED",
        "QKD-CLASSICAL-AUTH",
        "QKD-PQC-AUTH",
        "PQC-BASE",
        "PQC-DIVERSE",
        "HYBRID",
        "HYBRID-DIVERSE",
    }
    assert all(profile["implemented"] for profile in profiles.values())
    assert profiles["QKD-ASSUMED"]["supports_data_plane"] is False
    assert profiles["HYBRID-DIVERSE"]["supports_data_plane"] is True


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


def test_completed_bb84_response_exposes_length_but_withholds_final_simulator_key():
    response = client.post(
        "/api/simulations/bb84",
        json={"protocol": "bb84", "n_signals": 256, "seed": 2026, "channels": []},
    )

    assert response.status_code == 200
    postprocessing = response.json()["postprocessing"]
    assert postprocessing["status"] == "completed"
    assert postprocessing["n_final"] > 0
    assert "final_key" not in postprocessing


def test_aborted_bb84_response_exposes_reason_and_no_secret_material():
    response = client.post(
        "/api/simulations/bb84",
        json={"protocol": "bb84", "n_signals": 1, "seed": 3, "channels": []},
    )

    assert response.status_code == 200
    postprocessing = response.json()["postprocessing"]
    assert postprocessing["status"] == "aborted"
    assert postprocessing["abort_reason"]
    assert "final_key" not in postprocessing


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


def test_backend_gives_protocol_and_each_eve_stage_independent_rng_streams(monkeypatch):
    attack_rngs: list[BaseRNG] = []
    protocol_rngs: list[BaseRNG] = []
    constructed_seeds: list[int] = []

    class TrackingSeededRNG(SeededRNG):
        def __init__(self, seed: int) -> None:
            constructed_seeds.append(seed)
            super().__init__(seed)

    class TrackingAttack(InterceptResendAttack):
        def __init__(self, intercept_fraction: float, rng: BaseRNG) -> None:
            attack_rngs.append(rng)
            super().__init__(intercept_fraction, rng)

    def tracking_protocol(*, channel: QuantumChannel, rng: BaseRNG) -> BB84Protocol:
        protocol_rngs.append(rng)
        return BB84Protocol(channel=channel, rng=rng)

    monkeypatch.setattr(adapters, "InterceptResendAttack", TrackingAttack)
    monkeypatch.setattr(adapters, "BB84Protocol", tracking_protocol)
    monkeypatch.setattr(adapters, "SeededRNG", TrackingSeededRNG)

    response = client.post(
        "/api/simulations/bb84",
        json={
            "protocol": "bb84",
            "n_signals": 64,
            "seed": 33,
            "channels": [
                {"type": "intercept_resend", "intercept_fraction": 0.3},
                {"type": "intercept_resend", "intercept_fraction": 0.7},
            ],
        },
    )

    assert response.status_code == 200
    assert len(protocol_rngs) == 1
    assert len(attack_rngs) == 2
    assert len({id(protocol_rngs[0]), *(id(rng) for rng in attack_rngs)}) == 3
    assert constructed_seeds[0] == 33
    assert len(set(constructed_seeds)) == 3


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


def test_session_api_records_real_qkd_trace_metrics_and_eve_diagnostics():
    response = client.post(
        "/api/sessions",
        json={
            "profile": "QKD-ASSUMED",
            "n_signals": 512,
            "seed": 823,
            "channels": [{"type": "intercept_resend", "intercept_fraction": 0.6}],
        },
    )

    assert response.status_code == 200
    body = response.json()
    record = body["record"]
    assert record["profile"] == "QKD-ASSUMED"
    assert record["result"]["authentication"]["qkd_classical"]["executed"] is False
    assert record["metrics"]["qkd"] is not None
    assert record["metrics"]["pqc"] is None
    assert [event["sequence"] for event in record["trace"]["events"]] == list(
        range(len(record["trace"]["events"]))
    )
    assert body["data_plane_available"] is False
    assert body["attack_diagnostics"][0]["n_intercepted"] > 0
    serialized = response.text.casefold()
    for forbidden in ("k_session", "k_confirm", "shared_secret", "private_key"):
        assert forbidden not in serialized


def test_run_list_and_compare_use_exactly_two_distinct_public_records():
    first = client.post(
        "/api/sessions",
        json={"profile": "QKD-ASSUMED", "n_signals": 512, "seed": 2026},
    ).json()
    second = client.post(
        "/api/sessions",
        json={"profile": "QKD-ASSUMED", "n_signals": 512, "seed": 2027},
    ).json()
    first_id = first["record"]["run_id"]
    second_id = second["record"]["run_id"]

    runs = client.get("/api/runs")
    comparison = client.post("/api/compare", json={"run_ids": [first_id, second_id]})
    duplicate = client.post("/api/compare", json={"run_ids": [first_id, first_id]})

    assert runs.status_code == 200
    assert {run["record"]["run_id"] for run in runs.json()["runs"]} >= {first_id, second_id}
    assert comparison.status_code == 200
    assert comparison.json()["compatibility"]["qkd_metrics"] is True
    assert comparison.json()["compatibility"]["pqc_timing"] is False
    assert duplicate.status_code == 422


def test_established_pqc_run_protects_payload_without_exporting_session_key():
    session = client.post("/api/sessions", json={"profile": "PQC-BASE"})

    assert session.status_code == 200
    body = session.json()
    assert body["record"]["result"]["status"] == "established"
    assert body["data_plane_available"] is True
    run_id = body["record"]["run_id"]
    protected = client.post(
        f"/api/runs/{run_id}/protect",
        json={"plaintext": "thesis demonstration", "aad": "QuantumSec/test"},
    )

    assert protected.status_code == 200
    result = protected.json()
    assert result["algorithm"] == "AES-256-GCM"
    assert result["round_trip_verified"] is True
    assert result["tamper_rejected"] is True
    assert "thesis demonstration" not in protected.text


@pytest.mark.parametrize(
    ("profile", "uses_qkd", "data_plane"),
    [
        ("QKD-ASSUMED", True, False),
        ("QKD-CLASSICAL-AUTH", True, False),
        ("QKD-PQC-AUTH", True, False),
        ("PQC-BASE", False, True),
        ("PQC-DIVERSE", False, True),
        ("HYBRID", True, True),
        ("HYBRID-DIVERSE", True, True),
    ],
)
def test_session_api_executes_every_current_public_profile(profile, uses_qkd, data_plane):
    payload = {"profile": profile}
    if uses_qkd:
        payload.update({"n_signals": 512, "seed": 2026})
    if profile.startswith("HYBRID"):
        payload["qkd_authentication_profile"] = "QKD-ASSUMED"

    response = client.post("/api/sessions", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["record"]["profile"] == profile
    assert body["record"]["result"]["status"] == "established"
    assert body["data_plane_available"] is data_plane
