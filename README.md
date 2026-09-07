# QuantumSec — Quantum-Safe Session Laboratory

QuantumSec is a modular and reproducible laboratory for executing, visualizing, and evaluating
quantum-safe session-establishment strategies based on QKD, post-quantum cryptography (PQC), and
hybrid QKD–PQC composition.

The web is the laboratory interface. Protocols and primitives are the systems under study.
Experiments are the evaluation method. The experimental results and their interpretation are the
academic contribution of the Master's thesis.

QuantumSec is not primarily an educational website, a collection of algorithms, an isolated QKD
simulator, or a demonstration that QKD and PQC can merely be combined.

## Status vocabulary

- **CURRENT** — implemented and tested.
- **PARTIAL** — executable, but a required capability or guarantee remains incomplete.
- **PLANNED** — required for the TFM, but not implemented.
- **FUTURE** — outside the TFM definition of done.

## Current repository status

| Area | Status | What exists |
|---|---|---|
| Core and quantum mathematics | **CURRENT** | Injected RNGs, immutable values, validation, linear algebra, information measures, and projective measurements |
| BB84 execution | **CURRENT** | Seeded logical-qubit simulation, channel pipeline, sifting, basis-stratified parameter estimation, Cascade, reconciled-key verification, asymptotic length estimation, Toeplitz privacy amplification, and explicit aborts |
| BB84 security estimator | **CURRENT, ASYMPTOTIC** | Per-basis `e_Z/e_X`, diagnostic aggregate QBER, an explicit mixed-basis phase-error bound, and conservative aborts; no composable finite-key claim |
| QKD classical-channel authentication | **CURRENT** | Explicit assumed baseline plus executed one-time Toeplitz/Wegman–Carter-style and ML-DSA-65 transcript-checkpoint profiles |
| PQC establishment | **CURRENT** | Mutually authenticated `PQC-BASE`/`PQC-DIVERSE` handshakes using ML-KEM-768, optional HQC-3, ML-DSA-65, structured KEM input, HKDF-SHA-384, and bilateral Finished |
| Intercept-resend Eve | **CURRENT** | Seeded, configurable adversary stage with diagnostics and analytical `QBER ~= 0.25 f` validation |
| Hybrid QKD–PQC | **CURRENT** | Authenticated raw QKD/KEM contributions, canonical encoding, independent HKDF keys, and bilateral hybrid Finished |
| AES-256-GCM data protection | **CURRENT** | Session-bound payload protection with 96-bit direction/counter nonces, full 128-bit tags, canonical AAD, and explicit tamper failure |
| Experiment engine | **CURRENT V1** | Versioned secret-free config/runtime/record contracts, seven-profile execution, batch order/warm-up, JSON/CSV, median/IQR, and Wilson intervals; E1–E5 campaign not yet run |
| Web laboratory | **CURRENT, PARTIAL** | Working BB84 builder/results view; target Builder, Run, and two-run Compare screens are not complete |

## Research focus

> What computational and communication costs are introduced by different quantum-safe
> session-establishment strategies based on QKD, PQC, and hybrid composition, and how do the
> channel model, authentication, and the presence of an adversary affect their behavior and the
> validity of their security guarantees?

The project evaluates four related contributions:

- **Experimental:** cost and behavior of executed QKD authentication, PQC authentication, KEM
  diversification, and hybrid composition.
- **Validation:** BB84 behavior against analytical channel and intercept-resend predictions,
  including correction and revalidation of the aggregate-QBER symmetry assumption.
- **Engineering:** acyclic sibling QKD/PQC domains with upper orchestration and reproducible
  configuration, trace, metric, and result contracts.
- **Visualization:** a bounded web laboratory that exposes protocol, adversary, authentication,
  assumptions, derivation, metrics, and outcome.

The definitive academic contract, hypotheses, methodology, experiments, and definition of done are
in [`TFM_GOAL.md`](TFM_GOAL.md).

## Architecture

Current:

```text
ui/frontend -> ui/backend -> qkd -> quantum -> core

                         experiments
                              |
                              v
                         orchestration
                           /       \
                         qkd       pqc
```

Target:

```text
ui/frontend
    -> ui/backend
        -> session orchestration                     [CURRENT all seven profiles]
            -> qkd                                   [CURRENT domain]
            -> pqc                                   [CURRENT domain]
            -> data protection                       [CURRENT]
        -> direct BB84 adapter                        [CURRENT]
```

`qkd` and `pqc` never import each other. Hybrid composition and authentication policy belong in
the upper orchestration layer. See [`docs/structure.md`](docs/structure.md).

