import json
from pathlib import Path

import pytest

from experiments.analysis.thesis_v1 import (
    analyze_campaign,
    raw_hashes,
    secret_audit,
    summarize_e4,
    weighted_interval,
)


def _record(profile: str, metrics: dict[str, object], **extra: object) -> dict[str, object]:
    return {
        "profile": profile,
        "condition_id": str(extra.pop("condition_id", profile.lower())),
        "metrics": metrics,
        "result": extra.pop("result", {"status": "established"}),
        **extra,
    }


def _qkd(errors_z: int, trials_z: int, errors_x: int, trials_x: int, n_final: int = 10) -> dict[str, int]:
    return {
        "estimated_z_errors": errors_z,
        "estimated_z_trials": trials_z,
        "estimated_x_errors": errors_x,
        "estimated_x_trials": trials_x,
        "estimated_aggregate_errors": errors_z + errors_x,
        "estimated_aggregate_trials": trials_z + trials_x,
        "n_final": n_final,
    }


def _pqc(total: int, *, hqc: int | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "crypto_software_time_ns": total,
        "kem_public_key_bytes": 1,
        "kem_ciphertext_bytes": 2,
        "signature_bytes": 3,
        "finished_bytes": 4,
        "canonical_protocol_bytes": 5,
        "transcript_bytes": 6,
        "public_key_provisioning_bytes": 7,
        "serialized_transport_bytes": None,
    }
    operations = (
        "ml_kem_keygen",
        "server_offer_sign",
        "server_offer_verify",
        "ml_kem_encapsulate",
        "client_exchange_sign",
        "client_exchange_verify",
        "ml_kem_decapsulate",
        "transcript_construction_hash",
        "kem_combiner_encoding",
        "hkdf_session",
        "hkdf_confirmation",
        "finished_generation",
        "finished_verification",
    )
    result.update({f"{name}_time_ns": 1 for name in operations})
    for name in ("hqc_keygen", "hqc_encapsulate", "hqc_decapsulate"):
        result[f"{name}_time_ns"] = hqc
    return result


def _auth(executed: bool) -> tuple[dict[str, object], dict[str, object]]:
    outcome: dict[str, object] = {
        "qkd_classical": {
            "executed": executed,
            "verified": True if executed else None,
            "mechanism": "test" if executed else "assumed",
            "trust_assumption": "fixture",
        }
    }
    metric: dict[str, object] = {
        "authenticated_bytes": 10 if executed else 0,
        "evidence_bytes": 5 if executed else 0,
        "checkpoints": 1 if executed else 0,
        "generation_operations": 1 if executed else 0,
        "verification_operations": 1 if executed else 0,
        "generation_time_ns": 3 if executed else 0,
        "verification_time_ns": 2 if executed else 0,
        "total_time_ns": 5 if executed else 0,
        "secret_bits_consumed": 8 if executed else None,
        "public_key_provisioning_bytes": 9 if executed else None,
        "forgery_bound": "fixture" if executed else None,
    }
    return outcome, metric


def test_weighted_qber_pools_counts_instead_of_averaging_rates() -> None:
    records = [
        _record("QKD-ASSUMED", {"qkd": _qkd(1, 10, 0, 10)}),
        _record("QKD-ASSUMED", {"qkd": _qkd(9, 90, 0, 90)}),
    ]
    interval = weighted_interval(records, "estimated_z_errors", "estimated_z_trials")
    assert interval.successes == 10
    assert interval.trials == 100
    assert interval.estimate == pytest.approx(0.1)


def test_not_executed_authentication_is_null_not_zero() -> None:
    outcome, auth = _auth(False)
    rows = summarize_e4(
        [_record("QKD-ASSUMED", {"qkd_authentication": auth}, result={"authentication": outcome})]
    )
    assert rows[0]["authentication_executed"] is False
    assert rows[0]["total_time_median_ns"] is None
    assert rows[0]["evidence_bytes_median"] is None


