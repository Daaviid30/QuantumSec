# Graph Report - QuantumSec  (2026-09-08)

## Corpus Check
- 309 files · ~142,420 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3281 nodes · 7922 edges · 157 communities (129 shown, 24 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 349 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0bdf3a28`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- main.py
- run_qkd_profile
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- test_client_exchange.py
- pqc/errors.py
- Revisión final independiente — Fase 7: Motor Experimental Reproducible V1
- compilerOptions
- as_ket
- test_measures.py
- QuantumChannel
- hybrid/runner.py
- reconcile_cascade
- pqc/__init__.py
- api.ts
- ExperimentConfig
- laboratory.py
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- Basis
- WegmanCarterAuthenticationContext
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- test_key_confirmation.py
- constants.py
- P2 — Polish
- PQCProfile
- dm_from_ket
- ._tag
- Adaptive Agents for QKD
- ComparePage.tsx
- runtime.py
- BB84Result
- _new_kem
- HybridPublicContext
- ProtectedSession
- LaboratoryPage.tsx
- test_config.py
- qber_by_basis
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- adapters.py
- ResizeObserverMock
- BB84Protocol
- 3. Análisis Detallado de Hallazgos
- quantum.information Module
- QuantumSec Web UI Architecture
- App.tsx
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
- .from_dict
- quantumsec
- validate_density_matrix
- EXPERIMENTS.md
- SessionConfig
- AuthenticatedQKDSessionResult
- ServerKeyOfferFactory
- Reproducible Experiment Engine V1
- postprocessing/__init__.py
- experiments/__init__.py
- MLDSAIdentity
- oqs_backend.py
- .__exit__
- EstablishedPQCSession
- SessionProfile
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- key_confirmation.py
- 13. Experiments
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- orchestration/__init__.py
- QuantumSec Deployment Guide
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- PQCParty
- QuantumSec Web UI V1
- SessionResult
- .__exit__
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- AuthenticationFrame
- BaseRNG
- 10. Security Model
- export.py
- test_authentication.py
- QuantumSec Conventions Memory
- UnsupportedAlgorithmError
- qkd/transcript.py
- .generate
- analysis/thesis_v1.py
- bb84.py
- KrausChannel
- validation.py
- _prepare_density_matrix
- test_intercept_resend_bb84.py
- .__exit__
- TrustedIdentityStore
- BitFlipChannel
- test_key_schedule.py
- test_api.py
- QuantumSec Web Laboratory redesign
- DepolarizingChannel
- _KEMSharedSecretStateBase
- campaigns/__init__.py
- campaigns/thesis_v1.py
- analysis/__init__.py
- RunWorkspace.tsx
- experiments/config.py
- amplify_privacy
- Thesis Campaign `thesis-v1.0.1`
- schemas.py
- ProtocolTrace.tsx
- .apply
- ChannelPipeline
- d1.py
- _top_level_imports
- BB84PostprocessingConfig
- PQCOperationTimer
- AttackDiagnostics
- benchmark_measurements.py
- ._active_ml_kem
- test_ideal.py
- _ChoiceGenerator
- .apply
- .apply
- test_supported_channels_match_analytical_per_basis_qber

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 129 edges
2. `PQCParty` - 80 edges
3. `SessionConfig` - 64 edges
4. `BB84Protocol` - 63 edges
5. `SignedServerKeyOffer` - 62 edges
6. `PQCProfile` - 53 edges
7. `ExperimentConfig` - 52 edges
8. `SessionProfile` - 51 edges
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

## Communities (157 total, 24 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.08
Nodes (28): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking…, Validate that the input value is a byte string, raising a TypeError if it is…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs. (+20 more)

### Community 1 - "main.py"
Cohesion: 0.14
Nodes (21): get, HealthResponse, post, project_version(), Return the installed project version with a source-tree fallback., compare_runs(), get_run(), health() (+13 more)

### Community 2 - "run_qkd_profile"
Cohesion: 0.21
Nodes (20): Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), _imports_top_level(), parametrize, Path, _session_id(), test_authenticated_ideal_bb84_completes() (+12 more)

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

### Community 7 - "test_client_exchange.py"
Cohesion: 0.20
Nodes (24): _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation., test_bob_decapsulates_but_never_encapsulates(), test_client_canonical_serialization_authenticates_every_field() (+16 more)

### Community 8 - "pqc/errors.py"
Cohesion: 0.05
Nodes (44): OQSKEMBackend, OQSKEMDetails, Adapter isolating the liboqs-python key-encapsulation API., Extract and validate a required metadata field from the liboqs algorithm…, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Query and return validated metadata and buffer dimensions for a KEM algorithm…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, Immutable data structure storing algorithm parameters and buffer dimensions… (+36 more)

### Community 9 - "Revisión final independiente — Fase 7: Motor Experimental Reproducible V1"
Cohesion: 0.04
Nodes (44): 10. Evidencia de validación, 11. Preparación por experimento, 12. Correcciones aplicadas, 13. Conclusión, 1. Dictamen, 2. Alcance inspeccionado, 3. Arquitectura y propiedades verificadas, 4. Tabla de hallazgos (+36 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 12 - "test_measures.py"
Cohesion: 0.08
Nodes (38): Any, Reusable standard projective measurements for QKD protocols., _immutable(), ndarray, Named pure states commonly used by QKD protocols., _born_probabilities(), measure_projective(), MeasurementResult (+30 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.14
Nodes (16): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+8 more)

### Community 14 - "hybrid/runner.py"
Cohesion: 0.08
Nodes (36): AuthenticationOutcome, Exception, _hybrid_public_context_entries(), _pqc_outcome(), _qkd_outcome(), Orchestrate authenticated QKD and raw authenticated PQC contributions., Establish a hybrid key only after both source protocols and hybrid Finished…, run_hybrid_session() (+28 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.08
Nodes (29): CascadeConfig, CascadePassStatistics, CascadePublicEvent, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+21 more)

### Community 16 - "pqc/__init__.py"
Cohesion: 0.05
Nodes (41): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeProcessingStatus, ProcessedClientKeyExchange, StrEnum, Return whether Alice was authenticated and all required KEMs were decapsulated., Bob-side authentication, binding, and decapsulation outcome., Bob-side result containing private KEM output only after successful…, AuthenticatedKEMContributions (+33 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (21): GuidedChannelControls(), GuidedChannelControlsProps, StagePipelineEditor(), StagePipelineEditorProps, AdversaryCapability, AttackDiagnosticsSummary, ChannelCapability, ChannelDraft (+13 more)

### Community 18 - "ExperimentConfig"
Cohesion: 0.16
Nodes (15): ExperimentConfig, One normalized instruction for an experimental session execution., Run ordered configurations sequentially, optionally shuffling reproducibly.…, run_batch(), _qkd_protocol_values(), test_pqc_reproducibility_preserves_method_not_random_artifacts(), test_same_qkd_config_and_seed_reproduce_protocol_outcome(), _hybrid_config() (+7 more)

### Community 19 - "laboratory.py"
Cohesion: 0.11
Nodes (22): AttackDiagnosticsSummary, RunRecord, _attack_diagnostics(), _experiment_config(), CompareResponse, ProtectedMessageResponse, RunListResponse, SessionRunRequest (+14 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.14
Nodes (27): QRNGSimulator, Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG, parametrize, test_base_rng_cannot_be_instantiated() (+19 more)

### Community 22 - "Basis"
Cohesion: 0.05
Nodes (40): Aggregate and per-basis quantum bit error rate metrics., _copy_bb84_bases(), estimate_qber_from_sample(), _explicit_stratified_counts(), ParameterEstimationResult, ArrayLike, ndarray, Sampled QBER estimation with mandatory removal of disclosed key positions. (+32 more)

### Community 23 - "WegmanCarterAuthenticationContext"
Cohesion: 0.09
Nodes (15): AuthenticationSessionRegistry, AuthenticationSessionReplayError, RuntimeError, Raised when a session identifier is reused within persistent authentication…, Thread-safe replay registry that contains identifiers, never authentication…, MLDSAAuthenticationContext, Pre-provisioned bilateral ML-DSA identities and peer trust stores., Self (+7 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (5): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return aggregate full-key QBER as a backwards-compatible alias., Return aggregate sampled QBER as a backwards-compatible alias., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "registry.py"
Cohesion: 0.08
Nodes (24): Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations. (+16 more)

### Community 26 - "client.ts"
Cohesion: 0.16
Nodes (17): compareRuns(), getCapabilities(), getHealth(), protectMessage(), QuantumSecApiError, requestJson(), runBB84Simulation(), runSession() (+9 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.20
Nodes (13): AppView, viewFromHash(), views, viewTitles, AppShell(), AppShellProps, Header(), HeaderProps (+5 more)

### Community 29 - "test_key_confirmation.py"
Cohesion: 0.07
Nodes (48): PQCOperationObserver, validate_operation_observer(), _compute_finished_verify_data(), ConfirmedPQCHandshake, _finished_mac_input(), PQCConfirmationKeyState, PQCKeyConfirmation, Compute one Finished value with the standard-library HMAC-SHA-384 primitive. (+40 more)

### Community 30 - "constants.py"
Cohesion: 0.31
Nodes (6): Project-wide numerical constants with no domain-layer dependencies., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 31 - "P2 — Polish"
Cohesion: 0.05
Nodes (37): 1. Executive assessment, 2. What is already strong (do not redesign), 3. Findings, 4. Cross-page design-system recommendations, 5. Screens and states manually reviewed, 6. Changes selected for implementation, 7. Phase 2 — implementation record, Components (+29 more)

### Community 32 - "PQCProfile"
Cohesion: 0.05
Nodes (49): canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), hqc_3_metadata(), Retrieve HQC-3 metadata for the NIST Round 4 selection exposed by liboqs., ml_kem_768_metadata(), Retrieve and cache standardized ML-KEM-768 (NIST FIPS 203) metadata validated… (+41 more)

### Community 33 - "dm_from_ket"
Cohesion: 0.11
Nodes (24): _immutable_density(), InterceptResendAttack, ArrayLike, ComplexArray, Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., Reset aggregate counters without rewinding the injected RNG stream., Possibly intercept one qubit, then return a fresh transmitted state., Measure selected signals in a random BB84 basis and resend fresh states. The… (+16 more)

### Community 34 - "._tag"
Cohesion: 0.21
Nodes (11): AuthenticationMaterialError, AuthenticationMaterialExhaustedError, AuthenticationMaterialReuseError, _frame_bits(), NDArray, RuntimeError, uint8, Base error for unsafe or unavailable authentication material. (+3 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "ComparePage.tsx"
Cohesion: 0.19
Nodes (12): SessionMetricsView(), SessionMetricsViewProps, formatBytes(), formatDurationNs(), formatPercent(), authLabel(), ComparePage(), ComparePageProps (+4 more)

### Community 37 - "runtime.py"
Cohesion: 0.11
Nodes (15): ExperimentRunner, Execute one configuration and retain only copied public evidence., ExperimentRuntime, ExperimentRuntimeFactory, PQCIdentityProvisioning, Runtime-only provisioning for experiment configurations., Create per-run contexts while retaining persistent laboratory identities. ML-…, Provision and time persistent campaign identities exactly once. (+7 more)

### Community 38 - "BB84Result"
Cohesion: 0.07
Nodes (18): _optional_probability(), QBERByBasis, Immutable aggregate and BB84 basis-conditioned error metrics., BB84Result, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention. (+10 more)

### Community 39 - "_new_kem"
Cohesion: 0.07
Nodes (22): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _new_kem(), _OQSKEM, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule (+14 more)

### Community 40 - "HybridPublicContext"
Cohesion: 0.11
Nodes (16): HybridPublicContext, create_finished(), HybridFinishedMessage, HybridFinishedRole, _mac_input(), StrEnum, Versioned, role-separated HMAC-SHA-384 Finished exchange for hybrid keys., verify_finished() (+8 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "LaboratoryPage.tsx"
Cohesion: 0.14
Nodes (25): CompositionSummary(), CompositionSummaryProps, familyMeta, ProfileSelector(), ProfileSelectorProps, LaboratoryMode, QKDControls(), QKDControlsProps (+17 more)

### Community 43 - "test_config.py"
Cohesion: 0.12
Nodes (20): build_channel_pipeline(), build_channel_stage(), _optional_number(), StrEnum, QKDChannelStageSpec, QKDChannelStageType, Public, Pydantic-free specifications for reproducible QKD channel pipelines., Build one domain channel from a validated neutral stage specification. (+12 more)

### Community 44 - "qber_by_basis"
Cohesion: 0.23
Nodes (14): ArrayLike, ndarray, qber(), qber_by_basis(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, Return Z, X, and aggregate QBER without inventing absent-basis values., parametrize, test_qber_by_basis_marks_an_absent_basis_as_undefined() (+6 more)

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

### Community 50 - "adapters.py"
Cohesion: 0.15
Nodes (21): _bb84_basis_value(), _channel_summary(), BB84SimulationRequest, BB84SimulationResponse, Adapters between typed HTTP data and the QuantumSec simulation domain., Narrow the general QKD Basis enum to BB84's two supported bases., Execute BB84 with the engine's seeded RNG and adapt its immutable result., run_bb84() (+13 more)

### Community 52 - "BB84Protocol"
Cohesion: 0.16
Nodes (24): IdentityChannel, Channel that returns an independent copy of the input state., BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, _InvalidOutputChannel, parametrize, test_bb84_accepts_existing_noisy_quantum_channel_without_statistical_exactness(), test_bb84_encoding_convention_returns_expected_density_matrix() (+16 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 56 - "App.tsx"
Cohesion: 0.18
Nodes (14): getRuns(), App(), useRuns(), requestFromRecord(), root, LaboratoryPageProps, familyLabels, OverviewPage() (+6 more)

### Community 70 - "capabilities.py"
Cohesion: 0.15
Nodes (20): Return all executable profiles in stable public-enum order., session_capabilities(), ParameterCapability, ProfileCapability, test_all_seven_public_capabilities_are_current_and_stably_ordered(), get_capabilities(), _probability(), _profile_capability() (+12 more)

### Community 71 - ".from_dict"
Cohesion: 0.17
Nodes (14): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+6 more)

### Community 73 - "validate_density_matrix"
Cohesion: 0.15
Nodes (25): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+17 more)

### Community 74 - "EXPERIMENTS.md"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "SessionConfig"
Cohesion: 0.12
Nodes (39): Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., Dispatch a normalized session config to its domain-specific adapter., run_session() (+31 more)

### Community 79 - "AuthenticatedQKDSessionResult"
Cohesion: 0.21
Nodes (7): AuthenticatedQKDSessionResult, _optional_key_copy(), NDArray, uint8, Terminal QKD decision; key fields exist only after all required checks pass., Return defensive immutable copies only for an accepted session., Serialize bounded public metadata, never transcript payloads or key material.

### Community 80 - "ServerKeyOfferFactory"
Cohesion: 0.09
Nodes (29): OfferCreation, Self, Enter a managed lifetime for this ephemeral responder state., Return a safe string representation showing profile and closed status., Factory creating responder ephemeral KEM states and authenticated…, Maintains ephemeral private KEM key pairs for an active handshake responder…, Validate session ID length, profile compatibility, and presence of required KEM…, Return the public HQC encapsulation key if the session uses the HIGH profile,… (+21 more)

### Community 81 - "Reproducible Experiment Engine V1"
Cohesion: 0.25
Nodes (8): Batch and statistics, CLI, Configuration, Definitive campaign, Environment and record schema, Metrics and exports, Reproducible Experiment Engine V1, Runtime and secret lifecycle

### Community 82 - "postprocessing/__init__.py"
Cohesion: 0.07
Nodes (40): Classical QKD post-processing algorithms and immutable transcripts., PrivacyAmplificationResult, Toeplitz-universal privacy amplification for reconciled QKD keys., Immutable final keys and public Toeplitz seed metadata., Deterministic basis reconciliation for QKD raw keys., generate_toeplitz_seed(), ArrayLike, NDArray (+32 more)

### Community 83 - "experiments/__init__.py"
Cohesion: 0.09
Nodes (19): _distribution_version(), ExperimentEnvironment, _git_state(), _quantumsec_version(), Best-effort environment snapshots that contextualize experimental evidence., Reproducible, secret-free experimental execution for QuantumSec., BatchProvenance, ExperimentRecord (+11 more)

### Community 84 - "MLDSAIdentity"
Cohesion: 0.08
Nodes (24): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without… (+16 more)

### Community 85 - "oqs_backend.py"
Cohesion: 0.07
Nodes (28): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), oqs_runtime_versions(), OQSKeyPair, _OQSModule, OQSRuntimeVersions, _OQSSignature (+20 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "EstablishedPQCSession"
Cohesion: 0.13
Nodes (8): EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key., Enter a managed lifetime for this established local session.

### Community 88 - "SessionProfile"
Cohesion: 0.15
Nodes (27): canonical_hybrid_secret_input(), _expected_algorithms(), hybrid_component_metadata_bytes(), hybrid_kem_label(), HybridSecretComponent, Unambiguous encoding of independently established QKD and KEM contributions., Return encoded bytes attributable to one component's non-secret…, Return the canonical hybrid label for a supported KEM algorithm. (+19 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "key_confirmation.py"
Cohesion: 0.05
Nodes (42): Runtime-only accumulation of exact PQC operation timings., _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes() (+34 more)

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

### Community 100 - "orchestration/__init__.py"
Cohesion: 0.09
Nodes (27): Enum, Versioned public configuration for common QuantumSec session execution., Runtime-only capabilities kept separate from reproducible public configuration., Establishment-to-data-plane adapter with explicit session-key ownership…, Upper-layer composition of independent QKD and PQC domain modules., CapabilityStatus, EstablishmentSource, StrEnum (+19 more)

### Community 101 - "QuantumSec Deployment Guide"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 102 - "BB84 security model"
Cohesion: 0.14
Nodes (13): AES-256-GCM data plane, Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Hybrid session composition, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication (+5 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "PQCParty"
Cohesion: 0.06
Nodes (59): Reusable execution of the existing mutually authenticated PQC phases 2--4., PQCOperationObserver, Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., Verify Alice's response and only then recover Bob's matching KEM secrets., InitiatorKEMState, ProcessedServerOffer, PQCOperationObserver, Authenticate Bob's offer before producing Alice's KEM encapsulations. (+51 more)

### Community 105 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 106 - "SessionResult"
Cohesion: 0.09
Nodes (7): _authentication_dict(), EstablishedKeyCapability, Self, Return whether this result no longer exposes live key material., Export accepted key bytes; QKD exact bit length remains in result metadata., Private export boundary for accepted key bytes with exact bit-length metadata., SessionResult

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release references to ephemeral private KEM instances to prevent subsequent…, Release the private KEM capabilities when leaving a managed lifetime.

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "AuthenticationFrame"
Cohesion: 0.10
Nodes (29): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationEvidence, AuthenticationFrame, AuthenticationMetrics, AuthenticationState, AuthenticationVerification, AuthenticatorMetadata (+21 more)

### Community 111 - "BaseRNG"
Cohesion: 0.10
Nodes (21): BaseRNG, GlobalRNG, ABC, ndarray, random_basis(), random_bit(), random_unitary(), Injectable random-number sources for reproducible simulations. (+13 more)

### Community 112 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 113 - "export.py"
Cohesion: 0.18
Nodes (23): ArgumentParser, main(), _parser(), Minimal command-line interface for reproducible QuantumSec runs., _canonical_cell(), _csv_value(), dumps_csv(), dumps_json() (+15 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.15
Nodes (20): PreSharedAuthenticationMaterial, Consumable PSK bit stream whose contents are never exposed or serialized., _frame(), _ml_dsa_authenticator(), parametrize, test_ml_dsa_rejects_missing_signature(), test_ml_dsa_rejects_modified_or_cross_context_frame(), test_ml_dsa_rejects_modified_signature() (+12 more)

### Community 115 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 116 - "UnsupportedAlgorithmError"
Cohesion: 0.09
Nodes (23): Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-… (+15 more)

### Community 117 - "qkd/transcript.py"
Cohesion: 0.08
Nodes (30): AuthenticationContext, Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), Authenticated public context binding every hybrid session input. (+22 more)

### Community 119 - "analysis/thesis_v1.py"
Cohesion: 0.06
Nodes (78): generate_all(), _number(), _numbers(), _plot_e1(), _plot_e2(), _plot_e3(), _plot_e4(), _plot_e5() (+70 more)

### Community 120 - "bb84.py"
Cohesion: 0.22
Nodes (11): _copy_bb84_bases(), encode_bb84_state(), ArrayLike, ComplexArray, Reproducible prepare-and-measure simulation of the BB84 protocol., Build an immutable density matrix for a validated named BB84 state., Return an independent density matrix for one BB84 bit/basis symbol. The…, _trusted_density_matrix() (+3 more)

### Community 121 - "KrausChannel"
Cohesion: 0.16
Nodes (12): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, A completely positive trace-preserving map validated at construction., Return the Hilbert-space dimension acted on by the channel., parametrize, test_kraus_channel_applies_operator_sum_without_mutating_input(), test_kraus_channel_rejects_invalid_operator_sets() (+4 more)

### Community 122 - "validation.py"
Cohesion: 0.09
Nodes (48): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+40 more)

### Community 123 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 124 - "test_intercept_resend_bb84.py"
Cohesion: 0.18
Nodes (11): BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., A basis average must not authorize extraction on an asymmetric channel., test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error(), parametrize, _run_with_eve(), test_attack_and_noise_pipeline_is_reproducible_end_to_end() (+3 more)

### Community 125 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 126 - "TrustedIdentityStore"
Cohesion: 0.07
Nodes (28): Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PublicIdentity, Immutable public verification identity associating an owner name with public…, Serialize this public identity into a JSON-compatible dictionary with…, Return this party's public identity for distribution and registration in peer… (+20 more)

### Community 127 - "BitFlipChannel"
Cohesion: 0.12
Nodes (14): BitFlipChannel, PauliChannel, PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability. (+6 more)

### Community 128 - "test_key_schedule.py"
Cohesion: 0.10
Nodes (43): ClientKeyExchangeFactory, ClientKeyExchangeProcessor, Package and sign Alice's already-created Phase 3 public encapsulation response., Authenticate Alice and validate session binding before Bob decapsulates., PQCSessionKeyDeriver, Derive the same key for either role using one shared transcript-bound schedule., Self, Construct and validate a transcript from the two authenticated wire messages. (+35 more)

### Community 129 - "test_api.py"
Cohesion: 0.11
Nodes (4): parametrize, test_backend_gives_protocol_and_each_eve_stage_independent_rng_streams(), test_intercept_resend_configuration_rejects_invalid_fraction(), test_session_api_executes_every_current_public_profile()

### Community 130 - "QuantumSec Web Laboratory redesign"
Cohesion: 0.22
Nodes (8): Backend/API changes, Current-state audit, Event and data flow, Explicit non-goals, Implementation phases, Information architecture, QuantumSec Web Laboratory redesign, Retained and replaced

### Community 131 - "DepolarizingChannel"
Cohesion: 0.15
Nodes (21): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, DepolarizingChannel, ArrayLike, ComplexArray, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, Apply depolarizing noise to a single-qubit density matrix., assert_valid_qubit_density_matrix() (+13 more)

### Community 132 - "_KEMSharedSecretStateBase"
Cohesion: 0.12
Nodes (11): _KEMSharedSecretStateBase, BaseException, Self, TracebackType, Release secret references when leaving a managed lifetime., Internal validated storage shared by initiator and responder secret states., Return whether the private shared-secret references were released., Release secret references idempotently without claiming memory zeroization. (+3 more)

### Community 134 - "campaigns/thesis_v1.py"
Cohesion: 0.15
Nodes (27): raw_hashes(), validate_manifest_hashes(), build_campaign_plan(), CampaignPlan, CampaignPreset, _config(), _e2_conditions(), _e5_config() (+19 more)

### Community 136 - "RunWorkspace.tsx"
Cohesion: 0.23
Nodes (9): OUTCOME_HEADINGS, RunWorkspace(), RunWorkspaceProps, run, SecurityEvidence(), SecurityEvidenceProps, AuthenticationOutcome, SecretProvenance (+1 more)

### Community 137 - "experiments/config.py"
Cohesion: 0.25
Nodes (12): _invalid_stage(), _number(), _optional_integer(), _postprocessing_from_public_dict(), Strict, versioned, secret-free experiment configuration., _reject_unknown(), _session_from_public_dict(), config_from_json() (+4 more)

### Community 138 - "amplify_privacy"
Cohesion: 0.15
Nodes (16): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., ArrayLike, Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, verify_reconciled_keys(), Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, parametrize (+8 more)

### Community 139 - "Thesis Campaign `thesis-v1.0.1`"
Cohesion: 0.40
Nodes (4): Interpretation boundary, Reproduction, Status, Thesis Campaign `thesis-v1.0.1`

### Community 140 - "schemas.py"
Cohesion: 0.17
Nodes (16): BaseModel, model_validator, AmplitudeDampingChannelConfiguration, ApiError, BitFlipChannelConfiguration, CompareRequest, DepolarizingChannelConfiguration, IdentityChannelConfiguration (+8 more)

### Community 141 - "ProtocolTrace.tsx"
Cohesion: 0.30
Nodes (8): EventTone, ProtocolTrace(), ProtocolTraceProps, CANONICAL_TOKENS, formatIdentifier(), formatSource(), formatToken(), SessionTraceEvent

### Community 142 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 143 - "ChannelPipeline"
Cohesion: 0.31
Nodes (9): ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels(), test_pipeline_copies_channel_collection_and_does_not_mutate_input(), test_pipeline_matches_manual_sequential_application(), test_pipeline_rejects_non_channel_components() (+1 more)

### Community 144 - "d1.py"
Cohesion: 0.29
Nodes (7): D1Record, _expect_invalid_tag(), _flip_first(), Secret-free executable D1 protected-session demonstration., Establish HYBRID-DIVERSE, transfer its key, and test AES-GCM rejection., run_d1(), TamperOutcome

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

### Community 146 - "BB84PostprocessingConfig"
Cohesion: 0.29
Nodes (5): BB84PostprocessingConfig, Configuration for BB84 post-processing under assumed channel authentication.…, test_postprocessing_config_accepts_the_canonical_phase_error_threshold_name(), test_postprocessing_config_preserves_the_legacy_qber_threshold_name(), test_postprocessing_config_rejects_conflicting_non_default_threshold_names()

### Community 147 - "PQCOperationTimer"
Cohesion: 0.29
Nodes (4): PQCOperationTimer, PQCOperationTimings, Accumulate successful direct timings without observing secret values., test_e1_operation_timer_accumulates_only_direct_observations()

### Community 148 - "AttackDiagnostics"
Cohesion: 0.29
Nodes (4): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, Return an immutable simulator-only snapshot of cumulative counters., Small immutable snapshot of simulator-only attack observations.

### Community 149 - "benchmark_measurements.py"
Cohesion: 0.47
Nodes (5): _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark()

### Community 150 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

### Community 151 - "test_ideal.py"
Cohesion: 0.60
Nodes (4): parametrize, test_identity_keeps_cheap_checks_when_full_validation_is_disabled(), test_identity_preserves_pure_and_mixed_states_without_aliasing(), test_identity_rejects_nonphysical_density_matrices_by_default()

### Community 153 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

## Knowledge Gaps
- **376 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+371 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1338 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868)
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `dm_from_ket`, `run_qkd_profile`, `test_api.py`, `runtime.py`, `amplify_privacy`, `test_config.py`, `SessionConfig`, `test_measures.py`, `BaseRNG`, `reconcile_cascade`, `postprocessing/__init__.py`, `adapters.py`, `BB84Protocol`, `benchmark_measurements.py`, `Basis`, `test_supported_channels_match_analytical_per_basis_qber`, `test_intercept_resend_bb84.py`, `BitFlipChannel`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `test_key_schedule.py`, `orchestration/__init__.py`, `runtime.py`, `test_client_exchange.py`, `SessionConfig`, `pqc/__init__.py`, `ServerKeyOfferFactory`, `MLDSAIdentity`, `test_key_confirmation.py`, `TrustedIdentityStore`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `QuantumSec TFM Goal` connect `QuantumSec TFM Goal` to `10. Security Model`, `EXPERIMENTS.md`, `13. Experiments`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `SeededRNG` (e.g. with `ExperimentRuntimeFactory` and `build_channel_pipeline()`) actually correct?**
  _`SeededRNG` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SessionConfig` (e.g. with `QKDProfile` and `SessionProfile`) actually correct?**
  _`SessionConfig` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._