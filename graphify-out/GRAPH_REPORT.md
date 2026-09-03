# Graph Report - QuantumSec  (2026-09-03)

## Corpus Check
- 186 files · ~48,376 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1567 nodes · 3150 edges · 107 communities (76 shown, 28 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 132 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `391d9b09`
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
- BB84Result
- reconcile_cascade
- BaseRNG
- api.ts
- KrausChannel
- test_noise.py
- BitFlipChannel
- test_rng.py
- copy_binary_vector
- BackendOperationError
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- TrustedIdentityStore
- SeededRNG
- SimulationConfigurator.tsx
- verify_reconciled_keys
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- _prepare_density_matrix
- measures.py
- estimate_qber_from_sample
- SimulatorPage.tsx
- amplify_privacy
- .apply
- ChannelPipeline.tsx
- PQCParty
- QuantumSec Web UI V1
- initiator.py
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- PublicIdentity
- ResizeObserverMock
- test_party.py
- protocol/__init__.py
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
- .from_dict
- oqs_kem_backend.py
- primitives/states.py
- _OQSSignature
- sift_keys
- test_providers.py
- constants.py
- backends/__init__.py
- .encapsulate
- benchmark_measurements.py
- _ChoiceGenerator
- operations.py
- _OQSKEM
- .__post_init__
- OQSSignatureBackend
- .generate
- dm_from_ket
- identity.py
- .apply
- .metadata
- .public_key
- .sign
- .verify
- .metadata
- _RegisteredSignature

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 55 edges
3. `dm_from_ket()` - 34 edges
4. `BaseRNG` - 30 edges
5. `SignedServerKeyOffer` - 29 edges
6. `PublicIdentity` - 27 edges
7. `QuantumChannel` - 25 edges
8. `IdentityChannel` - 25 edges
9. `StrictModel` - 25 edges
10. `ServerKeyOfferProcessor` - 24 edges

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

## Communities (107 total, 28 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

### Community 1 - "adapters.py"
Cohesion: 0.06
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
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 8 - "bb84.py"
Cohesion: 0.10
Nodes (28): Enum, Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols. (+20 more)

### Community 9 - "information.py"
Cohesion: 0.26
Nodes (15): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+7 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "test_measures.py"
Cohesion: 0.12
Nodes (24): Any, measure_projective(), ProjectiveMeasurement, ArrayLike, Sample a projective outcome without constructing a collapsed state. Parameters…, Sample a projective outcome and apply the Lueders state update. Parameters…, A complete projective measurement validated once at construction time., Return the Hilbert-space dimension measured by the projectors. (+16 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.12
Nodes (19): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+11 more)

### Community 14 - "BB84Result"
Cohesion: 0.09
Nodes (14): BB84PostprocessingConfig, BB84Result, BB84SessionStatus, StrEnum, Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return simulator-diagnostic QBER over the complete sifted key. This value is… (+6 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (28): Classical QKD post-processing algorithms and immutable transcripts., CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+20 more)

### Community 16 - "BaseRNG"
Cohesion: 0.09
Nodes (32): BaseRNG, GlobalRNG, ABC, random_basis(), Injectable random-number sources for reproducible simulations., Generate generic binary choices for adaptation by the QKD layer., Return the underlying NumPy generator., Process-wide generator initialized from operating-system entropy. (+24 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 19 - "test_noise.py"
Cohesion: 0.11
Nodes (25): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., DepolarizingChannel, ArrayLike, ComplexArray (+17 more)

### Community 20 - "BitFlipChannel"
Cohesion: 0.30
Nodes (11): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels(), test_pipeline_copies_channel_collection_and_does_not_mutate_input() (+3 more)

### Community 21 - "test_rng.py"
Cohesion: 0.08
Nodes (34): integer, ndarray, QRNGSimulator, random_bit(), random_unitary(), Generate binary choices using this simulator's bias/correlation model., Generate one or more uniformly distributed classical bits., Generate a Haar-distributed random unitary using QR decomposition. (+26 more)

### Community 22 - "copy_binary_vector"
Cohesion: 0.13
Nodes (22): ArrayLike, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, Sampled QBER estimation with mandatory removal of disclosed key positions., Universal-hash key confirmation after information reconciliation., copy_binary_vector(), copy_indices() (+14 more)

### Community 23 - "BackendOperationError"
Cohesion: 0.05
Nodes (38): OQSKEMBackend, Extract and validate a required metadata field from the liboqs algorithm…, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Query and return validated metadata and buffer dimensions for a KEM algorithm…, Generate a fresh key pair for the specified KEM algorithm using liboqs., Decapsulate a ciphertext using the provided secret key via liboqs to recover…, _required_detail(), BackendOperationError (+30 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (11): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+3 more)

### Community 25 - "registry.py"
Cohesion: 0.24
Nodes (10): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., SignatureMetadata, SignatureProvider, Post-quantum digital-signature providers. (+2 more)

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
Cohesion: 0.09
Nodes (15): Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, Named PQC parties with signing and pre-provisioned verification trust., Return the explicit store of trusted peer identities configured for this party., Explicit pre-provisioned trust for public PQC identities., Thread-safe in-memory registry mapping peer names to pre-provisioned trusted…, Initialize an empty trusted identity store., Register a public identity as trusted, raising an error if already present… (+7 more)

### Community 30 - "SeededRNG"
Cohesion: 0.17
Nodes (24): Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., SeededRNG, IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel (+16 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 33 - "PQCProfile"
Cohesion: 0.09
Nodes (23): PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites., Immutable algorithm suite specification for a QuantumSec PQC profile., Retrieve the immutable algorithm suite definition for the specified QuantumSec… (+15 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.18
Nodes (20): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+12 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (11): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+3 more)

### Community 37 - "measures.py"
Cohesion: 0.18
Nodes (10): _born_probabilities(), MeasurementResult, MeasurementSample, ComplexArray, RealArray, General projective-measurement domain objects and operations., A sampled logical outcome and its normalized post-measurement state., A sampled projector index and logical outcome, without state collapse. (+2 more)

### Community 38 - "estimate_qber_from_sample"
Cohesion: 0.20
Nodes (12): estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Immutable transcript and remaining material from parameter estimation., Disclose a random sample without replacement and remove it from both keys.…, parametrize, test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error(), test_parameter_estimation_explicit_sample_size_preserves_alignment() (+4 more)

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.21
Nodes (10): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly() (+2 more)

### Community 41 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "PQCParty"
Cohesion: 0.10
Nodes (33): ProcessedServerOffer, Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., ServerKeyOfferProcessor, Immutable container wrapping a ServerKeyOffer and its responder signature., Serialize this signed public offer to a JSON-compatible mapping. (+25 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "initiator.py"
Cohesion: 0.08
Nodes (23): KEMMetadata, Immutable specification and buffer dimensions for a Key Encapsulation Mechanism., Validate that descriptive strings are non-empty and buffer sizes are positive…, hqc_3_metadata(), Retrieve and cache standardized HQC-3 (NIST Round 4) metadata validated against…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, Post-quantum key-encapsulation providers., ml_kem_768_metadata() (+15 more)

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
Cohesion: 0.06
Nodes (31): MLDSAIdentity, PublicIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+23 more)

### Community 52 - "test_party.py"
Cohesion: 0.17
Nodes (14): Raised when an operation requires an identity from a peer not found in the…, UnknownTrustedPeerError, Self, Create a new party instance initialized with a fresh ML-DSA-65 signing identity., alice(), bob(), fixture, Tests for parties and explicit pre-provisioned trust. (+6 more)

### Community 53 - "protocol/__init__.py"
Cohesion: 0.18
Nodes (9): Post-quantum identity and authentication primitives., Identity, trust, and party models for PQC authentication., EncapsulationResponse, InitiatorKEMState, StrEnum, Authentication outcome produced before any Alice-side response is sent., Alice-local KEM secrets created only after authenticating the responder., Unsigned public KEM ciphertext material prepared for the next phase. (+1 more)

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

### Community 82 - ".from_dict"
Cohesion: 0.21
Nodes (10): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Ensure all required transport keys exist in the provided payload dictionary., _require_transport_fields(), FixtureRequest (+2 more)

### Community 83 - "oqs_kem_backend.py"
Cohesion: 0.11
Nodes (28): Exception, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), Adapter isolating the liboqs-python signature API., Dynamically import and cache the liboqs Python module, raising…, Verify that the requested signature algorithm is enabled in the liboqs library., Initialize and return a new liboqs signature instance for the specified… (+20 more)

### Community 84 - "primitives/states.py"
Cohesion: 0.22
Nodes (9): _immutable(), ndarray, Named pure states commonly used by QKD protocols., parametrize, test_entropy_rejects_significant_negativity_without_full_validation(), test_fidelity_psd_square_root_rejects_significant_negativity(), test_pair_metrics_require_equal_shapes(), test_purity_analytical_cases() (+1 more)

### Community 85 - "_OQSSignature"
Cohesion: 0.12
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 86 - "sift_keys"
Cohesion: 0.14
Nodes (18): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match. (+10 more)

### Community 87 - "test_providers.py"
Cohesion: 0.17
Nodes (16): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., hqc(), ml_kem(), fixture, FixtureRequest (+8 more)

### Community 88 - "constants.py"
Cohesion: 0.31
Nodes (6): Project-wide numerical constants with no domain-layer dependencies., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 91 - ".encapsulate"
Cohesion: 0.50
Nodes (3): OQSKEMEncapsulation, Encapsulate a secret against the public key via liboqs, returning ciphertext…, Immutable container holding ciphertext and shared secret produced by liboqs…

### Community 92 - "benchmark_measurements.py"
Cohesion: 0.47
Nodes (5): _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark()

### Community 94 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 95 - "_OQSKEM"
Cohesion: 0.14
Nodes (8): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager., Protocol for the liboqs KeyEncapsulation constructor callable.

### Community 100 - "OQSSignatureBackend"
Cohesion: 0.14
Nodes (11): MonkeyPatch, OQSKeyPair, OQSSignatureBackend, Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend., Immutable container transferring generated key pairs across the liboqs adapter…, Low-level adapter managing liboqs signature contexts, key generation, signing,…, Generate a fresh key pair for the specified signature algorithm using liboqs. (+3 more)

### Community 103 - "dm_from_ket"
Cohesion: 0.17
Nodes (14): Reusable standard projective measurements for QKD protocols., dm_from_ensemble(), dm_from_ket(), ArrayLike, ComplexArray, Construction helpers for quantum density matrices., Construct the pure-state density matrix ``|psi><psi|``., Construct a density matrix from a finite ensemble of pure states. Parameters… (+6 more)

### Community 104 - "identity.py"
Cohesion: 0.25
Nodes (6): Private and public identities for PQC authentication., Verify a signature against the message using this public identity's algorithm…, _metadata_for_algorithm(), Look up algorithm metadata from the registry, or return None if unsupported., Verify a signature by dispatching to the registered provider for the specified…, verify_signature()

## Knowledge Gaps
- **140 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+135 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 637 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_server_offer.py`, `initiator.py`, `PublicIdentity`, `test_party.py`, `protocol/__init__.py`, `TrustedIdentityStore`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Basis` connect `bb84.py` to `adapters.py`, `dm_from_ket`, `BB84Result`, `sift_keys`, `SeededRNG`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `QuantumChannel` connect `QuantumChannel` to `adapters.py`, `_prepare_density_matrix`, `bb84.py`, `KrausChannel`, `test_noise.py`, `BitFlipChannel`, `SeededRNG`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PQCParty` (e.g. with `ServerKeyOfferProcessor` and `MLDSAIdentity`) actually correct?**
  _`PQCParty` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `BaseRNG` (e.g. with `estimate_qber_from_sample()` and `amplify_privacy()`) actually correct?**
  _`BaseRNG` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ServerKeyOfferProcessor` and `ServerKeyOfferFactory`) actually correct?**
  _`SignedServerKeyOffer` has 2 INFERRED edges - model-reasoned connections that need verification._