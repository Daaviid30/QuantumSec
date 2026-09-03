# Graph Report - QuantumSec  (2026-09-03)

## Corpus Check
- 190 files · ~52,332 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1681 nodes · 3484 edges · 104 communities (74 shown, 27 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 149 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `297bb4b5`
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
- test_client_exchange.py
- constants.py
- information.py
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- Basis
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- bb84.py
- BackendOperationError
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- PublicIdentity
- test_bb84.py
- SimulationConfigurator.tsx
- .from_dict
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- BB84Result
- _require_bytes
- estimate_qber_from_sample
- SimulatorPage.tsx
- amplify_privacy
- PauliChannel
- ChannelPipeline.tsx
- PQCParty
- QuantumSec Web UI V1
- OQSSignatureBackend
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- protocol/__init__.py
- _metadata_for_algorithm
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
- verify_signature
- .generate
- _prepare_density_matrix
- oqs_kem_backend.py
- .public_key
- UnsupportedAlgorithmError
- .verify
- OQSKEMBackend
- .metadata
- backends/__init__.py
- ReconciliationResult
- .__repr__
- _RegisteredSignature
- pqc/core.md
- .__exit__
- BaseRNG
- .__exit__
- _length_prefixed
- .generate
- .apply
- .apply
- operations.py
- core.md
- .__enter__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 68 edges
3. `SignedServerKeyOffer` - 41 edges
4. `PQCProfile` - 34 edges
5. `dm_from_ket()` - 34 edges
6. `ServerKeyOfferProcessor` - 32 edges
7. `BaseRNG` - 30 edges
8. `PublicIdentity` - 29 edges
9. `profile_definition()` - 27 edges
10. `BackendOperationError` - 25 edges

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

## Communities (104 total, 27 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.18
Nodes (15): MLDSA65, Self, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures., signer() (+7 more)

### Community 1 - "adapters.py"
Cohesion: 0.06
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

### Community 6 - "asymptotic_bb84_secret_length"
Cohesion: 0.24
Nodes (12): asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits under the simulator's asymptotic BB84 model. The…, parametrize (+4 more)

### Community 7 - "test_client_exchange.py"
Cohesion: 0.17
Nodes (27): ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation. (+19 more)

### Community 8 - "constants.py"
Cohesion: 0.09
Nodes (35): Project-wide numerical constants with no domain-layer dependencies., _immutable(), ndarray, Named pure states commonly used by QKD protocols., as_ket(), inner_product(), normalize(), outer_product() (+27 more)

### Community 9 - "information.py"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "test_measures.py"
Cohesion: 0.07
Nodes (41): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), _born_probabilities(), measure_projective() (+33 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.18
Nodes (13): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+5 more)

