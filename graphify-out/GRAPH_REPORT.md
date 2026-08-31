# Graph Report - QuantumSec  (2026-08-22)

## Corpus Check
- 130 files · ~26,738 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 937 nodes · 1782 edges · 55 communities (42 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 68 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1f3d647d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- QuantumSec Development Task Roadmap
- dm_from_ket
- SeededRNG
- validation.py
- IdentityChannel
- ProjectiveMeasurement
- as_ket
- Tarea 10 — Crear quantum/information.py
- information.py
- QuantumChannel
- bases.py
- test_noise.py
- PauliChannel
- KrausChannel
- _prepare_density_matrix
- PhaseFlipChannel
- api.ts
- .apply
- .apply
- Tarea 22 — Revisar dependencias
- Immutable Compact Measurement Result
- benchmarks/__init__.py
- core/__init__.py
- qkd/__init__.py
- qber
- sift_keys
- integer
- BB84Result
- errors.py
- quantum/__init__.py
- quantumsec
- schemas.py
- devDependencies
- compilerOptions
- bb84.py
- test_pipeline.py
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- compilerOptions
- AppShell.tsx
- QuantumSec Web UI V1
- _InvalidOutputChannel
- test_ideal.py
- ResizeObserverMock
- .apply
- FeatureComingSoon.tsx
- tsconfig.json
- test_ui/__init__.py
- backend/__init__.py
- ui/__init__.py

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 39 edges
2. `dm_from_ket()` - 35 edges
3. `StrictModel` - 24 edges
4. `KrausChannel` - 23 edges
5. `QuantumChannel` - 20 edges
6. `run_bb84()` - 19 edges
7. `IdentityChannel` - 19 edges
8. `sample_projective_outcome()` - 19 edges
9. `sift_keys()` - 19 edges
10. `DepolarizingChannel` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Modular and Extensible Architecture` --semantically_similar_to--> `QuantumSec Project Structure`  [INFERRED] [semantically similar]
  README.md → docs/structure.md
- `RNG Dependency Injection` --semantically_similar_to--> `Config-and-Seed Reproducibility`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → docs/structure.md
- `build_channel()` --calls--> `IdentityChannel`  [INFERRED]
  ui/backend/adapters.py → qkd/channel/ideal.py
- `build_channel()` --calls--> `AmplitudeDampingChannel`  [INFERRED]
  ui/backend/adapters.py → qkd/channel/noise/amplitude_damping.py
- `build_channel()` --calls--> `DepolarizingChannel`  [INFERRED]
  ui/backend/adapters.py → qkd/channel/noise/depolarizing.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Adaptive QKD Agent Roles** — docs_agents_protocol_controller_agent, docs_agents_adaptive_channel_agent, docs_agents_experiment_orchestrator, docs_agents_qkdn_routing_agent, docs_agents_observe_decide_act [EXTRACTED 1.00]
- **Layered Module Architecture** — docs_structure_core_layer, docs_structure_quantum_layer, docs_structure_qkd_layer, docs_structure_pqc_layer, docs_structure_experiments_layer [EXTRACTED 1.00]
- **Projective Measurement Refactor** — docs_tasks_projectivemeasurement, docs_tasks_measurementsample, docs_tasks_sample_projective_outcome, docs_tasks_measure_projective, docs_tasks_probability_validation_before_clipping, docs_tasks_optional_state_validation [EXTRACTED 1.00]
- **Measurement Validation and Behavior Test Coverage** — reports_11_projector_tests_projector_validation_tests, reports_12_projective_measurement_tests_complete_projective_measurement_tests, reports_13_projective_measurement_tests_projectivemeasurement_tests, reports_14_sampling_tests_sampling_tests, reports_15_collapse_tests_collapse_tests, reports_16_information_tests_quantum_information_tests [INFERRED 0.85]
- **Minimal and Extensible Quantum Architecture** — reports_18_numpy_types_preserve_numpy_model, reports_22_dependencies_dependency_minimization, reports_23_no_wrappers_no_numeric_wrappers, reports_23_no_wrappers_domain_class_exception, reports_24_povm_boundary_projective_api_boundary, reports_24_povm_boundary_future_povm_support [INFERRED 0.85]
- **Projective Measurement Execution Pipeline** — reports_03_projective_measurement_projectivemeasurement, reports_05_probability_validation_born_probability_validation, reports_07_sampling_and_collapse_sample_projective_outcome, reports_07_sampling_and_collapse_measure_projective, reports_04_refactor_measure_projective_luders_update [INFERRED 0.95]

## Communities (55 total, 13 thin omitted)

### Community 0 - "QuantumSec Development Task Roadmap"
Cohesion: 0.06
Nodes (62): Gitignore-Aware Indexing, Python Language Server, QuantumSec Serena Project Configuration, UTF-8 Project Encoding, Whole-Project Workspace, BaseRNG, RNG Dependency Injection, Domain Random Helper Functions (+54 more)

### Community 1 - "dm_from_ket"
Cohesion: 0.05
Nodes (57): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., Reusable standard projective measurements for QKD protocols. (+49 more)

### Community 2 - "SeededRNG"
Cohesion: 0.07
Nodes (43): BaseRNG, GlobalRNG, ABC, integer, ndarray, QRNGSimulator, random_basis(), random_bit() (+35 more)

### Community 3 - "validation.py"
Cohesion: 0.09
Nodes (48): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+40 more)

### Community 4 - "IdentityChannel"
Cohesion: 0.23
Nodes (14): IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, parametrize, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness(), test_bb84_encoding_convention_returns_expected_density_matrix(), test_bb84_encoding_rejects_invalid_symbols() (+6 more)

### Community 5 - "ProjectiveMeasurement"
Cohesion: 0.08
Nodes (39): MeasurementSample, Tarea 2 — Añadir MeasurementSample, Sampling Result Without Post-state, Prevalidated Read-only Measurement, ProjectiveMeasurement, Tarea 3 — Crear ProjectiveMeasurement, Lüders State Update, measure_projective (+31 more)

### Community 6 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 7 - "Tarea 10 — Crear quantum/information.py"
Cohesion: 0.10
Nodes (27): Born Probability Validation, Tarea 5 — Validar probabilidades antes de recortar, Validate Before Clipping, Tarea 6 — Añadir validate_state, Safe and Fast Measurement Paths, validate_state, fidelity, PSD Matrix Square Root (+19 more)

### Community 8 - "information.py"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

### Community 9 - "QuantumChannel"
Cohesion: 0.18
Nodes (13): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+5 more)

### Community 10 - "bases.py"
Cohesion: 0.18
Nodes (15): Enum, bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases. (+7 more)

### Community 11 - "test_noise.py"
Cohesion: 0.19
Nodes (18): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result() (+10 more)

### Community 12 - "PauliChannel"
Cohesion: 0.22
Nodes (5): Return a finite scalar probability in the closed unit interval., _validate_probability(), PauliChannel, Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability.

### Community 13 - "KrausChannel"
Cohesion: 0.14
Nodes (15): KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel., Evaluate ``sum_i K_i rho K_i^dagger``., Named single-qubit operators commonly used by QKD protocols. (+7 more)

### Community 14 - "_prepare_density_matrix"
Cohesion: 0.22
Nodes (8): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Apply each component from first to last without mutating the input.

### Community 15 - "PhaseFlipChannel"
Cohesion: 0.20
Nodes (8): PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix., Single-qubit channel that applies Pauli Z with probability ``p``., test_phase_flip_maps_plus_to_minus()

### Community 16 - "api.ts"
Cohesion: 0.05
Nodes (67): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), App(), Panel(), PanelProps (+59 more)

### Community 17 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 18 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 19 - "Tarea 22 — Revisar dependencias"
Cohesion: 0.67
Nodes (4): Minimize Mandatory Dependencies, Optional Qiskit Extra, Pyright Virtual-environment Resolution, Tarea 22 — Revisar dependencias

### Community 20 - "Immutable Compact Measurement Result"
Cohesion: 1.00
Nodes (3): Immutable Compact Measurement Result, MeasurementResult, Tarea 1 — Mejorar MeasurementResult

### Community 24 - "qber"
Cohesion: 0.19
Nodes (13): QKD metric computations., _binary_vector(), ArrayLike, ndarray, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, Return a validated one-dimensional binary integer vector. (+5 more)

### Community 25 - "sift_keys"
Cohesion: 0.10
Nodes (27): Classical QKD post-processing., _basis_vector(), _copy_binary_vector(), _copy_indices(), ArrayLike, Basis, intp, NDArray (+19 more)

### Community 27 - "BB84Result"
Cohesion: 0.11
Nodes (14): BB84Result, _copy_binary_vector(), intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation. (+6 more)

### Community 31 - "schemas.py"
Cohesion: 0.08
Nodes (56): BaseModel, Basis, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post (+48 more)

### Community 32 - "devDependencies"
Cohesion: 0.04
Nodes (47): jsdom, lucide-react, react, react-dom, recharts, tailwindcss, @tailwindcss/vite, @testing-library/jest-dom (+39 more)

### Community 33 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 34 - "bb84.py"
Cohesion: 0.21
Nodes (13): integer, _copy_bb84_bases(), encode_bb84_state(), ArrayLike, Basis, ComplexArray, Reproducible prepare-and-measure simulation of the BB84 protocol., Build an immutable density matrix for a validated named BB84 state. (+5 more)

### Community 35 - "test_pipeline.py"
Cohesion: 0.22
Nodes (12): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_bit_flip_channel_extremes(), test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels() (+4 more)

### Community 36 - "Q: How should the BB84 core integrate with QuantumSec architecture?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How should the BB84 core integrate with QuantumSec architecture?, Source Nodes

### Community 37 - "Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron, Source Nodes

### Community 38 - "Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??, Source Nodes

### Community 39 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 40 - "AppShell.tsx"
Cohesion: 0.23
Nodes (9): AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection, sections, Sidebar() (+1 more)

### Community 42 - "QuantumSec Web UI V1"
Cohesion: 0.29
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 43 - "_InvalidOutputChannel"
Cohesion: 0.33
Nodes (5): QuantumChannel, _InvalidOutputChannel, ArrayLike, ComplexArray, test_bb84_validates_the_injected_channels_output_by_default()

### Community 44 - "test_ideal.py"
Cohesion: 0.60
Nodes (4): parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing(), test_identity_rejects_nonphysical_density_matrices_by_default()

### Community 46 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

## Knowledge Gaps
- **109 isolated node(s):** `quantumsec`, `Supported V1 features`, `API`, `Development`, `Verification` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_bb84()` connect `schemas.py` to `SeededRNG`, `test_pipeline.py`, `IdentityChannel`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `dm_from_ket()` connect `dm_from_ket` to `bb84.py`, `validation.py`, `IdentityChannel`, `test_pipeline.py`, `as_ket`, `information.py`, `test_noise.py`, `test_ideal.py`, `KrausChannel`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `dm_from_ket`, `_InvalidOutputChannel`, `IdentityChannel`, `schemas.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `SeededRNG` (e.g. with `test_eigenstates_sample_deterministically()` and `test_fast_sampling_path_keeps_probability_checks_before_clipping()`) actually correct?**
  _`SeededRNG` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `KrausChannel` (e.g. with `AmplitudeDampingChannel` and `DepolarizingChannel`) actually correct?**
  _`KrausChannel` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `quantumsec`, `Supported V1 features`, `API` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `QuantumSec Development Task Roadmap` be split into smaller, more focused modules?**
  _Cohesion score 0.05711263881544157 - nodes in this community are weakly interconnected._