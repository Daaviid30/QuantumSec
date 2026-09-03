# QuantumSec Project Structure

> Project: Modular simulation platform for QKD, quantum primitives, PQC authentication, and reproducible experiments.
>
> Scope: Master's thesis foundation, with a path toward research and educational tooling.
>
> Current architectural decision: `core` is infrastructure only; reusable quantum mathematics lives in `quantum`.

---

## 1. Design Principles

QuantumSec is organized around four rules:

1. **Separation of concerns.** Randomness, configuration, quantum mathematics, QKD protocol logic, PQC authentication, and experiments live in different modules.
2. **Reproducibility.** Every component that needs randomness receives an injected RNG object. Experiments must be reproducible from config plus seed.
3. **Layered dependencies.** Upper layers may depend on lower layers; lower layers never import upper layers.
4. **Scientific clarity.** Physics checks and cryptographic assumptions should be explicit, testable, and documented.

The most important boundary is this:

```text
core     = general project infrastructure
quantum  = reusable quantum mathematics and validation
qkd      = QKD-specific primitives, channels, protocols, and metrics
pqc      = post-quantum cryptographic mechanisms
experiments = orchestration, comparison, analysis, and export
```

---

## 2. Target Directory Layout

```text
QuantumSec/
|
|-- core/
|   |-- __init__.py
|   |-- rng.py
|   |-- config.py
|   |-- logging.py
|   `-- benchmarking.py
|
|-- quantum/
|   |-- __init__.py
|   |-- linalg.py
|   |-- validation.py
|   |-- states.py
|   |-- measures.py
|   `-- errors.py
|
|-- qkd/
|   |-- __init__.py
|   |-- primitives/
|   |   |-- __init__.py
|   |   |-- states.py
|   |   |-- operations.py
|   |   |-- bases.py
|   |   `-- measurements.py
|   |-- channel/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- ideal.py
|   |   |-- kraus.py
|   |   |-- pipeline.py
|   |   `-- noise/
|   |       |-- __init__.py
|   |       |-- depolarizing.py
|   |       |-- pauli.py
|   |       `-- amplitude_damping.py
|   |-- protocols/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- bb84.py
|   |   |-- b92.py
|   |   `-- e91.py
|   |-- postprocessing/
|   |   |-- __init__.py
|   |   |-- sifting.py
|   |   |-- reconciliation.py
|   |   `-- privacy_amplification.py
|   `-- metrics/
|       |-- __init__.py
|       |-- qber.py
|       |-- key_rate.py
|       `-- security.py
|
|-- pqc/
|   |-- __init__.py
|   |-- errors.py
|   |-- profiles.py
|   |-- backends/
|   |   |-- oqs_backend.py
|   |   `-- oqs_kem_backend.py
|   |-- kem/
|   |   |-- base.py
|   |   |-- ml_kem.py
|   |   `-- hqc.py
|   |-- signatures/
|   |   |-- base.py
|   |   `-- ml_dsa.py
|   `-- protocol/
|       |-- identity.py
|       |-- trust.py
|       |-- party.py
|       |-- messages.py
|       `-- server_offer.py
|
|-- experiments/
|   |-- __init__.py
|   |-- scenarios/
|   |-- runner/
|   |-- analysis/
|   `-- exporter/
|
|-- configs/
|-- data/
|-- docs/
|-- tests/
|-- pyproject.toml
`-- README.md
```

The current repository may not contain every folder yet. This structure is the roadmap for building modules incrementally without mixing responsibilities.

---

## 3. Layer Architecture

Allowed dependency direction:

```text
ui / notebooks
    -> ui backend / experiments
        -> qkd, pqc
            -> quantum
                -> core
                    -> external libraries
```

More explicitly:

```text
experiments -> qkd, pqc, quantum, core
ui/backend -> qkd, quantum, core
qkd         -> quantum, core
pqc         -> core
quantum     -> core, numpy/scipy
core        -> numpy/scipy/yaml/standard library only
```