## Security profiles

Public documentation and UI use the following profile names:

| Profile | Establishment | Authentication | Status |
|---|---|---|---|
| `QKD-ASSUMED` | BB84 | Authenticated classical channel assumed, not executed | **CURRENT baseline** |
| `QKD-CLASSICAL-AUTH` | BB84 | One-time Toeplitz/Wegman–Carter-style tags with explicit pre-shared material | **CURRENT** |
| `QKD-PQC-AUTH` | BB84 | ML-DSA-65 and pre-provisioned identities over the canonical public transcript | **CURRENT** |
| `PQC-BASE` | ML-KEM-768 | ML-DSA-65 | **CURRENT** as internal `PQCProfile.LOW` |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 | ML-DSA-65 | **CURRENT** as internal `PQCProfile.HIGH` |
| `HYBRID` | BB84 + ML-KEM-768 | Explicit QKD policy + ML-DSA-65 PQC authentication | **CURRENT** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 | Explicit QKD policy + ML-DSA-65 PQC authentication | **CURRENT** |

`LOW` and `HIGH` remain internal identifiers because they are bound into the current transcript
and HKDF context. Renaming the presentation does not alter derived keys or wire contracts.

## Current QKD path

```text
prepare BB84 signals
    -> ordered logical-qubit channel/adversary pipeline
    -> Bob measurement
    -> basis sifting
    -> basis-stratified Z/X QBER estimation and disclosure removal
    -> explicit phase-error bound and threshold decision
    -> Cascade reconciliation
    -> universal-hash reconciled-key verification
    -> asymptotic secret-length estimate
    -> Toeplitz privacy amplification
    -> simulated final material or explicit abort
```

The implemented channels are Identity, Depolarizing, Bit Flip, Phase Flip, general Pauli mixture,
and Amplitude Damping. The same pipeline also accepts the seeded Intercept-Resend adversary at any
configured position. Amplitude damping is qubit relaxation, not optical fiber loss.

