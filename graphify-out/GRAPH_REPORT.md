# Graph Report - QuantumSec  (2026-09-05)

## Corpus Check
- 209 files · ~73,604 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2025 nodes · 4359 edges · 122 communities (96 shown, 22 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 209 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bc410ec4`
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
- BB84Result
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- estimate_qber_from_sample
- BackendOperationError
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- PublicIdentity
- test_bb84.py
- SimulationConfigurator.tsx
- PQCConfirmationKeyState
- PQCProfile
- test_server_offer.py
- Adaptive Agents for QKD
- BaseRNG
- Basis
- information.py
- SimulatorPage.tsx
- toeplitz_hash
- PauliChannel
- ChannelPipeline.tsx
- PQCParty
- QuantumSec Web UI V1
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- ResponderKEMState
- 3. Análisis Detallado de Hallazgos
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
- test_full_six_phase_handshake_crosses_pure_json_transport
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- ProjectiveMeasurement & Sampling Refactor Spec
- ml_kem_768_metadata
- GlobalRNG
- verify_reconciled_keys
- ConfirmedPQCHandshake
- oqs_kem_backend.py
- test_states.py
- oqs_backend.py
- .__exit__
- PQCFinishedMessage
- derive_hkdf_sha384
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- pqc/__init__.py
- test_providers.py
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- .__exit__
- test_key_schedule.py
- create_phase5_flow
- .generate
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- bb84.py
- _prepare_density_matrix
- operations.py
- .__exit__
- ui/core.md
- protocol/__init__.py
- _OQSSignature
- amplify_privacy
- random_basis
- .__exit__
- .run
- .apply
- .__enter__
- .apply
- .apply
- primitives/states.py
- .__enter__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 77 edges
2. `PQCParty` - 71 edges
3. `PQCProfile` - 62 edges
4. `SignedServerKeyOffer` - 55 edges
5. `ServerKeyOfferProcessor` - 38 edges
6. `_create_flow()` - 36 edges
7. `dm_from_ket()` - 34 edges
8. `profile_definition()` - 31 edges
9. `SignedClientKeyExchange` - 31 edges
10. `BaseRNG` - 30 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Knowledge Graph Integration Rules` --semantically_similar_to--> `Graphify Knowledge Graph Guidelines`  [INFERRED] [semantically similar]
  AGENTS.md → .agents/rules/graphify.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `QuantumSec Project Scope & Invariants`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/core.md
- `RNG Architecture Design Principles` --semantically_similar_to--> `Injected RNG Convention`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → .serena/memories/conventions.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `Layered Dependency Discipline`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/conventions.md
- `BB84 Classical Post-Processing Pipeline Spec` --semantically_similar_to--> `BB84 Session Simulation Flow`  [INFERRED] [semantically similar]
  docs/structure.md → README.md

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

## Communities (122 total, 22 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.08
Nodes (28): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking…, Validate that the input value is a byte string, raising a TypeError if it is…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs. (+20 more)

### Community 1 - "adapters.py"
Cohesion: 0.06
Nodes (61): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+53 more)

### Community 2 - "validation.py"
Cohesion: 0.09
Nodes (48): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+40 more)

### Community 3 - "QuantumSec Serena Root Memory"
Cohesion: 0.12
Nodes (19): Detailed Module Responsibilities Blueprint, Query: BB84 Core Integration Architecture, Query: Serena Onboarding & Memory Creation, QuantumSec Serena Root Memory, Core Constants Centralization, Core Layer Infrastructure Memory, Serena Memory Progressive Discovery Model, Memory Maintenance Guidelines (+11 more)

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
Cohesion: 0.21
Nodes (23): _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation., test_bob_decapsulates_but_never_encapsulates(), test_client_canonical_serialization_authenticates_every_field() (+15 more)

### Community 8 - "constants.py"
Cohesion: 0.14
Nodes (27): Project-wide numerical constants with no domain-layer dependencies., as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray (+19 more)

### Community 9 - "PQCHandshakeTranscript"
Cohesion: 0.17
Nodes (5): PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob., Serialize this public transcript to a JSON-compatible mapping.

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

