# Graph Report - QuantumSec  (2026-09-06)

## Corpus Check
- 218 files · ~91,310 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2217 nodes · 4719 edges · 134 communities (104 shown, 26 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 224 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b6c75e9`
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
- OQSKEMProvider
- _OQSKEM
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- as_ket
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- dm_from_ket
- DepolarizingChannel
- ChannelPipeline
- test_rng.py
- estimate_qber_from_sample
- .generate
- BB84SessionResult
- identity.py
- client.ts
- compilerOptions
- AppShell.tsx
- test_server_offer.py
- SeededRNG
- SimulationConfigurator.tsx
- PQCHandshakeTranscript
- PQCProfile
- qber_by_basis
- Adaptive Agents for QKD
- bb84.py
- Basis
- BB84Result
- create_phase5_flow
- PublicIdentity
- .apply
- SimulatorPage.tsx
- test_initiator.py
- QuantumSec Web UI V1
- postprocessing/__init__.py
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- SignedServerKeyOffer
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
- test_states.py
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- _validated_identity_name
- OQSKEMBackend
- Revisión independiente del TFM — QuantumSec
- amplify_privacy
- toeplitz_hash
- BackendOperationError
- PQCParty
- UnsupportedAlgorithmError
- .__exit__
- .__exit__
- GlobalRNG
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- .__enter__
- ._active_ml_kem
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- .__exit__
- Experimental Design Review
- test_key_schedule.py
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- TrustedIdentityStore
- _prepare_density_matrix
- test_api.py
- .__exit__
- ui/core.md
- Recommended Changes to TFM_GOAL.md
- Clasificación
- pqc/errors.py
- verify_reconciled_keys
- _require_bytes
- ml_kem_768_metadata
- Security Concerns / Overclaims
- 13. Experiments
- copy_binary_vector
- encode_bb84_state
- Executive Assessment
- .from_dict
- Scope Matrix
- 10. Security Model
- Problems I Found
- Recommended Research Question
- Up to Three Improvements Worth Adding
- .__enter__
- Recommended Security Profiles
- _OQSSignature
- _require_bytes
- ._active_hqc
- .generate
- .apply

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 97 edges
2. `PQCParty` - 71 edges
3. `PQCProfile` - 62 edges
4. `SignedServerKeyOffer` - 55 edges
5. `dm_from_ket()` - 41 edges
6. `ServerKeyOfferProcessor` - 38 edges
7. `_create_flow()` - 36 edges
8. `BaseRNG` - 35 edges
9. `BB84Protocol` - 35 edges
10. `Basis` - 32 edges

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

## Communities (134 total, 26 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.13
Nodes (17): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return standardized FIPS 204 metadata and key/signature lengths for ML-DSA-65., Return the immutable ML-DSA-65 public key., fixture (+9 more)

### Community 1 - "adapters.py"
Cohesion: 0.07
Nodes (64): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+56 more)

### Community 2 - "validation.py"
Cohesion: 0.06
Nodes (73): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+65 more)

### Community 3 - "QuantumSec Serena Root Memory"
Cohesion: 0.12
Nodes (20): Detailed Module Responsibilities Blueprint, Query: BB84 Core Integration Architecture, Query: Serena Onboarding & Memory Creation, QuantumSec Serena Root Memory, Core Constants Centralization, Core Layer Infrastructure Memory, Core RNG Abstractions, Serena Memory Progressive Discovery Model (+12 more)

### Community 4 - "devDependencies"
Cohesion: 0.04
Nodes (47): jsdom, lucide-react, react, react-dom, recharts, tailwindcss, @tailwindcss/vite, @testing-library/jest-dom (+39 more)

### Community 5 - "ProjectiveMeasurement Class"
Cohesion: 0.07
Nodes (34): MeasurementSample Dataclass, Report: MeasurementSample Data Structure, ProjectiveMeasurement Class, Report: ProjectiveMeasurement Class, measure_projective Function, Report: Refactor measure_projective, Born Probability Validation Order, Report: Born Probability Validation Order (+26 more)

### Community 6 - "asymptotic_bb84_secret_length"
Cohesion: 0.23
Nodes (14): asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits from an explicit asymptotic phase-error bound. The…, parametrize (+6 more)

### Community 7 - "test_client_exchange.py"
Cohesion: 0.16
Nodes (29): Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, _create_flow(), _Phase4Flow, _prepare_phase3(), _private_initiator_state(), _process(), parametrize (+21 more)

### Community 8 - "OQSKEMProvider"
Cohesion: 0.07
Nodes (29): KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Immutable specification and buffer dimensions for a Key Encapsulation Mechanism., Generate and encapsulate a fresh shared secret against the target public key., Decapsulate an incoming ciphertext using this provider instance's private key. (+21 more)

### Community 9 - "_OQSKEM"
Cohesion: 0.14
Nodes (8): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager., Protocol for the liboqs KeyEncapsulation constructor callable.

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
Cohesion: 0.08
Nodes (28): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, Return a finite scalar probability in the closed unit interval., _validate_probability(), Ideal quantum channel., Public quantum-channel API for QKD simulations. (+20 more)

### Community 14 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (27): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+19 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.07
Nodes (50): _compute_finished_verify_data(), ConfirmedPQCHandshake, _finished_mac_input(), PQCConfirmationKeyState, PQCKeyConfirmation, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released. (+42 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "dm_from_ket"
Cohesion: 0.10
Nodes (24): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, InterceptResendAttack, Return an immutable simulator-only snapshot of cumulative counters., Small immutable snapshot of simulator-only attack observations., Measure selected signals in a random BB84 basis and resend fresh states. The…, dm_from_ensemble(), dm_from_ket() (+16 more)

### Community 19 - "DepolarizingChannel"
Cohesion: 0.09
Nodes (28): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., DepolarizingChannel, ArrayLike, ComplexArray (+20 more)

### Community 20 - "ChannelPipeline"
Cohesion: 0.16
Nodes (20): BitFlipChannel, PhaseFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., Single-qubit channel that applies Pauli Z with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_bit_flip_channel_extremes(), test_phase_flip_maps_plus_to_minus() (+12 more)

### Community 21 - "test_rng.py"
Cohesion: 0.12
Nodes (26): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., parametrize, test_base_rng_cannot_be_instantiated(), test_different_seeds_produce_different_streams() (+18 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.09
Nodes (20): _copy_bb84_bases(), estimate_qber_from_sample(), _explicit_stratified_counts(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade. (+12 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (12): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+4 more)

### Community 25 - "identity.py"
Cohesion: 0.08
Nodes (23): Private and public identities for PQC authentication., Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Verify a signature against the message using this public identity's algorithm…, ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations. (+15 more)

### Community 26 - "client.ts"
Cohesion: 0.27
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), useCapabilities(), useSimulation(), SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.16
Nodes (12): App(), AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection (+4 more)

### Community 29 - "test_server_offer.py"
Cohesion: 0.21
Nodes (16): OfferCreation, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages., test_bob_signs_canonical_offer_with_existing_identity(), test_canonical_serialization_is_deterministic_and_domain_separated() (+8 more)

### Community 30 - "SeededRNG"
Cohesion: 0.13
Nodes (30): Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., SeededRNG, IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, BB84SessionStatus, StrEnum (+22 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "PQCHandshakeTranscript"
Cohesion: 0.12
Nodes (10): _confirmation_key_info(), Require a live Phase 5 key state bound to the exact Phase 6 transcript., Build explicit HKDF info for the Phase 6 confirmation-key purpose., _validated_session_key_state(), PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob. (+2 more)

### Community 33 - "PQCProfile"
Cohesion: 0.06
Nodes (50): Enum, Internal canonical binary encoding primitives shared across PQC domains., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites. (+42 more)

### Community 34 - "qber_by_basis"
Cohesion: 0.15
Nodes (19): QKD metric computations., _optional_probability(), ArrayLike, ndarray, qber(), qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics. (+11 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "bb84.py"
Cohesion: 0.08
Nodes (30): Project-wide numerical constants with no domain-layer dependencies., BaseRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+22 more)

### Community 37 - "Basis"
Cohesion: 0.12
Nodes (19): _immutable_density(), ArrayLike, ComplexArray, Possibly intercept one qubit, then return a fresh transmitted state., bases_from_bits(), Basis, basis_from_bit(), integer (+11 more)

### Community 38 - "BB84Result"
Cohesion: 0.07
Nodes (14): BB84PostprocessingConfig, BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return aggregate simulator-diagnostic QBER over the complete sifted key. This…, Return simulator-only Z, X, and aggregate full-sifted QBER. (+6 more)

### Community 39 - "create_phase5_flow"
Cohesion: 0.17
Nodes (21): PQCConfirmationKeyDeriver, Derive a private role-local confirmation key from authenticated Phase 5 state., create_phase5_flow(), derive_session_keys(), initiator_secret_state(), Phase5Flow, Shared real PQC handshake setup for Phase 5/6 tests., Complete authenticated flow retaining both parties' private Phase 4 states. (+13 more)

### Community 40 - "PublicIdentity"
Cohesion: 0.13
Nodes (10): PublicIdentity, Export the non-secret public identity suitable for peer trust stores., Verify a message signature against an explicitly provided public identity., Immutable public verification identity associating an owner name with public…, Serialize this public identity into a JSON-compatible dictionary with…, Return this party's public identity for distribution and registration in peer…, Add a peer's public identity to this party's trusted store with optional…, test_public_identity_validates_known_algorithm_key_length() (+2 more)

### Community 41 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "test_initiator.py"
Cohesion: 0.12
Nodes (24): Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., ServerKeyOfferProcessor, EncapsulationResponse, Unsigned public KEM ciphertext message prepared for the next phase., Serialize this public response to a JSON-compatible mapping., FixtureRequest, parametrize (+16 more)

### Community 44 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 45 - "postprocessing/__init__.py"
Cohesion: 0.13
Nodes (20): Classical QKD post-processing algorithms and immutable transcripts., _basis_vector(), ArrayLike, ndarray, Deterministic basis reconciliation for QKD raw keys., Validate a one-dimensional sequence of named QKD bases., Aligned sifted keys and the raw positions retained by reconciliation., Return the number of positions retained after basis reconciliation. (+12 more)

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

### Community 52 - "SignedServerKeyOffer"
Cohesion: 0.06
Nodes (36): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeFactory, ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, ProcessedClientKeyExchange, StrEnum, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice. (+28 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 71 - "QuantumSec Conventions Memory"
Cohesion: 0.22
Nodes (9): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+1 more)

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "_validated_identity_name"
Cohesion: 0.20
Nodes (5): Validate that the given identity name is a non-empty string and return its…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Validate the owner name and ensure the internal signer is an MLDSA65 instance., _validated_identity_name(), Return the trusted public identity for an owner, raising…

### Community 79 - "OQSKEMBackend"
Cohesion: 0.12
Nodes (21): OQSKEMBackend, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Self, Generate a new ephemeral key pair via liboqs and return a ready-to-use provider… (+13 more)

### Community 80 - "Revisión independiente del TFM — QuantumSec"
Cohesion: 0.17
Nodes (11): 6,5 / 10, Documentation Problems, Fuentes, Métricas medidas de referencia, Nota de procedimiento, Proposed Thesis Title, Revisión independiente del TFM — QuantumSec, Strongest Thesis Contribution (+3 more)

### Community 81 - "amplify_privacy"
Cohesion: 0.21
Nodes (10): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly() (+2 more)

### Community 82 - "toeplitz_hash"
Cohesion: 0.18
Nodes (17): generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Return the public seed length for an ``output_length x input_length`` matrix., Generate the public Toeplitz diagonal seed through the injected RNG., Multiply a binary vector by a seeded Toeplitz matrix using FFT convolution. For…, toeplitz_hash() (+9 more)

### Community 83 - "BackendOperationError"
Cohesion: 0.09
Nodes (24): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule, Adapter isolating the liboqs-python key-encapsulation API. (+16 more)

### Community 84 - "PQCParty"
Cohesion: 0.09
Nodes (29): Raised when an operation requires an identity from a peer not found in the…, UnknownTrustedPeerError, PQCParty, Self, Protocol participant holding a private signing identity and a trusted peer…, Validate that the party identity and trusted peer store instances are valid., Create a new party instance initialized with a fresh ML-DSA-65 signing identity., Return the owner name of this party's private identity. (+21 more)

### Community 85 - "UnsupportedAlgorithmError"
Cohesion: 0.09
Nodes (27): MonkeyPatch, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, OQSSignatureBackend, Protocol (+19 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 88 - "GlobalRNG"
Cohesion: 0.33
Nodes (4): GlobalRNG, Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., test_global_rng_is_a_singleton()

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 92 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

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
Cohesion: 0.10
Nodes (20): 11. Profiles, 12. Experimental Methodology, 14. Metrics, 15. Deliverables, 16. Definition of Done, 17. Out of Scope, 18. Future Work, 19. Threats to Validity (+12 more)

### Community 99 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release secret references idempotently without claiming memory zeroization., Release secret references when leaving a managed lifetime.

### Community 100 - "Experimental Design Review"
Cohesion: 0.20
Nodes (10): Cómo comparar QKD vs PQC vs híbrido correctamente, E1 — Descomposición del coste PQC, E2 — Coste en el cable, E3 — Validación del simulador BB84 (reemplaza «BB84 channel behaviour»), E4 — Detección de adversario *(nuevo — obligatorio)*, E5 — Establecimiento híbrido, E6 — Sesión extremo a extremo con AES-256-GCM, Experimental Design Review (+2 more)

### Community 101 - "test_key_schedule.py"
Cohesion: 0.07
Nodes (39): _length_prefixed(), Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation. (+31 more)

### Community 102 - "BB84 security model"
Cohesion: 0.22
Nodes (8): Analytical channel expectations, BB84 security model, Intercept-resend threat model, Key and parameter-estimation model, Phase-error relation, Reference, Secret-length and abort policy, Security boundary and remaining limitations

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "TrustedIdentityStore"
Cohesion: 0.12
Nodes (10): Return the explicit store of trusted peer identities configured for this party., Thread-safe in-memory registry mapping peer names to pre-provisioned trusted…, Initialize an empty trusted identity store., Return a sorted tuple of all trusted owner names registered in the store., Check whether an owner name is registered in the trusted identity store., Iterate over all trusted public identities in deterministic owner order., Return the total number of trusted peer identities in the store., Return a string representation listing registered trusted owner names. (+2 more)

### Community 105 - "_prepare_density_matrix"
Cohesion: 0.11
Nodes (15): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+7 more)

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "Recommended Changes to TFM_GOAL.md"
Cohesion: 0.22
Nodes (9): §11 — Security Profiles — REESCRIBIR (tabla), §12 — Methodology — REESCRIBIR (añadir el bloque estadístico), §15 — Definition of Done — REESCRIBIR, §3 — Research Question — REESCRIBIR, §4 — Subquestions — REESCRIBIR, §7 — Contribution — REESCRIBIR, AÑADIR §19 — Threats to Validity, AÑADIR §20 — Related Work Positioning (+1 more)

### Community 110 - "Clasificación"
Cohesion: 0.22
Nodes (9): Clasificación, Minimum Web Laboratory, Pantallas para una defensa de 10-15 min, Protected Message Demo, Protocol Visualizer, Quantum-Safe Explorer, Results / Metrics, Session Builder (+1 more)

### Community 111 - "pqc/errors.py"
Cohesion: 0.18
Nodes (9): Exception, PQCError, Domain errors for post-quantum cryptographic operations., Raised when adding an identity for an existing peer without overwrite…, Base exception class for all post-quantum cryptography domain errors in…, TrustedIdentityConflictError, Named PQC parties with signing and pre-provisioned verification trust., Explicit pre-provisioned trust for public PQC identities. (+1 more)

### Community 112 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (10): ArrayLike, Immutable public key-agreement verification data and protocol decision., Return the number of public Alice tag bits., Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+2 more)

### Community 113 - "_require_bytes"
Cohesion: 0.07
Nodes (13): EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key., Enter a managed lifetime for this established local session. (+5 more)

### Community 114 - "ml_kem_768_metadata"
Cohesion: 0.20
Nodes (8): hqc_3_metadata(), Retrieve HQC-3 metadata for the NIST Round 4 selection exposed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for…, ml_kem_768_metadata(), Retrieve and cache standardized ML-KEM-768 (NIST FIPS 203) metadata validated…, Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, Validate protocol version, session ID, nonce, profile, and algorithm public key…, test_high_kem_input_requires_both_valid_length_secrets()

### Community 115 - "Security Concerns / Overclaims"
Cohesion: 0.29
Nodes (7): AES-GCM (aún no implementado — requisitos para cuando se haga), Combinador híbrido — el punto más delicado, HQC, Key confirmation, PQC, QKD, Security Concerns / Overclaims

### Community 116 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

### Community 117 - "copy_binary_vector"
Cohesion: 0.27
Nodes (10): copy_binary_vector(), copy_indices(), ArrayLike, intp, NDArray, uint8, Return a defensive, read-only copy of one-dimensional integer indices., Validate and copy two aligned binary keys. (+2 more)

### Community 118 - "encode_bb84_state"
Cohesion: 0.20
Nodes (12): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+4 more)

### Community 119 - "Executive Assessment"
Cohesion: 0.40
Nodes (5): 1. La pregunta de investigación no es empírica, 2. No existe adversario en ninguna parte del código, 3. Existe un fallo real en el modelo de seguridad de QKD, no documentado, Executive Assessment, Veredicto resumido

### Community 120 - ".from_dict"
Cohesion: 0.14
Nodes (15): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+7 more)

### Community 122 - "Scope Matrix"
Cohesion: 0.40
Nodes (5): FUTURE WORK — NO tocar antes de entregar, MUST HAVE — sin esto no hay tesis defendible, NICE TO HAVE — solo si sobra tiempo, Scope Matrix, SHOULD HAVE — muy recomendable si el coste es pequeño

### Community 123 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 124 - "Problems I Found"
Cohesion: 0.50
Nodes (4): Críticos, Importantes, Menores, Problems I Found

### Community 125 - "Recommended Research Question"
Cohesion: 0.50
Nodes (4): La actual (para contraste), Recomendada, Recommended Research Question, Subpreguntas

### Community 126 - "Up to Three Improvements Worth Adding"
Cohesion: 0.50
Nodes (4): Mejora 1 — Modelo de adversario intercept-resend, Mejora 2 — Autenticación real del canal clásico QKD con ML-DSA-65, Mejora 3 — Frontera de entrega de clave con forma ETSI GS QKD 014, Up to Three Improvements Worth Adding

### Community 128 - "Recommended Security Profiles"
Cohesion: 0.67
Nodes (3): Problema con la taxonomía actual, Recommended Security Profiles, Taxonomía recomendada

### Community 129 - "_OQSSignature"
Cohesion: 0.18
Nodes (5): _OQSSignature, BaseException, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager.

### Community 130 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

## Knowledge Gaps
- **307 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+302 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 976 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `Basis` to `PQCProfile`, `qber_by_basis`, `adapters.py`, `bb84.py`, `BB84Result`, `postprocessing/__init__.py`, `dm_from_ket`, `estimate_qber_from_sample`, `encode_bb84_state`, `SeededRNG`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `adapters.py`, `bb84.py`, `test_measures.py`, `reconcile_cascade`, `verify_reconciled_keys`, `amplify_privacy`, `dm_from_ket`, `toeplitz_hash`, `ChannelPipeline`, `test_rng.py`, `estimate_qber_from_sample`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `DerivedSessionKeyState` connect `SignedServerKeyOffer` to `PQCHandshakeTranscript`, `PQCProfile`, `create_phase5_flow`, `test_key_confirmation.py`, `_require_bytes`, `.__exit__`, `.__enter__`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `SeededRNG` (e.g. with `test_supported_channels_match_analytical_per_basis_qber()` and `test_bb84_rejects_non_positive_or_non_integer_signal_counts()`) actually correct?**
  _`SeededRNG` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 8 INFERRED edges - model-reasoned connections that need verification._