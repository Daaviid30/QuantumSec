# Graph Report - QuantumSec  (2026-09-04)

## Corpus Check
- 197 files · ~55,795 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1779 nodes · 3805 edges · 119 communities (84 shown, 32 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ef204e04`
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
- PQCHandshakeTranscript
- compilerOptions
- ResultsWorkspace.tsx
- dm_from_ket
- QuantumChannel
- test_bases_and_measurements.py
- reconcile_cascade
- toeplitz_hash
- api.ts
- KrausChannel
- test_noise.py
- BitFlipChannel
- SeededRNG
- estimate_qber_from_sample
- BackendOperationError
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- TrustedIdentityStore
- test_bb84.py
- SimulationConfigurator.tsx
- ml_kem_768_metadata
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- bb84.py
- sift_keys
- information.py
- SimulatorPage.tsx
- amplify_privacy
- .apply
- ChannelPipeline.tsx
- PQCParty
- QuantumSec Web UI V1
- pqc/__init__.py
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- SignedClientKeyExchange
- _validated_identity_name
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
- PublicIdentity
- verify_reconciled_keys
- _prepare_density_matrix
- oqs_kem_backend.py
- constants.py
- UnsupportedAlgorithmError
- .__exit__
- test_providers.py
- OQSKEMBackend
- backends/__init__.py
- encode_bb84_state
- .__enter__
- test_party.py
- pqc/core.md
- quantum/states.py
- _require_bytes
- OQSSignatureBackend
- .__exit__
- BaseRNG
- .__exit__
- identity.py
- test_key_schedule.py
- .generate
- _ChoiceGenerator
- verify_signature
- .apply
- operations.py
- .apply
- core.md
- .__enter__
- .generate
- .__enter__
- .metadata
- .__post_init__
- .public_key
- .sign
- .verify
- .metadata
- _RegisteredSignature

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

## Communities (119 total, 32 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

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
Cohesion: 0.22
Nodes (13): QKD metric computations., asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits under the simulator's asymptotic BB84 model. The… (+5 more)

### Community 7 - "test_client_exchange.py"
Cohesion: 0.10
Nodes (37): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Restore and validate a client exchange from a transport mapping., Ensure all required transport keys exist in the provided payload dictionary. (+29 more)

### Community 8 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 9 - "PQCHandshakeTranscript"
Cohesion: 0.17
Nodes (5): PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob., Serialize this public transcript to a JSON-compatible mapping.

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.07
Nodes (43): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Reusable standard projective measurements for QKD protocols., _born_probabilities() (+35 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.15
Nodes (16): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+8 more)

### Community 14 - "test_bases_and_measurements.py"
Cohesion: 0.20
Nodes (10): bases_from_bits(), basis_from_bit(), integer, ndarray, Map the QKD random-bit convention 0/1 to the Z/X basis., Map a one-dimensional sequence of random bits to QKD bases., parametrize, test_bases_from_bits_maps_vectors_and_rejects_non_vectors() (+2 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (27): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+19 more)

### Community 16 - "toeplitz_hash"
Cohesion: 0.21
Nodes (15): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash(), _dense_reference() (+7 more)

### Community 17 - "api.ts"
Cohesion: 0.12
Nodes (18): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, BasisCounts (+10 more)

### Community 18 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 19 - "test_noise.py"
Cohesion: 0.14
Nodes (21): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, PauliChannel, Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., assert_valid_qubit_density_matrix() (+13 more)

### Community 20 - "BitFlipChannel"
Cohesion: 0.24
Nodes (12): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_bit_flip_channel_extremes(), test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels() (+4 more)

### Community 21 - "SeededRNG"
Cohesion: 0.14
Nodes (28): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+20 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.09
Nodes (30): ArrayLike, qber(), Quantum bit error rate for aligned QKD key material., Return the differing-bit fraction for two aligned non-empty binary keys. An…, estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Sampled QBER estimation with mandatory removal of disclosed key positions. (+22 more)

### Community 23 - "BackendOperationError"
Cohesion: 0.06
Nodes (33): BackendOperationError, Domain errors for post-quantum cryptographic operations., Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata. (+25 more)

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

### Community 29 - "TrustedIdentityStore"
Cohesion: 0.12
Nodes (9): Return the explicit store of trusted peer identities configured for this party., Thread-safe in-memory registry mapping peer names to pre-provisioned trusted…, Initialize an empty trusted identity store., Return a sorted tuple of all trusted owner names registered in the store., Check whether an owner name is registered in the trusted identity store., Iterate over all trusted public identities in deterministic owner order., Return the total number of trusted peer identities in the store., Return a string representation listing registered trusted owner names. (+1 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.18
Nodes (20): IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel, ArrayLike, ComplexArray, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness() (+12 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "ml_kem_768_metadata"
Cohesion: 0.12
Nodes (21): _length_prefixed(), Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), Canonical KEM input construction and HKDF primitives for QuantumSec., hqc_3_metadata() (+13 more)

### Community 33 - "PQCProfile"
Cohesion: 0.09
Nodes (30): Internal canonical binary encoding primitives shared across PQC domains., Raised when an operation requires an identity from a peer not found in the…, UnknownTrustedPeerError, PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes. (+22 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.17
Nodes (21): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+13 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "bb84.py"
Cohesion: 0.05
Nodes (39): Enum, Classical QKD post-processing algorithms and immutable transcripts., PrivacyAmplificationResult, Toeplitz-universal privacy amplification for reconciled QKD keys., Immutable final keys and public Toeplitz seed metadata., Deterministic basis reconciliation for QKD raw keys., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation. (+31 more)

### Community 37 - "sift_keys"
Cohesion: 0.22
Nodes (14): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Keep aligned raw bits whose named preparation and measurement bases match., sift_keys(), parametrize, test_empty_sifting_is_valid_but_efficiency_is_undefined() (+6 more)

### Community 38 - "information.py"
Cohesion: 0.15
Nodes (24): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+16 more)

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "amplify_privacy"
Cohesion: 0.33
Nodes (8): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly(), test_privacy_amplification_rejects_invalid_target(), test_privacy_amplification_reproduces_public_seed_and_final_key()

### Community 41 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "PQCParty"
Cohesion: 0.08
Nodes (49): Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ProcessedServerOffer, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., ServerKeyOfferProcessor, Immutable container wrapping a ServerKeyOffer and its responder signature. (+41 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "pqc/__init__.py"
Cohesion: 0.09
Nodes (17): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeFactory, ClientKeyExchangeProcessingStatus, StrEnum, Package and sign Alice's already-created Phase 3 public encapsulation response., Bob-side authentication, binding, and decapsulation outcome., StrEnum, Authentication outcome produced before any Alice-side response is sent. (+9 more)

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
Cohesion: 0.13
Nodes (17): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Generate an ML-DSA-65 signature over message bytes using this identity's…, Return a safe string representation showing owner and algorithm without…, Deserialize and validate a public identity from a JSON-compatible dictionary…, Named private identity holding an ML-DSA-65 signing capability and associated…, alice_identity() (+9 more)

### Community 52 - "SignedClientKeyExchange"
Cohesion: 0.07
Nodes (20): ClientKeyExchangeProcessor, ProcessedClientKeyExchange, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., Immutable container wrapping Alice's client exchange and ML-DSA signature., Serialize this signed public client exchange to a JSON-compatible mapping. (+12 more)

### Community 53 - "_validated_identity_name"
Cohesion: 0.14
Nodes (7): Validate that the given identity name is a non-empty string and return its…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Validate the owner name and ensure the internal signer is an MLDSA65 instance., _validated_identity_name(), Validate wrapped offer type, signer name, signature algorithm, and signature…, Validate the wrapped exchange, signer identity, algorithm, and signature bytes., Return the trusted public identity for an owner, raising…

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

### Community 80 - "PublicIdentity"
Cohesion: 0.14
Nodes (9): PublicIdentity, Export the non-secret public identity suitable for peer trust stores., Verify a message signature against an explicitly provided public identity., Immutable public verification identity associating an owner name with public…, Serialize this public identity into a JSON-compatible dictionary with…, Return this party's public identity for distribution and registration in peer…, Add a peer's public identity to this party's trusted store with optional…, test_public_identity_validates_known_algorithm_key_length() (+1 more)

### Community 81 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, verify_reconciled_keys(), BB84PostprocessingConfig, Configuration for BB84's authenticated classical post-processing. The default…, Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…, test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 82 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (11): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+3 more)

### Community 83 - "oqs_kem_backend.py"
Cohesion: 0.07
Nodes (25): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _new_kem(), _OQSKEM, OQSKEMDetails, OQSKEMKeyPair, _OQSModule (+17 more)

### Community 84 - "constants.py"
Cohesion: 0.19
Nodes (9): Project-wide numerical constants with no domain-layer dependencies., _immutable(), ndarray, Named pure states commonly used by QKD protocols., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket() (+1 more)

### Community 85 - "UnsupportedAlgorithmError"
Cohesion: 0.07
Nodes (29): Exception, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, _OQSSignature, BaseException (+21 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session key when leaving a managed lifetime., Release the session-key reference idempotently without claiming memory…

### Community 87 - "test_providers.py"
Cohesion: 0.13
Nodes (18): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, hqc(), ml_kem() (+10 more)

### Community 88 - "OQSKEMBackend"
Cohesion: 0.17
Nodes (9): OQSKEMBackend, OQSKEMEncapsulation, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Encapsulate a secret against the public key via liboqs, returning ciphertext…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, Immutable container holding ciphertext and shared secret produced by liboqs…, Self, Generate a new ephemeral key pair via liboqs and return a ready-to-use provider… (+1 more)

### Community 90 - "encode_bb84_state"
Cohesion: 0.20
Nodes (12): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+4 more)

### Community 92 - "test_party.py"
Cohesion: 0.18
Nodes (9): Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, Register a public identity as trusted, raising an error if already present…, Tests for parties and explicit pre-provisioned trust., test_party_name_remains_bound_to_immutable_private_identity(), test_party_representation_contains_no_key_material(), test_trust_store_collection_protocol(), test_trust_store_is_not_coupled_to_ml_dsa() (+1 more)

### Community 94 - "quantum/states.py"
Cohesion: 0.24
Nodes (9): dm_from_ensemble(), ArrayLike, ComplexArray, Construction helpers for quantum density matrices., Construct a density matrix from a finite ensemble of pure states. Parameters…, parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing() (+1 more)

### Community 95 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

### Community 96 - "OQSSignatureBackend"
Cohesion: 0.33
Nodes (6): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 97 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 98 - "BaseRNG"
Cohesion: 0.10
Nodes (20): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+12 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 100 - "identity.py"
Cohesion: 0.40
Nodes (3): Private and public identities for PQC authentication., Named PQC parties with signing and pre-provisioned verification trust., Explicit pre-provisioned trust for public PQC identities.

### Community 101 - "test_key_schedule.py"
Cohesion: 0.07
Nodes (49): derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), Bob-local KEM secrets recovered after authenticating Alice's response. Raw-…, ResponderSharedSecretState, InitiatorKEMState (+41 more)

### Community 104 - "verify_signature"
Cohesion: 0.50
Nodes (3): Verify a signature against the message using this public identity's algorithm…, Verify a signature by dispatching to the registered provider for the specified…, verify_signature()

### Community 105 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 107 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

## Knowledge Gaps
- **141 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 718 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_server_offer.py`, `identity.py`, `test_key_schedule.py`, `test_client_exchange.py`, `pqc/__init__.py`, `PublicIdentity`, `MLDSAIdentity`, `SignedClientKeyExchange`, `test_party.py`, `TrustedIdentityStore`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `Basis` connect `bb84.py` to `adapters.py`, `sift_keys`, `dm_from_ket`, `test_bases_and_measurements.py`, `encode_bb84_state`, `test_bb84.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `ResponderKEMState` connect `SignedClientKeyExchange` to `PQCProfile`, `.__exit__`, `test_server_offer.py`, `test_key_schedule.py`, `test_client_exchange.py`, `PQCParty`, `.__enter__`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 17 INFERRED edges - model-reasoned connections that need verification._