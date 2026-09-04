# Graph Report - QuantumSec  (2026-09-04)

## Corpus Check
- 200 files · ~59,710 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1900 nodes · 4207 edges · 113 communities (87 shown, 23 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `847d9557`
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
- PQCHandshakeTranscript
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- test_bases_and_measurements.py
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- estimate_qber_from_sample
- KEMMetadata
- BB84SessionResult
- identity.py
- client.ts
- compilerOptions
- AppShell.tsx
- PublicIdentity
- test_bb84.py
- SimulationConfigurator.tsx
- ml_kem_768_metadata
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- postprocessing/__init__.py
- sift_keys
- information.py
- SimulatorPage.tsx
- amplify_privacy
- PauliChannel
- ChannelPipeline.tsx
- SignedServerKeyOffer
- QuantumSec Web UI V1
- PQCParty
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- protocol/__init__.py
- PQCConfirmationKeyState
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
- BB84Result
- verify_reconciled_keys
- _prepare_density_matrix
- _OQSKEM
- test_states.py
- _OQSSignature
- .__exit__
- test_providers.py
- BackendOperationError
- backends/__init__.py
- encode_bb84_state
- EstablishedPQCSession
- oqs_kem_backend.py
- pqc/core.md
- OQSKEMProvider
- .from_dict
- bb84.py
- .__exit__
- BaseRNG
- .__exit__
- derive_hkdf_sha384
- test_key_schedule.py
- .generate
- BB84PostprocessingConfig
- .generate_keypair
- .apply
- operations.py
- .apply
- core.md
- DerivedSessionKeyState
- .__repr__
- .__enter__
- .__post_init__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 70 edges
3. `PQCProfile` - 61 edges
4. `SignedServerKeyOffer` - 54 edges
5. `ServerKeyOfferProcessor` - 36 edges
6. `_create_flow()` - 36 edges
7. `dm_from_ket()` - 34 edges
8. `profile_definition()` - 31 edges
9. `BaseRNG` - 30 edges
10. `ProcessedServerOffer` - 30 edges

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

## Communities (113 total, 23 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.07
Nodes (30): MonkeyPatch, OQSSignatureBackend, Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend., Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking… (+22 more)

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
Cohesion: 0.19
Nodes (24): Deserialize a signed client exchange without authenticating its signature., _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation., test_bob_decapsulates_but_never_encapsulates() (+16 more)

### Community 8 - "constants.py"
Cohesion: 0.14
Nodes (27): Project-wide numerical constants with no domain-layer dependencies., as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray (+19 more)

### Community 9 - "PQCHandshakeTranscript"
Cohesion: 0.14
Nodes (7): Require a live Phase 5 key state bound to the exact Phase 6 transcript., _validated_session_key_state(), PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob., Serialize this public transcript to a JSON-compatible mapping.

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
Cohesion: 0.18
Nodes (13): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+5 more)

