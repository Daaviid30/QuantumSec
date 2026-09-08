"""Deterministic, non-interactive figures for the thesis campaign."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

_COLORS = ("#264653", "#2A9D8F", "#E9C46A", "#E76F51", "#457B9D")


def generate_all(summaries: Mapping[str, Sequence[Mapping[str, object]]], root: Path) -> None:
    _plot_e1(summaries["e1"], root / "e1" / "figures")
    _plot_e2(summaries["e2"], root / "e2" / "figures")
    _plot_e3(summaries["e3"], root / "e3" / "figures")
    _plot_e4(summaries["e4"], root / "e4" / "figures")
    _plot_e5(summaries["e5"], root / "e5" / "figures")


def _style() -> None:
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "axes.axisbelow": True,
        }
    )


def _save(fig: Figure, directory: Path, name: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(directory / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(directory / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _numbers(rows: Sequence[Mapping[str, object]], key: str) -> list[float]:
    return [_number(row.get(key), key) for row in rows]


def _number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric for plotting.")
    return float(value)


def _plot_e1(rows: Sequence[Mapping[str, object]], directory: Path) -> None:
    _style()
    operations = (
        ("ml_kem_keygen", "ML-KEM keygen"),
        ("hqc_keygen", "HQC keygen"),
        ("server_offer_sign", "Offer sign"),
        ("server_offer_verify", "Offer verify"),
        ("ml_kem_encapsulate", "ML-KEM encaps"),
        ("hqc_encapsulate", "HQC encaps"),
        ("client_exchange_sign", "Exchange sign"),
        ("client_exchange_verify", "Exchange verify"),
        ("ml_kem_decapsulate", "ML-KEM decaps"),
        ("hqc_decapsulate", "HQC decaps"),
        ("transcript_construction_hash", "Transcript/hash"),
        ("kem_combiner_encoding", "KEM encoding"),
        ("hkdf_session", "HKDF session"),
        ("hkdf_confirmation", "HKDF confirm"),
        ("finished_generation", "Finished gen"),
        ("finished_verification", "Finished verify"),
    )
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    y = np.arange(len(operations), dtype=float)
    height = 0.36
    for index, row in enumerate(rows):
        values = [_number(row.get(f"{field}_median_ns") or 0, field) / 1e6 for field, _ in operations]
        errors = [_number(row.get(f"{field}_iqr_ns") or 0, field) / 2e6 for field, _ in operations]
        ax.barh(
            y + (index - 0.5) * height,
            values,
            height,
            xerr=errors,
            label=str(row["profile"]),
            color=_COLORS[index],
        )
    ax.set_yticks(y, [label for _, label in operations])
    ax.set_xlabel("Median operation time (ms); error bar = IQR/2")
    ax.set_title("E1 exact PQC operation timings")
    ax.legend()
    _save(fig, directory, "e1_latency_breakdown")

    byte_fields = (
        ("kem_public_key_bytes_median", "Ephemeral KEM public keys"),
        ("kem_ciphertext_bytes_median", "KEM ciphertexts"),
        ("signature_bytes_median", "Signatures"),
        ("finished_bytes_median", "Finished"),
        ("canonical_protocol_bytes_median", "Canonical protocol objects"),
    )
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    x = np.arange(len(byte_fields))
    width = 0.8 / len(rows)
    for index, row in enumerate(rows):
        values = [_number(row.get(field), field) for field, _ in byte_fields]
        ax.bar(
            x + (index - (len(rows) - 1) / 2) * width,
            values,
            width,
            label=str(row["profile"]),
            color=_COLORS[index],
        )
    ax.set_xticks(x, [label for _, label in byte_fields], rotation=20, ha="right")
    ax.set_ylabel("Bytes per category")
    ax.set_title("E1 raw cryptographic material vs canonical protocol objects")
    ax.legend()
    _save(fig, directory, "e1_bytes_breakdown")


def _plot_e2(rows: Sequence[Mapping[str, object]], directory: Path) -> None:
    _style()
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(10.5, 4.5))
    observed = _numbers(rows, "aggregate_estimate")
    lower = np.maximum(0.0, np.asarray(observed) - np.asarray(_numbers(rows, "aggregate_lower")))
    upper = np.maximum(0.0, np.asarray(_numbers(rows, "aggregate_upper")) - np.asarray(observed))
    ax.errorbar(
        x, observed, yerr=np.vstack((lower, upper)), fmt="o", ms=3, capsize=2, label="Simulation, Wilson 95%"
    )
    ax.scatter(x, _numbers(rows, "theory_aggregate"), marker="x", color=_COLORS[3], label="Analytical")
    ax.set_xticks(x, [str(row["condition_id"]) for row in rows], rotation=70, ha="right")
    ax.set_ylabel("Aggregate QBER")
    ax.set_ylim(bottom=0)
    ax.set_title("E2 analytical model vs numerical simulation")
    ax.legend()
    _save(fig, directory, "e2_theory_vs_simulation")

    asymmetric = [
        row
        for row in rows
        if abs(_number(row.get("theory_z"), "theory_z") - _number(row.get("theory_x"), "theory_x")) > 1e-12
    ]
    x = np.arange(len(asymmetric))
    width = 0.38
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    ax.bar(x - width / 2, _numbers(asymmetric, "z_estimate"), width, label="Observed eZ", color=_COLORS[0])
    ax.bar(x + width / 2, _numbers(asymmetric, "x_estimate"), width, label="Observed eX", color=_COLORS[1])
    ax.scatter(x - width / 2, _numbers(asymmetric, "theory_z"), marker="x", color="black", label="Theory")
    ax.scatter(x + width / 2, _numbers(asymmetric, "theory_x"), marker="x", color="black")
    ax.set_xticks(x, [str(row["condition_id"]) for row in asymmetric], rotation=65, ha="right")
    ax.set_ylabel("Basis-specific QBER")
    ax.set_ylim(bottom=0)
    ax.set_title("E2 basis asymmetry")
    ax.legend()
    _save(fig, directory, "e2_basis_asymmetry")


def _plot_e3(rows: Sequence[Mapping[str, object]], directory: Path) -> None:
    _style()
    fractions = _numbers(rows, "intercept_fraction")
    observed = np.asarray(_numbers(rows, "qber_estimate"))
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.errorbar(
        fractions,
        observed,
        yerr=np.vstack(
            (
                np.maximum(0.0, observed - _numbers(rows, "qber_lower")),
                np.maximum(0.0, np.asarray(_numbers(rows, "qber_upper")) - observed),
            )
        ),
        fmt="o-",
        capsize=3,
        label="Simulation, Wilson 95%",
    )
    ax.plot(fractions, _numbers(rows, "theory_qber"), "--", color=_COLORS[3], label="Theory f/4")
    ax.set(
        xlabel="Intercepted fraction f",
        ylabel="Aggregate QBER",
        ylim=(0, None),
        title="E3 intercept-resend QBER",
    )
    ax.legend()
    _save(fig, directory, "e3_qber_vs_interception")

    probability = np.asarray(_numbers(rows, "abort_estimate"))
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.errorbar(
        fractions,
        probability,
        yerr=np.vstack(
            (
                np.maximum(0.0, probability - _numbers(rows, "abort_lower")),
                np.maximum(0.0, np.asarray(_numbers(rows, "abort_upper")) - probability),
            )
        ),
        fmt="o-",
        capsize=3,
        color=_COLORS[3],
    )
    ax.set(
        xlabel="Intercepted fraction f",
        ylabel="Abort probability",
        ylim=(0, 1.03),
        title="E3 protocol abort probability",
    )
    _save(fig, directory, "e3_abort_probability")

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    medians = np.asarray(_numbers(rows, "n_final_median"))
    ax.errorbar(
        fractions,
        medians,
        yerr=np.asarray(_numbers(rows, "n_final_iqr")) / 2,
        fmt="o-",
        capsize=3,
        color=_COLORS[1],
    )
    ax.set(
        xlabel="Intercepted fraction f",
        ylabel="Final key material (bits)",
        ylim=(0, None),
        title="E3 retained final material (aborts included as zero)",
    )
    _save(fig, directory, "e3_final_material")


def _plot_e4(rows: Sequence[Mapping[str, object]], directory: Path) -> None:
    _style()
    executed = [row for row in rows if bool(row["authentication_executed"])]
    labels = [str(row["profile"]) for row in executed]
    x = np.arange(len(executed))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(x, _numbers(executed, "evidence_bytes_median"), color=_COLORS[: len(executed)])
    ax.set_xticks(x, labels)
    ax.set(ylabel="Authentication evidence bytes", title="E4 executed authentication evidence")
    ax.text(0.02, 0.96, "QKD-ASSUMED: NOT EXECUTED", transform=ax.transAxes, va="top")
    _save(fig, directory, "e4_authentication_bytes")

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    values = np.asarray(_numbers(executed, "total_time_median_ns")) / 1e6
    errors = np.asarray(_numbers(executed, "total_time_iqr_ns")) / 2e6
    ax.bar(x, values, yerr=errors, capsize=4, color=_COLORS[: len(executed)])
    ax.set_xticks(x, labels)
    ax.set(ylabel="Authentication-specific time (ms)", title="E4 executed authentication software cost")
    ax.text(0.02, 0.96, "QKD-ASSUMED: NOT EXECUTED", transform=ax.transAxes, va="top")
    _save(fig, directory, "e4_authentication_time")

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.8))
    secret_rows = [row for row in executed if row.get("secret_bits_consumed_median") is not None]
    public_rows = [row for row in executed if row.get("public_key_provisioning_bytes_median") is not None]
    axes[0].bar(
        [str(row["profile"]) for row in secret_rows],
        _numbers(secret_rows, "secret_bits_consumed_median"),
        color=_COLORS[: len(secret_rows)],
    )
    axes[0].set_ylabel("Per-session secret bits consumed")
    axes[0].set_title("Secret consumption")
    axes[1].bar(
        [str(row["profile"]) for row in public_rows],
        _numbers(public_rows, "public_key_provisioning_bytes_median"),
        color=_COLORS[: len(public_rows)],
    )
    axes[1].set_ylabel("Provisioned public-key bytes")
    axes[1].set_title("Persistent identity material")
    for axis in axes:
        axis.tick_params(axis="x", rotation=15)
    _save(fig, directory, "e4_authentication_material")


def _plot_e5(rows: Sequence[Mapping[str, object]], directory: Path) -> None:
    _style()
    hybrid = [row for row in rows if row["hybrid_composition_median_ns"] is not None]
    labels = [str(row["profile"]) for row in hybrid]
    x = np.arange(len(hybrid))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    values = np.asarray(_numbers(hybrid, "hybrid_composition_median_ns")) / 1e6
    errors = np.asarray(_numbers(hybrid, "hybrid_composition_iqr_ns")) / 2e6
    ax.bar(x, values, yerr=errors, capsize=4, color=_COLORS[: len(hybrid)])
    ax.set_xticks(x, labels)
    ax.set(
        ylabel="Hybrid composition time (ms)", title="E5 local composition cost (excludes BB84 simulation)"
    )
    _save(fig, directory, "e5_hybrid_composition_time")

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(x, _numbers(hybrid, "extra_transmitted_bytes_median"), color=_COLORS[: len(hybrid)])
    ax.set_xticks(x, labels)
    ax.set(ylabel="Additional transmitted bytes", title="E5 hybrid Finished messages only")
    _save(fig, directory, "e5_hybrid_protocol_bytes")

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ratios = _numbers(hybrid, "overhead_ratio_median")
    ratio_errors = np.asarray(_numbers(hybrid, "overhead_ratio_iqr")) / 2
    ax.bar(x, ratios, yerr=ratio_errors, capsize=4, color=_COLORS[: len(hybrid)])
    ax.set_xticks(x, labels)
    ax.set(ylabel="Composition / PQC crypto ratio", ylim=(0, None), title="E5 marginal composition ratio")
    _save(fig, directory, "e5_overhead_ratio")
