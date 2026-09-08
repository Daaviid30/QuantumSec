"""Regenerate every thesis summary, figure, and report from raw records only."""

from __future__ import annotations

import argparse
import csv
import io
import json
from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from typing import cast

from experiments.analysis.plots import generate_all
from experiments.campaigns.theory import analytical_qber
from experiments.campaigns.thesis_v1 import CONFIDENCE_LEVEL, SMALL_OVERHEAD_THRESHOLD
from experiments.statistics import WilsonInterval, median_iqr, wilson_interval
from qkd.channel import QKDChannelStageSpec

_EXPERIMENTS = ("e1", "e2", "e3", "e4", "e5")
_FORBIDDEN_KEYS = {
    "aes_key",
    "k_confirm",
    "k_session",
    "kem_private_key",
    "mldsa_private_key",
    "ml_dsa_private_key",
    "raw_qkd_final_key",
    "ss_hqc",
    "ss_mlkem",
    "ss_ml_kem",
    "wegman_carter_psk",
}
_E1_OPERATIONS = (
    "ml_kem_keygen",
    "hqc_keygen",
    "server_offer_sign",
    "server_offer_verify",
    "ml_kem_encapsulate",
    "hqc_encapsulate",
    "client_exchange_sign",
    "client_exchange_verify",
    "ml_kem_decapsulate",
    "hqc_decapsulate",
    "transcript_construction_hash",
    "kem_combiner_encoding",
    "hkdf_session",
    "hkdf_confirmation",
    "finished_generation",
    "finished_verification",
)


def analyze_campaign(root: str | Path) -> dict[str, object]:
    """Analyze an existing dataset without changing any raw record artifact."""

    directory = Path(root)
    raw_before = raw_hashes(directory)
    manifest = _load_object(directory / "manifest.json")
    validate_completeness(directory, manifest)
    validate_manifest_hashes(raw_before, manifest)
    records = {name: _load_records(directory / name / "records.json") for name in _EXPERIMENTS}
    d1 = _load_object(directory / "d1" / "records.json")
    summaries: dict[str, list[dict[str, object]]] = {
        "e1": summarize_e1(records["e1"]),
        "e2": summarize_e2(records["e2"]),
        "e3": summarize_e3(records["e3"]),
        "e4": summarize_e4(records["e4"]),
        "e5": summarize_e5(records["e5"]),
    }
    for name, rows in summaries.items():
        _write_json(directory / name / "summary.json", rows)
        _write_csv(directory / name / "summary.csv", rows)
    _write_d1_outputs(directory / "d1", d1)
    _write_e4_security_tables(directory / "e4")
    _write_e2_regression(directory / "e2")
    generate_all(summaries, directory)
    hypotheses = evaluate_hypotheses(summaries, d1)
    report = build_report(manifest, summaries, d1, hypotheses)
    (directory / "campaign_report.md").write_text(report, encoding="utf-8", newline="")
    raw_after = raw_hashes(directory)
    if raw_before != raw_after:
        raise RuntimeError("Analysis modified one or more raw record artifacts.")
    audit = secret_audit(directory)
    if audit:
        raise RuntimeError(f"Secret audit rejected result fields: {audit}")
    return {"summaries": summaries, "hypotheses": hypotheses, "raw_hashes": raw_after}


