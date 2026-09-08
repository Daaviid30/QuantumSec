# Graph Report - QuantumSec  (2026-09-08)

## Corpus Check
- 289 files · ~122,112 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2988 nodes · 7118 edges · 143 communities (109 shown, 29 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 305 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cf51da1b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- adapters.py
- BB84Protocol
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- test_client_exchange.py
- BackendOperationError
- Revisión final independiente — Fase 7: Motor Experimental Reproducible V1
- compilerOptions
- ResultsWorkspace.tsx
- dm_from_ket
- QuantumChannel
- hybrid/runner.py
- reconcile_cascade
- PQCConfirmationKeyState
- api.ts
- InterceptResendAttack
- SessionResult
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- estimate_qber_from_sample
- information.py
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- test_key_confirmation.py
- ConfirmedPQCHandshake
- SimulationConfigurator.tsx
- test_key_schedule.py
- ChannelPipeline
- authentication/__init__.py
- Adaptive Agents for QKD
- _integer
- bb84.py
- BB84Result
- _OQSKEM
- run_hybrid_session
- ProtectedSession
- SimulatorPage.tsx
- PQCProfile
- qber_by_basis
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- AuthenticationFrame
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
- OQSSignatureBackend
- _require_bytes
- quantumsec
- HybridDerivedKeys
- QuantumSec Project Overview & README
- SessionConfig
- AuthenticatedQKDSessionResult
- QuantumSec Conventions Memory
- BB84SessionStatus
- postprocessing/__init__.py
- ExperimentRecord
- pqc/errors.py
- _OQSSignature
- .__exit__
- EstablishedPQCSession
- test_hybrid_primitives.py
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- _ChoiceGenerator
- 13. Experiments
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- _metadata_for_algorithm
- QuantumSec Deployment Guide
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- PQCParty
- QuantumSec Web UI V1
- orchestration/__init__.py
- .__exit__
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- authentication/base.py
- SessionProfile
- 10. Security Model
- export.py
- test_authentication.py
- .apply
- test_kem_private_material_is_not_exposed
- qkd/transcript.py
- .generate
- experiments/__init__.py
- KrausChannel
- validation.py
- .generate
- _imports_top_level
- .verify
- protocol/__init__.py
- .apply
- .__post_init__
- test_api.py
- .sign
- DepolarizingChannel
- .verify
- .metadata
- EXPERIMENTS.md
- test_states.py
- _RegisteredSignature
- experiments/config.py
- rng.py
- SignedServerKeyOffer
- test_full_six_phase_handshake_crosses_pure_json_transport
- _top_level_imports

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 129 edges
2. `PQCParty` - 80 edges
3. `BB84Protocol` - 63 edges
4. `SignedServerKeyOffer` - 62 edges
5. `SessionConfig` - 60 edges
6. `PQCProfile` - 53 edges
7. `IdentityChannel` - 45 edges
8. `ExperimentConfig` - 43 edges
9. `run_hybrid_session()` - 42 edges
10. `dm_from_ket()` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Graphify Knowledge Graph Integration Rules` --semantically_similar_to--> `Graphify Knowledge Graph Guidelines`  [INFERRED] [semantically similar]
  AGENTS.md → .agents/rules/graphify.md
- `BB84 Classical Post-Processing Pipeline Spec` --semantically_similar_to--> `BB84 Session Simulation Flow`  [INFERRED] [semantically similar]
  docs/structure.md → README.md
- `Core Design Principles and Boundary Rules` --semantically_similar_to--> `QuantumSec Project Scope & Invariants`  [INFERRED] [semantically similar]
  docs/structure.md → .serena/memories/core.md
- `RNG Architecture Design Principles` --semantically_similar_to--> `Injected RNG Convention`  [INFERRED] [semantically similar]
  core/docs/rng_man.md → .serena/memories/conventions.md
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

## Communities (143 total, 29 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

### Community 1 - "adapters.py"
Cohesion: 0.07
Nodes (62): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+54 more)

### Community 2 - "BB84Protocol"
Cohesion: 0.08
Nodes (53): AuthenticationContext, AuthenticationTransportHook, Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig (+45 more)

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
Cohesion: 0.23
Nodes (14): asymptotic_bb84_secret_length(), binary_entropy(), _non_negative_int(), _probability(), Stateless security-length metrics for the current asymptotic BB84 model., Return binary Shannon entropy ``h2(p)`` with exact endpoint handling., Estimate extractable bits from an explicit asymptotic phase-error bound. The…, parametrize (+6 more)

### Community 7 - "test_client_exchange.py"
Cohesion: 0.15
Nodes (30): ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., InitiatorKEMState, Alice-local KEM secrets created only after authenticating the responder. Raw-…, _create_flow(), _Phase4Flow, _prepare_phase3(), _private_initiator_state() (+22 more)

### Community 8 - "BackendOperationError"
Cohesion: 0.04
Nodes (70): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, Adapter isolating the liboqs-python key-encapsulation API. (+62 more)

### Community 9 - "Revisión final independiente — Fase 7: Motor Experimental Reproducible V1"
Cohesion: 0.04
Nodes (44): 10. Evidencia de validación, 11. Preparación por experimento, 12. Correcciones aplicadas, 13. Conclusión, 1. Dictamen, 2. Alcance inspeccionado, 3. Arquitectura y propiedades verificadas, 4. Tabla de hallazgos (+36 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.06
Nodes (51): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., BaseRNG (+43 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.08
Nodes (36): _prepare_density_matrix(), ABC, ArrayLike, ComplexArray, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, Apply the channel to a density matrix. (+28 more)

### Community 14 - "hybrid/runner.py"
Cohesion: 0.08
Nodes (38): Enum, Runtime-only capabilities kept separate from reproducible public configuration., Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, _hybrid_public_context_entries(), _pqc_outcome(), _qkd_outcome(), Orchestrate authenticated QKD and raw authenticated PQC contributions. (+30 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.08
Nodes (29): CascadeConfig, CascadePassStatistics, CascadePublicEvent, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+21 more)

### Community 16 - "PQCConfirmationKeyState"
Cohesion: 0.10
Nodes (10): PQCConfirmationKeyState, Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released., Return whether this state has released its role-local confirmation key., Return whether this role completed its local send/verify Finished work., Release the confirmation-key reference without closing the session key., PQCFinishedMessage, Immutable public transport message carrying one role-bound Finished MAC. (+2 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "InterceptResendAttack"
Cohesion: 0.12
Nodes (18): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, InterceptResendAttack, Return an immutable simulator-only snapshot of cumulative counters., Reset aggregate counters without rewinding the injected RNG stream., Small immutable snapshot of simulator-only attack observations., Measure selected signals in a random BB84 basis and resend fresh states. The…, Validate Hermiticity, unit trace, and positive semidefiniteness. (+10 more)

### Community 19 - "SessionResult"
Cohesion: 0.07
Nodes (12): Establishment-to-data-plane adapter with explicit session-key ownership…, _authentication_dict(), EstablishedKeyCapability, EstablishedKeyType, Self, StrEnum, Return whether this result no longer exposes live key material., Export accepted key bytes; QKD exact bit length remains in result metadata. (+4 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.13
Nodes (29): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+21 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.10
Nodes (20): _copy_bb84_bases(), estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the… (+12 more)

### Community 23 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (12): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+4 more)

### Community 25 - "registry.py"
Cohesion: 0.18
Nodes (13): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., Return the immutable public verification key bytes., SignatureMetadata, SignatureProvider (+5 more)

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
Cohesion: 0.19
Nodes (25): Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., _derive_confirmation_states(), _exchange_finished(), _flipped(), _Phase6States, parametrize, Tests for Phase 6 role-separated Finished key confirmation. (+17 more)

### Community 30 - "ConfirmedPQCHandshake"
Cohesion: 0.14
Nodes (9): ConfirmedPQCHandshake, PQCKeyConfirmation, Self, Enter a managed lifetime for this private confirmation-key state., Capability produced only after both role-separated Finished MACs verify., Enter a managed lifetime for this established local session., Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Verify Alice's chained Finished and produce mutual-confirmation proof. (+1 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "test_key_schedule.py"
Cohesion: 0.05
Nodes (63): _length_prefixed(), Prefix bytes with an unsigned 32-bit big-endian length., derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), Canonical KEM input construction and HKDF primitives for QuantumSec. (+55 more)

### Community 33 - "ChannelPipeline"
Cohesion: 0.14
Nodes (20): BitFlipChannel, Single-qubit channel that applies Pauli X with probability ``p``., ChannelPipeline, ArrayLike, ComplexArray, Apply an immutable sequence of channels in order. An empty pipeline is defined…, Apply each component from first to last without mutating the input., test_empty_pipeline_is_an_identity_without_aliasing_input() (+12 more)

### Community 34 - "authentication/__init__.py"
Cohesion: 0.12
Nodes (23): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationMetrics, AuthenticationState, ClassicalAuthenticationResult, StrEnum, authenticate_transcript_checkpoints(), AuthenticationTransportHook (+15 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "_integer"
Cohesion: 0.12
Nodes (17): ndarray, random_basis(), random_bit(), Generate binary choices using this simulator's bias/correlation model., Generate one or more uniformly distributed classical bits., Generate generic binary choices for adaptation by the QKD layer., Generate binary choices, allowing specialized RNGs to override their model., Generate raw bits with the configured bias and temporal correlation. (+9 more)

### Community 37 - "bb84.py"
Cohesion: 0.10
Nodes (26): Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., Map the QKD random-bit convention 0/1 to the Z/X basis. (+18 more)

### Community 38 - "BB84Result"
Cohesion: 0.11
Nodes (8): BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return aggregate simulator-diagnostic QBER over the complete sifted key. This…, Return simulator-only Z, X, and aggregate full-sifted QBER., Immutable raw and sifted material produced by one complete BB84 run.

### Community 39 - "_OQSKEM"
Cohesion: 0.12
Nodes (10): _KEMFactory, _OQSKEM, _OQSModule, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager. (+2 more)

### Community 40 - "run_hybrid_session"
Cohesion: 0.29
Nodes (10): create_finished(), HybridFinishedMessage, HybridFinishedRole, _mac_input(), StrEnum, Versioned, role-separated HMAC-SHA-384 Finished exchange for hybrid keys., verify_finished(), Establish a hybrid key only after both source protocols and hybrid Finished… (+2 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "PQCProfile"
Cohesion: 0.05
Nodes (57): Internal canonical binary encoding primitives shared across PQC domains., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), hqc_3_metadata(), Retrieve HQC-3 metadata for the NIST Round 4 selection exposed by liboqs., ml_kem_768_metadata() (+49 more)

### Community 44 - "qber_by_basis"
Cohesion: 0.15
Nodes (19): QKD metric computations., _optional_probability(), ArrayLike, ndarray, qber(), qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics. (+11 more)

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

### Community 50 - "AuthenticationFrame"
Cohesion: 0.14
Nodes (10): AuthenticationFrame, Canonical authentication unit binding payload to anti-replay context., _frame_bits(), NDArray, uint8, Authenticate one direction with fresh Toeplitz-selector and mask bits., Bilateral, direction-separated PSK material for one or more QKD sessions., Atomically reserve fresh bits for one unique authenticated frame context. (+2 more)

### Community 52 - "ExperimentConfig"
Cohesion: 0.08
Nodes (33): ExperimentConfig, _invalid_stage(), One normalized instruction for an experimental session execution., config_from_json(), configs_from_json(), load_config_json(), _loads_without_duplicate_keys(), StrEnum (+25 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "OQSSignatureBackend"
Cohesion: 0.20
Nodes (8): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend., test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 71 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

### Community 74 - "QuantumSec Project Overview & README"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "SessionConfig"
Cohesion: 0.16
Nodes (28): Self, Provision matching but independent copies for each communication direction., Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Dispatch a normalized session config to its domain-specific adapter., run_session(), test_wegman_carter_context_enforces_directional_key_separation(), _context() (+20 more)

### Community 79 - "AuthenticatedQKDSessionResult"
Cohesion: 0.21
Nodes (7): AuthenticatedQKDSessionResult, _optional_key_copy(), NDArray, uint8, Return defensive immutable copies only for an accepted session., Serialize bounded public metadata, never transcript payloads or key material., Terminal QKD decision; key fields exist only after all required checks pass.

### Community 80 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 81 - "BB84SessionStatus"
Cohesion: 0.33
Nodes (5): BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., A basis average must not authorize extraction on an asymmetric channel., test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error()

### Community 82 - "postprocessing/__init__.py"
Cohesion: 0.07
Nodes (40): Classical QKD post-processing algorithms and immutable transcripts., Sampled QBER estimation with mandatory removal of disclosed key positions., PrivacyAmplificationResult, Toeplitz-universal privacy amplification for reconciled QKD keys., Immutable final keys and public Toeplitz seed metadata., generate_toeplitz_seed(), ArrayLike, NDArray (+32 more)

### Community 83 - "ExperimentRecord"
Cohesion: 0.10
Nodes (15): ExperimentKind, StrEnum, BatchProvenance, ExperimentRecord, _freeze(), _freeze_mapping(), Immutable, versioned public evidence produced by one experiment run., Copy public evidence before the caller closes the live session capability. (+7 more)

### Community 84 - "pqc/errors.py"
Cohesion: 0.05
Nodes (44): Exception, _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, Adapter isolating the liboqs-python signature API., Initialize and return a new liboqs signature instance for the specified…, Generate a fresh key pair for the specified signature algorithm using liboqs. (+36 more)

### Community 85 - "_OQSSignature"
Cohesion: 0.11
Nodes (10): _OQSModule, _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable. (+2 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "EstablishedPQCSession"
Cohesion: 0.13
Nodes (10): EstablishedPQCSession, BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key. (+2 more)

### Community 88 - "test_hybrid_primitives.py"
Cohesion: 0.11
Nodes (34): HybridPublicContext, Authenticated public context binding every hybrid session input., canonical_hybrid_secret_input(), _expected_algorithms(), hybrid_component_metadata_bytes(), hybrid_kem_label(), HybridSecretComponent, Unambiguous encoding of independently established QKD and KEM contributions. (+26 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

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

### Community 100 - "_metadata_for_algorithm"
Cohesion: 0.50
Nodes (3): Validate owner, algorithm, and public key buffer dimensions, storing an…, _metadata_for_algorithm(), Look up algorithm metadata from the registry, or return None if unsupported.

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
Cohesion: 0.04
Nodes (71): OfferCreation, Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PublicIdentity, Private and public identities for PQC authentication., Immutable public verification identity associating an owner name with public… (+63 more)

### Community 105 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 106 - "orchestration/__init__.py"
Cohesion: 0.15
Nodes (15): Versioned public configuration for common QuantumSec session execution., Upper-layer composition of independent QKD and PQC domain modules., CapabilityStatus, EstablishmentSource, StrEnum, qkd_profile_definition(), QKDProfile, QKDProfileDefinition (+7 more)

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "authentication/base.py"
Cohesion: 0.11
Nodes (18): AuthenticationEvidence, AuthenticationSessionRegistry, AuthenticationSessionReplayError, AuthenticationVerification, AuthenticatorMetadata, DirectionalAuthenticator, ABC, RuntimeError (+10 more)

### Community 111 - "SessionProfile"
Cohesion: 0.20
Nodes (14): MLDSAAuthenticationContext, Pre-provisioned bilateral ML-DSA identities and peer trust stores., open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., SessionProfile, _establish(), _parties(), parametrize (+6 more)

### Community 112 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 113 - "export.py"
Cohesion: 0.11
Nodes (31): ArgumentParser, main(), _parser(), Minimal command-line interface for reproducible QuantumSec runs., _canonical_cell(), _csv_value(), dumps_csv(), dumps_json() (+23 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.15
Nodes (20): PreSharedAuthenticationMaterial, Consumable PSK bit stream whose contents are never exposed or serialized., _frame(), _ml_dsa_authenticator(), parametrize, test_ml_dsa_rejects_missing_signature(), test_ml_dsa_rejects_modified_or_cross_context_frame(), test_ml_dsa_rejects_modified_signature() (+12 more)

### Community 115 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 116 - "test_kem_private_material_is_not_exposed"
Cohesion: 0.67
Nodes (4): FixtureRequest, parametrize, test_kem_private_material_is_not_exposed(), test_modified_ciphertext_does_not_recover_original_secret()

### Community 117 - "qkd/transcript.py"
Cohesion: 0.08
Nodes (30): Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), QKD session orchestration and canonical public transcript contracts., StrEnum (+22 more)

### Community 119 - "experiments/__init__.py"
Cohesion: 0.20
Nodes (16): Reproducible, secret-free experimental execution for QuantumSec., median_iqr(), Small statistical summaries required by the first experiment campaigns., Summarize finite values with NumPy's linear percentile convention., Return the two-sided Wilson score interval (not Clopper-Pearson exact)., TimingSummary, wilson_interval(), WilsonInterval (+8 more)

### Community 120 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 122 - "validation.py"
Cohesion: 0.05
Nodes (78): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+70 more)

### Community 124 - "_imports_top_level"
Cohesion: 1.00
Nodes (3): _imports_top_level(), Path, test_qkd_and_pqc_remain_independent_sibling_domains()

### Community 126 - "protocol/__init__.py"
Cohesion: 0.03
Nodes (66): Reusable execution of the existing mutually authenticated PQC phases 2--4., Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, ProcessedClientKeyExchange, StrEnum, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets. (+58 more)

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 129 - "test_api.py"
Cohesion: 0.13
Nodes (3): parametrize, test_backend_gives_protocol_and_each_eve_stage_independent_rng_streams(), test_intercept_resend_configuration_rejects_invalid_fraction()

### Community 131 - "DepolarizingChannel"
Cohesion: 0.10
Nodes (27): AmplitudeDampingChannel, ArrayLike, ComplexArray, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, Apply amplitude damping to a single-qubit density matrix., DepolarizingChannel, ArrayLike, ComplexArray (+19 more)

### Community 134 - "EXPERIMENTS.md"
Cohesion: 0.12
Nodes (16): Batch and statistics, CLI, Configuration, Environment and record schema, Metrics and exports, Reproducible Experiment Engine V1, Runtime and secret lifecycle, _distribution_version() (+8 more)

### Community 135 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 137 - "experiments/config.py"
Cohesion: 0.57
Nodes (6): _number(), _optional_integer(), _postprocessing_from_public_dict(), Strict, versioned, secret-free experiment configuration., _reject_unknown(), _session_from_public_dict()

### Community 138 - "rng.py"
Cohesion: 0.10
Nodes (22): GlobalRNG, ABC, Injectable random-number sources for reproducible simulations., Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length. (+14 more)

### Community 139 - "SignedServerKeyOffer"
Cohesion: 0.09
Nodes (35): Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ProcessedServerOffer, StrEnum, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Authentication outcome produced before any Alice-side response is sent., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed. (+27 more)

### Community 142 - "test_full_six_phase_handshake_crosses_pure_json_transport"
Cohesion: 0.14
Nodes (18): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+10 more)

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

## Knowledge Gaps
- **328 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+323 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1237 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `ChannelPipeline`, `BB84Protocol`, `DepolarizingChannel`, `test_api.py`, `adapters.py`, `rng.py`, `SessionConfig`, `dm_from_ket`, `QuantumChannel`, `SessionProfile`, `reconcile_cascade`, `export.py`, `BB84SessionStatus`, `InterceptResendAttack`, `ExperimentConfig`, `postprocessing/__init__.py`, `estimate_qber_from_sample`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `SessionConfig` connect `SessionConfig` to `BB84Protocol`, `EXPERIMENTS.md`, `run_hybrid_session`, `experiments/config.py`, `orchestration/__init__.py`, `hybrid/runner.py`, `SessionProfile`, `export.py`, `ExperimentConfig`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `QuantumSec Project Structure and Architectural Blueprint` connect `QuantumSec Project Overview & README` to `QuantumSec Conventions Memory`, `QuantumSec Serena Root Memory`, `EXPERIMENTS.md`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `SeededRNG` (e.g. with `ExperimentRuntimeFactory` and `build_channel_pipeline()`) actually correct?**
  _`SeededRNG` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 11 INFERRED edges - model-reasoned connections that need verification._