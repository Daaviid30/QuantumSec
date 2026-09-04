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
|   |-- _encoding.py
|   |-- errors.py
|   |-- profiles.py
|   |-- backends/
|   |   |-- oqs_backend.py
|   |   `-- oqs_kem_backend.py
|   |-- kem/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- ml_kem.py
|   |   `-- hqc.py
|   |-- kdf/
|   |   |-- __init__.py
|   |   |-- combiner.py
|   |   `-- hkdf.py
|   |-- signatures/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   `-- ml_dsa.py
|   `-- protocol/
|       |-- __init__.py
|       |-- _shared_secret_state.py
|       |-- identity.py
|       |-- trust.py
|       |-- party.py
|       |-- messages.py
|       |-- server_offer.py
|       |-- initiator.py
|       |-- client_exchange.py
|       |-- transcript.py
|       |-- key_schedule.py
|       `-- key_confirmation.py
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

Implemented PQC structure through Phase 6:

```text
pqc/backends/       = isolated external-provider adapters
pqc/signatures/     = signature interface and ML-DSA-65 implementation
pqc/kem/            = KEM interface plus ML-KEM-768 and HQC-3 providers
pqc/kdf/            = canonical KEM-secret encoding and the cryptography HKDF-SHA-384 adapter
pqc/profiles.py     = centralized LOW/HIGH QuantumSec profiles
pqc/protocol/       = identities, trust, messages, transcript, key schedule, Finished confirmation, and established sessions
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
- canonical, domain-separated `ClientKeyExchange` serialization containing Alice's fresh nonce and bound to the exact offer by SHA-384
- validated JSON-compatible Base64 transport mappings for public handshake messages
- explicit, idempotent release of ephemeral responder KEM references on session abort/expiry
- ML-DSA-65 authentication of Bob's public ephemeral KEM offer
- trust-backed Alice-side authentication before any KEM encapsulation
- private `InitiatorKEMState` secrets separated from public `EncapsulationResponse` ciphertexts
- explicit, idempotent release of Alice's shared-secret references on session abort/expiry
- Alice's ML-DSA-65 signature over the existing Phase 3 ciphertexts, without re-encapsulation
- Bob-side session, profile, offer-hash, trust, and signature validation before any decapsulation
- private `ResponderSharedSecretState` separated from the public signed client exchange
- one-shot release of Bob's ephemeral KEM private capabilities after every required decapsulation succeeds
- a private shared-secret state base centralizing validation, repr safety, idempotent closure, and context-manager lifecycle without merging the semantic Alice/Bob state types
- exact authenticated public-message references retained by successful Phase 3/4 results to prevent transcript/result mixing
- immutable canonical `PQCHandshakeTranscript` containing both messages, signer identities, algorithms, and signatures, with public JSON-compatible structural round-trip helpers that do not authenticate signatures
- public SHA-384 transcript hash used as the HKDF salt
- LOW canonical ML-KEM input and HIGH fixed-order ML-KEM-768/HQC-3 input with algorithm and length boundaries
- shared Alice/Bob `PQCSessionKeyDeriver` backed by `cryptography` HKDF-SHA-384
- private, repr-safe, non-serializable `DerivedSessionKeyState` containing the 32-byte transcript-bound session key and requiring explicit live-state export for symmetric-key consumers
- separate 32-byte `K_CONFIRM` derivation from the same canonical KEM input under the `ConfirmationKey` HKDF domain
- immutable, JSON-compatible `PQCFinishedMessage` values with explicit session, profile, transcript, algorithm, and sender role
- role-separated HMAC-SHA-384 Finished inputs; Alice's Finished additionally binds Bob's verified `verify_data`
- constant-time Finished verification and an ordered Bob-to-Alice-to-Bob state machine
- `ConfirmedPQCHandshake` proof and role-local `EstablishedPQCSession` handles created only after both Finished values verify
- release of source KEM secret references after successful confirmation-key derivation, without claiming memory zeroization

The staged flow now covers six phases: (1) ML-DSA identities and explicit trust, (2) Bob's signed
ephemeral KEM offer, (3) Alice's verification and encapsulation, and (4) Alice's signed
`ClientKeyExchange` followed by Bob's verify-before-decapsulate processing, and (5) canonical
transcript construction plus HKDF-SHA-384 session-key derivation, and (6) separate confirmation-key
derivation plus mutual role-bound Finished verification. The HIGH keys are bound to both
independently established KEM secrets through QuantumSec's explicit research diversity
construction; this is not a standardized NIST multi-KEM combiner or a formal robust-combiner claim.

The KEM source states expose only a private KDF-input method and release their secret references
after both `K_SESSION` and `K_CONFIRM` have been derived successfully. `K_CONFIRM` is never exported;
`K_SESSION` has no transport mapping and remains available only through an explicit live-state
export. A session is established by the Finished state machine, never by direct Alice/Bob key
comparison. Application-data encryption and QKD/PQC composition remain later work.
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
| canonical KEM input, HKDF-SHA-384 adapter | `pqc/kdf/` |
| `PQCProfile` | `pqc/profiles.py` |
| `ServerKeyOffer`, `SignedServerKeyOffer`, `EncapsulationResponse`, `ClientKeyExchange`, `SignedClientKeyExchange` | `pqc/protocol/messages.py` |
| `ResponderKEMState`, `ServerKeyOfferFactory` | `pqc/protocol/server_offer.py` |
| `ServerKeyOfferProcessor`, `InitiatorKEMState` | `pqc/protocol/initiator.py` |
| `ClientKeyExchangeFactory`, `ClientKeyExchangeProcessor`, `ResponderSharedSecretState` | `pqc/protocol/client_exchange.py` |
| shared private lifecycle for initiator/responder KEM secrets | `pqc/protocol/_shared_secret_state.py` |
| `PQCHandshakeTranscript` | `pqc/protocol/transcript.py` |
| `PQCSessionKeyDeriver`, `DerivedSessionKeyState` | `pqc/protocol/key_schedule.py` |
| `PQCConfirmationKeyDeriver`, `PQCKeyConfirmation`, `ConfirmedPQCHandshake`, `EstablishedPQCSession` | `pqc/protocol/key_confirmation.py` |
| `PQCFinishedMessage`, `PQCFinishedRole` | `pqc/protocol/messages.py` |
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
9. PQC authentication and key establishment: identity/trust, signed ephemeral exchange, Bob-side decapsulation, transcript-bound key derivation, and mutual HMAC-SHA-384 Finished confirmation complete; comparative experiments remain

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
and all six PQC handshake phases are in place. After mutual authentication and KEM establishment,
both roles derive transcript-bound session and confirmation keys under separate HKDF domains. Bob's
Finished is verified before Alice's chained Finished is created; only Bob's successful final
verification yields confirmed, role-local established-session handles. Tests may compare Alice and
Bob keys as an oracle, but the protocol never uses direct key comparison for establishment.
Application-data protection and QKD/PQC orchestration remain future work.