### Community 14 - "Basis"
Cohesion: 0.09
Nodes (29): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Keep aligned raw bits whose named preparation and measurement bases match., sift_keys(), bases_from_bits(), Basis (+21 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.14
Nodes (21): CascadeConfig, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray, uint8 (+13 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.14
Nodes (21): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash(), ArrayLike (+13 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.18
Nodes (12): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, A completely positive trace-preserving map validated at construction., Return the Hilbert-space dimension acted on by the channel., parametrize, test_kraus_channel_applies_operator_sum_without_mutating_input(), test_kraus_channel_rejects_invalid_operator_sets() (+4 more)

### Community 19 - "test_noise.py"
Cohesion: 0.19
Nodes (18): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result() (+10 more)

### Community 20 - "dm_from_ket"
Cohesion: 0.16
Nodes (19): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, dm_from_ensemble(), dm_from_ket(), ArrayLike, ComplexArray (+11 more)

### Community 21 - "SeededRNG"
Cohesion: 0.14
Nodes (28): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+20 more)

### Community 22 - "bb84.py"
Cohesion: 0.06
Nodes (44): QKD metric computations., ArrayLike, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, Classical QKD post-processing algorithms and immutable transcripts., Sampled QBER estimation with mandatory removal of disclosed key positions., PrivacyAmplificationResult (+36 more)

### Community 23 - "BackendOperationError"
Cohesion: 0.07
Nodes (32): BackendOperationError, Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Immutable specification and buffer dimensions for a Key Encapsulation Mechanism. (+24 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (11): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+3 more)

### Community 25 - "registry.py"
Cohesion: 0.17
Nodes (12): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., Generate a digital signature over the provided message bytes using the private…, SignatureMetadata (+4 more)

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
Cohesion: 0.06
Nodes (32): Exception, PQCError, Domain errors for post-quantum cryptographic operations., Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, Base exception class for all post-quantum cryptography domain errors in…, TrustedIdentityConflictError, UnknownTrustedPeerError (+24 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.06
Nodes (46): IdentityChannel, ArrayLike, ComplexArray, Channel that returns an independent copy of the input state., Return the same physical state without aliasing the input array., BB84PostprocessingConfig, BB84Protocol, BB84SessionStatus (+38 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - ".from_dict"
Cohesion: 0.18
Nodes (13): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Restore and validate a client exchange from a transport mapping., Deserialize a signed client exchange without authenticating its signature. (+5 more)

### Community 33 - "PQCProfile"
Cohesion: 0.07
Nodes (40): Enum, hqc_3_metadata(), Retrieve and cache standardized HQC-3 (NIST Round 4) metadata validated against…, ml_kem_768_metadata(), Retrieve and cache standardized ML-KEM-768 (NIST FIPS 203) metadata validated…, PQCProfile, PQCProfileDefinition, profile_definition() (+32 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.18
Nodes (20): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages., test_bob_signs_canonical_offer_with_existing_identity() (+12 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BB84Result"
Cohesion: 0.15
Nodes (8): BB84Result, _copy_bb84_bases(), Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return simulator-diagnostic QBER over the complete sifted key. This value is…, Immutable raw and sifted material produced by one complete BB84 run., _validate_bb84_basis()

### Community 37 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

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

### Community 43 - "PQCParty"
Cohesion: 0.07
Nodes (54): Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., InitiatorKEMState, ProcessedServerOffer, Verify a trusted responder and encapsulate only after authentication., Alice-local KEM secrets created only after authenticating the responder. Raw-…, Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., Authenticate Bob's offer before producing Alice's KEM encapsulations. (+46 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "OQSSignatureBackend"
Cohesion: 0.33
Nodes (6): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

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
Cohesion: 0.09
Nodes (21): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+13 more)

### Community 52 - "protocol/__init__.py"
Cohesion: 0.05
Nodes (36): Post-quantum identity and authentication primitives., ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, ProcessedClientKeyExchange, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side authentication, binding, and decapsulation outcome. (+28 more)

### Community 53 - "_metadata_for_algorithm"
Cohesion: 0.50
Nodes (3): Validate owner, algorithm, and public key buffer dimensions, storing an…, _metadata_for_algorithm(), Look up algorithm metadata from the registry, or return None if unsupported.

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

### Community 80 - "verify_signature"
Cohesion: 0.50
Nodes (3): Verify a signature against the message using this public identity's algorithm…, Verify a signature by dispatching to the registered provider for the specified…, verify_signature()

### Community 82 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 83 - "oqs_kem_backend.py"
Cohesion: 0.06
Nodes (29): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _new_kem(), _OQSKEM, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair (+21 more)

### Community 85 - "UnsupportedAlgorithmError"
Cohesion: 0.07
Nodes (27): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, _OQSSignature, BaseException, Protocol (+19 more)

### Community 87 - "OQSKEMBackend"
Cohesion: 0.10
Nodes (23): OQSKEMBackend, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-… (+15 more)

### Community 90 - "ReconciliationResult"
Cohesion: 0.29
Nodes (3): Return the conservative leakage: one bit per disclosed Alice parity., Immutable corrected key and conservative public parity transcript size., ReconciliationResult

### Community 97 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 98 - "BaseRNG"
Cohesion: 0.10
Nodes (20): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+12 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 101 - "_length_prefixed"
Cohesion: 0.33
Nodes (4): _length_prefixed(), Serialize authenticated offer fields into a deterministic length-prefixed byte…, Prefix byte data with a 4-byte big-endian length header for canonical…, Serialize every authenticated field deterministically and unambiguously.

### Community 104 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 105 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

## Knowledge Gaps
- **141 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 685 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `Basis` to `PQCProfile`, `adapters.py`, `BB84Result`, `bb84.py`, `test_bb84.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `adapters.py`, `BaseRNG`, `estimate_qber_from_sample`, `amplify_privacy`, `test_measures.py`, `reconcile_cascade`, `toeplitz_hash`, `test_bb84.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_server_offer.py`, `test_client_exchange.py`, `MLDSAIdentity`, `protocol/__init__.py`, `PublicIdentity`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `PQCProfile` (e.g. with `ClientKeyExchangeProcessor` and `ProcessedClientKeyExchange`) actually correct?**
  _`PQCProfile` has 13 INFERRED edges - model-reasoned connections that need verification._