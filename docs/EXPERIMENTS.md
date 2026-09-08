# Reproducible Experiment Engine V1

The experiment engine is a small execution and evidence layer. It observes the existing session
orchestration; it does not implement cryptography or replace protocol metrics.

```text
ExperimentConfig
      |
      v
runtime build (secrets and pre-provisioning stay here)
      |
      v
run_session() -> SessionResult
      |
      v
ExperimentRecord (copied public result + trace + categorized metrics)
      |
      +--> JSON
      `--> CSV --> record-only E1-E5/D1 analysis, figures, and report
```

## Configuration

`ExperimentConfig` version 1 contains `experiment_kind`, `condition_id`, `replicate_index`, the
normalized `SessionConfig`, the applicable simulation `seed`, ordered `qkd_stages`, and at most 16
short public tags. Unknown fields are rejected. QKD and hybrid profiles require a seed; PQC-only
profiles reject QKD stages and use `seed: null` because liboqs retains real cryptographic
randomness. JSON loaders also reject duplicate object keys. The engine rejects obvious label/profile
contradictions: E2-E4 require QKD, E3 additionally requires an `intercept_resend` stage, and
E1/E5/D1 require a PQC component.

The Pydantic-free `QKDChannelStageSpec` supports, in exact listed order, `identity`,
`depolarizing(p)`, `bit_flip(p)`, `phase_flip(p)`, `amplitude_damping(gamma)`,
`pauli(px, py, pz)`, and `intercept_resend(intercept_fraction)`. Both the HTTP adapter and experiment
runtime use the builder in `qkd.channel`; the experiment package never imports UI schemas. Eve RNG
streams are deterministically domain-separated from the BB84 protocol stream by root seed and
stage index.

## Runtime and secret lifecycle

`ExperimentRuntimeFactory` converts a public config into a non-serializable
`SessionExecutionContext`. PQC parties, ML-DSA identities, and peer trust are provisioned lazily and
reused by a factory. This happens before the session stopwatches. A QKD ML-DSA run reuses those
identities but gets a fresh anti-replay registry. A Wegman-Carter run receives fresh pre-shared
authentication material for each run. The factory uses a conservative capacity scaled by signal
count and Cascade passes, while storing PSK bytes in packed form; the public provisioning metadata
records only bytes provisioned per direction and `secret_bits_consumed`, never the material. For
PQC, the one-time Alice/Bob ML-DSA identity-generation durations and public identity bytes are
recorded explicitly as provisioning metadata and remain outside session handshake timing.

The generic runner never exports an established key. It copies `SessionResult.to_public_dict()`,
separates its result, trace, and metrics sections, freezes those copies, and closes the live
`SessionResult` in `finally`. Protocol `ABORTED` and expected operational `FAILED` outcomes remain
records. Invalid config and unexpected programming failures propagate as errors.

## Environment and record schema

Every run records a UUID4, timezone-aware UTC timestamp, config version, record version, seed,
condition/replicate, optional execution-order index, and an environment snapshot containing:

- Python version and implementation;
- NumPy, liboqs-python, liboqs, cryptography, and QuantumSec versions when available;
- OS name/release/version, machine architecture, and CPU identifier when available; and
- best-effort Git commit SHA and worktree-dirty state (nullable for source archives).

`ExperimentRecord.to_public_dict()` has stable top-level fields: `version`, `run_id`,
`experiment_kind`, `condition_id`, `replicate_index`, `batch`, `execution_order_index`,
`timestamp_utc`, `seed`, `profile`, `environment`, `config`, `provisioning`, `result`, `trace`, `metrics`, and
`artifact`. `artifact.experiment_record_json_bytes` is the standalone pretty-printed public JSON
object size, excluding an export file's final newline.

`result` includes only public session ID, profile, status/abort reason, key type/bit count,
provenance, authentication outcome, and public context. It has no key value. `trace` and `metrics`
are copied from their existing public serializers and checked against their stable root schemas.
Non-finite floats and explicitly secret-bearing field names are rejected as a second export barrier.

## Metrics and exports

Metrics remain in separate `qkd`, `pqc`, `qkd_authentication`, `pqc_authentication`, and `hybrid`
sections. QKD exports protocol estimates (`estimated_qber_z`, `estimated_qber_x`, aggregate and
phase-error bound), explicitly named simulator diagnostics, all material counts, sifting
efficiency, final secret fraction, exact Z/X/aggregate error and trial counts, transcript bytes,
and simulation software time. QKD simulation
runtime is not physical QKD performance and is never summed, ranked, or compared with PQC
cryptographic software time.

JSON is UTF-8, versioned, and pretty-printed. CSV has one row per run, a fixed union schema across
profiles, dotted numeric metric columns, and canonical JSON cells for config, ordered stages,
provenance, authentication, public context, and trace. Non-applicable metrics are empty, never zero.
The PQC record preserves phase totals and separately exposes narrow direct timings around actual
ML-KEM/HQC key generation, encapsulation and decapsulation, ML-DSA sign/verify, transcript/hash,
canonical KEM input, both HKDF derivations, and Finished generation/verification. No primitive
timing is inferred by subtracting phase totals. Raw cryptographic, canonical protocol, and actual
hybrid Finished-message sizes remain separate; serialized transport is `null` because no transport
serialization is defined.

## Batch and statistics

`run_batch` is sequential. `shuffle=True` requires a separate non-negative `order_seed`; it never
changes a config's BB84 seed. Every retained record shares versioned `batch` provenance containing
a UUID4 `batch_run_id`, `shuffle`, `order_seed`, and `warmup_runs`, and receives its own
`execution_order_index`. Explicit warm-ups execute before measurements and are discarded. No QKD
warm-up is automatic.

`median_iqr` returns `n`, median, quartiles, IQR, minimum, and maximum using NumPy's linear
percentile convention. `wilson_interval` returns a two-sided Wilson score interval (not exact
Clopper-Pearson) for QBER/abort proportions without adding SciPy.

## CLI

From the repository root:

```bash
uv run python -m experiments.cli run examples/experiments/qkd_eve_example.json \
  --output experiments/output/qkd-eve.json

