# QuantumSec — Quantum-Safe Security Laboratory

QuantumSec is a modular and reproducible laboratory for designing, executing, visualizing, and
comparing quantum-safe session-establishment strategies based on QKD, post-quantum cryptography
(PQC), and planned hybrid QKD–PQC composition.

The project is the software and experimental foundation of a Master's thesis. Its contribution is
the integration and evaluation of established techniques under one architecture and methodology;
it does not introduce a new QKD protocol, PQC algorithm, or formal combiner proof.

## Project status

The labels used throughout the documentation have strict meanings:

- **CURRENT** — implemented in the repository and covered by tests.
- **PLANNED** — required to complete the TFM, but not implemented yet.
- **FUTURE** — explicitly outside the TFM's definition of done.

| Area | Status | Repository capability |
|---|---|---|
| Core and quantum mathematics | CURRENT | Injected RNGs, immutable quantum values, validation, linear algebra, information measures, and projective measurements |
| QKD | CURRENT | Seeded BB84 prepare-and-measure simulation, composable logical-qubit channels, sifting, sampled QBER estimation, Cascade, universal-hash verification, asymptotic length estimation, and Toeplitz privacy amplification |
| PQC | CURRENT | Standalone mutually authenticated LOW/HIGH handshakes using ML-KEM-768, optional HQC-3, ML-DSA-65, a canonical KEM-secret encoding, HKDF-SHA-384, and bilateral Finished messages |
| Web laboratory | CURRENT, partial | A working BB84 session builder and results workspace; no PQC, hybrid, comparison, or protected-message endpoints yet |
| Hybrid QKD–PQC | PLANNED | Upper-layer composition of BB84-derived material with ML-KEM-768 and optional HQC-3 material |
| Data protection | PLANNED | AES-256-GCM demonstration driven by the established 256-bit `K_SESSION` |
| Experiments | PLANNED | Reproducible run orchestration, trace/metric capture, export, and profile comparison |
| Additional QKD protocols and QKDN | FUTURE | B92, E91, BBM92, QKD networks, repeaters, routing, and hardware integration |

## Thesis focus

QuantumSec studies this question:

> How can implemented QKD and PQC session-establishment paths, and planned hybrid compositions of
> their secret material, be evaluated within one reproducible laboratory without obscuring their
> different security assumptions and operational costs?

The intended contribution has four parts:

- **Engineering:** modular integration, explicit security profiles, and a common session boundary.
- **Experimental:** comparable measurements of behavior, cost, and overhead.
- **Methodological:** repeatable configuration, trace, metrics, result, and comparison contracts.
- **Educational/visual:** protocol views that distinguish key establishment from data protection.

The academic contract and definition of done are in [`TFM_GOAL.md`](TFM_GOAL.md).

## Architecture

The current domain packages preserve this dependency discipline:

```text
ui/frontend -> ui/backend -> qkd -> quantum -> core

                  pqc (independent sibling domain)
```

The intended TFM composition adds an upper orchestration layer without coupling the sibling
domains directly:

```text
ui/frontend
    -> ui/backend
        -> session / experiment orchestration       [PLANNED]
            -> qkd                                  [CURRENT]
            -> pqc                                  [CURRENT]
            -> data protection                      [PLANNED]
        -> qkd                                      [CURRENT direct BB84 adapter]

qkd -> quantum -> core
pqc -> external cryptographic backends
```

`qkd` and `pqc` do not import each other. Hybrid integration belongs above both packages, where it
can preserve provenance, collect metrics, and avoid circular dependencies. See
[`docs/structure.md`](docs/structure.md) for the detailed current and target architecture.

## Current QKD path

`BB84Protocol` implements the following seeded logical-qubit simulation:

```text
prepare random bits and Z/X bases
    -> transmit density matrices through an ordered CPTP channel pipeline
    -> measure in Bob's random Z/X bases
    -> sift matching bases
    -> disclose a seeded random sample and estimate QBER
    -> abort if the configured threshold is exceeded
    -> Cascade reconciliation
    -> universal-hash key verification
    -> asymptotic BB84 secret-length estimate
    -> FFT Toeplitz privacy amplification
    -> final simulated secret material or an explicit abort result
```

