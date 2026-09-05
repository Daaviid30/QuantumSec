# QuantumSec Project Structure

> **Identity:** QuantumSec is a modular, reproducible laboratory for quantum-safe session
> establishment using QKD, PQC, and planned hybrid QKD–PQC strategies.
>
> **Status date:** 2026-09-05. Source code and tests take precedence over this target architecture.

## 1. Scope and status model

This document describes both the repository that exists now and the architecture required to
finish the TFM. Every capability is classified as:

- **CURRENT:** implemented and tested.
- **PLANNED:** part of the TFM definition of done, but absent or incomplete.
- **FUTURE:** deliberately outside the TFM boundary.

The TFM integrates and evaluates established techniques. It does not design a new QKD protocol,
PQC primitive, application cipher, or formally proven cryptographic combiner.

## 2. Design philosophy

1. **Acyclic layers.** Higher layers orchestrate lower layers; domain packages never depend on the
   UI or on sibling domains.
2. **Explicit assumptions.** Authentication, trust, numerical models, security estimates, and
   backend guarantees are documented rather than implied.
3. **Reproducible science.** Simulation randomness is injected. Experiments will preserve
   configuration, applicable seed, run identifier, trace, metrics, and backend metadata.
4. **Immutable boundaries.** Domain values validate defensive copies and protect stored arrays or
   secret-bearing state where appropriate.
5. **Real traces and metrics.** The UI and experiment layer expose events produced by actual domain
   flows, never invented protocol messages or unavailable measurements.
6. **Separate planes.** Session establishment produces key material; AES-256-GCM will consume an
   established key in a distinct data-protection plane.

## 3. Architecture

### 3.1 Current dependency graph

```text
ui/frontend -> JSON/HTTP -> ui/backend -> qkd -> quantum -> core

pqc -> liboqs / cryptography / Python standard library
```

The current UI backend adapts BB84 only. The standalone `pqc` package is complete through mutual
Finished confirmation but has no HTTP route. `qkd` and `pqc` are siblings and do not import each
other.

### 3.2 Target TFM dependency graph

```text
ui/frontend
    -> ui/backend
        -> session orchestration
            -> qkd
            -> pqc
            -> data protection
        -> experiment orchestration
            -> session orchestration
            -> result/export adapters

qkd -> quantum -> core
pqc -> external cryptographic backends
```

The planned session and experiment layers are the only places that may compose QKD and PQC.
Neither composition nor the data-protection package may create reverse imports into `qkd`, `pqc`,
`quantum`, or `core`.

### 3.3 Allowed and forbidden imports

Allowed target direction:

```text
ui/backend, experiments -> orchestration -> qkd, pqc
ui/backend              -> qkd                    # existing BB84 adapter
qkd                     -> quantum, core
quantum                 -> core
```

Forbidden:

```text
core    -> quantum, qkd, pqc, orchestration, experiments, ui
quantum -> qkd, pqc, orchestration, experiments, ui
qkd     -> pqc, orchestration, experiments, ui
pqc     -> qkd, orchestration, experiments, ui
```

## 4. Repository layout

The implemented packages are shown without a status suffix; planned TFM additions are annotated.

```text
QuantumSec/
|-- core/                       # constants and RNG abstractions
|-- quantum/                    # general quantum mathematics
|-- qkd/
|   |-- primitives/
|   |-- channel/
|   |   `-- noise/
|   |-- protocols/              # BB84 only
|   |-- postprocessing/
|   `-- metrics/
|-- pqc/
|   |-- backends/
|   |-- kem/
|   |-- signatures/
|   |-- kdf/
|   `-- protocol/
|-- ui/
|   |-- backend/                # current BB84 HTTP adapter
|   `-- frontend/               # current React BB84 laboratory
|-- benchmarks/                 # quantum-measurement benchmark only
|-- tests/
|-- docs/
|-- experiments/                # PLANNED: run/trace/metrics/result/compare
|-- orchestration/              # PLANNED: unified session profiles
|-- data_protection/            # PLANNED: AES-256-GCM demo boundary
|-- TFM_GOAL.md
|-- pyproject.toml
`-- README.md
```

The exact names of planned packages may change during implementation. Their responsibilities and
dependency direction may not.

## 5. Current module responsibilities

### 5.1 `core/` — CURRENT

General infrastructure with zero domain dependencies:

- `DEFAULT_ATOL`;
- `BaseRNG`, `SeededRNG`, `GlobalRNG`, and `QRNGSimulator`;
- binary and unitary random helpers.

Scientific domain code that needs modeled randomness receives a `BaseRNG`. Deterministic tests use
`SeededRNG`. Cryptographic key generation in the PQC backend is deliberately excluded from seeded
simulation randomness.

### 5.2 `quantum/` — CURRENT

Reusable quantum mathematics with no QKD semantics:

- ket/matrix conversion and linear algebra;
- state and density-matrix construction;
- physical validation;
- immutable projective measurements and sampling;
- purity, fidelity, trace distance, and von Neumann entropy;
- shared NumPy input/output types.

`quantum` does not know about Alice, Bob, BB84, QBER, or authentication.

### 5.3 `qkd/` — CURRENT BB84 domain

The implemented path is:

```text
random bits/bases
    -> BB84 state preparation
    -> ordered logical-qubit CPTP channel pipeline
    -> projective measurement
    -> basis sifting
    -> sampled parameter estimation
    -> threshold/size abort checks
    -> Cascade reconciliation
    -> universal-hash verification
    -> asymptotic secret-length estimate
    -> FFT Toeplitz privacy amplification