uv run python -m experiments.cli batch configs.json \
  --shuffle --order-seed 2026 --warmup-runs 2 \
  --json experiments/output/records.json \
  --csv experiments/output/records.csv
```

Generated `experiments/output/` and `results/` trees are ignored. Selected thesis datasets can be
archived later by an explicit decision. The specialized D1 runner transfers the live established
key directly into the existing data plane, closes the session capability, and exports only public
sizes/outcomes. The generic runner still rejects D1 and never exports a key.

## Definitive campaign

`experiments.campaigns.thesis_v1` provides fixed `smoke` and `thesis` presets. Version
`thesis-v1.0.1` executed 100 E1, 250 E2, 550 E3, 90 E4, 120 E5, and one D1 record. The manifest is
written before execution and then sealed with raw JSON/CSV SHA-256 digests, expected/actual
completeness, figure inventory, and secret-audit status. PQC timing orders are randomized with
fixed order seeds; warm-ups and persistent identity provisioning are discarded/excluded from
session timings as declared.

```bash
uv run python -m experiments.campaigns.thesis_v1 \
  --preset smoke --output results/thesis_v1_smoke

uv run python -m experiments.campaigns.thesis_v1 \
  --preset thesis --output results/thesis_v1

uv run python -m experiments.analysis.thesis_v1 results/thesis_v1
```

The analysis command reads only `records.json`/`records.csv`, verifies their manifest hashes and
counts, and regenerates summaries, 13 figures in PDF/PNG, the E2 regression note, E4 security table,
D1 tamper matrix, and `campaign_report.md`. It never reruns cryptography or mutates raw records.
