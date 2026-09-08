"""Canonical configuration matrix for the definitive thesis campaign."""

from __future__ import annotations

import argparse
import csv
import io
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Final

from experiments.config import EXPERIMENT_CONFIG_VERSION, ExperimentConfig, ExperimentKind
from experiments.d1 import D1Record, run_d1
from experiments.environment import ExperimentEnvironment
from experiments.export import export_csv, export_json
from experiments.record import EXPERIMENT_RECORD_VERSION
from experiments.runner import ExperimentRunner, run_batch
from experiments.runtime import ExperimentRuntimeFactory
from orchestration.config import SessionConfig
from orchestration.profiles import QKDProfile, SessionProfile
from qkd.channel import QKDChannelStageSpec, QKDChannelStageType

CAMPAIGN_VERSION: Final = "thesis-v1.0.1"
CONFIDENCE_LEVEL: Final = 0.95
SMALL_OVERHEAD_THRESHOLD: Final = 0.10
ORDER_SEEDS: Final = {"E1": 701_001, "E5": 705_001}


class CampaignPreset(StrEnum):
    SMOKE = "smoke"
    THESIS = "thesis"


@dataclass(frozen=True, slots=True)
class CampaignPlan:
    preset: CampaignPreset
    e1: tuple[ExperimentConfig, ...]
    e1_warmups: tuple[ExperimentConfig, ...]
    e2: tuple[ExperimentConfig, ...]
    e3: tuple[ExperimentConfig, ...]
    e4: tuple[ExperimentConfig, ...]
    e5: tuple[ExperimentConfig, ...]
    e5_warmups: tuple[ExperimentConfig, ...]
    d1: ExperimentConfig

    @property
    def expected_record_counts(self) -> dict[str, int]:
        return {
            "e1": len(self.e1),
            "e2": len(self.e2),
            "e3": len(self.e3),
            "e4": len(self.e4),
            "e5": len(self.e5),
            "d1": 1,
        }