Forbidden dependencies:

```text
core    -> quantum, qkd, pqc, experiments
quantum -> qkd, pqc, experiments
qkd     -> pqc
pqc     -> qkd
core    -> ui
quantum -> ui
qkd     -> ui
```

QKD and PQC integration belongs in `experiments/` or in an explicit authentication boundary, not through direct circular imports.

---

## 4. Module Responsibilities

### `core/`

General infrastructure. It must not contain quantum-state logic or cryptographic protocol logic.

Responsibilities:

- RNG abstractions: `BaseRNG`, `SeededRNG`, `GlobalRNG`, `QRNGSimulator`
- deterministic helper functions: `random_bit`, `random_basis`, `random_unitary`
- configuration loading and validation
- structured logging
- benchmarking helpers

Good fit:

```text
core/rng.py
core/config.py
core/benchmarking.py
```

Bad fit:

```text
core/math.py with is_quantum_state()
core/qkd_helpers.py
core/dilithium.py
```

### `quantum/`

Reusable quantum mathematics. This layer knows about vectors, matrices, density matrices, measurements as mathematical objects, and validation of physical constraints. It does not know about BB84, Alice, Bob, Eve, QBER, or authentication.

Suggested files:

```text
quantum/linalg.py
quantum/validation.py
quantum/states.py
quantum/measures.py
quantum/errors.py
```

Responsibilities:

- canonical vector/matrix conversions: `as_ket`
- linear algebra wrappers: `dagger`, `tensor`, `matrix_trace`, `partial_trace`
- state construction: `dm_from_ket`, `dm_from_ensemble`
- validation: `is_normalized_state`, `is_unitary`, `is_hermitian`, `is_density_matrix`, `is_quantum_state`
- quantum measures: `fidelity`, `trace_distance`, `von_neumann_entropy`, `purity`
- validation errors currently use standard `ValueError`; `quantum/errors.py` is reserved for a
  future domain-exception hierarchy if concrete callers require one

Rule of thumb:

```text
If the function is true for quantum mechanics in general, it belongs in quantum/.
If it only makes sense for a QKD protocol, it belongs in qkd/.
```

Examples:

```text
quantum.validation.is_quantum_state()     # yes
quantum.validation.is_density_matrix()    # yes
qkd.metrics.qber()                        # no, QKD-specific
qkd.primitives.bases.Basis.Z              # no, QKD/convention-specific
```

### `qkd/`

QKD simulation domain. The physical package name is lowercase `qkd/` so imports
have identical behavior on case-sensitive and case-insensitive filesystems. This
layer uses `quantum/` to implement concrete protocol behavior.

Suggested structure:

```text
qkd/primitives/
qkd/channel/
qkd/protocols/
qkd/postprocessing/
qkd/metrics/
```

Responsibilities:

- protocol states and bases: `KET0`, `KET1`, `PLUS`, `MINUS`, `Basis.Z`, `Basis.X`
- gates/operators used by QKD simulations: `X`, `Y`, `Z`, `H`, `CNOT`
- measurements with injected RNG
- deterministic CPTP channel models: identity, depolarizing, Pauli errors, and amplitude damping
- sequential channel composition through `ChannelPipeline`
- future optical transmission/loss models, kept separate from logical-qubit CPTP noise
- future attacks such as intercept-resend and classical man-in-the-middle studies
- protocols: BB84, B92, E91
- postprocessing: sifting, reconciliation, privacy amplification
- metrics: QBER, key generation rate, efficiency, security thresholds

Important distinction:

```text
quantum/validation.py can say whether a vector is a valid quantum state.
qkd/primitives/states.py can say which valid states are used by BB84.
qkd/protocols/bb84.py decides how Alice and Bob use those states.
```

The channel boundary is intentionally split by physical meaning:

```text
qkd/channel/noise/    = deterministic CPTP transformations of density matrices
optical loss          = future transmission model with vacuum/no-detection outcomes
```