Implemented channels are Identity, Depolarizing, Bit Flip, Phase Flip, general Pauli mixture, and
Amplitude Damping. Amplitude damping models qubit relaxation, not optical photon loss.

The result exposes raw and sifted sizes, sifting efficiency, diagnostic full-sifted QBER, sampled
QBER, disclosed positions, Cascade leakage and corrected errors, verification outcome and leakage,
reconciled/final sizes, compression ratio, final secret fraction, and final simulated key material
for educational inspection.

Security decisions use the disclosed sample, not the full-key diagnostic QBER. Disclosed positions
are removed. The current estimator is asymptotic and assumes a symmetric phase-error rate; it is
not a composable finite-key proof. All BB84 classical communication is currently **assumed to be
authenticated**. The simulator therefore does not claim that standalone BB84 establishes an
end-to-end authenticated session.

## Current PQC path

QuantumSec implements two standalone deployment profiles:

| Code profile | Conceptual profile | Components | Status |
|---|---|---|---|
| `LOW` | PQC | ML-KEM-768 + ML-DSA-65 | CURRENT |
| `HIGH` | PQC Diversified | ML-KEM-768 + HQC-3 + ML-DSA-65 | CURRENT |

The six implemented phases are:

```text
Bob:   create ephemeral KEM material
       -> ServerKeyOffer -> sign with ML-DSA-65

Alice: resolve Bob from pre-provisioned trust
       -> verify before encapsulation
       -> encapsulate ML-KEM-768 [and HQC-3 for HIGH]
       -> bind ClientKeyExchange to the exact offer with SHA-384
       -> sign with ML-DSA-65

Bob:   resolve and verify Alice before decapsulation
       -> decapsulate every profile-required KEM

Both:  canonical authenticated transcript
       -> canonical profile-aware KEM-secret input
       -> HKDF-SHA-384 -> 32-byte K_SESSION
       -> separate HKDF-SHA-384 domain -> 32-byte K_CONFIRM
       -> Finished_B (HMAC-SHA-384)
       -> Finished_A (HMAC-SHA-384, chained to Finished_B)
       -> confirmed role-local session handles
```

The KEM input is not an undocumented `secret1 || secret2`. It includes an explicit domain, a
component count, fixed algorithm order, algorithm identifiers, lengths, and secret boundaries.
The authenticated transcript hash is the HKDF salt; the HKDF `info` binds purpose, protocol
version, and profile. `K_SESSION` and `K_CONFIRM` are purpose-separated.

`HIGH` explores cryptographic diversification with independently established ML-KEM-768 and HQC-3
material. It is not a standardized NIST multi-KEM construction and QuantumSec does not claim that
one secure component automatically proves the security of the resulting key.

As of **2026-09-05**, ML-KEM is standardized in NIST FIPS 203 and ML-DSA in NIST FIPS 204. HQC was
selected by NIST for standardization on 2025-03-11, but is not presented here as a final FIPS
standard. The implementation uses the `HQC-3` algorithm exposed by the configured liboqs backend.

The current simulator can materialize both role-local sessions in process. In a distributed
deployment Alice would additionally need an authenticated transport acknowledgement that Bob
accepted `Finished_A`; the current two public Finished messages do not prove that remote event to
Alice. No such third protocol acknowledgement is fabricated by the API.

## Security profiles

| Profile | Secret/authentication components | Purpose | Status |
|---|---|---|---|
| QKD Experimental | BB84 final material; authenticated classical channel is an explicit assumption | Study simulated QKD channel and post-processing behavior | CURRENT path; PLANNED unified session profile |
| PQC (`LOW`) | ML-KEM-768 + ML-DSA-65 | Authenticated standalone PQC establishment | CURRENT |
| PQC Diversified (`HIGH`) | ML-KEM-768 + HQC-3 + ML-DSA-65 | Study diverse KEM integration and overhead | CURRENT |
| Hybrid QKD–PQC | BB84 material + ML-KEM-768 + authentication policy | Combine independently established QKD and PQC material | PLANNED |
| Hybrid Diversified | BB84 material + ML-KEM-768 + HQC-3 + authentication policy | Measure added diversity and overhead | PLANNED |

The hybrid combiner will extend the current canonical encoding with QKD material, explicit labels,
lengths, provenance, and domain separation before HKDF-SHA-384 derives `K_SESSION`. Its precise
security claim must be limited to the construction and assumptions actually implemented and
evaluated; the TFM does not provide a new formal robust-combiner proof.

