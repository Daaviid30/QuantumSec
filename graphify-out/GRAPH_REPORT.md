# Graph Report - QuantumSec  (2026-09-07)

## Corpus Check
- 234 files · ~102,171 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2465 nodes · 5383 edges · 152 communities (118 shown, 30 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 241 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8cdbf32d`
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
- KEMMetadata
- BackendOperationError
- compilerOptions
- ResultsWorkspace.tsx
- dm_from_ket
- QuantumChannel
- information.py
- reconcile_cascade
- PQCFinishedMessage
- api.ts
- InterceptResendAttack
- DepolarizingChannel
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- ParameterEstimationResult
- .generate
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- ServerKeyOfferFactory
- BB84Protocol
- SimulationConfigurator.tsx
- runner.py
- PQCProfile
- AuthenticationFrame
- Adaptive Agents for QKD
- BaseRNG
- bb84.py
- BB84Result
- test_key_confirmation.py
- qkd/transcript.py
- authentication/base.py
- SimulatorPage.tsx
- SignedServerKeyOffer
- QuantumSec Web UI V1
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- MLDSAIdentity
- ResizeObserverMock
- pqc/__init__.py
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
- KrausChannel
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- _require_bytes
- test_providers.py
- Revisión independiente del TFM — QuantumSec
- copy_binary_vector
- postprocessing/__init__.py
- OQSKEMProvider
- BitFlipChannel
- pqc/errors.py
- .__exit__
- EstablishedPQCSession
- PQCConfirmationKeyState
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- _OQSKEM
- ResponderKEMState
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
- PQCParty
- _prepare_density_matrix
- test_api.py
- .__exit__
- ui/core.md
- Recommended Changes to TFM_GOAL.md
- Clasificación
- ChannelPipeline
- verify_reconciled_keys
- estimate_qber_from_sample
- test_authentication.py
- Security Concerns / Overclaims
- 13. Experiments
- BB84SessionStatus
- encode_bb84_state
- Executive Assessment
- test_full_six_phase_handshake_crosses_pure_json_transport
- Scope Matrix
- 10. Security Model
- Problems I Found
- Recommended Research Question
- Up to Three Improvements Worth Adding
- .apply
- Recommended Security Profiles
- _OQSSignature
- OQSSignatureBackend
- NDArray
- _require_bytes
- .apply
- _validate_probability
- .apply
- ._active_ml_kem
- ConfirmedPQCHandshake
- ._active_hqc
- .apply
- operations.py
- verify_signature
- PQCHandshakeTranscript
- test_qkd_profiles.py
- .generate
- .__enter__
- .__enter__
- .__post_init__
- .public_key
- .verify
- .metadata
- _RegisteredSignature

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 113 edges
2. `PQCParty` - 71 edges
3. `SignedServerKeyOffer` - 55 edges
4. `BB84Protocol` - 51 edges
5. `PQCProfile` - 43 edges
6. `dm_from_ket()` - 42 edges
7. `BaseRNG` - 39 edges
8. `ServerKeyOfferProcessor` - 37 edges
9. `IdentityChannel` - 36 edges
10. `_create_flow()` - 36 edges

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

## Communities (152 total, 30 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

### Community 1 - "adapters.py"
Cohesion: 0.07
Nodes (66): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _adversary_seed() (+58 more)

### Community 2 - "validation.py"
Cohesion: 0.05
Nodes (77): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+69 more)

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
Cohesion: 0.11
Nodes (26): QKD metric computations., ArrayLike, qber(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability() (+18 more)

### Community 7 - "test_client_exchange.py"
Cohesion: 0.14
Nodes (33): ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., _create_flow(), _Phase4Flow, _prepare_phase3(), _private_initiator_state(), _process(), parametrize (+25 more)

### Community 8 - "KEMMetadata"
Cohesion: 0.10
Nodes (19): KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata., Immutable specification and buffer dimensions for a Key Encapsulation Mechanism., Generate and encapsulate a fresh shared secret against the target public key., Decapsulate an incoming ciphertext using this provider instance's private key. (+11 more)

### Community 9 - "BackendOperationError"
Cohesion: 0.09
Nodes (28): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule (+20 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.06
Nodes (48): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., Linear-algebra helpers for finite-dimensional quantum systems. (+40 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.19
Nodes (11): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+3 more)

### Community 14 - "information.py"
Cohesion: 0.16
Nodes (21): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+13 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.11
Nodes (26): CascadeConfig, CascadePassStatistics, CascadePublicEvent, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+18 more)

### Community 16 - "PQCFinishedMessage"
Cohesion: 0.15
Nodes (17): PQCKeyConfirmation, Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., Verify Alice's chained Finished and produce mutual-confirmation proof., PQCFinishedMessage, Immutable public transport message carrying one role-bound Finished MAC., Encode the public Finished message using fixed, unambiguous field order. (+9 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "InterceptResendAttack"
Cohesion: 0.13
Nodes (20): InterceptResendAttack, Reset aggregate counters without rewinding the injected RNG stream., Measure selected signals in a random BB84 basis and resend fresh states. The…, Validate Hermiticity, unit trace, and positive semidefiniteness., validate_density_matrix(), parametrize, test_attack_diagnostics_can_be_reset_without_rewinding_the_rng(), test_full_interception_resends_a_pure_state_from_a_mixed_input() (+12 more)

### Community 19 - "DepolarizingChannel"
Cohesion: 0.12
Nodes (24): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness() (+16 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.13
Nodes (29): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+21 more)

### Community 22 - "ParameterEstimationResult"
Cohesion: 0.13
Nodes (6): ParameterEstimationResult, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the…, Immutable basis-aware transcript and remaining candidate material., test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error()

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (5): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return aggregate full-key QBER as a backwards-compatible alias., Return aggregate sampled QBER as a backwards-compatible alias., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "registry.py"
Cohesion: 0.18
Nodes (13): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., Generate a digital signature over the provided message bytes using the private…, SignatureMetadata, SignatureProvider (+5 more)

### Community 26 - "client.ts"
Cohesion: 0.27
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), useCapabilities(), useSimulation(), SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.16
Nodes (12): App(), AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection (+4 more)

### Community 29 - "ServerKeyOfferFactory"
Cohesion: 0.17
Nodes (21): OfferCreation, Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+13 more)

### Community 30 - "BB84Protocol"
Cohesion: 0.11
Nodes (31): IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig, BB84Protocol, Configuration for BB84 post-processing under assumed channel authentication.…, Run BB84 with an injected random source and density-matrix channel. Alice's…, Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, parametrize (+23 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "runner.py"
Cohesion: 0.09
Nodes (25): AuthenticationContext, Upper-layer composition of independent QKD and PQC domain modules., EstablishmentSource, StrEnum, qkd_profile_definition(), QKDProfile, QKDProfileDefinition, Public session profiles with orthogonal establishment and authentication… (+17 more)

### Community 33 - "PQCProfile"
Cohesion: 0.07
Nodes (44): Enum, Internal canonical binary encoding primitives shared across PQC domains., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites. (+36 more)

### Community 34 - "AuthenticationFrame"
Cohesion: 0.09
Nodes (27): AuthenticationEvidence, AuthenticationFrame, AuthenticationVerification, AuthenticatorMetadata, DirectionalAuthenticator, ABC, Generate and verify evidence for one authenticated communication direction., Canonical authentication unit binding payload to anti-replay context. (+19 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BaseRNG"
Cohesion: 0.10
Nodes (21): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+13 more)

### Community 37 - "bb84.py"
Cohesion: 0.08
Nodes (32): Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., _optional_probability(), ndarray, qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics., Immutable aggregate and BB84 basis-conditioned error metrics., Return Z, X, and aggregate QBER without inventing absent-basis values. (+24 more)

### Community 38 - "BB84Result"
Cohesion: 0.11
Nodes (8): BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return aggregate simulator-diagnostic QBER over the complete sifted key. This…, Return simulator-only Z, X, and aggregate full-sifted QBER., Immutable raw and sifted material produced by one complete BB84 run.

### Community 39 - "test_key_confirmation.py"
Cohesion: 0.20
Nodes (20): Phase5Flow, Complete authenticated flow retaining both parties' private Phase 4 states., Return Bob's authenticated private KEM state for tests., responder_secret_state(), _derive_confirmation_states(), _exchange_finished(), _Phase6States, parametrize (+12 more)

### Community 40 - "qkd/transcript.py"
Cohesion: 0.13
Nodes (19): Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), _bases_payload(), _binary_payload() (+11 more)

### Community 41 - "authentication/base.py"
Cohesion: 0.12
Nodes (16): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationMetrics, AuthenticationSessionRegistry, AuthenticationSessionReplayError, AuthenticationState, ClassicalAuthenticationResult, RuntimeError (+8 more)

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "SignedServerKeyOffer"
Cohesion: 0.09
Nodes (39): ProcessedServerOffer, StrEnum, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Authentication outcome produced before any Alice-side response is sent., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., ServerKeyOfferProcessor (+31 more)

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
Cohesion: 0.07
Nodes (26): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+18 more)

### Community 52 - "pqc/__init__.py"
Cohesion: 0.07
Nodes (40): Post-quantum identity, authentication, KEM, and key-establishment primitives., ProcessedClientKeyExchange, Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., PQCConfirmationKeyDeriver, Require a live Phase 5 key state bound to the exact Phase 6 transcript., Derive a private role-local confirmation key from authenticated Phase 5 state., Derive Alice's confirmation state and retire her KEM secret state. (+32 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "KrausChannel"
Cohesion: 0.16
Nodes (14): KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel., Evaluate ``sum_i K_i rho K_i^dagger``., parametrize (+6 more)

### Community 71 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "_require_bytes"
Cohesion: 0.11
Nodes (9): Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ClientKeyExchange, Validate wrapped offer type, signer name, signature algorithm, and signature…, Immutable public KEM ciphertext message bound to Bob's exact signed offer., Validate the protocol binding and profile-specific ciphertext fields., Validate that an argument is non-empty bytes and matches an optional expected…, Serialize every authenticated field deterministically and unambiguously., Serialize this public client exchange to a JSON-compatible mapping. (+1 more)

### Community 79 - "test_providers.py"
Cohesion: 0.13
Nodes (18): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, hqc(), ml_kem() (+10 more)

### Community 80 - "Revisión independiente del TFM — QuantumSec"
Cohesion: 0.17
Nodes (11): 6,5 / 10, Documentation Problems, Fuentes, Métricas medidas de referencia, Nota de procedimiento, Proposed Thesis Title, Revisión independiente del TFM — QuantumSec, Strongest Thesis Contribution (+3 more)

### Community 81 - "copy_binary_vector"
Cohesion: 0.15
Nodes (13): Immutable corrected key and conservative public parity transcript size., Return the conservative leakage: one bit per disclosed Alice parity., ReconciliationResult, copy_binary_vector(), copy_indices(), ArrayLike, intp, NDArray (+5 more)

### Community 82 - "postprocessing/__init__.py"
Cohesion: 0.09
Nodes (34): Classical QKD post-processing algorithms and immutable transcripts., amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Toeplitz-universal privacy amplification for reconciled QKD keys., Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., generate_toeplitz_seed() (+26 more)

### Community 83 - "OQSKEMProvider"
Cohesion: 0.14
Nodes (11): OQSKEMProvider, Return a safe string representation with public key size without exposing…, Validate that the input value is a byte string, raising a TypeError if it is…, Base provider implementing KEM operations through the liboqs backend., Validate key lengths against algorithm metadata and store immutable defensive…, Return standardized algorithm metadata defining expected key and ciphertext…, Return the algorithm metadata associated with this provider instance., Return the public key bytes used for encapsulating secrets. (+3 more)

### Community 84 - "BitFlipChannel"
Cohesion: 0.16
Nodes (11): Single-qubit CPTP noise models., BitFlipChannel, PauliChannel, PhaseFlipChannel, Single-qubit Pauli noise channels., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., Single-qubit channel that applies Pauli X with probability ``p``. (+3 more)

### Community 85 - "pqc/errors.py"
Cohesion: 0.11
Nodes (27): Exception, authenticate_transcript_checkpoints(), AuthenticationTransportHook, Bilateral authentication of a completed canonical QKD public transcript., Authenticate both directional views before any final key can be released. This…, _validate_authenticator_pair(), _ensure_signature_algorithm_enabled(), _load_oqs() (+19 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "EstablishedPQCSession"
Cohesion: 0.10
Nodes (13): EstablishedPQCSession, BaseException, Self, TracebackType, Enter a managed lifetime for this private confirmation-key state., Release the confirmation key when leaving its managed lifetime., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation. (+5 more)

### Community 88 - "PQCConfirmationKeyState"
Cohesion: 0.12
Nodes (13): _compute_finished_verify_data(), _finished_mac_input(), PQCConfirmationKeyState, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released., Return whether this state has released its role-local confirmation key., Return whether this role completed its local send/verify Finished work. (+5 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "_OQSKEM"
Cohesion: 0.14
Nodes (8): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager., Protocol for the liboqs KeyEncapsulation constructor callable.

### Community 92 - "ResponderKEMState"
Cohesion: 0.11
Nodes (14): ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Bob-side authentication, binding, and decapsulation outcome., Self, Enter a managed lifetime for this ephemeral responder state. (+6 more)

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
Cohesion: 0.09
Nodes (34): _length_prefixed(), Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation. (+26 more)

### Community 102 - "BB84 security model"
Cohesion: 0.17
Nodes (11): Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication, One-time Toeplitz/Wegman-Carter-style construction, Phase-error relation (+3 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "PQCParty"
Cohesion: 0.05
Nodes (47): Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PublicIdentity, Private and public identities for PQC authentication., Validate that the given identity name is a non-empty string and return its…, Immutable public verification identity associating an owner name with public… (+39 more)

### Community 105 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (11): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+3 more)

### Community 106 - "test_api.py"
Cohesion: 0.13
Nodes (3): parametrize, test_backend_gives_protocol_and_each_eve_stage_independent_rng_streams(), test_intercept_resend_configuration_rejects_invalid_fraction()

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "Recommended Changes to TFM_GOAL.md"
Cohesion: 0.22
Nodes (9): §11 — Security Profiles — REESCRIBIR (tabla), §12 — Methodology — REESCRIBIR (añadir el bloque estadístico), §15 — Definition of Done — REESCRIBIR, §3 — Research Question — REESCRIBIR, §4 — Subquestions — REESCRIBIR, §7 — Contribution — REESCRIBIR, AÑADIR §19 — Threats to Validity, AÑADIR §20 — Related Work Positioning (+1 more)

### Community 110 - "Clasificación"
Cohesion: 0.22
Nodes (9): Clasificación, Minimum Web Laboratory, Pantallas para una defensa de 10-15 min, Protected Message Demo, Protocol Visualizer, Quantum-Safe Explorer, Results / Metrics, Session Builder (+1 more)

### Community 111 - "ChannelPipeline"
Cohesion: 0.36
Nodes (9): ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels(), test_pipeline_copies_channel_collection_and_does_not_mutate_input(), test_pipeline_matches_manual_sequential_application(), test_pipeline_rejects_non_channel_components() (+1 more)

### Community 112 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (10): ArrayLike, Immutable public key-agreement verification data and protocol decision., Return the number of public Alice tag bits., Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+2 more)

### Community 113 - "estimate_qber_from_sample"
Cohesion: 0.25
Nodes (13): estimate_qber_from_sample(), ArrayLike, ndarray, Disclose a stratified BB84 sample and remove it from both keys. Sampling is…, parametrize, test_odd_explicit_sample_breaks_equal_basis_ties_with_the_injected_rng(), test_parameter_estimation_explicit_sample_size_preserves_alignment(), test_parameter_estimation_fails_closed_without_valid_data_for_both_bb84_bases() (+5 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.11
Nodes (24): PreSharedAuthenticationMaterial, Self, Bilateral, direction-separated PSK material for one or more QKD sessions., Provision matching but independent copies for each communication direction., Consumable PSK bit stream whose contents are never exposed or serialized., WegmanCarterAuthenticationContext, _frame(), _ml_dsa_authenticator() (+16 more)

### Community 115 - "Security Concerns / Overclaims"
Cohesion: 0.29
Nodes (7): AES-GCM (aún no implementado — requisitos para cuando se haga), Combinador híbrido — el punto más delicado, HQC, Key confirmation, PQC, QKD, Security Concerns / Overclaims

### Community 116 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

### Community 117 - "BB84SessionStatus"
Cohesion: 0.33
Nodes (5): BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., A basis average must not authorize extraction on an asymmetric channel., test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error()

### Community 118 - "encode_bb84_state"
Cohesion: 0.18
Nodes (11): encode_bb84_state(), ArrayLike, ComplexArray, integer, Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix(), _validate_bit() (+3 more)

### Community 119 - "Executive Assessment"
Cohesion: 0.40
Nodes (5): 1. La pregunta de investigación no es empírica, 2. No existe adversario en ninguna parte del código, 3. Existe un fallo real en el modelo de seguridad de QKD, no documentado, Executive Assessment, Veredicto resumido

### Community 120 - "test_full_six_phase_handshake_crosses_pure_json_transport"
Cohesion: 0.14
Nodes (18): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+10 more)

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

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 128 - "Recommended Security Profiles"
Cohesion: 0.67
Nodes (3): Problema con la taxonomía actual, Recommended Security Profiles, Taxonomía recomendada

### Community 129 - "_OQSSignature"
Cohesion: 0.11
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 130 - "OQSSignatureBackend"
Cohesion: 0.20
Nodes (8): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend., test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 131 - "NDArray"
Cohesion: 0.21
Nodes (7): intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation.

### Community 132 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

### Community 134 - "_validate_probability"
Cohesion: 0.17
Nodes (6): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, Return an immutable simulator-only snapshot of cumulative counters., Small immutable snapshot of simulator-only attack observations., Return a finite scalar probability in the closed unit interval., _validate_probability()

### Community 135 - ".apply"
Cohesion: 0.21
Nodes (9): _immutable_density(), ArrayLike, ComplexArray, Possibly intercept one qubit, then return a fresh transmitted state., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket() (+1 more)

### Community 136 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

### Community 137 - "ConfirmedPQCHandshake"
Cohesion: 0.40
Nodes (3): ConfirmedPQCHandshake, Capability produced only after both role-separated Finished MACs verify., Materialize one role-local session only from the completed Finished exchange.

### Community 139 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 140 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 141 - "verify_signature"
Cohesion: 0.50
Nodes (3): Verify a signature against the message using this public identity's algorithm…, Verify a signature by dispatching to the registered provider for the specified…, verify_signature()

### Community 142 - "PQCHandshakeTranscript"
Cohesion: 0.17
Nodes (5): PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob., Serialize this public transcript to a JSON-compatible mapping.

### Community 143 - "test_qkd_profiles.py"
Cohesion: 0.21
Nodes (20): AuthenticationTransportHook, Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), Path, _imports_top_level(), parametrize, _session_id() (+12 more)

## Knowledge Gaps
- **319 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+314 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1072 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `bb84.py` to `PQCProfile`, `adapters.py`, `BB84Result`, `asymptotic_bb84_secret_length`, `qkd/transcript.py`, `sift_keys`, `estimate_qber_from_sample`, `InterceptResendAttack`, `ParameterEstimationResult`, `encode_bb84_state`, `BB84Protocol`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_key_schedule.py`, `test_client_exchange.py`, `test_key_confirmation.py`, `_require_bytes`, `SignedServerKeyOffer`, `MLDSAIdentity`, `pqc/__init__.py`, `ResponderKEMState`, `ServerKeyOfferFactory`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `MLDSAIdentity` connect `MLDSAIdentity` to `PQCProfile`, `AuthenticationFrame`, `PQCParty`, `test_qkd_profiles.py`, `test_authentication.py`, `pqc/__init__.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `SeededRNG` (e.g. with `test_authenticated_ideal_bb84_completes()` and `test_supported_channels_match_analytical_per_basis_qber()`) actually correct?**
  _`SeededRNG` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._