`AmplitudeDampingChannel` models qubit relaxation from `|1>` to `|0>`. It is a
useful CPTP noise model, but it is not a general synonym for photon loss in fiber:
photonic loss normally leaves the logical qubit subspace as vacuum or a
no-detection event. A future optical-loss layer will represent that distinction
explicitly.

### `pqc/`

Post-quantum cryptography and authentication. This module should not import from `qkd/`. Its job is to provide cryptographic tools and interfaces that can be used by experiments or authentication adapters.

Implemented PQC structure through Phase 3:

```text
pqc/backends/       = isolated external-provider adapters
pqc/signatures/     = signature interface and ML-DSA-65 implementation
pqc/kem/            = KEM interface plus ML-KEM-768 and HQC-3 providers
pqc/profiles.py     = centralized LOW/HIGH QuantumSec profiles
pqc/protocol/       = identities, trust, canonical messages, offer creation, and initiator processing
```

ML-DSA-65 currently provides post-quantum digital identity and authentication primitives through
`liboqs-python`. `PublicIdentity` is an immutable, non-secret trust artifact; `PQCParty` signs with
its own private identity and verifies peers only through explicitly pre-provisioned public keys.
Receiving a public key never makes it trusted automatically.

PQC cryptographic randomness comes from liboqs and the operating-system CSPRNG. It is intentionally
not injected or seeded: reproducible `SeededRNG` instances remain specific to QKD simulations and
other scientific models.

Current responsibilities:

- signature interfaces: `keygen`, `sign`, `verify`
- real ML-DSA-65 execution behind a backend-independent adapter
- named private identities and immutable public identities
- explicit pre-provisioned peer trust
- real ML-KEM-768 and HQC-3 ephemeral key generation behind a separate OQS KEM adapter
- LOW (`ML-KEM-768`) and HIGH (`ML-KEM-768 + HQC-3`) QuantumSec profiles
- canonical, domain-separated `ServerKeyOffer` serialization for signing
- validated JSON-compatible Base64 transport mappings for public handshake messages
- explicit, idempotent release of ephemeral responder KEM references on session abort/expiry
- ML-DSA-65 authentication of Bob's public ephemeral KEM offer
- trust-backed Alice-side authentication before any KEM encapsulation
- private `InitiatorKEMState` secrets separated from public `EncapsulationResponse` ciphertexts
- explicit, idempotent release of Alice's shared-secret references on session abort/expiry

QuantumSec can now construct an authenticated KEM offer and Alice can verify Bob through her
pre-provisioned trust store before creating ML-KEM-768 and optional HQC-3 ciphertexts. The resulting
shared secrets remain private to Alice. Bob has not received or authenticated the response and has
not decapsulated it at the protocol level; response signing, combined secrets, KDFs, Finished
messages, session keys, and QKD/PQC composition belong to later phases.
`InitiatorKEMState` intentionally exposes no raw-secret export API yet: the later KDF phase must own
that consumption contract rather than broadening the Phase 3 public surface prematurely.
LOW and HIGH are QuantumSec deployment profiles, not NIST categories; HIGH is a diverse dual-KEM
offer and is not the future QKD + PQC `HYBRID` profile.

### `experiments/`

The scientific orchestration layer. This is where QKD and PQC can be composed for thesis experiments.

Responsibilities:

- scenario definitions
- parameter sweeps
- repeated runs with derived deterministic seeds
- result aggregation
- plots and tables
- JSON/CSV/LaTeX export

Example scenarios:

```text
BB84NoiseSweep
BB84InterceptResend
E91BellTest
AuthOverheadComparison
HybridVsPQCOnly
```

### `ui/`

The Web UI is an orchestration and visualization layer, split into:

```text
ui/backend/   = FastAPI routes, typed schemas, capabilities, and domain adapters
ui/frontend/  = React, TypeScript, Vite, Tailwind CSS, Recharts, and Lucide
```