## Web laboratory

The current React/FastAPI application is a working BB84 laboratory. It supports a signal count,
32-bit seed, ordered channel pipeline, real engine execution, abort/success output, charts, stage
shrinkage, and a bounded raw-transmission inspector. The backend currently exposes only:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The TFM target extends this UI into four coherent workspaces:

1. **Session Builder:** select only backend-supported profiles and parameters.
2. **Protocol Visualizer:** show real BB84, PQC, and hybrid events and message ordering.
3. **Results and Comparison:** inspect traces, metrics, configuration snapshots, and multiple runs.
4. **Protected Message Demo:** show `K_SESSION` feeding AES-256-GCM and distinguish the
   key-establishment plane from the data-protection plane.

A versioned Quantum-Safe Explorer may present sourced standards metadata, roles, benefits, and
limitations. It must not turn unsourced or time-sensitive standards claims into static fact.

## Reproducibility model

QKD simulations receive an injected `BaseRNG`; tests and repeatable runs use `SeededRNG(seed=...)`.
The same QKD configuration and seed reproduce the simulated path. PQC primitives intentionally use
liboqs and operating-system cryptographic randomness, so keys, signatures, and ciphertexts are not
made deterministic for experiments. Future experiment records must capture configuration, seed
where applicable, run identifier, algorithm/backend metadata, trace, metrics, and result.

## Quickstart

Prerequisites are Python 3.14, [`uv`](https://docs.astral.sh/uv/), Node.js 20.19+ (or 22.12+), npm,
and the native liboqs environment required by `liboqs-python` for PQC execution.

Install the locked environments:

```bash
uv sync --dev
cd ui/frontend
npm ci
```

Start the backend from the repository root:

```bash
uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
cd ui/frontend
npm run dev
```

Verify `http://127.0.0.1:8000/api/health`, then open `http://localhost:5173`. Detailed environment
and liboqs instructions are in [`DEPLOYMENT.md`](DEPLOYMENT.md); UI contracts and extension phases
are in [`ui/README.md`](ui/README.md).

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

## TFM roadmap

Completed/current:

1. Core and quantum architecture.
2. BB84 with logical-qubit channel/noise models and classical post-processing.
3. PQC identities, trust, KEM establishment, authenticated transcript, key schedule, and Finished
   confirmation for `LOW` and `HIGH`.
4. Interactive BB84 Web UI V1.

Remaining TFM work:

5. QKD–PQC hybrid orchestration and a precisely specified hybrid secret input.
6. AES-256-GCM protected-message demonstration using the established 256-bit `K_SESSION`, unique
   nonces per key, authentication-tag failure handling, and appropriate AAD.
7. Experiment configuration, run/trace/metric/result records, export, and comparisons.
8. Web-laboratory support for the principal PQC, hybrid, experiment, and protected-message flows.
9. Experimental campaign, analysis, and thesis results.

Future work:

10. B92, E91, BBM92, optical/hardware QKD, QKDN, routing, additional algorithms, richer combiners,
    formal verification, and production optimization.

## Limitations and non-claims

- Quantum states and channels are numerical logical-qubit models, not commercial QKD hardware.
- NumPy simulation duration is not physical link latency or secret-key rate.
- QKD establishes secret material; it is not application-data encryption and requires an
  authenticated classical channel.
- ML-KEM and HQC are KEMs, ML-DSA is a signature scheme, and HKDF is a key-derivation function;
  none encrypts application payloads.
- AES-256-GCM data protection is planned, not current.
- The software is research and educational infrastructure, not production-ready cryptography.

## Documentation

- [`TFM_GOAL.md`](TFM_GOAL.md) — academic contract, scope, deliverables, and definition of done.
- [`docs/structure.md`](docs/structure.md) — current and target architecture.
- [`docs/tasks.md`](docs/tasks.md) — concise implementation roadmap.
- [`ui/README.md`](ui/README.md) — current UI/API and planned laboratory evolution.
- [`DEPLOYMENT.md`](DEPLOYMENT.md) — development and research-hosting instructions.

Standards references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST's HQC selection announcement](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).

## Author

David Martín Castro
