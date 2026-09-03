# Graph Report - QuantumSec  (2026-09-02)

## Corpus Check
- 184 files · ~45,855 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1470 nodes · 2921 edges · 103 communities (79 shown, 20 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 123 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4c339b05`
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
- as_ket
- bb84.py
- information.py
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- .run_session
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- copy_binary_vector
- KEMMetadata
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- TrustedIdentityStore
- test_bb84.py
- SimulationConfigurator.tsx
- postprocessing/__init__.py
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- .apply
- BaseRNG
- estimate_qber_from_sample
- SimulatorPage.tsx
- amplify_privacy
- PauliChannel
- ChannelPipeline.tsx
- ReconciliationResult
- QuantumSec Web UI V1
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- PublicIdentity
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
- .verify
- .generate
- messages.py
- PQCParty
- oqs_kem_backend.py
- oqs_backend.py
- sift_keys
- test_providers.py
- OQSKEMProvider
- backends/__init__.py
- test_states.py
- BackendOperationError
- benchmark_measurements.py
- _ChoiceGenerator
- operations.py
- _OQSKEM
- ResponderKEMState
- encode_bb84_state
- identity.py
- qber
- OQSSignatureBackend
- .apply
- .generate

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

## Communities (103 total, 20 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.16
Nodes (15): MLDSA65, Self, Private ML-DSA-65 signing capability backed by liboqs., Generate a real ML-DSA-65 key pair using liboqs CSPRNG state., Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures., signer() (+7 more)

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
Cohesion: 0.22
Nodes (13): QKD metric computations., asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits under the simulator's asymptotic BB84 model. The… (+5 more)

### Community 7 - "as_ket"
Cohesion: 0.12
Nodes (30): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+22 more)

### Community 8 - "bb84.py"
Cohesion: 0.11
Nodes (23): Enum, Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols. (+15 more)

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
Cohesion: 0.08
Nodes (35): Any, Project-wide numerical constants with no domain-layer dependencies., _born_probabilities(), measure_projective(), MeasurementResult, MeasurementSample, ProjectiveMeasurement, ArrayLike (+27 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.14
Nodes (18): _prepare_density_matrix(), ABC, ArrayLike, ComplexArray, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Apply the channel to a density matrix. (+10 more)

### Community 14 - ".run_session"
Cohesion: 0.20
Nodes (7): BB84PostprocessingConfig, BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., Configuration for BB84's authenticated classical post-processing. The default…, Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…, QKD protocol implementations.

### Community 15 - "reconcile_cascade"
Cohesion: 0.12
Nodes (24): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+16 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.18
Nodes (17): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Return the public seed length for an ``output_length x input_length`` matrix., Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash() (+9 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.11
Nodes (17): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+9 more)

### Community 19 - "test_noise.py"
Cohesion: 0.19
Nodes (18): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result() (+10 more)

### Community 20 - "dm_from_ket"
Cohesion: 0.24
Nodes (14): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, dm_from_ket(), Construct the pure-state density matrix ``|psi><psi|``., test_bit_flip_channel_extremes(), test_empty_pipeline_is_an_identity_without_aliasing_input() (+6 more)

### Community 21 - "SeededRNG"
Cohesion: 0.13
Nodes (29): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+21 more)

### Community 22 - "copy_binary_vector"
Cohesion: 0.14
Nodes (18): Quantum bit error rate for aligned QKD key material., Sampled QBER estimation with mandatory removal of disclosed key positions., Toeplitz-universal privacy amplification for reconciled QKD keys., Efficient binary Toeplitz universal hashing for QKD post-processing., Universal-hash key confirmation after information reconciliation., copy_binary_vector(), copy_indices(), ArrayLike (+10 more)

### Community 23 - "KEMMetadata"
Cohesion: 0.09
Nodes (22): KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Non-secret description and sizes of a key-encapsulation mechanism., Decapsulate using this provider's private key., Primitive KEM output; its shared secret is never shown in representations. (+14 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (17): BB84Result, BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation. (+9 more)

### Community 25 - "registry.py"
Cohesion: 0.14
Nodes (13): ABC, Backend-independent signature contracts and metadata., Minimal backend-independent signing capability used by QuantumSec., Return the immutable public verification key., Sign a byte string with this provider's private identity., Verify a signature against an explicitly supplied public key., SignatureProvider, Post-quantum digital-signature providers. (+5 more)

### Community 26 - "client.ts"
Cohesion: 0.25
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), App(), useCapabilities(), root, SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.21
Nodes (10): AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection, sections (+2 more)

### Community 29 - "TrustedIdentityStore"
Cohesion: 0.12
Nodes (7): Identity, trust, and party models for PQC authentication., Named PQC parties with signing and pre-provisioned verification trust., Return this party's explicit trust store., Map peer names to public identities trusted out of band., Explicitly provision a peer, rejecting silent key replacement., Return trusted owner names in deterministic order., TrustedIdentityStore

### Community 30 - "test_bb84.py"
Cohesion: 0.15
Nodes (24): IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel, ArrayLike, ComplexArray, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness() (+16 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "postprocessing/__init__.py"
Cohesion: 0.14
Nodes (12): Classical QKD post-processing algorithms and immutable transcripts., PrivacyAmplificationResult, Immutable final keys and public Toeplitz seed metadata., ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult (+4 more)

### Community 33 - "PQCProfile"
Cohesion: 0.14
Nodes (18): Post-quantum identity and authentication primitives., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., QuantumSec profiles; these are not NIST security categories., Immutable algorithm selection for one QuantumSec profile. (+10 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.18
Nodes (20): OfferCreation, Create fresh KEM state, canonical offers, and responder signatures., ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+12 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply each component from first to last without mutating the input.

### Community 37 - "BaseRNG"
Cohesion: 0.10
Nodes (20): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+12 more)

### Community 38 - "estimate_qber_from_sample"
Cohesion: 0.20
Nodes (12): estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Immutable transcript and remaining material from parameter estimation., Disclose a random sample without replacement and remove it from both keys.…, parametrize, test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error(), test_parameter_estimation_explicit_sample_size_preserves_alignment() (+4 more)

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.33
Nodes (8): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly(), test_privacy_amplification_rejects_invalid_target(), test_privacy_amplification_reproduces_public_seed_and_final_key()

### Community 41 - "PauliChannel"
Cohesion: 0.14
Nodes (11): PauliChannel, PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., Apply Pauli noise to a single-qubit density matrix. (+3 more)

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

### Community 50 - "PublicIdentity"
Cohesion: 0.07
Nodes (28): MLDSAIdentity, PublicIdentity, Self, Generate a named ML-DSA-65 identity using secure backend randomness., Return public ML-DSA-65 metadata., Export the non-secret form suitable for trust provisioning., Sign a message with this identity's private capability., Verify against an explicitly selected public identity. (+20 more)

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

### Community 80 - ".verify"
Cohesion: 0.33
Nodes (3): Sign a message using the private ML-DSA-65 key., Return whether a signature is valid for a message and public key., _require_bytes()

### Community 82 - "messages.py"
Cohesion: 0.12
Nodes (15): _decode_base64_field(), _length_prefixed(), Self, Immutable public messages for the staged PQC handshake., Serialize authenticated fields in one deterministic, unambiguous order., Restore and validate an offer from its JSON-compatible mapping., A server key offer plus its long-lived responder identity signature., Serialize this signed public offer to a JSON-compatible mapping. (+7 more)

### Community 83 - "PQCParty"
Cohesion: 0.12
Nodes (19): PQCParty, Self, Mutable trust-bearing party with an immutable private ML-DSA identity., Create a party with a new real ML-DSA-65 identity., Return the immutable owner name of this party's private identity., Sign data using this party's private identity., Verify data using only the peer key already present in the trust store., alice() (+11 more)

### Community 84 - "oqs_kem_backend.py"
Cohesion: 0.16
Nodes (18): Exception, _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), _OQSModule, Adapter isolating the liboqs-python key-encapsulation API., BackendUnavailableError, PQCError (+10 more)

### Community 85 - "oqs_backend.py"
Cohesion: 0.12
Nodes (13): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, _OQSSignature, BaseException, Protocol (+5 more)

### Community 86 - "sift_keys"
Cohesion: 0.14
Nodes (18): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match. (+10 more)

### Community 87 - "test_providers.py"
Cohesion: 0.16
Nodes (17): HQC3, Private ephemeral HQC-3 capability backed by liboqs., MLKEM768, Private ephemeral ML-KEM-768 capability backed by liboqs., hqc(), ml_kem(), fixture, FixtureRequest (+9 more)

### Community 88 - "OQSKEMProvider"
Cohesion: 0.14
Nodes (10): OQSKEMProvider, Self, Private base for KEMs sharing the same liboqs lifecycle., Return cached metadata for the concrete OQS mechanism., Generate an ephemeral key pair through liboqs., Return cached backend-derived metadata., Return the immutable public encapsulation key., Encapsulate to a public key through liboqs. (+2 more)

### Community 90 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 91 - "BackendOperationError"
Cohesion: 0.18
Nodes (11): OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, Execute KEM operations through liboqs without leaking its lifecycle., Private transfer object used only across the OQS KEM boundary., Ciphertext and shared secret returned by the OQS adapter., Validated non-secret metadata reported by liboqs. (+3 more)

### Community 92 - "benchmark_measurements.py"
Cohesion: 0.47
Nodes (5): _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark()

### Community 94 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 95 - "_OQSKEM"
Cohesion: 0.17
Nodes (6): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType

### Community 96 - "ResponderKEMState"
Cohesion: 0.17
Nodes (6): Private ephemeral KEM capabilities retained by one responder session. Protocol-…, Return the public ML-KEM key for the associated offer., Return the public HQC key when the HIGH profile is active., Return whether the private KEM references have been released., Release references to ephemeral private capabilities, idempotently. Python…, ResponderKEMState

### Community 97 - "encode_bb84_state"
Cohesion: 0.20
Nodes (12): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+4 more)

### Community 98 - "identity.py"
Cohesion: 0.22
Nodes (6): Private and public identities for PQC authentication., Non-secret description of a digital-signature algorithm., Return public algorithm metadata., SignatureMetadata, Return standardized ML-DSA-65 metadata., _metadata_for_algorithm()

### Community 99 - "qber"
Cohesion: 0.33
Nodes (8): ArrayLike, qber(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, parametrize, test_qber_is_explicitly_undefined_for_empty_keys(), test_qber_matches_analytical_bit_error_fraction(), test_qber_rejects_non_binary_or_non_vector_inputs(), test_qber_rejects_unequal_key_lengths()

### Community 100 - "OQSSignatureBackend"
Cohesion: 0.25
Nodes (6): MonkeyPatch, OQSSignatureBackend, Execute signature operations through liboqs without leaking its lifecycle., test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 101 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

## Knowledge Gaps
- **141 isolated node(s):** `_RegisteredSignature`, `quantumsec`, `name`, `private`, `version` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 588 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `postprocessing/__init__.py`, `adapters.py`, `BaseRNG`, `estimate_qber_from_sample`, `amplify_privacy`, `test_measures.py`, `reconcile_cascade`, `toeplitz_hash`, `benchmark_measurements.py`, `test_bb84.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `Basis` connect `bb84.py` to `encode_bb84_state`, `adapters.py`, `sift_keys`, `BB84SessionResult`, `test_bb84.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `QuantumChannel` connect `QuantumChannel` to `adapters.py`, `bb84.py`, `PauliChannel`, `KrausChannel`, `test_noise.py`, `dm_from_ket`, `test_bb84.py`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `PQCParty` (e.g. with `MLDSAIdentity` and `PublicIdentity`) actually correct?**
  _`PQCParty` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseRNG` (e.g. with `estimate_qber_from_sample()` and `amplify_privacy()`) actually correct?**
  _`BaseRNG` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `PublicIdentity` (e.g. with `PQCParty` and `TrustedIdentityStore`) actually correct?**
  _`PublicIdentity` has 2 INFERRED edges - model-reasoned connections that need verification._