```

Implemented channels:

- Identity;
- Depolarizing;
- Bit Flip;
- Phase Flip;
- Pauli mixture;
- Amplitude Damping.

Amplitude damping is qubit relaxation within the modeled Hilbert space. It is not optical loss,
vacuum, detector behavior, or fiber attenuation.

`BB84PostprocessingConfig` currently provides `sample_fraction` (default `0.2`),
`qber_abort_threshold` (default `0.11` under the documented asymptotic model), Cascade settings,
`verification_tag_length` (default `16` bits), and `security_margin_bits` (default `0`). The Web UI
currently uses these defaults; it does not expose them as request fields.

Session outcomes are `completed` or `aborted`. Implemented abort paths cover insufficient sifted
material, disclosure leaving no candidate material, sampled QBER above threshold, insufficient
verification material, failed reconciled-key verification, and no extractable asymptotic secret
length.

The full-sifted QBER is diagnostic. Protocol decisions use the seeded disclosed sample, and those
positions are removed. Cascade counts public Alice parity disclosures; verification counts the
public tag. The estimator subtracts reconciliation and verification leakage once from candidate
material. Public Toeplitz seeds are not treated as secret consumption.

Security boundary:

- the current model is asymptotic, not a composable finite-key proof;
- the classical BB84 transcript is assumed authenticated;
- no implemented component currently connects PQC identity/authentication to this transcript;
- numerical run time is not physical QKD latency or secret-key rate.

### 5.4 `pqc/` — CURRENT standalone handshake

Implemented algorithms and backend-reported dimensions:

| Algorithm | Role | Standardization status as of 2026-09-05 | Public key | Ciphertext/signature | Shared secret |
|---|---|---|---:|---:|---:|
| ML-KEM-768 | KEM | NIST FIPS 203 | 1184 B | 1088 B ciphertext | 32 B |
| ML-DSA-65 | Signature | NIST FIPS 204 | 1952 B | 3309 B signature | — |
| HQC-3 | Diverse KEM | Selected by NIST for standardization on 2025-03-11; no final FIPS claimed | 4514 B | 8978 B ciphertext | 32 B |

KEM dimensions are read from the configured liboqs backend and should be recorded with the backend
version in experiments. HQC is code-based and intentionally mathematically diverse from the
module-lattice-based ML-KEM. Selection for standardization is not the same as a published standard.

The two code-level profiles are:

```text
LOW  = ML-KEM-768 + ML-DSA-65 authentication
HIGH = ML-KEM-768 + HQC-3 + ML-DSA-65 authentication
```

`LOW` and `HIGH` are QuantumSec names, not NIST security-category labels. `HIGH` means a diverse
dual-KEM research profile, not a QKD–PQC hybrid.

The implemented message and state flow is:

```text
1. Alice and Bob create ML-DSA-65 identities and provision trust explicitly.
2. Bob creates ephemeral KEM keys and a signed ServerKeyOffer.
3. Alice validates session/profile/algorithms/trust/signature before encapsulation.
4. Alice creates a fresh 32-byte client nonce, binds the exact offer with SHA-384,
   signs ClientKeyExchange, and Bob verifies before decapsulation.
5. Each side constructs the same canonical public transcript and derives K_SESSION.
6. Each side derives K_CONFIRM; Bob sends Finished_B, Alice verifies it and sends a
   role-separated Finished_A chained to Finished_B, then Bob verifies and confirms.
