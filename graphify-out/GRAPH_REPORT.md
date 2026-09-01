# Graph Report - QuantumSec  (2026-09-01)

## Corpus Check
- 171 files · ~40,982 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1244 nodes · 2409 edges · 88 communities (66 shown, 18 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 94 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e0d0c71f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- adapters.py
- validation.py
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- qber
- as_ket
- Basis
- information.py
- compilerOptions
- ResultsWorkspace.tsx
- dm_from_ket
- QuantumChannel
- BB84Result
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- IdentityChannel
- SeededRNG
- validate_aligned_keys
- sift_keys
- BB84SessionResult
- SignatureProvider
- client.ts
- compilerOptions
- AppShell.tsx
- PublicIdentity
- bb84.py
- SimulationConfigurator.tsx
- verify_reconciled_keys
- _copy_binary_vector
- .run
- Adaptive Agents for QKD
- _prepare_density_matrix
- BaseRNG
- postprocessing/__init__.py
- SimulatorPage.tsx
- amplify_privacy
- BitFlipChannel
- ChannelPipeline.tsx
- ReconciliationResult
- QuantumSec Web UI V1
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- PQCParty
- ResizeObserverMock
- .apply
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
- _require_bytes
- .generate
- UnsupportedAlgorithmError
- oqs_backend.py
- _OQSSignature
- MLDSAIdentity
- identity.py
- backends/__init__.py

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 70 edges
2. `dm_from_ket()` - 37 edges
3. `BaseRNG` - 29 edges
4. `QuantumChannel` - 25 edges
5. `StrictModel` - 25 edges
6. `IdentityChannel` - 24 edges
7. `PQCParty` - 23 edges
8. `KrausChannel` - 23 edges
9. `BB84SessionResult` - 23 edges
10. `MLDSA65` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Knowledge Graph Integration Rules` --semantically_similar_to--> `Graphify Knowledge Graph Guidelines`  [INFERRED] [semantically similar]
  AGENTS.md → .agents/rules/graphify.md
- `RNG Architecture Design Principles` --semantically_similar_to--> `Injected RNG Convention`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → .serena/memories/conventions.md
- `BB84 Classical Post-Processing Pipeline Spec` --semantically_similar_to--> `BB84 Session Simulation Flow`  [INFERRED] [semantically similar]
  docs/structure.md → README.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `QuantumSec Project Scope & Invariants`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/core.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `Layered Dependency Discipline`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/conventions.md

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

## Communities (88 total, 18 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (15): MLDSA65, Self, Private ML-DSA-65 signing capability backed by liboqs., Generate a real ML-DSA-65 key pair using liboqs CSPRNG state., Return standardized ML-DSA-65 metadata., Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+7 more)

### Community 1 - "adapters.py"
Cohesion: 0.07
Nodes (61): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+53 more)

### Community 2 - "validation.py"
Cohesion: 0.09
Nodes (48): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+40 more)

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

### Community 8 - "Basis"
Cohesion: 0.16
Nodes (16): Enum, Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols. (+8 more)

### Community 9 - "information.py"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.05
Nodes (56): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., Reusable standard projective measurements for QKD protocols. (+48 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.16
Nodes (14): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+6 more)

### Community 14 - "BB84Result"
Cohesion: 0.11
Nodes (13): BB84Result, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+5 more)

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
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 19 - "test_noise.py"
Cohesion: 0.19
Nodes (18): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result() (+10 more)

### Community 20 - "IdentityChannel"
Cohesion: 0.18
Nodes (16): IdentityChannel, Channel that returns an independent copy of the input state., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, Construction helpers for quantum density matrices., parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing() (+8 more)

### Community 21 - "SeededRNG"
Cohesion: 0.06
Nodes (58): ndarray, QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source. (+50 more)

### Community 22 - "validate_aligned_keys"
Cohesion: 0.21
Nodes (13): Sampled QBER estimation with mandatory removal of disclosed key positions., copy_binary_vector(), copy_indices(), ArrayLike, intp, NDArray, uint8, Internal validation helpers shared by QKD post-processing stages. (+5 more)

### Community 23 - "sift_keys"
Cohesion: 0.18
Nodes (14): Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., sift_keys(), SiftingResult, parametrize, test_empty_sifting_is_valid_but_efficiency_is_undefined() (+6 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.12
Nodes (4): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return full-key QBER as simulator-only information., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "SignatureProvider"
Cohesion: 0.12
Nodes (13): Return public ML-DSA-65 metadata., ABC, Backend-independent signature contracts and metadata., Non-secret description of a digital-signature algorithm., Minimal backend-independent signing capability used by QuantumSec., Return public algorithm metadata., Return the immutable public verification key., Sign a byte string with this provider's private identity. (+5 more)

### Community 26 - "client.ts"
Cohesion: 0.25
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), App(), useCapabilities(), root, SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.21
Nodes (10): AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection, sections (+2 more)

### Community 29 - "PublicIdentity"
Cohesion: 0.15
Nodes (8): Post-quantum identity and authentication primitives., PublicIdentity, Immutable public verification identity with no signing material., Map peer names to public identities trusted out of band., Explicitly provision or replace a peer's trusted public identity., Return a pre-provisioned identity or raise an explicit trust error., Return trusted owner names in deterministic order., TrustedIdentityStore

### Community 30 - "bb84.py"
Cohesion: 0.13
Nodes (20): BB84SessionStatus, _copy_bb84_bases(), _copy_binary_vector(), encode_bb84_state(), ArrayLike, ComplexArray, integer, Reproducible prepare-and-measure simulation of the BB84 protocol. (+12 more)

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
Cohesion: 0.33
Nodes (6): integer, random_basis(), random_bit(), Generate one or more uniformly distributed classical bits., Generate generic binary choices for adaptation by the QKD layer., Simulate preparation, transmission, measurement, sifting, and QBER data.

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (11): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+3 more)

### Community 37 - "BaseRNG"
Cohesion: 0.16
Nodes (10): BaseRNG, GlobalRNG, ABC, Injectable random-number sources for reproducible simulations., Return the underlying NumPy generator., Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., Common interface for random sources backed by a NumPy generator. (+2 more)

### Community 38 - "postprocessing/__init__.py"
Cohesion: 0.20
Nodes (5): Classical QKD post-processing algorithms and immutable transcripts., ParameterEstimationResult, Immutable transcript and remaining material from parameter estimation., PrivacyAmplificationResult, Immutable final keys and public Toeplitz seed metadata.

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.33
Nodes (8): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly(), test_privacy_amplification_rejects_invalid_target(), test_privacy_amplification_reproduces_public_seed_and_final_key()

### Community 41 - "BitFlipChannel"
Cohesion: 0.12
Nodes (14): BitFlipChannel, PauliChannel, PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability. (+6 more)

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

### Community 50 - "PQCParty"
Cohesion: 0.13
Nodes (9): PQCParty, An ML-DSA identity plus its explicitly trusted peers., Return the non-secret identity that peers may provision as trusted., Return this party's explicit trust store., Explicitly provision a peer's public identity as trusted., Sign data using this party's private identity., Verify data using only the peer key already present in the trust store., test_party_representation_contains_no_key_material() (+1 more)

### Community 52 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

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

### Community 80 - "_require_bytes"
Cohesion: 0.33
Nodes (3): Sign a message using the private ML-DSA-65 key., Return whether a signature is valid for a message and public key., _require_bytes()

### Community 83 - "UnsupportedAlgorithmError"
Cohesion: 0.16
Nodes (17): Exception, PQCError, Domain errors for post-quantum cryptographic operations., Raised when the backend cannot provide a requested algorithm., Raised when a peer is absent from the pre-provisioned trust store., Base class for PQC domain errors., UnknownTrustedPeerError, UnsupportedAlgorithmError (+9 more)

### Community 84 - "oqs_backend.py"
Cohesion: 0.16
Nodes (15): _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, OQSSignatureBackend, Adapter isolating the liboqs-python signature API., Private transfer object used only across the OQS adapter boundary., Execute signature operations through liboqs without leaking its lifecycle. (+7 more)

### Community 85 - "_OQSSignature"
Cohesion: 0.20
Nodes (4): BaseException, _OQSSignature, Self, TracebackType

### Community 86 - "MLDSAIdentity"
Cohesion: 0.14
Nodes (12): MLDSAIdentity, Self, Named private identity with ML-DSA-65 signing capability., Generate a named ML-DSA-65 identity using secure backend randomness., Export the non-secret form suitable for trust provisioning., Sign a message with this identity's private capability., Verify against an explicitly selected public identity., alice_identity() (+4 more)

### Community 88 - "identity.py"
Cohesion: 0.24
Nodes (5): Private and public identities for PQC authentication., _validated_identity_name(), Identity, trust, and party models for PQC authentication., Named PQC parties with signing and pre-provisioned verification trust., Explicit pre-provisioned trust for public PQC identities.

## Knowledge Gaps
- **140 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+135 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 504 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `verify_reconciled_keys`, `adapters.py`, `BaseRNG`, `amplify_privacy`, `dm_from_ket`, `reconcile_cascade`, `toeplitz_hash`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `UnsupportedAlgorithmError` connect `UnsupportedAlgorithmError` to `MLDSA65`, `oqs_backend.py`, `MLDSAIdentity`, `identity.py`, `PublicIdentity`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `dm_from_ket()` connect `dm_from_ket` to `validation.py`, `as_ket`, `information.py`, `KrausChannel`, `test_noise.py`, `IdentityChannel`, `SeededRNG`, `bb84.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseRNG` (e.g. with `estimate_qber_from_sample()` and `amplify_privacy()`) actually correct?**
  _`BaseRNG` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `quantumsec`, `name`, `private` to the rest of the system?**
  _140 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `MLDSA65` be split into smaller, more focused modules?**
  _Cohesion score 0.14736842105263157 - nodes in this community are weakly interconnected._