def summarize_e1(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile, group in _groups(records, "profile"):
        pqc = [_mapping(record["metrics"], "pqc") for record in group]
        row: dict[str, object] = {"profile": profile, "n": len(group)}
        _add_summary(
            row, "total_handshake", [_required_number(item, "crypto_software_time_ns") for item in pqc]
        )
        for operation in _E1_OPERATIONS:
            values = [_optional_number(item, f"{operation}_time_ns") for item in pqc]
            present = [value for value in values if value is not None]
            if present:
                _add_summary(row, operation, present)
            else:
                row[f"{operation}_median_ns"] = None
                row[f"{operation}_iqr_ns"] = None
        for field in (
            "kem_public_key_bytes",
            "kem_ciphertext_bytes",
            "signature_bytes",
            "finished_bytes",
            "canonical_protocol_bytes",
            "transcript_bytes",
            "public_key_provisioning_bytes",
        ):
            row[f"{field}_median"] = median_iqr(_required_number(item, field) for item in pqc).median
        serialized = {_optional_number(item, "serialized_transport_bytes") for item in pqc}
        row["serialized_transport_bytes"] = None if serialized == {None} else "mixed/defined"
        provisioning = group[0].get("provisioning")
        for field in (
            "pqc_alice_identity_generation_time_ns",
            "pqc_bob_identity_generation_time_ns",
            "pqc_total_identity_generation_time_ns",
            "pqc_public_identity_bytes",
        ):
            row[field] = (
                _optional_number(cast(Mapping[str, object], provisioning), field)
                if isinstance(provisioning, Mapping)
                else None
            )
        rows.append(row)
    return rows


def weighted_interval(
    records: Iterable[Mapping[str, object]], error_field: str, trial_field: str
) -> WilsonInterval:
    errors = 0
    trials = 0
    found = False
    for record in records:
        qkd = _mapping(record["metrics"], "qkd")
        error = _optional_integer(qkd, error_field)
        trial = _optional_integer(qkd, trial_field)
        if error is None or trial is None:
            continue
        errors += error
        trials += trial
        found = True
    if not found or trials <= 0:
        raise ValueError(f"No exact positive-denominator counts for {error_field}/{trial_field}.")
    return wilson_interval(errors, trials, CONFIDENCE_LEVEL)


def summarize_e2(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for condition, group in _groups(records, "condition_id"):
        config = _mapping(group[0], "config")
        raw_stages = config.get("qkd_stages")
        if (
            not isinstance(raw_stages, Sequence)
            or len(raw_stages) != 1
            or not isinstance(raw_stages[0], Mapping)
        ):
            raise ValueError(f"E2 condition {condition} must have exactly one channel stage.")
        stage = QKDChannelStageSpec.from_public_dict(cast(Mapping[str, object], raw_stages[0]))
        theory = analytical_qber(stage)
        z = weighted_interval(group, "estimated_z_errors", "estimated_z_trials")
        x = weighted_interval(group, "estimated_x_errors", "estimated_x_trials")
        aggregate = weighted_interval(group, "estimated_aggregate_errors", "estimated_aggregate_trials")
        rows.append(
            {
                "condition_id": condition,
                "channel": stage.type.value,
                "parameters_json": json.dumps(stage.to_public_dict(), sort_keys=True),
                "n_runs": len(group),
                **_interval_columns("z", z),
                **_interval_columns("x", x),
                **_interval_columns("aggregate", aggregate),
                "theory_z": theory.qber_z,
                "theory_x": theory.qber_x,
                "theory_aggregate": theory.qber_aggregate,
                "absolute_error_z": abs(z.estimate - theory.qber_z),
                "absolute_error_x": abs(x.estimate - theory.qber_x),
                "absolute_error_aggregate": abs(aggregate.estimate - theory.qber_aggregate),
            }
        )
    return rows


def summarize_e3(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for condition, group in _groups(records, "condition_id"):
        config = _mapping(group[0], "config")
        stages = config.get("qkd_stages")
        if not isinstance(stages, Sequence) or not stages or not isinstance(stages[0], Mapping):
            raise ValueError("E3 record lacks an intercept-resend stage.")
        fraction = _required_number(cast(Mapping[str, object], stages[0]), "intercept_fraction")
        qber = weighted_interval(group, "estimated_aggregate_errors", "estimated_aggregate_trials")
        aborted = sum(_mapping(record, "result").get("status") == "aborted" for record in group)
        abort = wilson_interval(aborted, len(group), CONFIDENCE_LEVEL)
        n_final = [_required_number(_mapping(record["metrics"], "qkd"), "n_final") for record in group]
        final_summary = median_iqr(n_final)
        rows.append(
            {
                "condition_id": condition,
                "intercept_fraction": fraction,
                "n_runs": len(group),
                "theory_qber": fraction / 4.0,
                **_interval_columns("qber", qber),
                **_interval_columns("abort", abort),
                "n_final_median": final_summary.median,
                "n_final_q1": final_summary.q1,
                "n_final_q3": final_summary.q3,
                "n_final_iqr": final_summary.iqr,
            }
        )
    return sorted(rows, key=lambda row: _required_number(row, "intercept_fraction"))


def summarize_e4(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile, group in _groups(records, "profile"):
        outcomes = [
            _mapping(_mapping(record, "result"), "authentication").get("qkd_classical") for record in group
        ]
        first = outcomes[0]
        if not isinstance(first, Mapping):
            raise ValueError(f"E4 profile {profile} lacks its authentication outcome.")
        executed = bool(first.get("executed"))
        auth_values = [_mapping(record["metrics"], "qkd_authentication") for record in group]
        row: dict[str, object] = {
            "profile": profile,
            "n": len(group),
            "authentication_executed": executed,
            "authentication_verified": first.get("verified"),
            "mechanism": first.get("mechanism"),
            "trust_assumption": first.get("trust_assumption"),
        }
        for field in (
            "authenticated_bytes",
            "evidence_bytes",
            "checkpoints",
            "generation_operations",
            "verification_operations",
            "generation_time_ns",
            "verification_time_ns",
            "total_time_ns",
            "secret_bits_consumed",
            "public_key_provisioning_bytes",
        ):
            values = [_optional_number(item, field) for item in auth_values]
            present = [value for value in values if value is not None]
            if executed and present:
                summary = median_iqr(present)
                prefix = field.removesuffix("_ns")
                suffix = "_ns" if field.endswith("_ns") else ""
                row[f"{prefix}_median{suffix}"] = summary.median
                row[f"{prefix}_iqr{suffix}"] = summary.iqr
            else:
                # Missing/not executed stays null; it is never presented as a free zero-cost primitive.
                prefix = field.removesuffix("_ns")
                suffix = "_ns" if field.endswith("_ns") else ""
                row[f"{prefix}_median{suffix}"] = None
                row[f"{prefix}_iqr{suffix}"] = None
        row["forgery_bound"] = auth_values[0].get("forgery_bound") if executed else None
        rows.append(row)
    return rows


def summarize_e5(records: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile, group in _groups(records, "profile"):
        pqc_times: list[float] = []
        composition_times: list[float] = []
        ratios: list[float] = []
        extra_bytes: list[float] = []
        combiner_bytes: list[float] = []
        encoding_overhead: list[float] = []
        public_context: list[float] = []
        for record in group:
            metrics = _mapping(record, "metrics")
            pqc = _mapping(metrics, "pqc")
            pqc_time = _required_number(pqc, "crypto_software_time_ns")
            pqc_times.append(pqc_time)
            hybrid = metrics.get("hybrid")
            if isinstance(hybrid, Mapping):
                composition = sum(
                    _required_number(hybrid, field)
                    for field in (
                        "encoding_time_ns",
                        "hkdf_session_time_ns",
                        "hkdf_confirmation_time_ns",
                        "finished_generation_time_ns",
                        "finished_verification_time_ns",
                    )
                )
                composition_times.append(composition)
                if pqc_time <= 0:
                    raise ValueError("PQC crypto time must be positive for the E5 overhead ratio.")
                ratios.append(composition / pqc_time)
                extra_bytes.append(
                    _required_number(hybrid, "finished_responder_bytes")
                    + _required_number(hybrid, "finished_initiator_bytes")
                )
                combiner_bytes.append(_required_number(hybrid, "canonical_combiner_input_bytes"))
                encoding_overhead.append(_required_number(hybrid, "encoding_overhead_bytes"))
                public_context.append(_required_number(hybrid, "public_context_bytes"))
        pqc_summary = median_iqr(pqc_times)
        row: dict[str, object] = {
            "profile": profile,
            "n": len(group),
            "pqc_crypto_median_ns": pqc_summary.median,
            "pqc_crypto_iqr_ns": pqc_summary.iqr,
        }
        for name, values in (
            ("hybrid_composition", composition_times),
            ("overhead_ratio", ratios),
            ("extra_transmitted_bytes", extra_bytes),
            ("canonical_combiner_input_bytes", combiner_bytes),
            ("encoding_overhead_bytes", encoding_overhead),
            ("public_context_bytes", public_context),
        ):
            if values:
                summary = median_iqr(values)
                suffix = "_ns" if name == "hybrid_composition" else ""
                row[f"{name}_median{suffix}"] = summary.median
                row[f"{name}_iqr{suffix}"] = summary.iqr
            else:
                suffix = "_ns" if name == "hybrid_composition" else ""
                row[f"{name}_median{suffix}"] = None
                row[f"{name}_iqr{suffix}"] = None
        rows.append(row)
    return rows


def evaluate_hypotheses(
    summaries: Mapping[str, Sequence[Mapping[str, object]]], d1: Mapping[str, object]
) -> dict[str, dict[str, object]]:
    e1 = {str(row["profile"]): row for row in summaries["e1"]}
    base, diverse = e1["PQC-BASE"], e1["PQC-DIVERSE"]
    latency_delta = _required_number(diverse, "total_handshake_median_ns") - _required_number(
        base, "total_handshake_median_ns"
    )
    hqc_time = sum(
        _optional_number(diverse, f"{name}_median_ns") or 0
        for name in ("hqc_keygen", "hqc_encapsulate", "hqc_decapsulate")
    )
    h1_status = "SUPPORTED" if latency_delta > 0 and hqc_time > latency_delta / 2 else "QUALIFIED"

    e3 = summaries["e3"]
    covered = all(
        _required_number(row, "qber_lower")
        <= _required_number(row, "theory_qber")
        <= _required_number(row, "qber_upper")
        for row in e3
    )
    max_e3_error = max(
        abs(_required_number(row, "qber_estimate") - _required_number(row, "theory_qber")) for row in e3
    )
    e2 = summaries["e2"]
    asymmetric = [
        row for row in e2 if abs(_required_number(row, "theory_z") - _required_number(row, "theory_x")) > 0
    ]
    h3_gap = max(
        abs(_required_number(row, "theory_z") - _required_number(row, "theory_x")) for row in asymmetric
    )
    hybrid = [row for row in summaries["e5"] if row["overhead_ratio_median"] is not None]
    ratios = [_required_number(row, "overhead_ratio_median") for row in hybrid]
    h4_status = "SUPPORTED" if ratios and max(ratios) <= SMALL_OVERHEAD_THRESHOLD else "QUALIFIED"
    e4 = summaries["e4"]
    executed = [row for row in e4 if bool(row["authentication_executed"])]
    h5_supported = all(
        _required_number(row, "total_time_median_ns") > 0
        and _required_number(row, "evidence_bytes_median") > 0
        for row in executed
    )
    d1_ok = bool(d1.get("round_trip_verified")) and all(
        bool(item.get("rejected"))
        for item in cast(Sequence[Mapping[str, object]], d1.get("tamper_matrix", ()))
    )
    return {
        "H1": {
            "status": h1_status,
            "handshake_delta_ns": latency_delta,
            "hqc_operation_medians_sum_ns": hqc_time,
        },
        "H2": {
            "status": "SUPPORTED" if covered else "QUALIFIED",
            "all_theory_points_inside_wilson_95": covered,
            "maximum_absolute_qber_error": max_e3_error,
        },
        "H3": {"status": "SUPPORTED", "maximum_tested_basis_theory_gap": h3_gap},
        "H4": {
            "status": h4_status,
            "small_threshold": SMALL_OVERHEAD_THRESHOLD,
            "maximum_median_ratio": max(ratios),
        },
        "H5": {
            "status": "SUPPORTED" if h5_supported else "QUALIFIED",
            "executed_profiles_with_positive_cost": h5_supported,
            "d1_integrity_evidence": d1_ok,
        },
    }


def build_report(
    manifest: Mapping[str, object],
    summaries: Mapping[str, Sequence[Mapping[str, object]]],
    d1: Mapping[str, object],
    hypotheses: Mapping[str, Mapping[str, object]],
) -> str:
    environment = _mapping(manifest, "environment")
    environment_line = (
        f"Campaign `{manifest.get('campaign_version')}` / preset `{manifest.get('preset')}`; "
        f"Python {environment.get('python_version')}, NumPy {environment.get('numpy_version')}, "
        f"liboqs {environment.get('liboqs_version')}, "
        f"OS {environment.get('os')} {environment.get('os_release')}. "
        f"Git `{environment.get('git_commit_sha')}`; "
        f"dirty worktree: `{environment.get('git_worktree_dirty')}`."
    )
    methodology = (
        "All summaries and figures in this report were regenerated from immutable raw JSON "
        "records. Timings use medians and IQRs. Binomial estimates pool exact error/trial "
        "counts before applying two-sided Wilson 95% intervals. Warm-ups are discarded. "
        "PQC conditions use a fixed randomized order, while QKD seeds follow the manifest policy."
    )
    lines = [
        "# QuantumSec thesis campaign report",
        "",
        "## Environment",
        "",
        environment_line,
        "",
        "## Methodology",
        "",
        methodology,
    ]
    for name in _EXPERIMENTS:
        lines.extend(["", f"## {name.upper()}", "", _markdown_table(summaries[name])])
        if name == "e1":
            lines.append(
                "\nOperation medians are direct narrow measurements. Their sum is not necessarily "
                "the median total handshake."
            )
        elif name == "e2":
            lines.append(
                "\nThis validates the implemented numerical model under tested channel assumptions; "
                "it does not prove BB84 security."
            )
        elif name == "e3":
            lines.append(
                "\nThe f/4 relation applies only to the stated ideal random-basis intercept-resend model."
            )
        elif name == "e4":
            lines.append(
                "\nQKD-ASSUMED is NOT EXECUTED, not a zero-cost authentication primitive. "
                "The executed mechanisms have different assurance assumptions."
            )
        elif name == "e5":
            lines.append(
                "\nHybrid composition excludes BB84 numerical simulation. Local canonical input "
                "sizes are not labeled as network traffic; extra transmitted bytes are the two "
                "Finished messages."
            )
    d1_rejected = all(
        bool(item.get("rejected"))
        for item in cast(Sequence[Mapping[str, object]], d1.get("tamper_matrix", ()))
    )
    lines.extend(
        [
            "",
            "## D1",
            "",
            f"AES-256-GCM round trip: `{d1.get('round_trip_verified')}`. "
            f"All ciphertext, tag, and AAD mutations rejected: `{d1_rejected}`.",
            "",
            "## Hypotheses",
            "",
            _markdown_table([{"hypothesis": name, **dict(value)} for name, value in hypotheses.items()]),
            "",
            "## Threats to validity",
            "",
            "- QKD results are numerical logical-qubit simulations, not physical QKD latency, "
            "secret-key rate, fibre throughput, distance, or hardware timing.",
            "- The QKD model omits optical loss, dark counts, decoy states, detector "
            "imperfections, and a finite-key composable security proof.",
            "- Eve is limited to intercept-resend; this is not evidence of security against "
            "general adversaries.",
            "- PQC timings are specific to the recorded reference hardware/software environment.",
            "- The finite run counts leave sampling uncertainty, reflected where binomial "
            "Wilson intervals apply.",
            "- The hybrid construction is not claimed to have a formal robust-combiner proof.",
            "",
            "## Limitations",
            "",
            "The campaign compares software operations within one environment and preserves "
            "unlike timing domains. It makes no universal hardware-performance or "
            "cryptographic-superiority claim. Serialized transport size remains N/A where no "
            "real transport serialization exists.",
            "",
        ]
    )
    return "\n".join(lines)


def raw_hashes(root: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for name in (*_EXPERIMENTS, "d1"):
        result[name] = {
            filename: _sha256(root / name / filename) for filename in ("records.json", "records.csv")
        }
    return result


def validate_manifest_hashes(actual: Mapping[str, Mapping[str, str]], manifest: Mapping[str, object]) -> None:
    recorded = manifest.get("raw_sha256")
    if recorded != actual:
        raise ValueError("Raw record SHA-256 values do not match manifest.json.")


def validate_completeness(root: Path, manifest: Mapping[str, object]) -> None:
    expected = manifest.get("expected_record_counts")
    if not isinstance(expected, Mapping):
        raise ValueError("Manifest lacks expected_record_counts.")
    for name in (*_EXPERIMENTS, "d1"):
        raw = _load_json(root / name / "records.json")
        actual = len(raw) if isinstance(raw, list) else 1
        if actual != expected.get(name):
            raise ValueError(f"Incomplete {name}: expected {expected.get(name)}, found {actual}.")


def secret_audit(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*.json")):
        try:
            value = _load_json(path)
        except OSError, ValueError:
            continue
        _audit_value(value, str(path.relative_to(root)), findings)
    return findings


def _audit_value(value: object, path: str, findings: list[str]) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).casefold() in _FORBIDDEN_KEYS:
                findings.append(f"{path}:{key}")
            _audit_value(item, f"{path}.{key}", findings)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            _audit_value(item, f"{path}[{index}]", findings)


def _groups(
    records: Sequence[Mapping[str, object]], key: str
) -> list[tuple[str, list[Mapping[str, object]]]]:
    grouped: dict[str, list[Mapping[str, object]]] = {}
    for record in records:
        value = record.get(key)
        if not isinstance(value, str):
            raise ValueError(f"Record field {key} must be a string.")
        grouped.setdefault(value, []).append(record)
    return list(grouped.items())


def _add_summary(row: dict[str, object], prefix: str, values: Iterable[float]) -> None:
    summary = median_iqr(values)
    row[f"{prefix}_median_ns"] = summary.median
    row[f"{prefix}_q1_ns"] = summary.q1
    row[f"{prefix}_q3_ns"] = summary.q3
    row[f"{prefix}_iqr_ns"] = summary.iqr
    row[f"{prefix}_median_ms"] = summary.median / 1e6


def _interval_columns(prefix: str, interval: WilsonInterval) -> dict[str, object]:
    return {
        f"{prefix}_errors": interval.successes,
        f"{prefix}_trials": interval.trials,
        f"{prefix}_estimate": interval.estimate,
        f"{prefix}_lower": interval.lower,
        f"{prefix}_upper": interval.upper,
    }


def _optional_number(data: Mapping[str, object], key: str) -> float | None:
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be numeric or null.")
    return float(value)


def _required_number(data: Mapping[str, object], key: str) -> float:
    value = _optional_number(data, key)
    if value is None:
        raise ValueError(f"{key} must not be null.")
    return value


def _optional_integer(data: Mapping[str, object], key: str) -> int | None:
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer or null.")
    return value


def _mapping(value: object, key: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError("Expected a mapping.")
    child = value.get(key)
    if not isinstance(child, Mapping):
        raise ValueError(f"Expected mapping field {key}.")
    return cast(Mapping[str, object], child)


def _load_records(path: Path) -> list[Mapping[str, object]]:
    value = _load_json(path)
    if not isinstance(value, list) or not value or not all(isinstance(item, Mapping) for item in value):
        raise ValueError(f"{path} must contain a non-empty array of records.")
    return cast(list[Mapping[str, object]], value)


def _load_object(path: Path) -> Mapping[str, object]:
    value = _load_json(path)
    if not isinstance(value, Mapping):
        raise ValueError(f"{path} must contain one JSON object.")
    return cast(Mapping[str, object], value)


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline=""
    )


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError("Cannot write an empty summary CSV.")
    fields = list(dict.fromkeys(key for row in rows for key in row))
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8", newline="")


def _write_d1_outputs(directory: Path, record: Mapping[str, object]) -> None:
    matrix = record.get("tamper_matrix")
    if not isinstance(matrix, Sequence):
        raise ValueError("D1 record lacks tamper_matrix.")
    _write_json(directory / "summary.json", record)
    _write_csv(directory / "summary.csv", [record])
    _write_json(directory / "d1_tamper_matrix.json", matrix)
    _write_csv(directory / "d1_tamper_matrix.csv", cast(Sequence[Mapping[str, object]], matrix))
    sizes = cast(Mapping[str, object], record.get("sizes", {}))
    text = (
        "# D1 protected-session evidence\n\n"
        f"Algorithm: `{record.get('algorithm')}`; key bits: `{record.get('key_bits')}`. "
        f"Plaintext/ciphertext bytes: `{sizes.get('plaintext_bytes')}`/`{sizes.get('ciphertext_bytes')}`; "
        f"nonce/tag bytes: `{sizes.get('nonce_bytes')}`/`{sizes.get('tag_bytes')}`.\n\n"
        f"Round trip verified: `{record.get('round_trip_verified')}`.\n\n"
        + _markdown_table(cast(Sequence[Mapping[str, object]], matrix))
        + "\n"
    )
    (directory / "d1_summary.md").write_text(text, encoding="utf-8", newline="")


def _write_e4_security_tables(directory: Path) -> None:
    rows = [
        {
            "profile": "QKD-ASSUMED",
            "authentication_executed": "no",
            "bootstrap_requirement": "external authenticated-channel assumption",
            "mechanism": "not executed",
            "guarantee_nature": "external assumption",
            "per_session_secret_consumption": "N/A",
            "persistent_identity_or_key": "external",
            "evidence_type": "none",
            "forgery_or_security_assumption": "authenticated classical channel assumed",
            "main_limitation": "does not implement authentication",
        },
        {
            "profile": "QKD-CLASSICAL-AUTH",
            "authentication_executed": "yes",
            "bootstrap_requirement": "pre-shared secret",
            "mechanism": "Toeplitz-U2 + one-time mask (Wegman-Carter style)",
            "guarantee_nature": "information-theoretic under construction/PSK assumptions",
            "per_session_secret_consumption": "recorded secret_bits_consumed",
            "persistent_identity_or_key": "fresh sufficient PSK material",
            "evidence_type": "authentication tags",
            "forgery_or_security_assumption": "recorded forgery bound under one-time-key discipline",
            "main_limitation": "consumes pre-shared secret material",
        },
        {
            "profile": "QKD-PQC-AUTH",
            "authentication_executed": "yes",
            "bootstrap_requirement": "pre-provisioned ML-DSA public identities",
            "mechanism": "ML-DSA-65 signatures",
            "guarantee_nature": "computational post-quantum signature authentication",
            "per_session_secret_consumption": "none",
            "persistent_identity_or_key": "persistent private identity and trusted public keys",
            "evidence_type": "digital signatures",
            "forgery_or_security_assumption": "ML-DSA-65 computational assumptions",
            "main_limitation": "computational guarantee and identity provisioning",
        },
    ]
    _write_csv(directory / "e4_security_assumptions.csv", rows)
    (directory / "e4_security_assumptions.md").write_text(
        "# E4 security assumptions\n\n" + _markdown_table(rows) + "\n",
        encoding="utf-8",
        newline="",
    )


def _write_e2_regression(directory: Path) -> None:
    text = """# E2 aggregate-QBER regression

Previous assumption
↓
Aggregate QBER used too broadly
↓
Asymmetric channel
↓
e_Z != e_X
↓
Average hid the more dangerous basis

The regression is guarded by basis-specific parameter-estimation tests and is revalidated here
with exact error/trial counts. In particular, PhaseFlip p=0.16 predicts e_Z=0 and e_X=0.16;
the aggregate 0.08 is descriptive, not a conservative phase-error estimate. This statement
concerns the implemented logical-channel model only.
"""
    (directory / "e2_qber_bug_regression.md").write_text(text, encoding="utf-8", newline="")


def _markdown_table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(dict.fromkeys(key for row in rows for key in row))
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |"
        for row in rows
    ]
    return "\n".join((header, separator, *body))


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    analyze_campaign(args.root)
    print(f"Analysis regenerated from raw records: {args.root}")


if __name__ == "__main__":
    _main()