def seed_for(kind: ExperimentKind, condition_index: int, replicate_index: int) -> int:
    """Map coordinates to a stable 64-bit seed without coupling experiments."""

    if not isinstance(kind, ExperimentKind):
        raise TypeError("kind must be an ExperimentKind.")
    for name, value in (("condition_index", condition_index), ("replicate_index", replicate_index)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer.")
    material = f"QuantumSec/{CAMPAIGN_VERSION}/{kind.value}/{condition_index}/{replicate_index}".encode()
    return int.from_bytes(sha256(material).digest()[:8], "big")


def build_campaign_plan(preset: CampaignPreset) -> CampaignPlan:
    if not isinstance(preset, CampaignPreset):
        raise TypeError("preset must be a CampaignPreset.")
    thesis = preset is CampaignPreset.THESIS
    e1_reps, e1_warmups = (50, 5) if thesis else (1, 1)
    qkd_reps, e3_reps, e4_reps, e5_reps = (10, 50, 30, 30) if thesis else (1, 1, 1, 1)
    e5_warmups = 3 if thesis else 1
    e2_signals = 20_000 if thesis else 512
    e3_signals = 10_000 if thesis else 512
    e4_signals = 8_192 if thesis else 1_024
    hybrid_signals = 4_096 if thesis else 1_024

    e1_profiles = (SessionProfile.PQC_BASE, SessionProfile.PQC_DIVERSE)
    e1 = tuple(
        _config(ExperimentKind.E1_PQC_COST, profile.value.lower(), replicate, profile)
        for profile in e1_profiles
        for replicate in range(e1_reps)
    )
    e1_warm = tuple(
        _config(ExperimentKind.E1_PQC_COST, f"{profile.value.lower()}-warmup", index, profile)
        for profile in e1_profiles
        for index in range(e1_warmups)
    )

    e2_conditions = _e2_conditions()
    e2 = tuple(
        _config(
            ExperimentKind.E2_BB84_VALIDATION,
            condition_id,
            replicate,
            SessionProfile.QKD_ASSUMED,
            signal_count=e2_signals,
            seed=seed_for(ExperimentKind.E2_BB84_VALIDATION, index, replicate),
            stages=(stage,),
        )
        for index, (condition_id, stage) in enumerate(e2_conditions)
        for replicate in range(qkd_reps)
    )

    fractions = tuple(index / 10.0 for index in range(11))
    e3 = tuple(
        _config(
            ExperimentKind.E3_INTERCEPT_RESEND,
            f"intercept-{fraction:.1f}",
            replicate,
            SessionProfile.QKD_ASSUMED,
            signal_count=e3_signals,
            seed=seed_for(ExperimentKind.E3_INTERCEPT_RESEND, index, replicate),
            stages=(
                QKDChannelStageSpec(
                    QKDChannelStageType.INTERCEPT_RESEND,
                    intercept_fraction=fraction,
                ),
            ),
        )
        for index, fraction in enumerate(fractions)
        for replicate in range(e3_reps)
    )

    e4_profiles = (
        SessionProfile.QKD_ASSUMED,
        SessionProfile.QKD_CLASSICAL_AUTH,
        SessionProfile.QKD_PQC_AUTH,
    )
    e4 = tuple(
        _config(
            ExperimentKind.E4_QKD_AUTHENTICATION,
            profile.value.lower(),
            replicate,
            profile,
            signal_count=e4_signals,
            # Paired design: the same replicate sees the same BB84 randomness.
            seed=seed_for(ExperimentKind.E4_QKD_AUTHENTICATION, 0, replicate),
            stages=(QKDChannelStageSpec(QKDChannelStageType.IDENTITY),),
        )
        for profile in e4_profiles
        for replicate in range(e4_reps)
    )

    e5_profiles = (
        SessionProfile.PQC_BASE,
        SessionProfile.PQC_DIVERSE,
        SessionProfile.HYBRID,
        SessionProfile.HYBRID_DIVERSE,
    )
    e5 = tuple(
        _e5_config(profile, replicate, hybrid_signals, warmup=False)
        for profile in e5_profiles
        for replicate in range(e5_reps)
    )
    e5_warm = tuple(
        _e5_config(profile, index, hybrid_signals, warmup=True)
        for profile in e5_profiles
        for index in range(e5_warmups)
    )
    d1 = _config(
        ExperimentKind.D1_PROTECTED_SESSION,
        "hybrid-diverse-aes-gcm",
        0,
        SessionProfile.HYBRID_DIVERSE,
        signal_count=hybrid_signals,
        seed=seed_for(ExperimentKind.D1_PROTECTED_SESSION, 0, 0),
        stages=(QKDChannelStageSpec(QKDChannelStageType.IDENTITY),),
        qkd_authentication_profile=QKDProfile.QKD_PQC_AUTH,
    )
    return CampaignPlan(preset, e1, e1_warm, e2, e3, e4, e5, e5_warm, d1)


def _config(
    kind: ExperimentKind,
    condition: str,
    replicate: int,
    profile: SessionProfile,
    *,
    signal_count: int | None = None,
    seed: int | None = None,
    stages: tuple[QKDChannelStageSpec, ...] = (),
    qkd_authentication_profile: QKDProfile | None = None,
) -> ExperimentConfig:
    return ExperimentConfig(
        experiment_kind=kind,
        condition_id=condition,
        replicate_index=replicate,
        session_config=SessionConfig(
            profile,
            qkd_authentication_profile=qkd_authentication_profile,
            qkd_signal_count=signal_count,
        ),
        seed=seed,
        qkd_stages=stages,
    )


def _e5_config(
    profile: SessionProfile,
    replicate: int,
    signal_count: int,
    *,
    warmup: bool,
) -> ExperimentConfig:
    hybrid = profile in {SessionProfile.HYBRID, SessionProfile.HYBRID_DIVERSE}
    condition = profile.value.lower() + ("-warmup" if warmup else "")
    return _config(
        ExperimentKind.E5_HYBRID_OVERHEAD,
        condition,
        replicate,
        profile,
        signal_count=signal_count if hybrid else None,
        seed=(
            seed_for(ExperimentKind.E5_HYBRID_OVERHEAD, list(SessionProfile).index(profile), replicate)
            if hybrid
            else None
        ),
        stages=(QKDChannelStageSpec(QKDChannelStageType.IDENTITY),) if hybrid else (),
        qkd_authentication_profile=QKDProfile.QKD_PQC_AUTH if hybrid else None,
    )


def _e2_conditions() -> tuple[tuple[str, QKDChannelStageSpec], ...]:
    conditions: list[tuple[str, QKDChannelStageSpec]] = [
        ("identity", QKDChannelStageSpec(QKDChannelStageType.IDENTITY))
    ]
    for value in (0.02, 0.05, 0.10, 0.15, 0.20, 0.25):
        conditions.append(
            (f"depolarizing-{value:.2f}", QKDChannelStageSpec(QKDChannelStageType.DEPOLARIZING, p=value))
        )
    for stage_type, label in (
        (QKDChannelStageType.BIT_FLIP, "bit-flip"),
        (QKDChannelStageType.PHASE_FLIP, "phase-flip"),
    ):
        for value in (0.02, 0.05, 0.10, 0.16, 0.20):
            conditions.append((f"{label}-{value:.2f}", QKDChannelStageSpec(stage_type, p=value)))
    for value in (0.02, 0.05, 0.10, 0.20, 0.30):
        conditions.append(
            (
                f"amplitude-damping-{value:.2f}",
                QKDChannelStageSpec(QKDChannelStageType.AMPLITUDE_DAMPING, gamma=value),
            )
        )
    for label, values in (
        ("pauli-symmetric", (0.02, 0.02, 0.02)),
        ("pauli-x-dominant", (0.08, 0.01, 0.02)),
        ("pauli-z-dominant", (0.02, 0.01, 0.08)),
    ):
        conditions.append(
            (label, QKDChannelStageSpec(QKDChannelStageType.PAULI, px=values[0], py=values[1], pz=values[2]))
        )
    assert len(conditions) == 25
    return tuple(conditions)


def execute_campaign(preset: CampaignPreset, output: str | Path) -> dict[str, object]:
    """Execute one fixed campaign, then invoke record-only analysis."""

    if not isinstance(preset, CampaignPreset):
        raise TypeError("preset must be a CampaignPreset.")
    destination = Path(output)
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"Refusing to mix a campaign with existing files: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("e1", "e2", "e3", "e4", "e5", "d1"):
        (destination / name).mkdir(exist_ok=True)

    plan = build_campaign_plan(preset)
    environment = ExperimentEnvironment.capture()
    factory = ExperimentRuntimeFactory()
    identities = factory.provision_pqc_identities()
    manifest = _manifest(plan, environment.to_public_dict(), identities.to_public_dict())
    _write_json(destination / "campaign_manifest.json", manifest)
    _write_json(destination / "manifest.json", manifest)
    _write_json(destination / "environment.json", environment.to_public_dict())

    runner = ExperimentRunner(factory)
    batches = (
        ("e1", plan.e1, True, ORDER_SEEDS["E1"], plan.e1_warmups),
        ("e2", plan.e2, False, None, ()),
        ("e3", plan.e3, False, None, ()),
        ("e4", plan.e4, False, None, ()),
        ("e5", plan.e5, True, ORDER_SEEDS["E5"], plan.e5_warmups),
    )
    for name, configs, shuffle, order_seed, warmups in batches:
        print(f"{name.upper()}: starting {len(configs)} recorded runs", flush=True)
        records = run_batch(
            configs,
            runner,
            shuffle=shuffle,
            order_seed=order_seed,
            warmup_configs=warmups,
            progress=_progress(name),
        )
        export_json(records, destination / name / "records.json")
        export_csv(records, destination / name / "records.csv")
        print(f"{name.upper()}: raw records written", flush=True)

    print("D1: establishing protected session and running tamper matrix", flush=True)
    d1_record = run_d1(plan.d1, factory)
    _write_json(destination / "d1" / "records.json", d1_record.to_public_dict())
    _write_d1_csv(destination / "d1" / "records.csv", d1_record)

    # Raw hashes and completion status are appended before analysis. Analysis verifies them
    # and never writes either raw artifact.
    from experiments.analysis.thesis_v1 import analyze_campaign, raw_hashes

    final_manifest = {
        **manifest,
        "execution_completed_utc": datetime.now(UTC).isoformat(),
        "raw_sha256": raw_hashes(destination),
        "status": "raw-records-complete",
    }
    _write_json(destination / "campaign_manifest.json", final_manifest)
    _write_json(destination / "manifest.json", final_manifest)
    result = analyze_campaign(destination)
    finalize_campaign(destination)
    print(f"Campaign complete: {destination}", flush=True)
    return result


def finalize_campaign(output: str | Path) -> dict[str, object]:
    """Verify raw integrity and required analysis artifacts, then seal the manifest."""

    from experiments.analysis.thesis_v1 import (
        raw_hashes,
        secret_audit,
        validate_completeness,
        validate_manifest_hashes,
    )

    destination = Path(output)
    manifest_value = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest_value, dict):
        raise ValueError("manifest.json must contain an object.")
    actual_hashes = raw_hashes(destination)
    validate_manifest_hashes(actual_hashes, manifest_value)
    validate_completeness(destination, manifest_value)
    findings = secret_audit(destination)
    if findings:
        raise RuntimeError(f"Secret audit rejected result fields: {findings}")
    pdf_count = len(tuple(destination.glob("e*/figures/*.pdf")))
    png_count = len(tuple(destination.glob("e*/figures/*.png")))
    if pdf_count != 13 or png_count != 13 or not (destination / "campaign_report.md").is_file():
        raise RuntimeError("Campaign analysis artifact inventory is incomplete.")
    complete = {
        **manifest_value,
        "analysis_completed_utc": datetime.now(UTC).isoformat(),
        "analysis_artifacts": {"pdf_figures": pdf_count, "png_figures": png_count},
        "secret_audit": "PASS",
        "status": "complete",
    }
    _write_json(destination / "campaign_manifest.json", complete)
    _write_json(destination / "manifest.json", complete)
    return complete


