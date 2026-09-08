# Graph Report - QuantumSec  (2026-09-08)

## Corpus Check
- 301 files · ~130,926 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3136 nodes · 7588 edges · 148 communities (116 shown, 27 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 331 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ac46477b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- adapters.py
- IdentityChannel
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- PQCProfile
- pqc/errors.py
- Revisión final independiente — Fase 7: Motor Experimental Reproducible V1
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- hybrid/runner.py
- bb84.py
- protocol/__init__.py
- api.ts
- campaigns/thesis_v1.py
- BB84Protocol
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- estimate_qber_from_sample
- runtime.py
- BB84SessionResult
- identity.py
- client.ts
- compilerOptions
- AppShell.tsx
- test_key_confirmation.py
- constants.py
- SimulationConfigurator.tsx
- test_key_schedule.py
- dm_from_ket
- DepolarizingChannel
- Adaptive Agents for QKD
- test_data_plane.py
- Basis
- BB84Result
- _OQSKEM
- HybridDerivedKeys
- ProtectedSession
- SimulatorPage.tsx
- profile_definition
- qber_by_basis
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- schemas.py
- ResizeObserverMock
- ExperimentConfig
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
- capabilities.py
- amplify_privacy
- quantumsec
- information.py
- EXPERIMENTS.md
- SessionConfig
- orchestration/profiles.py
- test_server_offer.py
- Reproducible Experiment Engine V1
- copy_binary_vector
- experiments/record.py
- MLDSAIdentity
- _OQSSignature
- .__exit__
- _require_bytes
- SessionProfile
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- PQCOperationTimer
- 13. Experiments
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- ChannelPipeline
- QuantumSec Deployment Guide
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- SignedServerKeyOffer
- QuantumSec Web UI V1
- PauliChannel
- .__exit__
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- AuthenticationFrame
- BaseRNG
- 10. Security Model
- export.py
- test_authentication.py
- QuantumSec Conventions Memory
- test_providers.py
- qkd/transcript.py
- .generate
- analysis/thesis_v1.py
- KrausChannel
- validation.py
- _prepare_density_matrix
- AuthenticatedKEMContributions
- .__exit__
- PQCParty
- .apply
- .__enter__
- test_api.py
- build_channel_stage
- test_noise.py
- .__exit__
- campaigns/__init__.py
- d1.py
- analysis/__init__.py
- BB84SessionStatus
- experiments/config.py
- verify_reconciled_keys
- Thesis Campaign `thesis-v1.0.1`
- health
- .canonical_bytes
- .from_dict
- operations.py
- _final_key_string
- _top_level_imports
- .__enter__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 129 edges
2. `PQCParty` - 80 edges
3. `BB84Protocol` - 63 edges
4. `SessionConfig` - 62 edges
5. `SignedServerKeyOffer` - 62 edges
6. `PQCProfile` - 53 edges
7. `ExperimentConfig` - 50 edges
8. `SessionProfile` - 46 edges
9. `IdentityChannel` - 45 edges
10. `run_hybrid_session()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `QuantumSec Project Scope & Invariants`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/core.md
- `RNG Architecture Design Principles` --semantically_similar_to--> `Injected RNG Convention`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → .serena/memories/conventions.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `Layered Dependency Discipline`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/conventions.md
- `Graphify Knowledge Graph Integration Rules` --semantically_similar_to--> `Graphify Knowledge Graph Guidelines`  [INFERRED] [semantically similar]
  AGENTS.md → .agents/rules/graphify.md
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

## Communities (148 total, 27 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.06
Nodes (48): Exception, MonkeyPatch, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, OQSRuntimeVersions, OQSSignatureBackend (+40 more)

### Community 1 - "adapters.py"
Cohesion: 0.14
Nodes (22): ChannelSummary, post, _bb84_basis_value(), _channel_summary(), BB84SimulationRequest, BB84SimulationResponse, Adapters between typed HTTP data and the QuantumSec simulation domain., Narrow the general QKD Basis enum to BB84's two supported bases. (+14 more)

### Community 2 - "IdentityChannel"
Cohesion: 0.10
Nodes (29): IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig, Configuration for BB84 post-processing under assumed channel authentication.…, _InvalidOutputChannel, ArrayLike, ComplexArray, parametrize (+21 more)

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
Cohesion: 0.20
Nodes (15): QKD metric computations., asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits from an explicit asymptotic phase-error bound. The… (+7 more)

### Community 7 - "PQCProfile"
Cohesion: 0.12
Nodes (36): PQCProfile, StrEnum, Enumeration of QuantumSec handshake profiles defining selected algorithm suites., Factory creating responder ephemeral KEM states and authenticated…, ServerKeyOfferFactory, _create_flow(), _Phase4Flow, _prepare_phase3() (+28 more)

### Community 8 - "pqc/errors.py"
Cohesion: 0.05
Nodes (52): _new_kem(), OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, Adapter isolating the liboqs-python key-encapsulation API., Initialize and return a new liboqs KeyEncapsulation instance for the specified…, Extract and validate a required metadata field from the liboqs algorithm… (+44 more)

### Community 9 - "Revisión final independiente — Fase 7: Motor Experimental Reproducible V1"
Cohesion: 0.04
Nodes (44): 10. Evidencia de validación, 11. Preparación por experimento, 12. Correcciones aplicadas, 13. Conclusión, 1. Dictamen, 2. Alcance inspeccionado, 3. Arquitectura y propiedades verificadas, 4. Tabla de hallazgos (+36 more)

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
Cohesion: 0.17
Nodes (15): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, build_channel_pipeline(), Public, Pydantic-free specifications for reproducible QKD channel pipelines., Build an ordered pipeline with domain-separated RNG streams for adversaries., _stage_seed() (+7 more)

### Community 14 - "hybrid/runner.py"
Cohesion: 0.05
Nodes (54): Versioned public configuration for common QuantumSec session execution., Runtime-only capabilities kept separate from reproducible public configuration., Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, Establishment-to-data-plane adapter with explicit session-key ownership…, _hybrid_public_context_entries(), _pqc_outcome(), _qkd_outcome() (+46 more)

### Community 15 - "bb84.py"
Cohesion: 0.07
Nodes (36): Classical QKD post-processing algorithms and immutable transcripts., CascadeConfig, CascadePassStatistics, CascadePublicEvent, _initial_block_size(), _parity(), _PassLayout, ArrayLike (+28 more)

### Community 16 - "protocol/__init__.py"
Cohesion: 0.05
Nodes (70): Reusable execution of the existing mutually authenticated PQC phases 2--4., Runtime-only accumulation of exact PQC operation timings., Post-quantum identity, authentication, KEM, and key-establishment primitives., Central QuantumSec deployment profiles for PQC handshakes., ClientKeyExchangeFactory, ClientKeyExchangeProcessingStatus, ProcessedClientKeyExchange, StrEnum (+62 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "campaigns/thesis_v1.py"
Cohesion: 0.10
Nodes (36): analytical_qber(), AnalyticalQBER, Analytical BB84 error predictions for the E2 validation campaign., Expected Z-, X-, and uniform-basis aggregate QBER., Return the exact E2 prediction implied by the implemented channel., build_campaign_plan(), CampaignPlan, CampaignPreset (+28 more)

### Community 19 - "BB84Protocol"
Cohesion: 0.19
Nodes (24): AuthenticationContext, AuthenticationTransportHook, Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _imports_top_level() (+16 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.12
Nodes (29): QRNGSimulator, Generate binary choices using this simulator's bias/correlation model., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., Generate raw bits with the configured bias and temporal correlation., SeededRNG (+21 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.08
Nodes (23): _copy_bb84_bases(), estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the… (+15 more)

### Community 23 - "runtime.py"
Cohesion: 0.12
Nodes (9): ExperimentRuntime, ExperimentRuntimeFactory, PQCIdentityProvisioning, Runtime-only provisioning for experiment configurations., Create per-run contexts while retaining persistent laboratory identities. ML-…, Provision and time persistent campaign identities exactly once., One-time ML-DSA identity-generation cost outside session timings., MLDSAAuthenticationContext (+1 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (12): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+4 more)

### Community 25 - "identity.py"
Cohesion: 0.08
Nodes (25): Private and public identities for PQC authentication., Verify a signature against the message using this public identity's algorithm…, ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations. (+17 more)

### Community 26 - "client.ts"
Cohesion: 0.27
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), useCapabilities(), useSimulation(), SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.16
Nodes (12): App(), AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection (+4 more)

### Community 29 - "test_key_confirmation.py"
Cohesion: 0.07
Nodes (53): _compute_finished_verify_data(), ConfirmedPQCHandshake, _finished_mac_input(), PQCConfirmationKeyState, PQCKeyConfirmation, PQCOperationObserver, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine. (+45 more)

### Community 30 - "constants.py"
Cohesion: 0.24
Nodes (7): Project-wide numerical constants with no domain-layer dependencies., Linear-algebra helpers for finite-dimensional quantum systems., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "test_key_schedule.py"
Cohesion: 0.06
Nodes (61): _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), derive_hkdf_sha384() (+53 more)

### Community 33 - "dm_from_ket"
Cohesion: 0.08
Nodes (31): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, _immutable_density(), InterceptResendAttack, ArrayLike, ComplexArray, Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., Return an immutable simulator-only snapshot of cumulative counters. (+23 more)

### Community 34 - "DepolarizingChannel"
Cohesion: 0.12
Nodes (16): DepolarizingChannel, ArrayLike, ComplexArray, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, Apply depolarizing noise to a single-qubit density matrix., parametrize, test_supported_channels_match_analytical_per_basis_qber(), test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness() (+8 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "test_data_plane.py"
Cohesion: 0.16
Nodes (16): Self, Bilateral, direction-separated PSK material for one or more QKD sessions., Provision matching but independent copies for each communication direction., WegmanCarterAuthenticationContext, open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., test_wegman_carter_context_enforces_directional_key_separation(), _establish() (+8 more)

### Community 37 - "Basis"
Cohesion: 0.11
Nodes (22): bases_from_bits(), Basis, basis_from_bit(), ndarray, Standard single-qubit measurement bases., Map the QKD random-bit convention 0/1 to the Z/X basis., Map a one-dimensional sequence of random bits to QKD bases., QKD-specific states, operations, bases, and standard measurements. (+14 more)

### Community 38 - "BB84Result"
Cohesion: 0.11
Nodes (8): BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return aggregate simulator-diagnostic QBER over the complete sifted key. This…, Return simulator-only Z, X, and aggregate full-sifted QBER., Immutable raw and sifted material produced by one complete BB84 run.

### Community 39 - "_OQSKEM"
Cohesion: 0.10
Nodes (14): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _OQSKEM, _OQSModule, BaseException, Protocol, Self (+6 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "profile_definition"
Cohesion: 0.05
Nodes (32): PQCProfileDefinition, profile_definition(), Immutable algorithm suite specification for a QuantumSec PQC profile., Return the configured KEM names in canonical protocol order., Retrieve the immutable algorithm suite definition for the specified QuantumSec…, ClientKeyExchangeProcessor, PQCOperationObserver, Authenticate Alice and validate session binding before Bob decapsulates. (+24 more)

### Community 44 - "qber_by_basis"
Cohesion: 0.16
Nodes (18): _optional_probability(), ArrayLike, ndarray, qber(), qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics., Immutable aggregate and BB84 basis-conditioned error metrics. (+10 more)

### Community 45 - "sift_keys"
Cohesion: 0.22
Nodes (14): _basis_vector(), ArrayLike, ndarray, Validate a one-dimensional sequence of named QKD bases., Keep aligned raw bits whose named preparation and measurement bases match., sift_keys(), parametrize, test_empty_sifting_is_valid_but_efficiency_is_undefined() (+6 more)

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

### Community 50 - "schemas.py"
Cohesion: 0.18
Nodes (16): BaseModel, model_validator, AmplitudeDampingChannelConfiguration, ApiError, AttackDiagnosticsSummary, BitFlipChannelConfiguration, DepolarizingChannelConfiguration, IdentityChannelConfiguration (+8 more)

### Community 52 - "ExperimentConfig"
Cohesion: 0.13
Nodes (17): ExperimentConfig, One normalized instruction for an experimental session execution., Run ordered configurations sequentially, optionally shuffling reproducibly.…, run_batch(), e3_config(), experiment_runner(), fixture, qkd_config() (+9 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "capabilities.py"
Cohesion: 0.18
Nodes (16): ParameterCapability, get_capabilities(), _probability(), project_version(), CapabilitiesResponse, Capability discovery backed by the features that exist in the repository., Return the installed project version with a source-tree fallback., Describe implemented and planned features without implying future support. (+8 more)

### Community 71 - "amplify_privacy"
Cohesion: 0.21
Nodes (10): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly() (+2 more)

### Community 73 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 74 - "EXPERIMENTS.md"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "SessionConfig"
Cohesion: 0.17
Nodes (28): Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Dispatch a normalized session config to its domain-specific adapter., run_session(), test_generic_runner_closes_live_session_result(), test_generic_runner_rejects_d1_until_the_data_plane_runner_exists(), _context(), parametrize (+20 more)

### Community 79 - "orchestration/profiles.py"
Cohesion: 0.07
Nodes (31): Enum, CapabilityStatus, EstablishmentSource, StrEnum, qkd_profile_definition(), QKDProfile, QKDProfileDefinition, Public session profiles with orthogonal establishment and authentication… (+23 more)

### Community 80 - "test_server_offer.py"
Cohesion: 0.14
Nodes (22): OfferCreation, bob(), high_creation(), low_creation(), fixture, FixtureRequest, parametrize, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+14 more)

### Community 81 - "Reproducible Experiment Engine V1"
Cohesion: 0.25
Nodes (8): Batch and statistics, CLI, Configuration, Definitive campaign, Environment and record schema, Metrics and exports, Reproducible Experiment Engine V1, Runtime and secret lifecycle

### Community 82 - "copy_binary_vector"
Cohesion: 0.09
Nodes (32): Sampled QBER estimation with mandatory removal of disclosed key positions., Toeplitz-universal privacy amplification for reconciled QKD keys., generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Efficient binary Toeplitz universal hashing for QKD post-processing., Generate the public Toeplitz diagonal seed through the injected RNG. (+24 more)

### Community 83 - "experiments/record.py"
Cohesion: 0.11
Nodes (13): BatchProvenance, ExperimentRecord, _freeze(), _freeze_mapping(), Immutable, versioned public evidence produced by one experiment run., Copy public evidence before the caller closes the live session capability., Public, versioned provenance shared by every retained run in one batch., _thaw() (+5 more)

### Community 84 - "MLDSAIdentity"
Cohesion: 0.06
Nodes (29): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+21 more)

### Community 85 - "_OQSSignature"
Cohesion: 0.11
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "_require_bytes"
Cohesion: 0.07
Nodes (13): EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key., Enter a managed lifetime for this established local session. (+5 more)

### Community 88 - "SessionProfile"
Cohesion: 0.09
Nodes (44): Canonical binary encoding helpers for upper-layer session protocols., HybridPublicContext, Authenticated public context binding every hybrid session input., canonical_hybrid_secret_input(), _expected_algorithms(), hybrid_component_metadata_bytes(), hybrid_kem_label(), HybridSecretComponent (+36 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "PQCOperationTimer"
Cohesion: 0.29
Nodes (4): PQCOperationTimer, PQCOperationTimings, Accumulate successful direct timings without observing secret values., test_e1_operation_timer_accumulates_only_direct_observations()

### Community 92 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

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

### Community 99 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (17): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Testing y Calidad, [H-01] Manejador de excepciones no parentizado en `ml_dsa.py` incompatible con Python $\le 3.13$, [H-02] Captura excesivamente restrictiva (`except ValueError:`) que deja escapar excepciones criptográficas y operativas del backend, Informe de Revisión de Código Independiente: Orquestación de Sesiones, Runners PQC/QKD y Composición Híbrida (Fases 4 y 5) (+9 more)

### Community 100 - "ChannelPipeline"
Cohesion: 0.24
Nodes (12): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_bit_flip_channel_extremes(), test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels() (+4 more)

### Community 101 - "QuantumSec Deployment Guide"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 102 - "BB84 security model"
Cohesion: 0.14
Nodes (13): AES-256-GCM data plane, Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Hybrid session composition, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication (+5 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "SignedServerKeyOffer"
Cohesion: 0.11
Nodes (33): InitiatorKEMState, PQCOperationObserver, StrEnum, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Authentication outcome produced before any Alice-side response is sent., Alice-local KEM secrets created only after authenticating the responder. Raw-…, ServerKeyOfferProcessor (+25 more)

### Community 105 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 106 - "PauliChannel"
Cohesion: 0.19
Nodes (8): Single-qubit CPTP noise models., PauliChannel, PhaseFlipChannel, Single-qubit Pauli noise channels., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability., Single-qubit channel that applies Pauli Z with probability ``p``., test_phase_flip_maps_plus_to_minus()

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release references to ephemeral private KEM instances to prevent subsequent…, Release the private KEM capabilities when leaving a managed lifetime.

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "AuthenticationFrame"
Cohesion: 0.06
Nodes (48): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationEvidence, AuthenticationFrame, AuthenticationMetrics, AuthenticationSessionRegistry, AuthenticationSessionReplayError, AuthenticationState (+40 more)

### Community 111 - "BaseRNG"
Cohesion: 0.10
Nodes (20): BaseRNG, GlobalRNG, ABC, ndarray, random_basis(), random_bit(), random_unitary(), Injectable random-number sources for reproducible simulations. (+12 more)

### Community 112 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 113 - "export.py"
Cohesion: 0.15
Nodes (29): ArgumentParser, main(), _parser(), Minimal command-line interface for reproducible QuantumSec runs., _canonical_cell(), config_from_json(), configs_from_json(), _csv_value() (+21 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.15
Nodes (20): PreSharedAuthenticationMaterial, Consumable PSK bit stream whose contents are never exposed or serialized., _frame(), _ml_dsa_authenticator(), parametrize, test_ml_dsa_rejects_missing_signature(), test_ml_dsa_rejects_modified_or_cross_context_frame(), test_ml_dsa_rejects_modified_signature() (+12 more)

### Community 115 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 116 - "test_providers.py"
Cohesion: 0.12
Nodes (19): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, hqc(), ml_kem() (+11 more)

### Community 117 - "qkd/transcript.py"
Cohesion: 0.13
Nodes (18): Encode replay-relevant context without the authenticated payload., length_prefixed(), Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), _bases_payload(), _binary_payload(), build_qkd_classical_transcript() (+10 more)

### Community 119 - "analysis/thesis_v1.py"
Cohesion: 0.07
Nodes (73): generate_all(), _number(), _numbers(), _plot_e1(), _plot_e2(), _plot_e3(), _plot_e4(), _plot_e5() (+65 more)

### Community 120 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 122 - "validation.py"
Cohesion: 0.05
Nodes (77): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+69 more)

### Community 123 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (11): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Return the same physical state without aliasing the input array. (+3 more)

### Community 124 - "AuthenticatedKEMContributions"
Cohesion: 0.22
Nodes (4): AuthenticatedKEMContributions, Consumable capability issued only for an authenticated exact PQC transcript., Return defensive secret copies once and retire the capability., test_contribution_capability_cannot_be_claimed_without_protocol_proof()

### Community 125 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 126 - "PQCParty"
Cohesion: 0.05
Nodes (49): Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PublicIdentity, Immutable public verification identity associating an owner name with public…, Serialize this public identity into a JSON-compatible dictionary with…, PQCParty (+41 more)

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 130 - "build_channel_stage"
Cohesion: 0.29
Nodes (7): build_channel_stage(), _optional_number(), Build one domain channel from a validated neutral stage specification., parametrize, test_every_public_qkd_stage_builds_the_expected_channel(), build_channel(), Map one validated API channel configuration to the public channel API.

### Community 131 - "test_noise.py"
Cohesion: 0.14
Nodes (19): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state() (+11 more)

### Community 132 - ".__exit__"
Cohesion: 0.25
Nodes (5): BaseException, TracebackType, Release secret references when leaving a managed lifetime., Release secret references idempotently without claiming memory zeroization., Transfer raw KEM contributions once to the domain-owned hybrid capability.

### Community 134 - "d1.py"
Cohesion: 0.13
Nodes (16): D1Record, _expect_invalid_tag(), _flip_first(), Secret-free executable D1 protected-session demonstration., Establish HYBRID-DIVERSE, transfer its key, and test AES-GCM rejection., run_d1(), TamperOutcome, _distribution_version() (+8 more)

### Community 136 - "BB84SessionStatus"
Cohesion: 0.25
Nodes (6): BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., QKD protocol implementations., A basis average must not authorize extraction on an asymmetric channel., test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error()

### Community 137 - "experiments/config.py"
Cohesion: 0.18
Nodes (16): _integer(), _invalid_stage(), _number(), _optional_integer(), _postprocessing_from_public_dict(), Strict, versioned, secret-free experiment configuration., _reject_unknown(), _session_from_public_dict() (+8 more)

### Community 138 - "verify_reconciled_keys"
Cohesion: 0.17
Nodes (11): ArrayLike, Immutable public key-agreement verification data and protocol decision., Return the number of public Alice tag bits., Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, VerificationResult, verify_reconciled_keys(), Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, test_different_keys_fail_for_deterministic_hash_setup() (+3 more)

### Community 139 - "Thesis Campaign `thesis-v1.0.1`"
Cohesion: 0.40
Nodes (4): Interpretation boundary, Reproduction, Status, Thesis Campaign `thesis-v1.0.1`

### Community 140 - "health"
Cohesion: 0.50
Nodes (4): get, HealthResponse, health(), HealthResponse

### Community 142 - ".from_dict"
Cohesion: 0.16
Nodes (14): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+6 more)

### Community 143 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 144 - "_final_key_string"
Cohesion: 0.50
Nodes (4): _final_key_string(), NDArray, uint8, Serialize a completed simulator key as a binary string for inspection.

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

## Knowledge Gaps
- **332 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+327 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1278 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `test_api.py`, `build_channel_stage`, `IdentityChannel`, `adapters.py`, `BB84SessionStatus`, `experiments/config.py`, `verify_reconciled_keys`, `test_measures.py`, `QuantumChannel`, `bb84.py`, `BB84Protocol`, `estimate_qber_from_sample`, `runtime.py`, `dm_from_ket`, `DepolarizingChannel`, `test_data_plane.py`, `amplify_privacy`, `SessionConfig`, `copy_binary_vector`, `BaseRNG`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `test_key_schedule.py`, `test_data_plane.py`, `PQCProfile`, `SignedServerKeyOffer`, `profile_definition`, `SessionConfig`, `hybrid/runner.py`, `protocol/__init__.py`, `test_server_offer.py`, `MLDSAIdentity`, `runtime.py`, `test_key_confirmation.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `SeededRNG` (e.g. with `ExperimentRuntimeFactory` and `build_channel_pipeline()`) actually correct?**
  _`SeededRNG` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SessionConfig` (e.g. with `QKDProfile` and `SessionProfile`) actually correct?**
  _`SessionConfig` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 11 INFERRED edges - model-reasoned connections that need verification._