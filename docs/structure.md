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
|   |   `-- measurement.py
|   |-- channel/
|   |   |-- __init__.py
|   |   |-- noise.py
|   |   |-- loss.py
|   |   `-- attacks.py
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
|   |-- signatures/
|   |-- kem/
|   |-- hybrid/
|   `-- auth/
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
    -> experiments
        -> qkd, pqc
            -> quantum
                -> core
                    -> external libraries
```

More explicitly:

```text
experiments -> qkd, pqc, quantum, core
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
- physics errors: `QuantumStateError`, `QuantumOperatorError`

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
qkd.primitives.states.BASIS_Z             # no, QKD/convention-specific
```

### `qkd/`

QKD simulation domain. This layer uses `quantum/` to implement concrete protocol behavior.

Suggested structure:

```text
qkd/primitives/
qkd/channel/
qkd/protocols/
qkd/postprocessing/
qkd/metrics/
```

Responsibilities:

- protocol states and bases: `KET0`, `KET1`, `PLUS`, `MINUS`, `BASIS_Z`, `BASIS_X`
- gates/operators used by QKD simulations: `X`, `Y`, `Z`, `H`, `CNOT`
- measurements with injected RNG
- channel models: depolarizing, bit flip, phase flip, amplitude damping, loss
- attacks: intercept-resend, man-in-the-middle model for classical channel studies
- protocols: BB84, B92, E91
- postprocessing: sifting, reconciliation, privacy amplification
- metrics: QBER, key generation rate, efficiency, security thresholds

Important distinction:

```text
quantum/validation.py can say whether a vector is a valid quantum state.
qkd/primitives/states.py can say which valid states are used by BB84.
qkd/protocols/bb84.py decides how Alice and Bob use those states.
```

### `pqc/`

Post-quantum cryptography and authentication. This module should not import from `qkd/`. Its job is to provide cryptographic tools and interfaces that can be used by experiments or authentication adapters.

Suggested structure:

```text
pqc/signatures/
pqc/kem/
pqc/hybrid/
pqc/auth/
```

Responsibilities:

- signature interfaces: `keygen`, `sign`, `verify`
- KEM interfaces: `keygen`, `encapsulate`, `decapsulate`
- hybrid schemes
- QKD classical-channel authentication wrappers
- benchmarkable authentication overhead results

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
| `measure(state, basis, rng)` | `qkd/primitives/measurement.py` |
| `DepolarizingChannel` | `qkd/channel/noise.py` |
| `BB84Protocol` | `qkd/protocols/bb84.py` |
| `qber` | `qkd/metrics/qber.py` |
| `DilithiumSignature` | `pqc/signatures/dilithium.py` |
| `QKDSessionAuthenticator` | `pqc/auth/` or `experiments/auth/` boundary |

---

## 6. Build Order

Recommended implementation order:

1. `core/rng.py`
2. `quantum/linalg.py`
3. `quantum/validation.py`
4. `quantum/states.py`
5. `quantum/measures.py`
6. `qkd/primitives/states.py`
7. `qkd/primitives/operations.py`
8. `qkd/primitives/measurement.py`
9. `qkd/channel/noise.py`
10. `qkd/protocols/base.py`
11. `qkd/protocols/bb84.py`
12. `qkd/postprocessing/sifting.py`
13. `qkd/metrics/qber.py`
14. `experiments/scenarios/bb84_noise_sweep.py`
15. `pqc/signatures/` and `pqc/auth/`
16. `experiments/scenarios/auth_overhead_comparison.py`

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
|   |-- test_channel.py
|   |-- test_bb84.py
|   `-- test_metrics.py
|-- test_pqc/
`-- test_experiments/
```

Testing rules:

- any test involving randomness must use `SeededRNG`
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

The short-term goal is to stabilize the mathematical foundation and QKD primitives:

- finish `quantum/linalg.py`
- finish `quantum/validation.py`
- implement `quantum/states.py`
- implement `quantum/measures.py`
- complete `qkd/primitives/states.py`
- complete `qkd/primitives/operations.py`
- add `qkd/primitives/measurement.py`
- keep tests updated under `tests/test_quantum/` and `tests/test_qkd/`

After that, BB84 can be implemented without needing to move core concepts around.