def test_record_only_analysis_regenerates_outputs_without_mutating_raw(tmp_path: Path) -> None:
    root = tmp_path / "campaign"
    for name in ("e1", "e2", "e3", "e4", "e5", "d1"):
        (root / name).mkdir(parents=True)

    records: dict[str, list[dict[str, object]]] = {
        "e1": [
            _record("PQC-BASE", {"pqc": _pqc(100)}),
            _record("PQC-DIVERSE", {"pqc": _pqc(200, hqc=30)}),
        ],
        "e2": [
            _record(
                "QKD-ASSUMED",
                {"qkd": _qkd(0, 100, 0, 100)},
                condition_id="identity",
                config={"qkd_stages": [{"type": "identity"}]},
            ),
            _record(
                "QKD-ASSUMED",
                {"qkd": _qkd(0, 100, 16, 100)},
                condition_id="phase-flip-0.16",
                config={"qkd_stages": [{"type": "phase_flip", "p": 0.16}]},
            ),
        ],
        "e3": [
            _record(
                "QKD-ASSUMED",
                {"qkd": _qkd(0, 100, 0, 100)},
                condition_id="intercept-0.0",
                config={"qkd_stages": [{"type": "intercept_resend", "intercept_fraction": 0.0}]},
            )
        ],
        "e4": [],
        "e5": [
            _record("PQC-BASE", {"pqc": _pqc(100)}),
            _record("PQC-DIVERSE", {"pqc": _pqc(200, hqc=30)}),
        ],
    }
    for profile in ("QKD-ASSUMED", "QKD-CLASSICAL-AUTH", "QKD-PQC-AUTH"):
        executed = profile != "QKD-ASSUMED"
        outcome, auth = _auth(executed)
        if profile == "QKD-CLASSICAL-AUTH":
            auth["public_key_provisioning_bytes"] = None
        if profile == "QKD-PQC-AUTH":
            auth["secret_bits_consumed"] = None
        records["e4"].append(
            _record(profile, {"qkd_authentication": auth}, result={"authentication": outcome})
        )
    hybrid_metrics = {
        "encoding_time_ns": 1,
        "hkdf_session_time_ns": 1,
        "hkdf_confirmation_time_ns": 1,
        "finished_generation_time_ns": 1,
        "finished_verification_time_ns": 1,
        "finished_responder_bytes": 48,
        "finished_initiator_bytes": 48,
        "canonical_combiner_input_bytes": 100,
        "encoding_overhead_bytes": 20,
        "public_context_bytes": 30,
    }
    records["e5"].extend(
        [
            _record("HYBRID", {"pqc": _pqc(100), "hybrid": hybrid_metrics}),
            _record("HYBRID-DIVERSE", {"pqc": _pqc(200, hqc=30), "hybrid": hybrid_metrics}),
        ]
    )
    d1 = {
        "algorithm": "AES-256-GCM",
        "key_bits": 256,
        "sizes": {"plaintext_bytes": 4, "ciphertext_bytes": 4, "nonce_bytes": 12, "tag_bytes": 16},
        "round_trip_verified": True,
        "tamper_matrix": [
            {"scenario": name, "rejected": True, "exception": "InvalidTag"}
            for name in ("ciphertext_bit_flip", "tag_bit_flip", "aad_change")
        ],
    }
    for name in ("e1", "e2", "e3", "e4", "e5"):
        (root / name / "records.json").write_text(json.dumps(records[name]), encoding="utf-8")
        (root / name / "records.csv").write_text("fixture\n", encoding="utf-8")
    (root / "d1" / "records.json").write_text(json.dumps(d1), encoding="utf-8")
    (root / "d1" / "records.csv").write_text("fixture\n", encoding="utf-8")
    manifest = {
        "campaign_version": "fixture",
        "preset": "smoke",
        "environment": {},
        "expected_record_counts": {
            name: len(value) if isinstance(value, list) else 1 for name, value in records.items()
        }
        | {"d1": 1},
        "raw_sha256": raw_hashes(root),
    }
    (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    before = raw_hashes(root)

    analyze_campaign(root)

    assert raw_hashes(root) == before
    assert (root / "campaign_report.md").is_file()
    assert len(tuple(root.glob("e*/figures/*.pdf"))) == 13
    assert len(tuple(root.glob("e*/figures/*.png"))) == 13
    assert secret_audit(root) == []


def test_secret_audit_rejects_secret_bearing_fields(tmp_path: Path) -> None:
    (tmp_path / "leak.json").write_text('{"k_session": "deadbeef"}', encoding="utf-8")
    assert secret_audit(tmp_path) == ["leak.json:k_session"]