```

Public wire messages have validated JSON/Base64 mappings. Secret states are repr-safe and not
serializable. Secret references are released through explicit state lifecycles without claiming
memory zeroization.

#### Current KEM-secret input and key schedule

`canonical_kem_secret_input()` provides:

- domain `QuantumSec/PQCHandshake/v1/KEMSecretInput`;
- explicit component count;
- fixed order: ML-KEM-768, then HQC-3 for `HIGH`;
- length-prefixed algorithm identifiers and secret values;
- validation against backend-reported 32-byte shared-secret lengths.

The SHA-384 hash of the canonical signed-message transcript is the HKDF salt. HKDF `info` includes
a length-prefixed purpose domain, protocol version, and profile. Separate purpose domains derive:

```text
K_SESSION = 32 bytes under .../SessionKey
K_CONFIRM = 32 bytes under .../ConfirmationKey
```

Finished values are 48-byte HMAC-SHA-384 outputs. Inputs bind the session identifier, profile,
role, MAC algorithm, and transcript hash; Alice's Finished additionally binds Bob's verified
Finished value. Verification uses constant-time comparisons.

This is a structured research diversity construction, not a standardized multi-KEM combiner and
not a formal claim that one uncompromised input automatically guarantees `K_SESSION`.

#### Distributed-session limitation

In process, Bob's confirmed capability can establish both role-local session handles. Across a
network, Alice cannot infer that Bob accepted `Finished_A` from the two public Finished messages
alone. A transport-level authenticated acknowledgement or a later protocol revision is required
before Alice treats that remote event as complete.

### 5.5 `ui/` — CURRENT BB84 laboratory, PLANNED expansion

Current backend routes:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The BB84 request supports `n_signals` from 1 to 100,000, a seed from 0 to 2^32−1, and up to 12
ordered implemented channels. Responses contain real engine output, measured adapter duration, a
UUID request identifier, summary metrics, post-processing status, distributions, and at most 64
raw transmission records.

The React application currently implements BB84 configuration, a channel pipeline editor, an
educational quantum-flow view, results/charts, and raw inspection. Unsupported protocols are
disabled from capability discovery. No PQC, hybrid, AES, experiment, or comparison route exists.

### 5.6 `benchmarks/` — CURRENT, narrow scope

The existing benchmark measures quantum projective-measurement paths. It is not the TFM experiment
engine and does not supply PQC or hybrid comparative results.

## 6. Security profiles

| Profile | Components | Purpose | Repository status |
|---|---|---|---|
| QKD Experimental | BB84 final material; authenticated classical channel modeled as an assumption | QKD behavior and post-processing study | CURRENT standalone path; PLANNED unified profile |
| PQC | ML-KEM-768 + ML-DSA-65 | Authenticated PQC session establishment | CURRENT as `LOW` |
| PQC Diversified | ML-KEM-768 + HQC-3 + ML-DSA-65 | Diverse KEM integration and overhead | CURRENT as `HIGH` |
| Hybrid QKD–PQC | BB84 material + ML-KEM-768 + explicit authentication policy | Combined QKD/PQC establishment | PLANNED |
| Hybrid Diversified | BB84 material + ML-KEM-768 + HQC-3 + explicit authentication policy | Combined path with diverse PQC input | PLANNED |

The unified profile model must record component and authentication provenance. It must not silently
present the BB84 simulation's assumed authenticated channel as a mechanism that was executed.

## 7. Planned hybrid session architecture

The hybrid layer will consume successful domain results rather than reach into domain internals:

```text
K_QKD                 [successful BB84 final material]
SS_ML_KEM             [authenticated PQC establishment]
SS_HQC optional       [HIGH/diversified profile only]
    -> canonical component encoding
    -> labels, lengths, profile and provenance
    -> hybrid-specific domain separation
    -> HKDF-SHA-384
    -> 32-byte K_SESSION
    -> confirmation appropriate to the final protocol design
```

The existing PQC-only `canonical_kem_secret_input()` must not be relabeled as hybrid. The new
encoding needs a separate domain and tests for order, boundaries, component/profile mismatch,
transcript binding, and sensitivity. The thesis evaluates integration and diversification; it does
not claim a new robust-combiner proof.

## 8. Planned data-protection plane

The final session demo will keep key establishment and payload protection distinct:

```text
established session -> 256-bit K_SESSION
                    -> AES-256-GCM
                    -> nonce + ciphertext + authentication tag
                    -> authenticated decrypt or explicit failure
