# Graph Report - QuantumSec  (2026-09-01)

## Corpus Check
- 158 files · ~38,683 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1078 nodes · 2115 edges · 83 communities (60 shown, 19 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 81 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c54e7632`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_bb84.py
- adapters.py
- validation.py
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- qber
- as_ket
- constants.py
- information.py
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- BB84Result
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- validate_aligned_keys
- sift_keys
- BB84SessionResult
- BaseRNG
- client.ts
- compilerOptions
- AppShell.tsx
- encode_bb84_state
- bb84.py
- SimulationConfigurator.tsx
- verify_reconciled_keys
- _copy_binary_vector
- .run
- Adaptive Agents for QKD
- _prepare_density_matrix
- estimate_qber_from_sample
- postprocessing/__init__.py
- SimulatorPage.tsx
- amplify_privacy
- PhaseFlipChannel
- ChannelPipeline.tsx
- ReconciliationResult
- QuantumSec Web UI V1
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- test_ideal.py
- ResizeObserverMock
- AmplitudeDampingChannel
- .apply
- quantum.information Module
- QuantumSec Web UI Architecture
- FeatureComingSoon.tsx
- tsconfig.json
- benchmarks/__init__.py
- core/__init__.py
- qkd/__init__.py
- errors.py
- quantum/__init__.py
- DEFAULT_ATOL Central Constant
- Standardized Error Messages and State Fix
- NumPy-style Docstrings Standard
- Project Dependencies and Pyright Setup
- test_ui/__init__.py
- backend/__init__.py
- ui/__init__.py
- QuantumSec Project Structure and Architectural Blueprint
- Core Layer Infrastructure Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Overview & README
- QuantumSec Development Task Roadmap
- QuantumSec Conventions Memory
- .gen
- .gen
- core.md

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 70 edges
2. `dm_from_ket()` - 37 edges
3. `BaseRNG` - 29 edges
4. `QuantumChannel` - 26 edges
5. `StrictModel` - 25 edges
6. `IdentityChannel` - 24 edges
7. `KrausChannel` - 23 edges
8. `BB84SessionResult` - 23 edges
9. `BB84Protocol` - 23 edges
10. `DepolarizingChannel` - 21 edges

## Surprising Connections (you probably didn't know these)
- `BB84 Classical Post-Processing Pipeline Spec` --semantically_similar_to--> `BB84 Session Simulation Flow`  [INFERRED] [semantically similar]
  docs/structure.md → README.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `QuantumSec Project Scope & Invariants`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/core.md
- `RNG Architecture Design Principles` --semantically_similar_to--> `Injected RNG Convention`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → .serena/memories/conventions.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `Layered Dependency Discipline`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/conventions.md
- `Graphify Knowledge Graph Integration Rules` --semantically_similar_to--> `Graphify Knowledge Graph Guidelines`  [INFERRED] [semantically similar]
  AGENTS.md → .agents/rules/graphify.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Complete BB84 Post-Processing & Execution Flow** — readme_bb84_simulation_pipeline, docs_structure_bb84_postprocessing_flow, serena_memories_qkd_core_channels_and_protocols [EXTRACTED 1.00]
- **Adaptive QKD Agent Roles** — docs_agents_protocol_controller_agent, docs_agents_adaptive_channel_agent, docs_agents_experiment_orchestrator, docs_agents_qkdn_routing_agent, docs_agents_observe_decide_act [EXTRACTED 1.00]
- **QuantumSec Layered Architecture Core-Quantum-QKD** — docs_structure_design_principles, serena_memories_conventions_layer_discipline, serena_memories_core_project_scope, docs_structure_module_responsibilities [EXTRACTED 1.00]
- **Projective Measurement Execution Pipeline** — reports_02_measurement_sample_measurement_sample, reports_03_projective_measurement_projective_measurement, reports_04_refactor_measure_projective_measure_projective, reports_07_sampling_and_collapse_sample_projective_outcome [EXTRACTED 1.00]
- **QKD Measurement Primitives and Standard Bases** — reports_08_basis_basis_enum, reports_09_standard_measurements_standard_measurements, reports_03_projective_measurement_projective_measurement [EXTRACTED 1.00]
- **Two-Tier Web Laboratory Frontend-Backend Deployment** — deployment_architecture, readme_web_lab, deployment_production_systemd [EXTRACTED 1.00]
- **Measurement and Sampling Test Suite** — reports_11_projector_tests_projector_tests, reports_12_projective_measurement_tests_measurement_tests, reports_13_projective_measurement_tests_class_tests, reports_14_sampling_tests_sampling_tests, reports_15_collapse_tests_collapse_tests [INFERRED 0.85]

## Communities (83 total, 19 thin omitted)

### Community 0 - "test_bb84.py"
Cohesion: 0.13
Nodes (24): IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig, BB84Protocol, Configuration for BB84's authenticated classical post-processing. The default…, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel, ArrayLike (+16 more)

### Community 1 - "adapters.py"
Cohesion: 0.07
Nodes (61): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+53 more)

### Community 2 - "validation.py"
Cohesion: 0.08
Nodes (50): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+42 more)

### Community 3 - "QuantumSec Serena Root Memory"
Cohesion: 0.20
Nodes (11): Query: Serena Onboarding & Memory Creation, QuantumSec Serena Root Memory, Serena Memory Progressive Discovery Model, Memory Maintenance Guidelines, Suggested Commands Memory, uv-Driven Tooling Commands, Task Completion Quality Gates Memory, Quality Gate Checklist (+3 more)

### Community 4 - "devDependencies"
Cohesion: 0.04
Nodes (47): jsdom, lucide-react, react, react-dom, recharts, tailwindcss, @tailwindcss/vite, @testing-library/jest-dom (+39 more)

### Community 5 - "ProjectiveMeasurement Class"
Cohesion: 0.07
Nodes (34): MeasurementSample Dataclass, Report: MeasurementSample Data Structure, ProjectiveMeasurement Class, Report: ProjectiveMeasurement Class, measure_projective Function, Report: Refactor measure_projective, Born Probability Validation Order, Report: Born Probability Validation Order (+26 more)

### Community 6 - "qber"
Cohesion: 0.11
Nodes (25): QKD metric computations., _binary_vector(), ArrayLike, ndarray, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, Return a validated one-dimensional binary integer vector. (+17 more)

### Community 7 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 8 - "constants.py"
Cohesion: 0.17
Nodes (12): Project-wide numerical constants with no domain-layer dependencies., bases_from_bits(), basis_from_bit(), integer, ndarray, Map the QKD random-bit convention 0/1 to the Z/X basis., Map a one-dimensional sequence of random bits to QKD bases., QKD-specific states, operations, bases, and standard measurements. (+4 more)

### Community 9 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "test_measures.py"
Cohesion: 0.06
Nodes (40): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), _born_probabilities(), measure_projective() (+32 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.15
Nodes (14): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+6 more)

### Community 14 - "BB84Result"
Cohesion: 0.11
Nodes (14): BB84Result, _copy_binary_vector(), intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation. (+6 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.13
Nodes (20): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+12 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.16
Nodes (20): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Efficient binary Toeplitz universal hashing for QKD post-processing., Return the public seed length for an ``output_length x input_length`` matrix., Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For… (+12 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.18
Nodes (12): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, A completely positive trace-preserving map validated at construction., Return the Hilbert-space dimension acted on by the channel., parametrize, test_kraus_channel_applies_operator_sum_without_mutating_input(), test_kraus_channel_rejects_invalid_operator_sets() (+4 more)

### Community 19 - "test_noise.py"
Cohesion: 0.14
Nodes (21): DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, BitFlipChannel, PauliChannel, Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., Single-qubit channel that applies Pauli X with probability ``p``., assert_valid_qubit_density_matrix() (+13 more)

### Community 20 - "dm_from_ket"
Cohesion: 0.15
Nodes (23): ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, dm_from_ensemble(), dm_from_ket(), ArrayLike, ComplexArray, Construction helpers for quantum density matrices., Construct the pure-state density matrix ``|psi><psi|``. (+15 more)

### Community 21 - "SeededRNG"
Cohesion: 0.17
Nodes (24): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Simulate a physical QRNG with bias and Markovian correlation., SeededRNG, parametrize, test_base_rng_cannot_be_instantiated() (+16 more)

### Community 22 - "validate_aligned_keys"
Cohesion: 0.21
Nodes (13): Sampled QBER estimation with mandatory removal of disclosed key positions., copy_binary_vector(), copy_indices(), ArrayLike, intp, NDArray, uint8, Internal validation helpers shared by QKD post-processing stages. (+5 more)

### Community 23 - "sift_keys"
Cohesion: 0.18
Nodes (14): Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., sift_keys(), SiftingResult, parametrize, test_empty_sifting_is_valid_but_efficiency_is_undefined() (+6 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.12
Nodes (4): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return full-key QBER as simulator-only information., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "BaseRNG"
Cohesion: 0.16
Nodes (10): BaseRNG, GlobalRNG, ABC, Injectable random-number sources for reproducible simulations., Return the underlying NumPy generator., Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., Common interface for random sources backed by a NumPy generator. (+2 more)

### Community 26 - "client.ts"
Cohesion: 0.25
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), App(), useCapabilities(), root, SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.21
Nodes (10): AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection, sections (+2 more)

### Community 29 - "encode_bb84_state"
Cohesion: 0.17
Nodes (12): BB84SessionStatus, encode_bb84_state(), ArrayLike, ComplexArray, integer, Terminal state of a complete BB84 session., Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The… (+4 more)

### Community 30 - "bb84.py"
Cohesion: 0.21
Nodes (11): Enum, Deterministic basis reconciliation for QKD raw keys., Basis, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., Reusable standard projective measurements for QKD protocols., Named pure states commonly used by QKD protocols., _copy_bb84_bases() (+3 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 33 - "_copy_binary_vector"
Cohesion: 0.22
Nodes (10): _basis_vector(), _copy_binary_vector(), _copy_indices(), ArrayLike, intp, NDArray, uint8, Validate and defensively copy a one-dimensional binary vector. (+2 more)

### Community 34 - ".run"
Cohesion: 0.24
Nodes (8): integer, ndarray, random_basis(), random_bit(), Generate one or more uniformly distributed classical bits., Generate generic binary choices for adaptation by the QKD layer., Generate raw bits with the configured bias and temporal correlation., Simulate preparation, transmission, measurement, sifting, and QBER data.

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 37 - "estimate_qber_from_sample"
Cohesion: 0.24
Nodes (10): estimate_qber_from_sample(), ArrayLike, Disclose a random sample without replacement and remove it from both keys.…, Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…, parametrize, test_parameter_estimation_explicit_sample_size_preserves_alignment(), test_parameter_estimation_is_reproducible_and_removes_disclosures(), test_parameter_estimation_rejects_invalid_fraction() (+2 more)

### Community 38 - "postprocessing/__init__.py"
Cohesion: 0.20
Nodes (5): Classical QKD post-processing algorithms and immutable transcripts., ParameterEstimationResult, Immutable transcript and remaining material from parameter estimation., PrivacyAmplificationResult, Immutable final keys and public Toeplitz seed metadata.

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.33
Nodes (8): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly(), test_privacy_amplification_rejects_invalid_target(), test_privacy_amplification_reproduces_public_seed_and_final_key()

### Community 41 - "PhaseFlipChannel"
Cohesion: 0.20
Nodes (8): PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix., Single-qubit channel that applies Pauli Z with probability ``p``., test_phase_flip_maps_plus_to_minus()

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "ReconciliationResult"
Cohesion: 0.29
Nodes (3): Return the conservative leakage: one bit per disclosed Alice parity., Immutable corrected key and conservative public parity transcript size., ReconciliationResult

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 46 - "Graphify Knowledge Graph Integration Rules"
Cohesion: 0.40
Nodes (5): Graphify Knowledge Graph Integration Rules, Antigravity AGENTS Project Rules, Graphify Knowledge Graph Guidelines, Graphify Agent Rule, Graphify Workflow

### Community 47 - "Q: How should the BB84 core integrate with QuantumSec architecture?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How should the BB84 core integrate with QuantumSec architecture?, Source Nodes

### Community 48 - "Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron, Source Nodes

### Community 49 - "Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??, Source Nodes

### Community 50 - "test_ideal.py"
Cohesion: 0.25
Nodes (7): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array., parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing(), test_identity_rejects_nonphysical_density_matrices_by_default()

### Community 52 - "AmplitudeDampingChannel"
Cohesion: 0.29
Nodes (6): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., test_amplitude_damping_extremes_and_fixed_ground_state()

### Community 53 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.25
Nodes (8): CPTP Noise vs Optical Loss Architectural Separation, Detailed Module Responsibilities Blueprint, QuantumSec Project Structure and Architectural Blueprint, Query: BB84 Core Integration Architecture, QKD Channels and Protocols Specification, QKD Layer Architecture Memory, Quantum Mathematics Layer Memory, Quantum Math Modules Specification

### Community 71 - "Core Layer Infrastructure Memory"
Cohesion: 0.29
Nodes (7): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Injected RNG Convention, Core Constants Centralization, Core Layer Infrastructure Memory, Core RNG Abstractions

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Overview & README"
Cohesion: 0.33
Nodes (5): BB84 Classical Post-Processing Pipeline Spec, Query: Initial Bitstring Length & BB84 Signals, BB84 Session Simulation Flow, QuantumSec Project Overview & README, PQC Authentication in QKD Research Goal

### Community 75 - "QuantumSec Development Task Roadmap"
Cohesion: 0.33
Nodes (6): ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, MeasurementResult Dataclass Hardening, Task 1 Report: MeasurementResult Improvement

### Community 79 - "QuantumSec Conventions Memory"
Cohesion: 0.40
Nodes (5): Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Validation Policy and Error Types, QuantumSec Project Scope & Invariants

## Knowledge Gaps
- **140 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+135 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 428 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `test_bb84.py`, `verify_reconciled_keys`, `adapters.py`, `estimate_qber_from_sample`, `amplify_privacy`, `test_measures.py`, `reconcile_cascade`, `toeplitz_hash`, `.gen`, `BaseRNG`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `QuantumChannel` connect `QuantumChannel` to `test_bb84.py`, `adapters.py`, `_prepare_density_matrix`, `PhaseFlipChannel`, `KrausChannel`, `test_noise.py`, `AmplitudeDampingChannel`, `dm_from_ket`, `bb84.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `BB84Result` connect `BB84Result` to `test_bb84.py`, `.run`, `sift_keys`, `encode_bb84_state`, `bb84.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseRNG` (e.g. with `estimate_qber_from_sample()` and `amplify_privacy()`) actually correct?**
  _`BaseRNG` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `quantumsec`, `name`, `private` to the rest of the system?**
  _140 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_bb84.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1349206349206349 - nodes in this community are weakly interconnected._