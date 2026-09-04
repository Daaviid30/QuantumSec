# Graph Report - QuantumSec  (2026-09-04)

## Corpus Check
- 197 files · ~55,319 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1769 nodes · 3785 edges · 102 communities (76 shown, 23 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d089b444`
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
- as_ket
- pqc/__init__.py
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- test_bases_and_measurements.py
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- bb84.py
- OQSKEMProvider
- BB84SessionResult
- identity.py
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
- sift_keys
- estimate_qber_from_sample
- SimulatorPage.tsx
- amplify_privacy
- BitFlipChannel
- ChannelPipeline.tsx
- PQCParty
- QuantumSec Web UI V1
- _OQSKEM
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- ResponderKEMState
- Basis
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
- NDArray
- verify_reconciled_keys
- .apply
- BackendOperationError
- .encapsulate
- oqs_backend.py
- .__exit__
- test_providers.py
- ._active_ml_kem
- backends/__init__.py
- ._active_hqc
- .__enter__
- pqc/core.md
- .__exit__
- BaseRNG
- .__exit__
- test_key_schedule.py
- .generate
- .apply
- operations.py
- core.md
- .__enter__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 69 edges
3. `SignedServerKeyOffer` - 50 edges
4. `PQCProfile` - 46 edges
5. `ServerKeyOfferProcessor` - 35 edges
6. `dm_from_ket()` - 34 edges
7. `profile_definition()` - 31 edges
8. `BaseRNG` - 30 edges
9. `PublicIdentity` - 29 edges
10. `SignedClientKeyExchange` - 26 edges

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

## Communities (102 total, 23 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.09
Nodes (29): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, MLDSA65, Self, Return a safe string representation with public key length without leaking… (+21 more)

### Community 1 - "adapters.py"
Cohesion: 0.06
Nodes (61): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+53 more)

### Community 2 - "validation.py"
Cohesion: 0.06
Nodes (73): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+65 more)

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
Cohesion: 0.21
Nodes (23): _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation., test_bob_decapsulates_but_never_encapsulates(), test_client_canonical_serialization_authenticates_every_field() (+15 more)

### Community 8 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 9 - "pqc/__init__.py"
Cohesion: 0.07
Nodes (23): Post-quantum identity, authentication, KEM, and key-establishment primitives., ProcessedClientKeyExchange, Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., StrEnum, Authentication outcome produced before any Alice-side response is sent., ServerOfferProcessingStatus, DerivedSessionKeyState (+15 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "test_measures.py"
Cohesion: 0.06
Nodes (47): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., _born_probabilities() (+39 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.14
Nodes (18): _prepare_density_matrix(), ABC, ArrayLike, ComplexArray, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Apply the channel to a density matrix. (+10 more)

### Community 14 - "test_bases_and_measurements.py"
Cohesion: 0.20
Nodes (10): bases_from_bits(), basis_from_bit(), integer, ndarray, Map the QKD random-bit convention 0/1 to the Z/X basis., Map a one-dimensional sequence of random bits to QKD bases., parametrize, test_bases_from_bits_maps_vectors_and_rejects_non_vectors() (+2 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (28): Classical QKD post-processing algorithms and immutable transcripts., CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+20 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.18
Nodes (17): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Return the public seed length for an ``output_length x input_length`` matrix., Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash() (+9 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 19 - "test_noise.py"
Cohesion: 0.15
Nodes (21): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, assert_valid_qubit_density_matrix() (+13 more)

### Community 20 - "dm_from_ket"
Cohesion: 0.14
Nodes (20): ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, Reusable standard projective measurements for QKD protocols., _immutable(), ndarray, Named pure states commonly used by QKD protocols., dm_from_ensemble(), dm_from_ket() (+12 more)

### Community 21 - "SeededRNG"
Cohesion: 0.14
Nodes (28): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+20 more)

### Community 22 - "bb84.py"
Cohesion: 0.09
Nodes (30): QKD metric computations., ArrayLike, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, Sampled QBER estimation with mandatory removal of disclosed key positions., PrivacyAmplificationResult, Toeplitz-universal privacy amplification for reconciled QKD keys. (+22 more)

### Community 23 - "OQSKEMProvider"
Cohesion: 0.08
Nodes (23): KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Immutable specification and buffer dimensions for a Key Encapsulation Mechanism., Generate and encapsulate a fresh shared secret against the target public key., Decapsulate an incoming ciphertext using this provider instance's private key. (+15 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.12
Nodes (4): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return full-key QBER as simulator-only information., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "identity.py"
Cohesion: 0.07
Nodes (26): Private and public identities for PQC authentication., Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive… (+18 more)

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
Nodes (36): Exception, PQCError, Domain errors for post-quantum cryptographic operations., Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, Base exception class for all post-quantum cryptography domain errors in…, TrustedIdentityConflictError, UnknownTrustedPeerError (+28 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.06
Nodes (46): IdentityChannel, ArrayLike, ComplexArray, Channel that returns an independent copy of the input state., Return the same physical state without aliasing the input array., BB84PostprocessingConfig, BB84Protocol, BB84SessionStatus (+38 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - ".from_dict"
Cohesion: 0.18
Nodes (13): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Restore and validate a client exchange from a transport mapping., Ensure all required transport keys exist in the provided payload dictionary. (+5 more)

### Community 33 - "PQCProfile"
Cohesion: 0.07
Nodes (40): Enum, PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites., Immutable algorithm suite specification for a QuantumSec PQC profile. (+32 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.17
Nodes (21): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+13 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BB84Result"
Cohesion: 0.15
Nodes (7): BB84Result, Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return simulator-diagnostic QBER over the complete sifted key. This value is…, Simulate preparation, transmission, measurement, sifting, and QBER data., Immutable raw and sifted material produced by one complete BB84 run.

### Community 37 - "sift_keys"
Cohesion: 0.17
Nodes (15): ArrayLike, Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match., sift_keys(), SiftingResult, parametrize (+7 more)

### Community 38 - "estimate_qber_from_sample"
Cohesion: 0.20
Nodes (12): estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Immutable transcript and remaining material from parameter estimation., Disclose a random sample without replacement and remove it from both keys.…, parametrize, test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error(), test_parameter_estimation_explicit_sample_size_preserves_alignment() (+4 more)

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

### Community 43 - "PQCParty"
Cohesion: 0.07
Nodes (55): ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ProcessedServerOffer, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed. (+47 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "_OQSKEM"
Cohesion: 0.14
Nodes (8): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager., Protocol for the liboqs KeyEncapsulation constructor callable.

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
Nodes (20): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+12 more)

### Community 52 - "ResponderKEMState"
Cohesion: 0.08
Nodes (17): ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side authentication, binding, and decapsulation outcome., ClientKeyExchange, Immutable public KEM ciphertext message bound to Bob's exact signed offer. (+9 more)

### Community 53 - "Basis"
Cohesion: 0.21
Nodes (10): _basis_vector(), ndarray, Deterministic basis reconciliation for QKD raw keys., Validate a one-dimensional sequence of named QKD bases., Basis, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., QKD-specific states, operations, bases, and standard measurements. (+2 more)

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

### Community 80 - "NDArray"
Cohesion: 0.21
Nodes (7): intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation.

### Community 81 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 82 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply each component from first to last without mutating the input.

### Community 83 - "BackendOperationError"
Cohesion: 0.08
Nodes (29): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule (+21 more)

### Community 84 - ".encapsulate"
Cohesion: 0.22
Nodes (6): Validate that the input value is a byte string, raising a TypeError if it is…, Validate key lengths against algorithm metadata and store immutable defensive…, Return standardized algorithm metadata defining expected key and ciphertext…, Return the algorithm metadata associated with this provider instance., Generate and encapsulate a shared secret against a given public key using…, _require_bytes()

### Community 85 - "oqs_backend.py"
Cohesion: 0.07
Nodes (24): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, _OQSSignature, BaseException, Protocol (+16 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session key when leaving a managed lifetime., Release the session-key reference idempotently without claiming memory…

### Community 87 - "test_providers.py"
Cohesion: 0.13
Nodes (18): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, hqc(), ml_kem() (+10 more)

### Community 88 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

### Community 97 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 98 - "BaseRNG"
Cohesion: 0.10
Nodes (19): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+11 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 101 - "test_key_schedule.py"
Cohesion: 0.08
Nodes (49): _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), derive_hkdf_sha384() (+41 more)

### Community 105 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

## Knowledge Gaps
- **141 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 716 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_server_offer.py`, `test_key_schedule.py`, `test_client_exchange.py`, `pqc/__init__.py`, `MLDSAIdentity`, `ResponderKEMState`, `PublicIdentity`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `ResponderKEMState` connect `ResponderKEMState` to `PQCProfile`, `.__exit__`, `test_server_offer.py`, `test_key_schedule.py`, `test_client_exchange.py`, `PQCParty`, `._active_ml_kem`, `._active_hqc`, `.__enter__`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `Basis` connect `Basis` to `PQCProfile`, `adapters.py`, `BB84Result`, `sift_keys`, `test_bases_and_measurements.py`, `dm_from_ket`, `bb84.py`, `test_bb84.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 17 INFERRED edges - model-reasoned connections that need verification._