The verification tag checks agreement after reconciliation. It does not authenticate the classical
BB84 transcript. Aggregate QBER remains a diagnostic and Cascade bit-error estimate; it is never
substituted automatically for phase error. The mixed-basis asymptotic policy uses the justified
common bound `max(e_Z, e_X)` and fails closed without observations from both bases. See
[`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md) for its assumptions and limitations.

## Current PQC path

```text
pre-provisioned ML-DSA-65 identities and trust
    -> signed ephemeral ServerKeyOffer
    -> verify before encapsulation
    -> ML-KEM-768 encapsulation [plus HQC-3 for PQC-DIVERSE]
    -> signed ClientKeyExchange bound to the offer
    -> verify before decapsulation
    -> canonical authenticated transcript
    -> structured, ordered KEM-secret input
    -> HKDF-SHA-384 -> 32-byte K_SESSION
    -> separate HKDF-SHA-384 domain -> 32-byte K_CONFIRM
    -> Finished_B and Finished_A with HMAC-SHA-384
```

ML-KEM performs key establishment, ML-DSA authentication, HQC diversification, HKDF derivation, and
Finished explicit key confirmation. AES-256-GCM is a separate data-plane operation that protects
application payloads only after a confirmed 256-bit `K_SESSION` exists.

As of **2026-09-05**, ML-KEM and ML-DSA are standardized in NIST FIPS 203 and FIPS 204. The
implementation uses the parameter set exposed by liboqs 0.16.0 as `HQC-3`. HQC was selected by
NIST for standardization on 2025-03-11, but is not described as a published NIST standard.

The structured dual-KEM input is a research diversification construction, not a standardized
multi-KEM combiner or proof that one uncompromised input automatically secures the final key.

## Current hybrid path and data protection

```text
K_QKD
SS_ML_KEM      -> canonical hybrid encoding -> HKDF-SHA-384 -> K_SESSION
SS_HQC optional
```

The current hybrid encoding binds labels, exact bit/byte lengths, deterministic order, domains,
profile, QKD/PQC transcript hashes, shared session ID, and component provenance. Independent
HKDF-SHA-384 calls derive 32-byte session and confirmation keys, followed by a hybrid-specific
Bob-then-Alice HMAC-SHA-384 Finished exchange. Passing information-theoretic QKD material through a
computational KDF does not automatically preserve information-theoretic security, and no formal
robust-combiner proof is claimed.

```text
ESTABLISHMENT PLANE -> 256-bit K_SESSION
DATA PLANE          -> AES-256-GCM -> protected payload or explicit authentication failure
```

The AES-GCM demonstration requires a 96-bit unique nonce, full 128-bit tag, appropriate session AAD,
valid decryption, and rejection of modified ciphertext, tag, or AAD without returning partial
plaintext. `open_data_plane()` accepts `PQC-BASE`, `PQC-DIVERSE`, `HYBRID`, and
`HYBRID-DIVERSE`; QKD-only bitstrings are rejected until an explicit application-key schedule is
defined.

## Experimental campaign

- **E1 — PQC Cost Decomposition:** `PQC-BASE` versus `PQC-DIVERSE`, operation by operation and
  across raw, canonical, and serialized byte sizes.
- **E2 — BB84 Model Validation:** per-basis and aggregate QBER versus applicable analytical channel
  predictions, including the estimator correction.
- **E3 — Eve / Intercept-Resend:** QBER, abort probability, and final material versus interception
  fraction.
- **E4 — QKD Authentication Cost:** assumed baseline versus executed classical and PQC
  authentication.
- **E5 — Hybrid Marginal Overhead:** provenance, bytes, orchestration, combination, derivation, and
  confirmation overhead.
- **D1 — Protected Session:** AES-256-GCM success and tamper-rejection demonstration.

The fundamental measurement rule is defined once in
[`TFM_GOAL.md §12`](TFM_GOAL.md#12-experimental-methodology): numerical BB84 runtime is not physical
QKD performance and is never compared temporally with real liboqs operations.

The reusable V1 engine is implemented; the campaign itself has deliberately not been executed.
See [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) for exact record/export schemas and CLI usage.

## Web Laboratory V1

The final UI is intentionally limited to three screens:

1. **Builder:** choose a supported profile and valid parameters; QKD includes signal count, seed,
   channel, channel parameters, and Eve fraction. Small contextual cards explain each selected
   component.
2. **Run:** show the real Alice/Bob/Eve timeline, authentication state, KEM/combiner/HKDF/Finished
   events where applicable, compatible metrics, outcome, and protected-message strip once
   `K_SESSION` exists.
3. **Compare:** compare exactly two stored runs, showing configuration differences, components,
   assumptions, compatible metrics, bytes, outcome, and security notes without placing incompatible
   QKD and PQC timings on one axis.

There is no separate Quantum-Safe Explorer in the TFM scope. Standards material appears only in
small, contextual, versioned cards with a source and status-as-of date.

Current backend routes:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

## Reproducibility

QKD receives an injected `BaseRNG`; repeatable runs use `SeededRNG(seed=...)`. PQC primitives use
liboqs and operating-system cryptographic randomness and are not forced to be deterministic.
Experiment records preserve the environment, versions, config, run ID, applicable seed, ordered
conditions, trace, metrics, and outcome without serializing secrets. Equal QKD config/seed means an
equal protocol outcome (not run ID, timestamp, or timing); equal PQC config means an equal method,
profile, algorithms, and metric schema, not equal random artifacts or timings.

## Quickstart

Prerequisites are Python 3.14, [`uv`](https://docs.astral.sh/uv/), Node.js 20.19+ (or 22.12+), npm,
and the native liboqs environment described in [`DEPLOYMENT.md`](DEPLOYMENT.md).

```bash
uv sync --dev
cd ui/frontend
npm ci
```

Start the backend from the repository root:

```bash
uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Then start the frontend from `ui/frontend`:

```bash
npm run dev
```

Run the secret-free experiment examples from the repository root:

```bash
uv run python -m experiments.cli run examples/experiments/qkd_eve_example.json --output experiments/output/qkd-eve.json
uv run python -m experiments.cli run examples/experiments/pqc_base_example.json --output experiments/output/pqc-base.json
```

## Verification

```bash
uv run pytest
uv run ruff check .
uv run pyright

cd ui/frontend
npm test
npm run typecheck
npm run build
```

## Documentation

- [`TFM_GOAL.md`](TFM_GOAL.md) — definitive academic contract.
- [`docs/structure.md`](docs/structure.md) — current and target architecture.
- [`docs/tasks.md`](docs/tasks.md) — exact implementation order.
- [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) — current experiment config, runtime, record, export, and CLI contracts.
- [`ui/README.md`](ui/README.md) — current UI/API and three-screen target.
- [`DEPLOYMENT.md`](DEPLOYMENT.md) — local and research-hosting setup.
- [`docs/reviews/`](docs/reviews/) and [`reports/`](reports/) — historical snapshots, not current
  status sources.

Standards references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST's HQC selection announcement](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).

## Author

David Martín Castro