The backend maps validated HTTP requests to `BB84Protocol`, `SeededRNG`, and the public channel
classes. It converts NumPy-backed domain results into JSON-safe DTOs. The frontend discovers real and
planned functionality through `/api/capabilities`; planned features are always disabled and never
produce fabricated data.

The UI currently exposes complete BB84 sessions, seeded reproducibility, sequential channel
composition, sifting, diagnostic full-key QBER, sampled parameter estimation, Cascade transcript
leakage, verification status, privacy-amplification summaries, basis/outcome distributions, and a
bounded raw-transmission inspector. It does not contain quantum or post-processing algorithms.
Completed sessions may expose their final **simulated** key for educational inspection, while large
public Toeplitz seeds remain internal to the backend.

### BB84 classical post-processing

The implemented QKD flow is:

```text
n_raw -> quantum transmission -> sifting -> n_sifted
      -> disclose random sample and remove it -> n_candidate
      -> Cascade reconciliation -> universal-hash confirmation
      -> asymptotic length estimator -> FFT Toeplitz hashing -> L_final
```

`BB84Result.qber` compares the complete sifted arrays and is simulation-only diagnostic data.
Security decisions use `ParameterEstimationResult.estimated_qber`, calculated from public sampled
bits that are then removed from both candidate keys. Cascade reveals Alice block/subdivision
parities and conservatively counts each disclosure in `leak_ec`. Confirmation reveals a short
universal-hash tag and counts its length. The Toeplitz seeds used for confirmation and extraction
are public randomness, not secret-key consumption.

The security estimator uses the asymptotic symmetric BB84 phase-error assumption and subtracts the
actual Cascade and verification leakage once. It is not a composable finite-key proof and makes no
invented epsilon-security claim. All classical communication is assumed authenticated; PQC
authentication belongs in a future upper-layer integration and is intentionally absent here.

---

## 5. Where Specific Functions Should Live

| Function or concept | Module |
|---|---|
| `SeededRNG` | `core/rng.py` |
| `random_bit` | `core/rng.py` |
| `as_ket` | `quantum/linalg.py` |
| `tensor` | `quantum/linalg.py` |
| `partial_trace` | `quantum/linalg.py` |
| `is_normalized_state` | `quantum/validation.py` |
| `is_quantum_state` | `quantum/validation.py` |
| `is_density_matrix` | `quantum/validation.py` |
| `is_unitary` | `quantum/validation.py` |
| `dm_from_ket` | `quantum/states.py` |
| `fidelity` | `quantum/measures.py` |
| `trace_distance` | `quantum/measures.py` |
| `KET0`, `KET1`, `PLUS`, `MINUS` | `qkd/primitives/states.py` |
| `X`, `Y`, `Z`, `H` | `qkd/primitives/operations.py` |
| standard Z/X/Y measurements | `qkd/primitives/measurements.py` |
| `QuantumChannel` | `qkd/channel/base.py` |
| `IdentityChannel` | `qkd/channel/ideal.py` |
| `KrausChannel` | `qkd/channel/kraus.py` |
| `DepolarizingChannel` | `qkd/channel/noise/depolarizing.py` |
| Pauli, bit-flip, and phase-flip channels | `qkd/channel/noise/pauli.py` |
| `AmplitudeDampingChannel` | `qkd/channel/noise/amplitude_damping.py` |
| `ChannelPipeline` | `qkd/channel/pipeline.py` |
| `BB84Protocol` | `qkd/protocols/bb84.py` |
| `qber` | `qkd/metrics/qber.py` |
| `MLDSA65` | `pqc/signatures/ml_dsa.py` |
| `PQCParty`, `PublicIdentity` | `pqc/protocol/` |
| `MLKEM768`, `HQC3` | `pqc/kem/` |
| `PQCProfile` | `pqc/profiles.py` |
| `ServerKeyOffer`, `SignedServerKeyOffer`, `EncapsulationResponse` | `pqc/protocol/messages.py` |
| `ResponderKEMState`, `ServerKeyOfferFactory` | `pqc/protocol/server_offer.py` |
| `ServerKeyOfferProcessor`, `InitiatorKEMState` | `pqc/protocol/initiator.py` |
| future QKD/PQC composition | upper orchestration layer, never direct `qkd`/`pqc` imports |