```

Requirements include secure nonce generation, no nonce reuse under one key, optional AAD binding
for session/transcript metadata, successful round-trip, and tamper rejection. This demonstrates a
usable session; it does not design a new cipher. No such feature exists today.

## 9. Planned experiment architecture

`experiments/` is central to the TFM and follows one contract:

```text
CONFIG -> RUN -> TRACE -> METRICS -> RESULT -> COMPARE
```

Each record should include:

- run ID and timestamps;
- security profile and normalized configuration snapshot;
- deterministic seed for modeled randomness;
- algorithm, library, and backend versions;
- ordered protocol events and terminal status/abort reason;
- available timings and byte counts;
- QKD sizes, QBER, leakage, and final material size where applicable;
- session-key length and component provenance, never secret values;
- serialization/export version.

Planned TFM experiments:

1. **PQC profile comparison:** `LOW` versus `HIGH`; measure key generation, encapsulation,
   decapsulation, signing, verification, total handshake duration, public/ciphertext/signature
   sizes, and bytes exchanged.
2. **BB84 channel behavior:** vary implemented channel parameters; analyze sampled QBER, sifted and
   final material, efficiency, and abort behavior. NumPy timings remain simulator timings.
3. **Hybrid establishment:** after implementation, compare QKD + ML-KEM-768 with the diversified
   variant; verify integration, provenance, reproducibility, and overhead.
4. **End-to-end session:** derive `K_SESSION`, protect a payload with AES-256-GCM, verify decryption,
   reject tampering, and retain session/profile metadata.

## 10. Target web laboratory

The current BB84 UI evolves into these modules without presenting unavailable controls:

- **Session Builder:** expose only profiles and parameters reported as implemented by the backend.
- **Protocol/Handshake Visualizer:** show actual BB84 events and actual PQC messages; converge the
  QKD/PQC branches only after hybrid orchestration exists.
- **Results/Metrics:** show available status, trace, timings, byte sizes, QKD metrics, profile,
  seed, and configuration snapshot; later compare multiple run records.
- **Protected Message Demo:** make the key-establishment/data-protection boundary visible.
- **Quantum-Safe Explorer:** use a structured, versioned, cited catalog with a “status as of” date
  for standards claims.

The UI never reimplements quantum or cryptographic domain logic.

## 11. Milestones

### Completed/current

1. Core and quantum foundations.
2. BB84 and logical-qubit channel/noise framework.
3. Sifting, QBER, parameter estimation, Cascade, verification, and privacy amplification.
4. ML-DSA-65 identity and explicit trust.
5. ML-KEM-768 and HQC-3 KEM establishment in `LOW`/`HIGH`.
6. Authenticated transcript, structured KEM input, HKDF-SHA-384, and `K_SESSION`.
7. Separate `K_CONFIRM` and mutual role-bound Finished confirmation.
8. BB84 Web UI V1.

### Remaining TFM work

9. QKD–PQC hybrid session orchestration.
10. AES-256-GCM protected-message demonstration.
11. Experiment contracts, metrics, serialization, export, and comparisons.
12. Web support for PQC, hybrid, experiments, and protected messages.
13. Experimental campaign and thesis analysis.

### Future work

14. Additional QKD protocols, QKDN, routing/repeaters, hardware integration, additional PQC
    algorithms, richer combiners, formal verification, larger benchmarks, and deployment research.

## 12. TFM boundary

The TFM is complete when the BB84, PQC, and hybrid paths are demonstrable; a 256-bit `K_SESSION`
drives an authenticated AES-256-GCM payload demo; the principal scenarios can be run and visualized
through the web laboratory; reproducible experiments produce comparable results; and the evidence
answers the research question in [`../TFM_GOAL.md`](../TFM_GOAL.md).

B92, E91, BBM92, QKDN, quantum repeaters, production hardware, new PQC algorithms, LLM agents, a
new formal combiner proof, production optimization, and full device-level physics are not required.

## 13. Testing and maintenance

- Simulation tests use `SeededRNG`; PQC tests assert invariants under secure backend randomness.
- Hybrid tests must validate boundaries, profile mismatch, provenance, and transcript/context
  separation.
- AES-GCM tests must cover unique nonce handling and modified ciphertext/tag rejection.
- Experiment tests must reproduce modeled runs and serialize configuration/result records.
- UI tests must ensure disabled capability states cannot produce fabricated runs.
- After code changes, run Python tests, Ruff, Pyright, frontend tests/typecheck/build, and
  `graphify update .`.

Standards references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST HQC selection](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).
