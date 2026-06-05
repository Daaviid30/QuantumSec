# STRUCTURE.md — Quantum Security Platform

> **Project:** Modular simulation platform for QKD, PQC authentication, and QKDN  
> **Author:** David  
> **Scope:** TFM (Master's Thesis) → Research → Industrial/Educational Platform  
> **Stack:** Python + NumPy (core), liboqs (PQC bindings), Matplotlib/Seaborn (analysis), Web UI (phase 3)

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Project Phases](#2-project-phases)
3. [Top-Level Directory Layout](#3-top-level-directory-layout)
4. [Layer Architecture](#4-layer-architecture)
5. [Module: core — Shared Infrastructure](#5-module-core--shared-infrastructure)
6. [Module: qkd — Quantum Key Distribution](#6-module-qkd--quantum-key-distribution)
7. [Module: pqc — Post-Quantum Cryptography](#7-module-pqc--post-quantum-cryptography)
8. [Module: qkdn — Quantum Key Distribution Network](#8-module-qkdn--quantum-key-distribution-network-future)
9. [Module: experiments — Orchestration & Analysis](#9-module-experiments--orchestration--analysis)
10. [Module: ui — Web Interface](#10-module-ui--web-interface-phase-3)
11. [Module: tests — Testing Infrastructure](#11-module-tests--testing-infrastructure)
12. [Cross-Cutting Concerns](#12-cross-cutting-concerns)
13. [Dependency Rules](#13-dependency-rules)
14. [Build Order & Milestones](#14-build-order--milestones)
15. [Key Design Decisions](#15-key-design-decisions)

---

## 1. Design Philosophy

The platform is built around four non-negotiable principles:

**Modularity.** Each module is self-contained. It can be imported, tested, and benchmarked independently of every other module. No protocol code reaches into the PQC layer; no analysis code modifies simulation state. This is what makes the codebase publishable and extensible.

**Reproducibility.** Every simulation run is fully determined by a configuration file and a random seed. Given the same config and seed, the exact same result must be produced on any machine, at any time. This is a hard requirement for scientific credibility.

**Physical accuracy.** Simulations reflect real quantum channel physics — noise models, loss rates, eavesdropping strategies — grounded in the literature (primary reference: Ramona Wolf, *Quantum Key Distribution*). Approximations are always documented and justified.

**Layered abstraction.** Upper layers call lower layers; never the reverse. This enforces clean interfaces and prevents accidental coupling. The dependency graph is a directed acyclic graph, not a web.

---

## 2. Project Phases

| Phase | Scope | Target |
|---|---|---|
| **Phase 0** | Shared infrastructure (`core/`) | Foundation before any quantum code |
| **Phase 1** | QKD simulation + classical auth | TFM core deliverable |
| **Phase 1.5** | PQC integration + hybrid auth | TFM extension, publishable result |
| **Phase 2** | Experiments & analysis framework | Scientific rigor, reproducibility |
| **Phase 3 (future)** | QKDN multi-node simulation | Research extension |
| **Phase 4 (future)** | Web UI | Educational/industrial tool |

---

## 3. Top-Level Directory Layout

```
quantum_sec/
│
├── core/               # Shared infrastructure — built first, used by everyone
├── qkd/                # QKD simulation engine — current primary focus
├── pqc/                # Post-quantum cryptography — NIST standards
├── qkdn/               # Multi-node network simulation [FUTURE]
├── experiments/        # Scenario runner, analysis, export
├── ui/                 # Web application [PHASE 4]
│
├── tests/              # Mirror of module structure — one test file per module
├── configs/            # YAML experiment configuration files
├── data/               # Raw simulation outputs [gitignored]
├── notebooks/          # Jupyter notebooks for exploration and visualization
├── docs/               # Architecture docs, API reference, research notes
│
├── STRUCTURE.md        # This file
├── README.md           # Project overview and quickstart
├── pyproject.toml      # Packaging and dependency management (Poetry or uv)
├── .env.example        # Environment variable template
└── Makefile            # Common tasks: test, lint, run, benchmark
```

---

## 4. Layer Architecture

The platform is organized into six horizontal layers. Each layer may only import from layers below it.

```
┌─────────────────────────────────────────────┐
│                   UI Layer                  │  Phase 4
├─────────────────────────────────────────────┤
│         Experiments & Orchestration         │  Phase 2
├──────────────────────┬──────────────────────┤
│    QKDN (future)     │                      │  Phase 3
├──────────────────────┤   PQC Module         │  Phase 1.5
│    QKD Module        │                      │  Phase 1
├──────────────────────┴──────────────────────┤
│           Core — Shared Infrastructure      │  Phase 0
└─────────────────────────────────────────────┘
```

The QKD and PQC modules are siblings — they do not import from each other directly. Their integration is handled by the `pqc/auth/` submodule and the `experiments/` layer, which knows about both.

---

## 5. Module: `core/` — Shared Infrastructure

The foundation layer. Contains no quantum or cryptographic logic — only mathematical utilities and infrastructure that every other module depends on.

```
core/
├── __init__.py
├── math/               # Linear algebra primitives
├── rng/                # Random number generation (PRNG + QRNG simulator)
├── config/             # Configuration loading and validation
├── logging/            # Structured experiment logging
└── benchmarking/       # Performance profiling decorators and utilities
```

### `core/math/`

Wraps NumPy into a stable API for quantum operations. All simulation code calls these functions — never NumPy directly. This indirection allows backend swapping (e.g. CuPy for GPU, JAX for autodiff) without touching protocol code.

**Key responsibilities:**
- Density matrix construction: `dm_from_ket(psi)`, `dm_from_ensemble(states, probs)`
- Tensor product: `tensor(*operators)`
- Partial trace: `partial_trace(rho, dims, subsystem)`
- Quantum information measures: `fidelity(rho, sigma)`, `trace_distance(rho, sigma)`, `von_neumann_entropy(rho)`
- Matrix validation: `is_hermitian(M)`, `is_positive_semidefinite(M)`, `is_unitary(U)`
- Spectral decomposition: `spectral_decomp(M)`

### `core/rng/`

All randomness in the platform flows through this module. The critical design requirement: every function that needs randomness must accept an `rng` parameter so tests can inject a seeded generator and get fully deterministic results.

**Key responsibilities:**
- `SeededRNG(seed)` — wraps `numpy.random.default_rng(seed)` for reproducible simulations
- `QRNGSimulator` — simulates true quantum randomness using physical noise models (for realism studies)
- `GlobalRNG` — singleton for production use when reproducibility is not required
- Helper functions: `random_bit()`, `random_basis()`, `random_unitary(n)`

### `core/config/`

YAML-based experiment configuration. Every parameter that affects a simulation — channel loss, noise rate, key length, protocol variant, authentication scheme — must be expressible in a config file.

**Key responsibilities:**
- `load_config(path)` — loads and validates a YAML config against a schema
- `ExperimentConfig` — typed dataclass representing a full simulation configuration
- Default config templates for each protocol
- Config merging: base config overridden by experiment-specific values

### `core/logging/`

Structured JSON logging tied to experiment identifiers. Every simulation run gets a unique `run_id` that is stamped on all log entries, enabling full traceability from final results back to raw runs.

**Key responsibilities:**
- `ExperimentLogger(run_id)` — structured logger with automatic parameter snapshotting
- Log levels: DEBUG (per-qubit events), INFO (per-frame summaries), WARNING (anomalies), ERROR (failures)
- Output: JSON Lines format for easy programmatic analysis

### `core/benchmarking/`

Timing and memory profiling. Essential for the overhead analysis comparing classical vs PQC authentication.

**Key responsibilities:**
- `@timed` — decorator that records wall-clock and CPU time per function call
- `@memory_profiled` — decorator that records peak memory per call
- `BenchmarkReport` — aggregates timing across many calls (mean, std, percentiles)
- Output compatible with the `experiments/analysis/` module

---

## 6. Module: `qkd/` — Quantum Key Distribution

The scientific core of the platform. Structured to separate physics (`primitives`, `channel`) from protocol logic (`protocols`) from classical post-processing (`postprocessing`). These are genuinely different concerns and must not be mixed.

```
qkd/
├── __init__.py
├── primitives/         # Quantum states, operators, measurement
├── channel/            # Physical transmission and noise models
├── protocols/          # Protocol implementations (BB84, E91, ...)
│   ├── bb84.py
│   ├── b92.py
│   ├── e91.py
│   └── bbm92.py
├── postprocessing/     # Sifting, reconciliation, privacy amplification
└── metrics/            # QBER, KGR, security parameters
```

### `qkd/primitives/`

Pure quantum mechanics. No protocol logic, no channel effects. This is the mathematical substrate that everything else is built on.

**Key responsibilities:**
- Computational basis states: `ket_0`, `ket_1`, `ket_plus`, `ket_minus`, `ket_i`, `ket_mi`
- Standard bases: `BASIS_Z` (rectilinear), `BASIS_X` (diagonal), `BASIS_Y` (circular)
- Single-qubit gates: Pauli X, Y, Z; Hadamard H; phase gates S, T; rotation gates Rx, Ry, Rz
- Two-qubit gates: CNOT, CZ, SWAP, controlled-U
- Bell state constructors: `bell_state(phi_plus | phi_minus | psi_plus | psi_minus)`
- Measurement operators: `measure(state, basis, rng)` — returns outcome + post-measurement state
- Projectors: `projector(ket)`, `povm(operators)`

### `qkd/channel/`

Models the physical quantum channel between Alice and Bob. This layer is where eavesdropping and noise are introduced. The QBER that emerges from a simulation is a product of what this layer does — it is not hardcoded or manually set.

**Key responsibilities:**

*Noise models (quantum channels as CPTP maps with Kraus operators):*
- `DepolarizingChannel(p)` — symmetric noise in all directions
- `BitFlipChannel(p)` — X errors only
- `PhaseFlipChannel(p)` — Z errors only
- `AmplitudeDampingChannel(gamma)` — photon loss and energy relaxation
- `GeneralizedChannel(kraus_ops)` — arbitrary user-defined channel

*Loss models:*
- `FiberLossChannel(length_km, attenuation_db_per_km)` — realistic fiber loss
- `TransmittanceModel(eta)` — generic transmittance parameter

*Eve attack models:*
- `InterceptResendAttack(intercept_fraction)` — Eve measures and resends qubits
- `BeamSplitterAttack(split_ratio)` — Eve taps a fraction of the optical signal
- `ManInTheMiddleAttack()` — full classical channel compromise (for auth studies)

*Channel composition:*
- `ChannelPipeline(*channels)` — chains multiple channels sequentially

### `qkd/protocols/`

Each file implements one complete protocol. All protocols share the same interface so the experiments layer can run them interchangeably.

**Shared protocol interface:**
```python
class QKDProtocol:
    def prepare(self, n_bits, rng) -> AliceState
    def transmit(self, alice_state, channel) -> BobState
    def measure(self, bob_state, rng) -> BobMeasurements
    def sift(self, alice_state, bob_measurements) -> SiftedKey
    def estimate_qber(self, sifted_key, sample_fraction) -> float
```

**`bb84.py`** — Bennett & Brassard 1984. Prepare-and-measure protocol using two conjugate bases (Z and X). Alice prepares random qubits in random bases; Bob measures in random bases; they discard mismatches. Reference: Wolf Ch. 3.

**`b92.py`** — Bennett 1992. Simplified two-state protocol. Uses only two non-orthogonal states. Higher qubit efficiency but lower noise tolerance.

**`e91.py`** — Ekert 1991. Entanglement-based protocol. Uses Bell state pairs; security is derived from violation of Bell inequalities (CHSH inequality). Reference: Wolf Ch. 5.

**`bbm92.py`** — Bennett, Brassard & Mermin 1992. Entanglement-based variant of BB84. Equivalent to BB84 from a security perspective but uses entangled pairs.

### `qkd/postprocessing/`

The classical pipeline that converts raw correlated bit strings into a verified, secret key. Runs after protocol completion.

**Key responsibilities:**

*Sifting:* `sift(alice_bases, bob_bases, alice_bits, bob_bits)` — discard bits where bases differ. Typically discards ~50% of raw bits in BB84.

*Information reconciliation:* Fix bit errors that remain after sifting.
- `CascadeReconciliation` — interactive parity-check protocol (classic, easy to implement)
- `LDPCReconciliation` — low-density parity-check codes (efficient, closer to production)
- Output: corrected key + number of bits leaked to Eve during reconciliation

*Privacy amplification:* Compress the reconciled key to eliminate any information Eve may have gained.
- `UniversalHashing(target_length)` — applies a random universal hash function
- `LeftoverHashLemma` — computes the achievable secret key length given QBER and reconciliation leakage
- Output: final secret key of length `l_final`

*Authentication of classical channel:* (interfaces with `pqc/auth/`)
- `ClassicalChannelAuth` — pluggable authenticator interface
- `MACSAuth` — information-theoretically secure MACs (Wegman-Carter)
- `PQCAuth` — delegates to `pqc/auth/` (Dilithium signatures)

### `qkd/metrics/`

Stateless metric computation. Takes simulation results as input; returns structured metric objects. Never modifies any simulation state.

**Key metrics:**
- **QBER** (Quantum Bit Error Rate) — `qber(alice_key, bob_key)`: fraction of differing bits after sifting
- **KGR** (Key Generation Rate) — `key_generation_rate(final_key_length, total_qubits_sent, time_elapsed)`
- **Efficiency** — `efficiency(sifted_key_length, raw_key_length)`: fraction of qubits that contributed to the final key
- **Mutual information** — `mutual_information_upper_bound(qber)`: Eve's maximum information under intercept-resend
- **Security parameter ε** — `security_parameter(privacy_amp_params)`: closeness to ideal secret key
- **SKR** (Secret Key Rate) — `secret_key_rate(qber, reconciliation_leakage, privacy_amp_output)`

---

## 7. Module: `pqc/` — Post-Quantum Cryptography

Implements NIST-standardized post-quantum algorithms, with a focus on their role in authenticating the classical channel of QKD sessions. The integration point with the QKD module is `pqc/auth/`.

```
pqc/
├── __init__.py
├── kem/                # Key Encapsulation Mechanisms
├── signatures/         # Digital signature schemes
├── hybrid/             # Classical + PQC hybrid schemes
└── auth/               # QKD classical channel authentication
```

**Backend strategy:** Use `liboqs-python` bindings (Open Quantum Safe project) for reference implementations. Wrap all calls behind an abstract interface so the backend can be swapped (e.g. to a pure-Python reference for debugging, or to a hardware module in production).

### `pqc/kem/`

Key Encapsulation Mechanisms based on lattice problems (Module-LWE).

**Algorithms:**
- `Kyber512` — NIST security level 1 (~AES-128 equivalent)
- `Kyber768` — NIST security level 3 (~AES-192 equivalent) ← primary target
- `Kyber1024` — NIST security level 5 (~AES-256 equivalent)

**Shared interface:**
```python
class KEM:
    def keygen() -> (PublicKey, SecretKey)
    def encapsulate(pk: PublicKey) -> (Ciphertext, SharedSecret)
    def decapsulate(sk: SecretKey, ct: Ciphertext) -> SharedSecret
```

**Metrics collected:** keygen time, encapsulation time, decapsulation time, public key size, ciphertext size.

### `pqc/signatures/`

Digital signature schemes. These are the primary mechanism for authenticating classical QKD messages (basis announcements, reconciliation data, parameter estimates).

**Algorithms:**
- `Dilithium2 / Dilithium3 / Dilithium5` — lattice-based, NIST primary recommendation ← TFM focus
- `Falcon512 / Falcon1024` — compact signatures, lattice-based (NTRU)
- `SPHINCS+` — hash-based, conservative security assumption

**Shared interface:**
```python
class SignatureScheme:
    def keygen() -> (PublicKey, SecretKey)
    def sign(sk: SecretKey, message: bytes) -> Signature
    def verify(pk: PublicKey, message: bytes, sig: Signature) -> bool
```

**Metrics collected:** keygen time, sign time, verify time, public key size, signature size.

### `pqc/hybrid/`

Combines classical and post-quantum algorithms for the transition period. The rationale: neither classical (vulnerable to Shor's algorithm) nor PQC alone (still maturing) is sufficient for high-assurance deployments.

**Schemes:**
- `X25519_Kyber768` — classical ECDH + Kyber KEM, combiner function produces a single shared secret
- `ECDSA_Dilithium3` — classical ECDSA + Dilithium signatures (dual-sign mode)
- `CombinerFunction` — pluggable KDF-based combiner (HKDF with domain separation)

**Threat model documented:** harvest-now-decrypt-later (HNDL) attacks, migration timeline analysis.

### `pqc/auth/`

The integration submodule. Implements the authenticated classical channel required by QKD protocols. This is the scientific core of the TFM's PQC contribution.

**Key responsibilities:**
- `QKDSessionAuthenticator` — wraps a `SignatureScheme` and provides `authenticate_message(msg)` and `verify_message(msg, sig)` for use during a QKD session
- `AuthOverhead` — measures and reports the computational and bandwidth overhead added by PQC authentication vs classical MAC-based authentication
- `AuthComparison` — runs both classical and PQC authentication on identical sessions and produces a comparison report (time, size, security level)
- Security model: documents what is protected (classical channel integrity), what is not (qubit transmission), and under what assumptions the scheme is secure

---

## 8. Module: `qkdn/` — Quantum Key Distribution Network [FUTURE]

Multi-node network simulation. Builds on the point-to-point QKD module by introducing topology, routing, and trusted node relay models.

```
qkdn/                   # [PHASE 3 - not yet implemented]
├── __init__.py
├── topology/           # Graph-based network representation
├── routing/            # Key routing algorithms
├── relay/              # Trusted node and quantum repeater models
└── metrics/            # Network-level metrics (end-to-end KGR, latency)
```

**High-level design intent:**

`topology/` — represents the network as a graph where nodes are QKD stations (Alice, Bob, or trusted relay) and edges are quantum channels with associated loss and noise parameters. Uses NetworkX as the graph backend.

`routing/` — finds paths between arbitrary source and destination pairs. Implements shortest-path (minimize hops), max-throughput (maximize KGR), and min-QBER routing strategies.

`relay/` — trusted node relay: XOR key chaining across hops. Quantum repeater model (future, requires entanglement swapping simulation).

`metrics/` — end-to-end secret key rate, hop-by-hop QBER accumulation, network throughput under load.

---

## 9. Module: `experiments/` — Orchestration & Analysis

The scientific layer. Defines reproducible scenarios, runs parameter sweeps, aggregates results, and generates publication-ready outputs. This is what transforms the simulation engine into a research platform.

```
experiments/
├── __init__.py
├── scenarios/          # Named, reproducible experiment definitions
│   ├── base.py         # Abstract Scenario class
│   ├── bb84_noise_sweep.py
│   ├── bb84_eve_attack.py
│   ├── e91_bell_test.py
│   └── auth_overhead_comparison.py
├── runner/             # Scenario execution engine
├── analysis/           # Statistical analysis and plotting
└── exporter/           # Result serialization (JSON, CSV, LaTeX)
```

### `experiments/scenarios/`

Each scenario is a self-contained experiment definition. A scenario specifies: which protocol, which channel model, which authentication scheme, which metrics to collect, and what the independent variable is (for sweeps).

**Abstract base:**
```python
class Scenario:
    config: ExperimentConfig
    def run(self, rng: SeededRNG) -> ScenarioResult
    def describe() -> str
```

**Example scenarios planned for TFM:**
- `BB84NoiseSweep` — sweep depolarizing noise from 0% to 15%; measure KGR, QBER, final key length
- `BB84EveIntercept` — vary Eve's intercept fraction; observe QBER increase and key rate collapse
- `E91BellTest` — measure CHSH inequality violation as a function of noise; security threshold analysis
- `AuthOverheadComparison` — compare Wegman-Carter MACs vs Dilithium3 vs Dilithium5 authentication overhead across 1000 sessions
- `HybridVsPQCOnly` — compare hybrid (ECDH+Kyber) vs PQC-only key establishment latency and size

### `experiments/runner/`

Executes scenarios with full reproducibility and optional parallelism.

**Key responsibilities:**
- `ScenarioRunner.run(scenario, n_runs, seed)` — runs a scenario n times with deterministic seeds derived from the master seed
- `ParameterSweepRunner` — varies one or more config parameters and runs a scenario for each combination
- Parallel execution via `concurrent.futures.ProcessPoolExecutor` (each worker gets its own seed)
- Progress tracking and graceful interruption handling
- Automatic result persistence to `data/` directory with config snapshot

### `experiments/analysis/`

Statistical aggregation and visualization. Takes raw `ScenarioResult` objects and produces analysis-ready outputs.

**Key responsibilities:**
- `aggregate(results)` — computes mean, std, min, max, 95th percentile across runs
- `qber_vs_noise_plot(results)` — QBER as a function of depolarizing noise
- `kgr_vs_distance_plot(results)` — key generation rate vs fiber distance
- `auth_overhead_plot(results)` — side-by-side comparison of authentication schemes
- `security_threshold_plot(results)` — maximum tolerable noise before security breaks down
- All plots use a consistent visual style (configurable, defaults to publication-ready black & white + one accent color)

### `experiments/exporter/`

Serializes results for external use.

**Key responsibilities:**
- `JSONExporter` — full fidelity, machine-readable, includes config snapshot and all raw runs
- `CSVExporter` — tabular summary, one row per (scenario, parameter value, metric)
- `LaTeXExporter` — generates `\begin{table}...\end{table}` blocks ready to paste into the TFM
- `FigureExporter` — saves matplotlib figures as PDF (vector) and PNG (raster) at publication DPI

---

## 10. Module: `ui/` — Web Interface [Phase 4]

Educational and industrial-facing interface. Allows non-experts to explore QKD and PQC concepts interactively, and allows researchers to launch experiments and visualize results without writing code.

```
ui/                     # [PHASE 4 - not yet designed in detail]
├── backend/            # FastAPI REST API + WebSocket for live simulation
└── frontend/           # React + D3.js interactive dashboard
```

**Planned features:**
- Interactive BB84 simulation: step through Alice preparation → channel transmission → Bob measurement → sifting → key generation
- Real-time QBER visualization as noise parameters are adjusted
- Protocol comparison dashboard
- Authentication overhead calculator (input session parameters, output latency and size)
- QKDN topology explorer (visualize network graph, routing paths, per-link KGR)

---

## 11. Module: `tests/` — Testing Infrastructure

The test tree mirrors the source tree exactly. Every module has a corresponding test file.

```
tests/
├── core/
│   ├── test_math.py
│   ├── test_rng.py
│   ├── test_config.py
│   └── test_logging.py
├── qkd/
│   ├── test_primitives.py
│   ├── test_channel.py
│   ├── test_bb84.py
│   ├── test_e91.py
│   ├── test_postprocessing.py
│   └── test_metrics.py
├── pqc/
│   ├── test_kem.py
│   ├── test_signatures.py
│   ├── test_hybrid.py
│   └── test_auth.py
└── experiments/
    ├── test_runner.py
    └── test_exporter.py
```

**Testing standards:**
- Unit tests must be deterministic: all tests that involve randomness must use a seeded RNG
- Physics validation tests: verify known analytical results (e.g. QBER of ideal BB84 = 0%, intercept-resend QBER ≈ 25%)
- Performance regression tests: key operations must not exceed documented time budgets
- All tests run via `pytest` with coverage report; target ≥ 90% line coverage on `core/` and `qkd/`

---

## 12. Cross-Cutting Concerns

### Reproducibility

Every simulation result must be 100% reproducible. The reproducibility contract:
1. Every function that uses randomness accepts an `rng: SeededRNG` parameter
2. Every experiment config includes a `seed` field
3. The runner derives per-run seeds deterministically from the master seed
4. Every result file includes the full config snapshot and seed used to produce it

### Serialization

All domain objects (qubit states, channel configurations, metric results) implement `to_dict()` and `from_dict()` for JSON serialization. No pickle.

### Error handling

Physics violations (e.g. non-trace-preserving channel, non-normalized state) raise `QuantumStateError` with a descriptive message. Configuration errors raise `ConfigValidationError`. All errors are logged before raising.

### Versioning

The library version is defined once in `pyproject.toml` and accessible as `quantum_sec.__version__`. Result files include the library version so old results can always be tied to the exact code that produced them.

---

## 13. Dependency Rules

The rule is simple: **a module may only import from modules in lower layers.** The dependency graph must remain acyclic.

```
Allowed import directions:
  ui           → experiments, qkd, pqc
  experiments  → qkd, pqc, core
  qkdn         → qkd, core
  qkd          → core
  pqc          → core
  core         → [external libraries only: numpy, scipy, yaml]

Forbidden (will break modularity):
  core         → qkd, pqc, experiments, ui
  qkd          → pqc, experiments, ui
  pqc          → qkd, experiments, ui
  qkd/channel  → qkd/protocols  (intra-module: lower cannot import upper)
```

Integration between `qkd` and `pqc` is handled exclusively in `pqc/auth/` and `experiments/`. Neither module imports the other.

---

## 14. Build Order & Milestones

### Milestone 0 — Foundation (Week 1–2)
- [ ] `core/math/` with full test suite
- [ ] `core/rng/` with seeded RNG interface
- [ ] `core/config/` with YAML loading and validation
- [ ] `core/logging/` with structured JSON output
- [ ] `Makefile` with `test`, `lint`, `format` targets

### Milestone 1 — QKD Core (Week 3–6)
- [ ] `qkd/primitives/` — qubit states, operators, measurement
- [ ] `qkd/channel/` — depolarizing and amplitude damping channels
- [ ] `qkd/protocols/bb84.py` — full prepare-and-measure BB84
- [ ] `qkd/postprocessing/` — sifting and privacy amplification
- [ ] `qkd/metrics/` — QBER and KGR computation
- [ ] End-to-end BB84 simulation producing a secret key

### Milestone 2 — Experiments Framework (Week 7–8)
- [ ] `experiments/scenarios/bb84_noise_sweep.py`
- [ ] `experiments/runner/` — basic scenario runner
- [ ] `experiments/analysis/` — QBER vs noise plot
- [ ] `experiments/exporter/` — JSON and CSV output
- [ ] First reproducible experiment with config file

### Milestone 3 — E91 + Eavesdropping (Week 9–11)
- [ ] `qkd/channel/` — intercept-resend attack model
- [ ] `qkd/protocols/e91.py` — entanglement-based protocol
- [ ] CHSH inequality measurement in metrics
- [ ] `experiments/scenarios/bb84_eve_attack.py`

### Milestone 4 — PQC Authentication (Week 12–15) ← TFM core
- [ ] `pqc/signatures/dilithium.py` — Dilithium2/3/5 via liboqs
- [ ] `pqc/auth/` — QKD session authenticator
- [ ] Authentication integration into BB84 postprocessing
- [ ] `experiments/scenarios/auth_overhead_comparison.py`
- [ ] TFM results: latency and size overhead tables

### Milestone 5 — TFM Completion (Week 16–18)
- [ ] Full experiment suite with reproducible results
- [ ] LaTeX table and figure export
- [ ] Documentation complete
- [ ] README with quickstart guide

### Future Milestones
- [ ] B92 and BBM92 protocols
- [ ] LDPC-based reconciliation
- [ ] Hybrid PQC schemes (`pqc/hybrid/`)
- [ ] QKDN module (`qkdn/`)
- [ ] Web UI (`ui/`)

---

## 15. Key Design Decisions

**Why pure NumPy instead of Qiskit?**
Performance and control. Qiskit's abstraction layer adds overhead and opacity. For a simulation platform focused on mathematical accuracy and benchmarking, direct NumPy operations are faster, easier to profile, and clearer in their physical meaning.

**Why YAML configs instead of code-defined experiments?**
Reproducibility and publication. A YAML file is a complete, human-readable description of an experiment that can be version-controlled, attached to a paper, and re-run by any reviewer. A Python script that defines parameters inline is fragile and harder to reproduce.

**Why separate `channel/` from `protocols/`?**
Because in real QKD, the channel is not part of the protocol — it is the environment the protocol must be secure against. Eve lives in the channel. Keeping them separate allows any protocol to be composed with any channel model without rewriting protocol logic.

**Why does `pqc/auth/` exist as a separate submodule?**
Because the integration between QKD and PQC is a research contribution, not a utility function. Elevating it to its own submodule gives it visibility, makes it independently testable, and makes the TFM contribution explicit in the code structure.

**Why no pickle?**
Pickle is not version-safe, not human-readable, and not language-portable. All serialization uses JSON via `to_dict()`/`from_dict()` interfaces. Results must outlive the code version that produced them.

---

*Last updated: project inception*  
*Next review: after Milestone 1 completion*