---

## 6. Build Order

Current development order:

1. Quantum and QKD primitives (complete)
2. Quantum-channel foundation (complete)
3. Ideal and noisy BB84 over composable quantum channels (complete)
4. Sifting and QBER (complete)
5. Web UI V1 for interactive BB84 simulation (complete)
6. Noise experiments using the CPTP channel models
7. Optical transmission and loss as a separate physical layer
8. Advanced postprocessing (parameter estimation, Cascade, confirmation, and Toeplitz extraction complete)
9. PQC authentication: identity/trust, authenticated ephemeral offers, and Alice-side encapsulation complete; signed response, Bob decapsulation, shared-key derivation, and comparative experiments remain

This order gives you useful tests early and avoids building experiment code before the mathematical foundation is stable.

---

## 7. Testing Structure

Tests should mirror the source tree:

```text
tests/
|-- test_core/
|   `-- test_rng.py
|-- test_quantum/
|   |-- test_linalg.py
|   |-- test_validation.py
|   |-- test_states.py
|   `-- test_measures.py
|-- test_qkd/
|   |-- test_primitives.py
|   |-- test_measurement.py
|   |-- test_channel/
|   |   |-- test_ideal.py
|   |   |-- test_kraus.py
|   |   |-- test_noise.py
|   |   `-- test_pipeline.py
|   |-- test_bb84.py
|   `-- test_metrics.py
|-- test_pqc/
`-- test_experiments/
```

Testing rules:

- simulation tests involving injected randomness must use `SeededRNG`
- PQC cryptographic tests must use secure backend randomness and assert invariants, not deterministic keys/signatures
- validation tests should include invalid shapes, non-normalized states, and floating-point tolerance cases
- QKD tests should include known analytical behavior, such as ideal BB84 producing QBER 0
- experiment tests should verify reproducibility from the same seed

---

## 8. Naming Rules

Use lowercase package names:

```text
qkd/
pqc/
quantum/
core/
experiments/
```

Avoid uppercase package directories such as `QKD/`. They work on Windows, but can cause portability issues on Linux and CI.

Prefer explicit module names:

```text
validation.py
measurement.py
privacy_amplification.py
```

Avoid broad names once the file starts growing:

```text
utils.py
math.py
helpers.py
```

---

## 9. Key Architectural Decisions

### Why `quantum/` exists separately from `core/`

`core/` should be usable by every part of the system, including PQC and experiments, without importing quantum physics concepts. Functions like `is_quantum_state` and `dm_from_ket` are reusable, but they are not generic infrastructure. They belong in `quantum/`.

### Why QKD primitives are not in `quantum/`

`quantum/` provides general mathematical truth. `qkd/` provides protocol-specific conventions. For example, a ket vector belongs conceptually to `quantum`, but the BB84 meaning of `PLUS` as a diagonal-basis bit belongs to `qkd`.

### Why QKD and PQC do not import each other

The thesis contribution is the comparison and integration of QKD sessions with PQC authentication. That integration should be explicit and measurable. Keeping QKD and PQC as siblings makes the experiments cleaner and avoids hidden coupling.

### Why experiments are a separate layer

Protocols should simulate behavior. Experiments should decide what to compare, how many runs to execute, what parameters to sweep, and how to export results.

---

## 10. Current Immediate Goal

The mathematical primitives, quantum-channel foundation, complete BB84 post-processing, Web UI,
and PQC Phases 1-3 are in place. Alice authenticates Bob's canonical LOW or HIGH offer using only
her provisioned trust store, then creates public ciphertexts and private KEM shared secrets. Bob has
not received or authenticated the response and has not decapsulated it at protocol level. Handshake
completion and QKD/PQC orchestration remain future work, so simulated QKD workflows must not yet be
treated as end-to-end authenticated sessions.