def _manifest(
    plan: CampaignPlan,
    environment: dict[str, object],
    identity_provisioning: dict[str, int],
) -> dict[str, object]:
    return {
        "campaign_version": CAMPAIGN_VERSION,
        "preset": plan.preset.value,
        "manifest_created_utc": datetime.now(UTC).isoformat(),
        "config_schema_version": EXPERIMENT_CONFIG_VERSION,
        "record_schema_version": EXPERIMENT_RECORD_VERSION,
        "environment": environment,
        "pqc_identity_provisioning": identity_provisioning,
        "expected_record_counts": plan.expected_record_counts,
        "experiments": {
            "e1": _experiment_manifest(plan.e1),
            "e2": _experiment_manifest(plan.e2),
            "e3": _experiment_manifest(plan.e3),
            "e4": _experiment_manifest(plan.e4),
            "e5": _experiment_manifest(plan.e5),
            "d1": _experiment_manifest((plan.d1,)),
        },
        "warmups": {
            "e1": len(plan.e1_warmups),
            "e5": len(plan.e5_warmups),
            "discarded": True,
        },
        "order_seeds": ORDER_SEEDS,
        "seed_generation_policy": (
            "uint64(first_8_bytes(SHA256('QuantumSec/thesis-v1.0.1/' + experiment + '/' + "
            "condition_index + '/' + replicate_index)), big-endian); E4 fixes condition_index=0 "
            "to pair BB84 streams across profiles"
        ),
        "confidence_level": CONFIDENCE_LEVEL,
        "confidence_interval": "two-sided Wilson score interval over pooled exact counts",
        "statistical_summaries": "median, q1, q3, IQR; no unweighted QBER pooling",
        "hypothesis_small_overhead_threshold": SMALL_OVERHEAD_THRESHOLD,
        "methodology_locked_before_execution": True,
        "raw_sha256": None,
        "status": "manifest-created-before-execution",
    }