### Community 14 - "BB84Result"
Cohesion: 0.11
Nodes (13): BB84Result, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+5 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (28): Classical QKD post-processing algorithms and immutable transcripts., CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+20 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.19
Nodes (25): Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., _derive_confirmation_states(), _exchange_finished(), _flipped(), _Phase6States, parametrize, Tests for Phase 6 role-separated Finished key confirmation. (+17 more)

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
Cohesion: 0.15
Nodes (20): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, dm_from_ensemble(), dm_from_ket(), ArrayLike, ComplexArray (+12 more)

### Community 21 - "SeededRNG"
Cohesion: 0.14
Nodes (28): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+20 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.20
Nodes (12): estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, Immutable transcript and remaining material from parameter estimation., Disclose a random sample without replacement and remove it from both keys.…, parametrize, test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error(), test_parameter_estimation_explicit_sample_size_preserves_alignment() (+4 more)

### Community 23 - "BackendOperationError"
Cohesion: 0.05
Nodes (39): OQSKEMBackend, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Generate a fresh key pair for the specified KEM algorithm using liboqs., Encapsulate a secret against the public key via liboqs, returning ciphertext…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, BackendOperationError, Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation (+31 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.12
Nodes (4): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return full-key QBER as simulator-only information., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "registry.py"
Cohesion: 0.08
Nodes (24): Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations. (+16 more)

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
Nodes (34): Exception, PQCError, Domain errors for post-quantum cryptographic operations., Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, Base exception class for all post-quantum cryptography domain errors in…, TrustedIdentityConflictError, UnknownTrustedPeerError (+26 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.11
Nodes (30): IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig, BB84Protocol, Configuration for BB84's authenticated classical post-processing. The default…, Run BB84 with an injected random source and density-matrix channel. Alice's…, Run BB84 through estimation, Cascade, confirmation, and extraction. Legitimate…, _InvalidOutputChannel (+22 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "PQCConfirmationKeyState"
Cohesion: 0.10
Nodes (13): _compute_finished_verify_data(), _finished_mac_input(), PQCConfirmationKeyState, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released., Return whether this state has released its role-local confirmation key., Return whether this role completed its local send/verify Finished work. (+5 more)

### Community 33 - "PQCProfile"
Cohesion: 0.07
Nodes (39): _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., Unambiguous profile-aware encoding of independently established KEM secrets., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum (+31 more)

### Community 34 - "test_server_offer.py"
Cohesion: 0.17
Nodes (21): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+13 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BaseRNG"
Cohesion: 0.08
Nodes (34): BaseRNG, ABC, Injectable random-number sources for reproducible simulations., Return the underlying NumPy generator., Common interface for random sources backed by a NumPy generator., ArrayLike, qber(), Quantum bit error rate for aligned QKD key material. (+26 more)

### Community 37 - "Basis"
Cohesion: 0.13
Nodes (17): Enum, Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols. (+9 more)

### Community 38 - "information.py"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "toeplitz_hash"
Cohesion: 0.21
Nodes (15): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash(), _dense_reference() (+7 more)

### Community 41 - "PauliChannel"
Cohesion: 0.14
Nodes (11): PauliChannel, PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., Apply Pauli noise to a single-qubit density matrix. (+3 more)

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "PQCParty"
Cohesion: 0.09
Nodes (44): Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., ServerKeyOfferProcessor, Immutable container wrapping a ServerKeyOffer and its responder signature., Serialize this signed public offer to a JSON-compatible mapping., SignedServerKeyOffer, PQCParty, Self (+36 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "sift_keys"
Cohesion: 0.14
Nodes (18): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation., Return the fraction of raw positions retained after sifting., Keep aligned raw bits whose named preparation and measurement bases match. (+10 more)

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
Cohesion: 0.08
Nodes (24): Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's… (+16 more)

### Community 52 - "ResponderKEMState"
Cohesion: 0.09
Nodes (17): ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side authentication, binding, and decapsulation outcome., Return a safe string representation showing profile and closed status., Maintains ephemeral private KEM key pairs for an active handshake responder… (+9 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "test_full_six_phase_handshake_crosses_pure_json_transport"
Cohesion: 0.17
Nodes (15): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+7 more)

### Community 71 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.26
Nodes (10): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals, BB84 Session Simulation Flow (+2 more)

### Community 75 - "ProjectiveMeasurement & Sampling Refactor Spec"
Cohesion: 0.67
Nodes (3): ProjectiveMeasurement & Sampling Refactor Spec, MeasurementResult Dataclass Hardening, Task 1 Report: MeasurementResult Improvement

### Community 79 - "ml_kem_768_metadata"
Cohesion: 0.15
Nodes (13): canonical_kem_secret_input(), Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), hqc_3_metadata(), Retrieve HQC-3 metadata for the NIST Round 4 selection exposed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for…, ml_kem_768_metadata(), Retrieve and cache standardized ML-KEM-768 (NIST FIPS 203) metadata validated… (+5 more)

### Community 80 - "GlobalRNG"
Cohesion: 0.33
Nodes (4): GlobalRNG, Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., test_global_rng_is_a_singleton()

### Community 81 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (9): ArrayLike, Immutable public verification transcript and protocol decision., Return the number of public Alice tag bits., Confirm keys by comparing reproducible Toeplitz-universal hash tags. The exact…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+1 more)

### Community 82 - "ConfirmedPQCHandshake"
Cohesion: 0.14
Nodes (9): ConfirmedPQCHandshake, PQCKeyConfirmation, Self, Enter a managed lifetime for this private confirmation-key state., Capability produced only after both role-separated Finished MACs verify., Enter a managed lifetime for this established local session., Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Verify Alice's chained Finished and produce mutual-confirmation proof. (+1 more)

### Community 83 - "oqs_kem_backend.py"
Cohesion: 0.07
Nodes (26): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _new_kem(), _OQSKEM, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair (+18 more)

### Community 84 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 85 - "oqs_backend.py"
Cohesion: 0.13
Nodes (16): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, Adapter isolating the liboqs-python signature API., Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend. (+8 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "PQCFinishedMessage"
Cohesion: 0.29
Nodes (4): PQCFinishedMessage, Immutable public transport message carrying one role-bound Finished MAC., Encode the public Finished message using fixed, unambiguous field order., Serialize this public Finished message to a JSON-compatible mapping.

### Community 88 - "derive_hkdf_sha384"
Cohesion: 0.27
Nodes (8): derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), Canonical KEM input construction and HKDF primitives for QuantumSec., test_hkdf_sha384_accepts_rfc5869_optional_or_empty_salt(), test_hkdf_sha384_is_deterministic_and_domain_separated()

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "pqc/__init__.py"
Cohesion: 0.06
Nodes (25): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., StrEnum, Authentication outcome produced before any Alice-side response is sent., ServerOfferProcessingStatus, EstablishedPQCSession (+17 more)

### Community 92 - "test_providers.py"
Cohesion: 0.16
Nodes (17): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., hqc(), ml_kem(), fixture, FixtureRequest (+9 more)

### Community 94 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Ausencia de métodos de serialización y transporte (`to_dict` / `from_dict`) en `EncapsulationResponse`, [H-02] Ubicación desalineada de `EncapsulationResponse` fuera de `pqc/protocol/messages.py`, Informe de Revisión de Código Independiente: Módulo `pqc` (Autenticación del Iniciador y Encapsulamiento KEM) (+5 more)

### Community 95 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] `ResponderKEMState` retiene claves privadas pero carece de método `decapsulate()`, Informe de Revisión de Código Independiente: Módulo `pqc` (KEM y Handshake PQC), [L-01] Ausencia de método explícito de destrucción/limpieza de claves efímeras (+5 more)

### Community 96 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)"
Cohesion: 0.17
Nodes (11): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor), [L-01] Ausencia de soporte para el protocolo de Context Manager (`with`) en estados efímeros, [L-02] Duplicación estructural entre `ResponderSharedSecretState` e `InitiatorKEMState` (+3 more)

### Community 97 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)"
Cohesion: 0.17
Nodes (11): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión), [L-01] Ausencia de propiedad `@property session_key` en `EstablishedPQCSession`, [L-02] Semántica sobrecargada de `is_closed` en estados de confirmación (+3 more)

### Community 98 - "QuantumSec TFM Goal"
Cohesion: 0.11
Nodes (19): 10. Security Model, 11. Security Profiles, 12. Experimental Methodology, 13. Key Metrics, 14. TFM Deliverables, 15. Definition of Done, 16. Out of Scope, 17. Future Work (+11 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 100 - "test_key_schedule.py"
Cohesion: 0.19
Nodes (16): Build explicit HKDF info for the Phase 5 session-key purpose., _session_key_info(), Return Bob's authenticated private KEM state for tests., responder_secret_state(), _flipped(), parametrize, Tests for canonical Phase 5 transcripts, KEM combination, and session-key…, test_client_nonce_changes_transcript_hash_and_hkdf_output() (+8 more)

### Community 101 - "create_phase5_flow"
Cohesion: 0.14
Nodes (24): Self, Construct and validate a transcript from the two authenticated wire messages., Deserialize public messages without authenticating their signatures. Successful…, create_phase5_flow(), derive_session_keys(), initiator_secret_state(), Phase5Flow, Complete authenticated flow retaining both parties' private Phase 4 states. (+16 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "bb84.py"
Cohesion: 0.17
Nodes (15): BB84SessionStatus, _copy_bb84_bases(), encode_bb84_state(), ArrayLike, ComplexArray, integer, StrEnum, Reproducible prepare-and-measure simulation of the BB84 protocol. (+7 more)

### Community 105 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "protocol/__init__.py"
Cohesion: 0.06
Nodes (39): ProcessedClientKeyExchange, Bob-local KEM secrets recovered after authenticating Alice's response. Raw-…, Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., ResponderSharedSecretState, Six-phase authenticated PQC handshake and confirmed session primitives., InitiatorKEMState, ProcessedServerOffer (+31 more)

### Community 110 - "_OQSSignature"
Cohesion: 0.14
Nodes (8): _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable., _SignatureFactory

### Community 111 - "amplify_privacy"
Cohesion: 0.21
Nodes (10): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly() (+2 more)

### Community 112 - "random_basis"
Cohesion: 0.27
Nodes (7): integer, ndarray, random_basis(), Generate binary choices using this simulator's bias/correlation model., Generate generic binary choices for adaptation by the QKD layer., Generate binary choices, allowing specialized RNGs to override their model., Generate raw bits with the configured bias and temporal correlation.

### Community 113 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 114 - ".run"
Cohesion: 0.50
Nodes (3): random_bit(), Generate one or more uniformly distributed classical bits., Simulate preparation, transmission, measurement, sifting, and QBER data.

### Community 115 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 117 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 118 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 119 - "primitives/states.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named pure states commonly used by QKD protocols.

## Knowledge Gaps
- **230 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+225 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 863 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `BB84Protocol` (2× useful, score=1.994278984) _(code changed — re-verify)_

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `Basis` to `adapters.py`, `bb84.py`, `sift_keys`, `BB84Result`, `test_bb84.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ResponderKEMState` connect `ResponderKEMState` to `PQCProfile`, `test_server_offer.py`, `test_client_exchange.py`, `.__exit__`, `PQCParty`, `protocol/__init__.py`, `.__enter__`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `adapters.py`, `BaseRNG`, `toeplitz_hash`, `test_measures.py`, `amplify_privacy`, `reconcile_cascade`, `verify_reconciled_keys`, `estimate_qber_from_sample`, `test_bb84.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `SeededRNG` (e.g. with `test_bb84_rejects_non_positive_or_non_integer_signal_counts()` and `test_parameter_estimation_rejects_invalid_fraction()`) actually correct?**
  _`SeededRNG` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 8 INFERRED edges - model-reasoned connections that need verification._