### Community 14 - "test_bases_and_measurements.py"
Cohesion: 0.20
Nodes (10): bases_from_bits(), basis_from_bit(), integer, ndarray, Map the QKD random-bit convention 0/1 to the Z/X basis., Map a one-dimensional sequence of random bits to QKD bases., parametrize, test_bases_from_bits_maps_vectors_and_rejects_non_vectors() (+2 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (27): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+19 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.11
Nodes (35): ConfirmedPQCHandshake, PQCKeyConfirmation, Capability produced only after both role-separated Finished MACs verify., Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., Verify Alice's chained Finished and produce mutual-confirmation proof., Materialize one role-local session only from the completed Finished exchange. (+27 more)

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
Cohesion: 0.16
Nodes (26): QRNGSimulator, Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG, parametrize, test_different_seeds_produce_different_streams() (+18 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.12
Nodes (20): ArrayLike, qber(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Immutable transcript and remaining material from parameter estimation., Disclose a random sample without replacement and remove it from both keys.… (+12 more)

### Community 23 - "KEMMetadata"
Cohesion: 0.12
Nodes (17): KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Immutable specification and buffer dimensions for a Key Encapsulation Mechanism., Generate and encapsulate a fresh shared secret against the target public key., Decapsulate an incoming ciphertext using this provider instance's private key. (+9 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.12
Nodes (4): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return full-key QBER as simulator-only information., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "identity.py"
Cohesion: 0.09
Nodes (23): Private and public identities for PQC authentication., ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations., Generate a fresh signing key pair using secure cryptographic backend randomness. (+15 more)

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
Nodes (24): PublicIdentity, Export the non-secret public identity suitable for peer trust stores., Verify a message signature against an explicitly provided public identity., Immutable public verification identity associating an owner name with public…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, Serialize this public identity into a JSON-compatible dictionary with…, Named PQC parties with signing and pre-provisioned verification trust. (+16 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.11
Nodes (30): IdentityChannel, ArrayLike, ComplexArray, Channel that returns an independent copy of the input state., Return the same physical state without aliasing the input array., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel (+22 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "ml_kem_768_metadata"
Cohesion: 0.10
Nodes (17): canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), hqc_3_metadata(), Retrieve and cache standardized HQC-3 (NIST Round 4) metadata validated against…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, ml_kem_768_metadata() (+9 more)

### Community 33 - "PQCProfile"
Cohesion: 0.09
Nodes (38): Enum, _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum (+30 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.21
Nodes (16): OfferCreation, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages., test_bob_signs_canonical_offer_with_existing_identity(), test_canonical_serialization_is_deterministic_and_domain_separated() (+8 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "postprocessing/__init__.py"
Cohesion: 0.08
Nodes (38): Quantum bit error rate for aligned QKD key material., Classical QKD post-processing algorithms and immutable transcripts., Sampled QBER estimation with mandatory removal of disclosed key positions., PrivacyAmplificationResult, Toeplitz-universal privacy amplification for reconciled QKD keys., Immutable final keys and public Toeplitz seed metadata., generate_toeplitz_seed(), ArrayLike (+30 more)

### Community 37 - "sift_keys"
Cohesion: 0.14
Nodes (18): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match. (+10 more)

### Community 38 - "information.py"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

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

### Community 43 - "SignedServerKeyOffer"
Cohesion: 0.10
Nodes (33): InitiatorKEMState, ProcessedServerOffer, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Alice-local KEM secrets created only after authenticating the responder. Raw-…, Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., ServerKeyOfferProcessor (+25 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "PQCParty"
Cohesion: 0.09
Nodes (31): ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., PQCParty, Self, Protocol participant holding a private signing identity and a trusted peer…, Validate that the party identity and trusted peer store instances are valid., Create a new party instance initialized with a fresh ML-DSA-65 signing identity. (+23 more)

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
Nodes (19): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Generate an ML-DSA-65 signature over message bytes using this identity's…, Return a safe string representation showing owner and algorithm without…, Deserialize and validate a public identity from a JSON-compatible dictionary…, Named private identity holding an ML-DSA-65 signing capability and associated… (+11 more)

### Community 52 - "protocol/__init__.py"
Cohesion: 0.04
Nodes (37): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side authentication, binding, and decapsulation outcome., Six-phase authenticated PQC handshake and confirmed session primitives. (+29 more)

### Community 53 - "PQCConfirmationKeyState"
Cohesion: 0.11
Nodes (18): _compute_finished_verify_data(), _confirmation_key_info(), _finished_mac_input(), PQCConfirmationKeyDeriver, PQCConfirmationKeyState, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released. (+10 more)

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

### Community 80 - "BB84Result"
Cohesion: 0.10
Nodes (14): BB84Result, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+6 more)

### Community 81 - "verify_reconciled_keys"
Cohesion: 0.18
Nodes (10): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…, test_different_keys_fail_for_deterministic_hash_setup() (+2 more)

### Community 82 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 83 - "_OQSKEM"
Cohesion: 0.12
Nodes (10): _KEMFactory, _OQSKEM, _OQSModule, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager. (+2 more)

### Community 84 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 85 - "_OQSSignature"
Cohesion: 0.12
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "test_providers.py"
Cohesion: 0.15
Nodes (17): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, hqc(), ml_kem(), fixture (+9 more)

### Community 88 - "BackendOperationError"
Cohesion: 0.12
Nodes (17): OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, Extract and validate a required metadata field from the liboqs algorithm…, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Query and return validated metadata and buffer dimensions for a KEM algorithm…, Generate a fresh key pair for the specified KEM algorithm using liboqs. (+9 more)

### Community 90 - "encode_bb84_state"
Cohesion: 0.25
Nodes (9): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+1 more)

### Community 91 - "EstablishedPQCSession"
Cohesion: 0.10
Nodes (13): EstablishedPQCSession, BaseException, Self, TracebackType, Enter a managed lifetime for this private confirmation-key state., Release the confirmation key when leaving its managed lifetime., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation. (+5 more)

### Community 92 - "oqs_kem_backend.py"
Cohesion: 0.10
Nodes (32): Exception, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), Adapter isolating the liboqs-python signature API., Dynamically import and cache the liboqs Python module, raising…, Verify that the requested signature algorithm is enabled in the liboqs library., Initialize and return a new liboqs signature instance for the specified… (+24 more)

### Community 94 - "OQSKEMProvider"
Cohesion: 0.12
Nodes (13): OQSKEMProvider, Self, Return a safe string representation with public key size without exposing…, Validate that the input value is a byte string, raising a TypeError if it is…, Base provider implementing KEM operations through the liboqs backend., Validate key lengths against algorithm metadata and store immutable defensive…, Return standardized algorithm metadata defining expected key and ciphertext…, Generate a new ephemeral key pair via liboqs and return a ready-to-use provider… (+5 more)

### Community 95 - ".from_dict"
Cohesion: 0.18
Nodes (13): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Ensure all required transport keys exist in the provided payload dictionary. (+5 more)

### Community 96 - "bb84.py"
Cohesion: 0.18
Nodes (12): Deterministic basis reconciliation for QKD raw keys., Basis, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., QKD-specific states, operations, bases, and standard measurements., Reusable standard projective measurements for QKD protocols., _immutable(), ndarray (+4 more)

### Community 97 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 98 - "BaseRNG"
Cohesion: 0.09
Nodes (22): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), random_unitary() (+14 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 100 - "derive_hkdf_sha384"
Cohesion: 0.27
Nodes (8): derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), Canonical KEM input construction and HKDF primitives for QuantumSec., test_hkdf_sha384_accepts_rfc5869_optional_or_empty_salt(), test_hkdf_sha384_is_deterministic_and_domain_separated()

### Community 101 - "test_key_schedule.py"
Cohesion: 0.10
Nodes (43): PQCSessionKeyDeriver, Derive the same key for either role using one shared transcript-bound schedule., Build explicit HKDF info for the Phase 5 session-key purpose., _session_key_info(), Self, Construct and validate a transcript from the two authenticated wire messages., Deserialize public messages without authenticating their signatures. Successful…, create_phase5_flow() (+35 more)

### Community 103 - "BB84PostprocessingConfig"
Cohesion: 0.25
Nodes (6): BB84PostprocessingConfig, BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., Configuration for BB84's authenticated classical post-processing. The default…, QKD protocol implementations.

### Community 104 - ".generate_keypair"
Cohesion: 0.50
Nodes (3): OQSKeyPair, Immutable container transferring generated key pairs across the liboqs adapter…, Generate a fresh key pair for the specified signature algorithm using liboqs.

### Community 105 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 107 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 109 - "DerivedSessionKeyState"
Cohesion: 0.10
Nodes (11): ProcessedClientKeyExchange, Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., DerivedSessionKeyState, Self, Explicitly export the live 256-bit key for a symmetric-key consumer. The…, Enter a managed lifetime for this private derived-key state., Derive Alice's key only from a successful authenticated Phase 3 result. (+3 more)

## Knowledge Gaps
- **141 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 764 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `bb84.py` to `PQCProfile`, `adapters.py`, `sift_keys`, `test_bases_and_measurements.py`, `BB84Result`, `encode_bb84_state`, `test_bb84.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `adapters.py`, `BaseRNG`, `postprocessing/__init__.py`, `amplify_privacy`, `test_measures.py`, `reconcile_cascade`, `verify_reconciled_keys`, `estimate_qber_from_sample`, `test_bb84.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_server_offer.py`, `test_key_schedule.py`, `test_client_exchange.py`, `SignedServerKeyOffer`, `MLDSAIdentity`, `protocol/__init__.py`, `oqs_kem_backend.py`, `PublicIdentity`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 8 INFERRED edges - model-reasoned connections that need verification._