def _experiment_manifest(configs: tuple[ExperimentConfig, ...]) -> dict[str, object]:
    conditions: dict[str, dict[str, object]] = {}
    replicate_counts: dict[str, int] = {}
    for config in configs:
        replicate_counts[config.condition_id] = replicate_counts.get(config.condition_id, 0) + 1
        conditions.setdefault(
            config.condition_id,
            {
                "profile": config.profile.value,
                "signal_count": config.session_config.qkd_signal_count,
                "qkd_authentication_profile": (
                    config.session_config.qkd_authentication_profile.value
                    if config.session_config.qkd_authentication_profile is not None
                    else None
                ),
                "qkd_stages": [stage.to_public_dict() for stage in config.qkd_stages],
            },
        )
    return {
        "recorded_runs": len(configs),
        "replicates_by_condition": replicate_counts,
        "conditions": conditions,
    }


def _progress(name: str):  # type: ignore[no-untyped-def]
    last = -1

    def report(done: int, total: int, _record: object) -> None:
        nonlocal last
        percentage = done * 100 // total
        bucket = percentage // 10
        if bucket != last or done == total:
            last = bucket
            print(f"{name.upper()}: {done}/{total}", flush=True)

    return report


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="",
    )


def _write_d1_csv(path: Path, record: D1Record) -> None:
    public = record.to_public_dict()
    sizes = public["sizes"]
    assert isinstance(sizes, dict)
    buffer = io.StringIO(newline="")
    fields = (
        "version",
        "timestamp_utc",
        "profile",
        "algorithm",
        "key_bits",
        "plaintext_bytes",
        "ciphertext_bytes",
        "nonce_bytes",
        "tag_bytes",
        "application_aad_bytes",
        "round_trip_verified",
        "tamper_matrix_json",
    )
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    config = public["config"]
    assert isinstance(config, dict)
    session_config = config["session"]
    assert isinstance(session_config, dict)
    writer.writerow(
        {
            "version": public["version"],
            "timestamp_utc": public["timestamp_utc"],
            "profile": session_config["profile"],
            "algorithm": public["algorithm"],
            "key_bits": public["key_bits"],
            **sizes,
            "round_trip_verified": public["round_trip_verified"],
            "tamper_matrix_json": json.dumps(public["tamper_matrix"], sort_keys=True),
        }
    )
    path.write_text(buffer.getvalue(), encoding="utf-8", newline="")


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=tuple(item.value for item in CampaignPreset), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    execute_campaign(CampaignPreset(args.preset), args.output)


if __name__ == "__main__":
    _main()
