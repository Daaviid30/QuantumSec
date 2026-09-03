# Graph Report - QuantumSec  (2026-09-03)

## Corpus Check
- 184 files · ~46,706 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1522 nodes · 2973 edges · 117 communities (82 shown, 31 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 123 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `49864d07`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- adapters.py
- validation.py
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- constants.py
- bb84.py
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
- BitFlipChannel
- SeededRNG
- copy_binary_vector
- BackendOperationError
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- PublicIdentity
- test_bb84.py
- SimulationConfigurator.tsx
- verify_reconciled_keys
- PQCProfile
- PQCParty
- Adaptive Agents for QKD
- _prepare_density_matrix
- BaseRNG
- estimate_qber_from_sample
- SimulatorPage.tsx
- amplify_privacy
- PhaseFlipChannel
- ChannelPipeline.tsx
- postprocessing/__init__.py
- QuantumSec Web UI V1
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
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
- ProjectiveMeasurement
- UnsupportedAlgorithmError
- PauliChannel
- _OQSSignature
- sift_keys
- test_providers.py
- GlobalRNG
- backends/__init__.py
- ParameterEstimationResult
- _new_kem
- benchmark_measurements.py
- _ChoiceGenerator
- operations.py
- _OQSKEM
- .run_session
- encode_bb84_state
- .__post_init__
- qber
- OQSSignatureBackend
- .apply
- .generate
- test_ideal.py
- verify_signature
- _parity
- dm_from_ensemble
- .apply
- .gen
- .gen
- .metadata
- .public_key
- .sign
- .verify
- .metadata
- _RegisteredSignature
- core.md

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 38 edges
3. `dm_from_ket()` - 34 edges
4. `BaseRNG` - 30 edges
5. `PublicIdentity` - 25 edges
6. `QuantumChannel` - 25 edges
7. `IdentityChannel` - 25 edges
8. `StrictModel` - 25 edges
9. `BackendOperationError` - 23 edges
10. `MLDSA65` - 23 edges

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

## Communities (117 total, 31 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

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

### Community 6 - "asymptotic_bb84_secret_length"
Cohesion: 0.24
Nodes (12): asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits under the simulator's asymptotic BB84 model. The…, parametrize (+4 more)

### Community 7 - "constants.py"
Cohesion: 0.11
Nodes (32): Project-wide numerical constants with no domain-layer dependencies., as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray (+24 more)

### Community 8 - "bb84.py"
Cohesion: 0.11
Nodes (23): Enum, bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases. (+15 more)

### Community 9 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.16
Nodes (23): Any, measure_projective(), MeasurementResult, ArrayLike, Sample a projective outcome without constructing a collapsed state. Parameters…, A sampled logical outcome and its normalized post-measurement state., Sample a projective outcome and apply the Lueders state update. Parameters…, sample_projective_outcome() (+15 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.18
Nodes (13): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+5 more)

### Community 14 - "BB84Result"
Cohesion: 0.12
Nodes (10): BB84Result, BB84SessionStatus, StrEnum, Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return simulator-diagnostic QBER over the complete sifted key. This value is…, Terminal state of a complete BB84 session. (+2 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.19
Nodes (17): CascadeConfig, _initial_block_size(), _PassLayout, ArrayLike, Configuration for the original-style Cascade block-size strategy. The first…, Correct Bob through disclosed block parities, binary searches, and look-back.…, reconcile_cascade(), parametrize (+9 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.16
Nodes (19): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Return the public seed length for an ``output_length x input_length`` matrix., Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash() (+11 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.16
Nodes (14): KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel., Evaluate ``sum_i K_i rho K_i^dagger``., parametrize (+6 more)

### Community 19 - "test_noise.py"
Cohesion: 0.19
Nodes (18): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result() (+10 more)

### Community 20 - "BitFlipChannel"
Cohesion: 0.22
Nodes (12): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_bit_flip_channel_extremes(), test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels() (+4 more)

### Community 21 - "SeededRNG"
Cohesion: 0.16
Nodes (27): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Simulate a physical QRNG with bias and Markovian correlation., SeededRNG, parametrize, test_base_rng_cannot_be_instantiated() (+19 more)

### Community 22 - "copy_binary_vector"
Cohesion: 0.16
Nodes (16): Quantum bit error rate for aligned QKD key material., Sampled QBER estimation with mandatory removal of disclosed key positions., Toeplitz-universal privacy amplification for reconciled QKD keys., Efficient binary Toeplitz universal hashing for QKD post-processing., Universal-hash key confirmation after information reconciliation., copy_binary_vector(), copy_indices(), ArrayLike (+8 more)

### Community 23 - "BackendOperationError"
Cohesion: 0.05
Nodes (50): OQSKEMBackend, OQSKEMDetails, Adapter isolating the liboqs-python key-encapsulation API., Extract and validate a required metadata field from the liboqs algorithm…, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Query and return validated metadata and buffer dimensions for a KEM algorithm…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, Immutable data structure storing algorithm parameters and buffer dimensions… (+42 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (11): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+3 more)

### Community 25 - "registry.py"
Cohesion: 0.21
Nodes (12): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., SignatureMetadata, SignatureProvider, Post-quantum digital-signature providers. (+4 more)

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
Cohesion: 0.05
Nodes (39): Post-quantum identity and authentication primitives., PublicIdentity, Private and public identities for PQC authentication., Validate that the given identity name is a non-empty string and return its…, Immutable public verification identity associating an owner name with public…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Serialize this public identity into a JSON-compatible dictionary with…, _validated_identity_name() (+31 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.19
Nodes (21): IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel, parametrize, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness(), test_bb84_encoding_convention_returns_expected_density_matrix() (+13 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 33 - "PQCProfile"
Cohesion: 0.06
Nodes (32): PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites., Immutable algorithm suite specification for a QuantumSec PQC profile., Retrieve the immutable algorithm suite definition for the specified QuantumSec… (+24 more)

### Community 34 - "PQCParty"
Cohesion: 0.09
Nodes (29): OfferCreation, PQCParty, Protocol participant holding a private signing identity and a trusted peer…, Validate that the party identity and trusted peer store instances are valid., Return the owner name of this party's private identity., Return this party's public identity for distribution and registration in peer…, Add a peer's public identity to this party's trusted store with optional…, Sign message bytes using this party's private ML-DSA signing identity. (+21 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "_prepare_density_matrix"
Cohesion: 0.22
Nodes (8): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Apply each component from first to last without mutating the input.

### Community 37 - "BaseRNG"
Cohesion: 0.12
Nodes (18): BaseRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations., Generate binary choices using this simulator's bias/correlation model. (+10 more)

### Community 38 - "estimate_qber_from_sample"
Cohesion: 0.31
Nodes (9): estimate_qber_from_sample(), ArrayLike, Disclose a random sample without replacement and remove it from both keys.…, parametrize, test_parameter_estimation_explicit_sample_size_preserves_alignment(), test_parameter_estimation_is_reproducible_and_removes_disclosures(), test_parameter_estimation_rejects_invalid_fraction(), test_parameter_estimation_rejects_sample_that_consumes_key() (+1 more)

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.21
Nodes (10): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly() (+2 more)

### Community 41 - "PhaseFlipChannel"
Cohesion: 0.20
Nodes (8): PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix., Single-qubit channel that applies Pauli Z with probability ``p``., test_phase_flip_maps_plus_to_minus()

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "postprocessing/__init__.py"
Cohesion: 0.16
Nodes (7): Classical QKD post-processing algorithms and immutable transcripts., CascadePassStatistics, Parity-based Cascade information reconciliation for aligned QKD keys., Return the conservative leakage: one bit per disclosed Alice parity., Immutable statistics and permutation for one Cascade pass., Immutable corrected key and conservative public parity transcript size., ReconciliationResult

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

### Community 50 - "MLDSAIdentity"
Cohesion: 0.10
Nodes (19): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without…, Deserialize and validate a public identity from a JSON-compatible dictionary… (+11 more)

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
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

### Community 82 - "ProjectiveMeasurement"
Cohesion: 0.15
Nodes (10): _born_probabilities(), ProjectiveMeasurement, ComplexArray, RealArray, A complete projective measurement validated once at construction time., Return the Hilbert-space dimension measured by the projectors., Return the number of projector/outcome pairs., Calculate and validate the Born probability vector. (+2 more)

### Community 83 - "UnsupportedAlgorithmError"
Cohesion: 0.07
Nodes (37): Exception, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, Adapter isolating the liboqs-python signature API., Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend. (+29 more)

### Community 84 - "PauliChannel"
Cohesion: 0.22
Nodes (5): Return a finite scalar probability in the closed unit interval., _validate_probability(), PauliChannel, Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability.

### Community 85 - "_OQSSignature"
Cohesion: 0.12
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 86 - "sift_keys"
Cohesion: 0.13
Nodes (19): _basis_vector(), ArrayLike, ndarray, Deterministic basis reconciliation for QKD raw keys., Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting. (+11 more)

### Community 87 - "test_providers.py"
Cohesion: 0.16
Nodes (17): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., hqc(), ml_kem(), fixture, FixtureRequest (+9 more)

### Community 88 - "GlobalRNG"
Cohesion: 0.33
Nodes (4): GlobalRNG, Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., test_global_rng_is_a_singleton()

### Community 90 - "ParameterEstimationResult"
Cohesion: 0.33
Nodes (3): ParameterEstimationResult, Immutable transcript and remaining material from parameter estimation., test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error()

### Community 91 - "_new_kem"
Cohesion: 0.15
Nodes (12): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMEncapsulation, OQSKEMKeyPair, Initialize and return a new liboqs KeyEncapsulation instance for the specified…, Generate a fresh key pair for the specified KEM algorithm using liboqs., Encapsulate a secret against the public key via liboqs, returning ciphertext… (+4 more)

### Community 92 - "benchmark_measurements.py"
Cohesion: 0.47
Nodes (5): _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark()

### Community 94 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 95 - "_OQSKEM"
Cohesion: 0.12
Nodes (10): _KEMFactory, _OQSKEM, _OQSModule, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager. (+2 more)

### Community 96 - ".run_session"
Cohesion: 0.40
Nodes (3): BB84PostprocessingConfig, Configuration for BB84's authenticated classical post-processing. The default…, Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…

### Community 97 - "encode_bb84_state"
Cohesion: 0.25
Nodes (9): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+1 more)

### Community 99 - "qber"
Cohesion: 0.25
Nodes (9): QKD metric computations., ArrayLike, qber(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, parametrize, test_qber_is_explicitly_undefined_for_empty_keys(), test_qber_matches_analytical_bit_error_fraction(), test_qber_rejects_non_binary_or_non_vector_inputs() (+1 more)

### Community 100 - "OQSSignatureBackend"
Cohesion: 0.33
Nodes (6): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 101 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 103 - "test_ideal.py"
Cohesion: 0.60
Nodes (4): parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing(), test_identity_rejects_nonphysical_density_matrices_by_default()

### Community 104 - "verify_signature"
Cohesion: 0.50
Nodes (3): Verify a signature against the message using this public identity's algorithm…, Verify a signature by dispatching to the registered provider for the specified…, verify_signature()

### Community 105 - "_parity"
Cohesion: 0.50
Nodes (4): _parity(), intp, NDArray, uint8

### Community 106 - "dm_from_ensemble"
Cohesion: 0.50
Nodes (4): dm_from_ensemble(), ArrayLike, ComplexArray, Construct a density matrix from a finite ensemble of pure states. Parameters…

## Knowledge Gaps
- **140 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+135 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 625 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `KrausChannel` connect `KrausChannel` to `test_noise.py`, `PauliChannel`, `QuantumChannel`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `QuantumChannel` connect `QuantumChannel` to `adapters.py`, `_prepare_density_matrix`, `bb84.py`, `PhaseFlipChannel`, `KrausChannel`, `test_noise.py`, `BitFlipChannel`, `PauliChannel`, `test_bb84.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `verify_reconciled_keys`, `adapters.py`, `BaseRNG`, `estimate_qber_from_sample`, `amplify_privacy`, `dm_from_ket`, `.gen`, `reconcile_cascade`, `toeplitz_hash`, `benchmark_measurements.py`, `test_bb84.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `PQCParty` (e.g. with `MLDSAIdentity` and `PublicIdentity`) actually correct?**
  _`PQCParty` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseRNG` (e.g. with `estimate_qber_from_sample()` and `amplify_privacy()`) actually correct?**
  _`BaseRNG` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PublicIdentity` (e.g. with `PQCParty` and `TrustedIdentityStore`) actually correct?**
  _`PublicIdentity` has 2 INFERRED edges - model-reasoned connections that need verification._