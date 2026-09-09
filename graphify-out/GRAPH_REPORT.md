# Graph Report - QuantumSec  (2026-09-08)

## Corpus Check
- 310 files · ~142,500 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3285 nodes · 7943 edges · 157 communities (129 shown, 24 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 349 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `81dac26f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- main.py
- PublicIdentity
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- test_client_exchange.py
- pqc/errors.py
- Revisión final independiente — Fase 7: Motor Experimental Reproducible V1
- compilerOptions
- issue_initiator_hybrid_contributions
- test_measures.py
- QuantumChannel
- orchestration/__init__.py
- reconcile_cascade
- PQCHandshakeTranscript
- api.ts
- ExperimentConfig
- laboratory.py
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- estimate_qber_from_sample
- WegmanCarterAuthenticationContext
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- App.tsx
- test_key_confirmation.py
- test_data_plane.py
- P2 — Polish
- PQCProfile
- dm_from_ket
- TrustedIdentityStore
- Adaptive Agents for QKD
- SessionMetricsView.tsx
- runtime.py
- BB84Result
- oqs_kem_backend.py
- SessionProfile
- ProtectedSession
- LaboratoryPage.tsx
- .generate
- test_party.py
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
- ProfileSelector.tsx
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
- information.py
- EXPERIMENTS.md
- SessionConfig
- AuthenticatedQKDSessionResult
- pqc/__init__.py
- Reproducible Experiment Engine V1
- verify_reconciled_keys
- ExperimentRecord
- MLDSAIdentity
- _OQSSignature
- identity.py
- .__exit__
- .__exit__
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- test_key_schedule.py
- 13. Experiments
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- SessionProfileDefinition
- QuantumSec Deployment Guide
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- BaseRNG
- QuantumSec Web UI V1
- SessionResult
- GlobalRNG
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- AuthenticationFrame
- .__exit__
- 10. Security Model
- export.py
- test_authentication.py
- QuantumSec Conventions Memory
- UnsupportedAlgorithmError
- qkd/transcript.py
- .generate
- analysis/thesis_v1.py
- .__exit__
- .apply
- validation.py
- StrEnum
- .__enter__
- EstablishedPQCSession
- PQCParty
- .apply
- test_api.py
- QuantumSec Web Laboratory redesign
- DepolarizingChannel
- .__enter__
- campaigns/__init__.py
- campaigns/thesis_v1.py
- analysis/__init__.py
- RunWorkspace.tsx
- experiments/config.py
- Thesis Campaign `thesis-v1.0.1`
- schemas.py
- CompositionSummary.tsx
- d1.py
- _top_level_imports
- exchange.py
- orchestration/profiles.py
- oqs_backend.py
- as_ket
- KrausChannel
- qber_by_basis
- bb84.py
- _prepare_density_matrix
- hybrid/runner.py
- amplify_privacy
- analytical_qber
- qkd/runner.py
- test_states.py
- .apply

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
Cohesion: 0.09
Nodes (27): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking…, Validate that the input value is a byte string, raising a TypeError if it is…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs. (+19 more)

### Community 1 - "main.py"
Cohesion: 0.14
Nodes (21): get, HealthResponse, post, project_version(), Return the installed project version with a source-tree fallback., compare_runs(), get_run(), health() (+13 more)

### Community 2 - "PublicIdentity"
Cohesion: 0.11
Nodes (11): PublicIdentity, Export the non-secret public identity suitable for peer trust stores., Verify a message signature against an explicitly provided public identity., Immutable public verification identity associating an owner name with public…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, Serialize this public identity into a JSON-compatible dictionary with…, Return this party's public identity for distribution and registration in peer… (+3 more)

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
Cohesion: 0.09
Nodes (36): ClientKeyExchangeFactory, PQCOperationObserver, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ClientKeyExchange, Immutable public KEM ciphertext message bound to Bob's exact signed offer., Validate the protocol binding and profile-specific ciphertext fields., Serialize every authenticated field deterministically and unambiguously. (+28 more)

### Community 8 - "pqc/errors.py"
Cohesion: 0.06
Nodes (38): OQSKEMBackend, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, BackendOperationError, Domain errors for post-quantum cryptographic operations., Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation, KEMMetadata (+30 more)

### Community 9 - "Revisión final independiente — Fase 7: Motor Experimental Reproducible V1"
Cohesion: 0.04
Nodes (44): 10. Evidencia de validación, 11. Preparación por experimento, 12. Correcciones aplicadas, 13. Conclusión, 1. Dictamen, 2. Alcance inspeccionado, 3. Arquitectura y propiedades verificadas, 4. Tabla de hallazgos (+36 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "issue_initiator_hybrid_contributions"
Cohesion: 0.17
Nodes (10): AuthenticatedKEMContributions, issue_initiator_hybrid_contributions(), issue_responder_hybrid_contributions(), Consumable capability issued only for an authenticated exact PQC transcript., Return defensive secret copies once and retire the capability., Consume Alice's state only after its authenticated transcript binding validates., Consume Bob's state only after its authenticated transcript binding validates., _transcript() (+2 more)

### Community 12 - "test_measures.py"
Cohesion: 0.06
Nodes (42): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., _born_probabilities() (+34 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.07
Nodes (43): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, build_channel_pipeline(), build_channel_stage(), _optional_number(), StrEnum (+35 more)

### Community 14 - "orchestration/__init__.py"
Cohesion: 0.07
Nodes (38): Versioned public configuration for common QuantumSec session execution., Runtime-only capabilities kept separate from reproducible public configuration., Establishment-to-data-plane adapter with explicit session-key ownership…, Upper-layer composition of independent QKD and PQC domain modules., PQCAuthenticationMetrics, PQCSessionMetrics, QKDSessionMetrics, Profile-compatible metrics that keep unlike timing categories separate. (+30 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (28): Classical QKD post-processing algorithms and immutable transcripts., CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+20 more)

### Community 16 - "PQCHandshakeTranscript"
Cohesion: 0.08
Nodes (16): PQCConfirmationKeyDeriver, PQCOperationObserver, Require a live Phase 5 key state bound to the exact Phase 6 transcript., Derive a private role-local confirmation key from authenticated Phase 5 state., Derive Alice's confirmation state and retire her KEM secret state., Derive Bob's confirmation state and retire his KEM secret state., _validated_session_key_state(), DerivedSessionKeyState (+8 more)

### Community 17 - "api.ts"
Cohesion: 0.10
Nodes (23): GuidedChannelControls(), GuidedChannelControlsProps, StagePipelineEditor(), StagePipelineEditorProps, AdversaryCapability, AttackDiagnosticsSummary, BB84SimulationRequest, ChannelCapability (+15 more)

### Community 18 - "ExperimentConfig"
Cohesion: 0.15
Nodes (18): ExperimentConfig, One normalized instruction for an experimental session execution., Run ordered configurations sequentially, optionally shuffling reproducibly.…, run_batch(), e3_config(), experiment_runner(), fixture, qkd_config() (+10 more)

### Community 19 - "laboratory.py"
Cohesion: 0.11
Nodes (22): AttackDiagnosticsSummary, RunRecord, _attack_diagnostics(), _experiment_config(), CompareResponse, ProtectedMessageResponse, RunListResponse, SessionRunRequest (+14 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.11
Nodes (33): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+25 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.08
Nodes (23): _copy_bb84_bases(), estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the… (+15 more)

### Community 23 - "WegmanCarterAuthenticationContext"
Cohesion: 0.12
Nodes (10): AuthenticationSessionRegistry, AuthenticationSessionReplayError, RuntimeError, Raised when a session identifier is reused within persistent authentication…, Thread-safe replay registry that contains identifiers, never authentication…, Self, Bilateral, direction-separated PSK material for one or more QKD sessions., Provision matching but independent copies for each communication direction. (+2 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.08
Nodes (5): BB84SessionResult, Stage-by-stage immutable result of a complete BB84 session., Return aggregate full-key QBER as a backwards-compatible alias., Return aggregate sampled QBER as a backwards-compatible alias., Return disclosed sample, reconciliation parities, and confirmation tag bits.…

### Community 25 - "registry.py"
Cohesion: 0.08
Nodes (23): ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations., Generate a fresh signing key pair using secure cryptographic backend randomness., Return the public algorithm metadata and key/signature buffer dimensions. (+15 more)

### Community 26 - "client.ts"
Cohesion: 0.14
Nodes (18): compareRuns(), getCapabilities(), getHealth(), getRuns(), protectMessage(), QuantumSecApiError, requestJson(), runBB84Simulation() (+10 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "App.tsx"
Cohesion: 0.16
Nodes (17): App(), AppView, viewFromHash(), views, viewTitles, AppShell(), AppShellProps, Header() (+9 more)

### Community 29 - "test_key_confirmation.py"
Cohesion: 0.07
Nodes (50): _compute_finished_verify_data(), ConfirmedPQCHandshake, _finished_mac_input(), PQCConfirmationKeyState, PQCKeyConfirmation, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released. (+42 more)

### Community 30 - "test_data_plane.py"
Cohesion: 0.35
Nodes (11): open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., _establish(), _parties(), parametrize, _qkd_authentication(), test_aborted_session_cannot_open_data_plane(), test_all_256_bit_session_key_profiles_open_data_plane() (+3 more)

### Community 31 - "P2 — Polish"
Cohesion: 0.05
Nodes (38): 1. Executive assessment, 2. What is already strong (do not redesign), 3. Findings, 4. Cross-page design-system recommendations, 5. Screens and states manually reviewed, 6. Changes selected for implementation, 7. Phase 2 — implementation record, 8. Follow-up verification (+30 more)

### Community 32 - "PQCProfile"
Cohesion: 0.04
Nodes (74): Enum, Runtime-only accumulation of exact PQC operation timings., _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.… (+66 more)

### Community 33 - "dm_from_ket"
Cohesion: 0.08
Nodes (37): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, InterceptResendAttack, Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., Return an immutable simulator-only snapshot of cumulative counters., Reset aggregate counters without rewinding the injected RNG stream., Small immutable snapshot of simulator-only attack observations., Measure selected signals in a random BB84 basis and resend fresh states. The… (+29 more)

### Community 34 - "TrustedIdentityStore"
Cohesion: 0.12
Nodes (9): Return the explicit store of trusted peer identities configured for this party., Thread-safe in-memory registry mapping peer names to pre-provisioned trusted…, Initialize an empty trusted identity store., Return a sorted tuple of all trusted owner names registered in the store., Check whether an owner name is registered in the trusted identity store., Iterate over all trusted public identities in deterministic owner order., Return the total number of trusted peer identities in the store., Return a string representation listing registered trusted owner names. (+1 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "SessionMetricsView.tsx"
Cohesion: 0.33
Nodes (8): SessionMetricsView(), SessionMetricsViewProps, formatBytes(), formatDurationNs(), formatPercent(), authLabel(), ComparePage(), SessionMetrics

### Community 37 - "runtime.py"
Cohesion: 0.13
Nodes (10): ExperimentRuntime, ExperimentRuntimeFactory, PQCIdentityProvisioning, Runtime-only provisioning for experiment configurations., Create per-run contexts while retaining persistent laboratory identities. ML-…, Provision and time persistent campaign identities exactly once., One-time ML-DSA identity-generation cost outside session timings., Public description of provisioning policy; it never contains key material. (+2 more)

### Community 38 - "BB84Result"
Cohesion: 0.08
Nodes (15): BB84Result, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+7 more)

### Community 39 - "oqs_kem_backend.py"
Cohesion: 0.07
Nodes (28): _ensure_kem_algorithm_enabled(), _KEMFactory, _load_oqs(), _new_kem(), _OQSKEM, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair (+20 more)

### Community 40 - "SessionProfile"
Cohesion: 0.18
Nodes (23): canonical_hybrid_secret_input(), _expected_algorithms(), HybridSecretComponent, Unambiguous encoding of independently established QKD and KEM contributions., Encode secret contributions in mandatory QKD, ML-KEM, optional HQC order., SessionProfile, _component(), _context() (+15 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "LaboratoryPage.tsx"
Cohesion: 0.25
Nodes (14): LaboratoryMode, QKDControls(), QKDControlsProps, createChannelDraft(), serializeChannels(), validateChannels(), DEFAULT_POSTPROCESSING, defaultRunRequest() (+6 more)

### Community 43 - ".generate"
Cohesion: 0.17
Nodes (10): Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Deserialize and validate a public identity from a JSON-compatible dictionary…, ml_dsa_identities(), fixture, ml_dsa_context(), fixture, test_public_identity_rejects_invalid_base64() (+2 more)

### Community 44 - "test_party.py"
Cohesion: 0.18
Nodes (9): Raised when an operation requires an identity from a peer not found in the…, UnknownTrustedPeerError, Return the trusted public identity for an owner, raising…, Tests for parties and explicit pre-provisioned trust., test_party_name_remains_bound_to_immutable_private_identity(), test_party_representation_contains_no_key_material(), test_trust_store_collection_protocol(), test_trust_store_is_not_coupled_to_ml_dsa() (+1 more)

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
Cohesion: 0.07
Nodes (58): AuthenticationContext, AuthenticationTransportHook, Validate runtime authentication capabilities before starting QKD work., Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), validate_qkd_authentication_context(), IdentityChannel (+50 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 56 - "ProfileSelector.tsx"
Cohesion: 0.15
Nodes (13): familyMeta, ProfileSelector(), ProfileSelectorProps, PROFILE_SHORT_LABELS, familyLabels, OverviewPage(), OverviewPageProps, capabilitiesFixture (+5 more)

### Community 70 - "capabilities.py"
Cohesion: 0.16
Nodes (19): Return all executable profiles in stable public-enum order., session_capabilities(), ParameterCapability, ProfileCapability, get_capabilities(), _probability(), _profile_capability(), CapabilitiesResponse (+11 more)

### Community 71 - ".from_dict"
Cohesion: 0.17
Nodes (14): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+6 more)

### Community 73 - "information.py"
Cohesion: 0.16
Nodes (21): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+13 more)

### Community 74 - "EXPERIMENTS.md"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "SessionConfig"
Cohesion: 0.14
Nodes (31): Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, Dispatch a normalized session config to its domain-specific adapter., run_session(), test_experiment_kind_rejects_obvious_profile_and_stage_mismatches(), test_generic_runner_closes_live_session_result() (+23 more)

### Community 79 - "AuthenticatedQKDSessionResult"
Cohesion: 0.21
Nodes (7): AuthenticatedQKDSessionResult, _optional_key_copy(), NDArray, uint8, Terminal QKD decision; key fields exist only after all required checks pass., Return defensive immutable copies only for an accepted session., Serialize bounded public metadata, never transcript payloads or key material.

### Community 80 - "pqc/__init__.py"
Cohesion: 0.05
Nodes (38): Post-quantum identity, authentication, KEM, and key-establishment primitives., MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, ProcessedClientKeyExchange, StrEnum (+30 more)

### Community 81 - "Reproducible Experiment Engine V1"
Cohesion: 0.25
Nodes (8): Batch and statistics, CLI, Configuration, Definitive campaign, Environment and record schema, Metrics and exports, Reproducible Experiment Engine V1, Runtime and secret lifecycle

### Community 82 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (10): ArrayLike, Immutable public key-agreement verification data and protocol decision., Return the number of public Alice tag bits., Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+2 more)

### Community 83 - "ExperimentRecord"
Cohesion: 0.12
Nodes (11): BatchProvenance, ExperimentRecord, _freeze(), _freeze_mapping(), Immutable, versioned public evidence produced by one experiment run., Copy public evidence before the caller closes the live session capability., Public, versioned provenance shared by every retained run in one batch., _thaw() (+3 more)

### Community 84 - "MLDSAIdentity"
Cohesion: 0.14
Nodes (13): MLDSAIdentity, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Generate an ML-DSA-65 signature over message bytes using this identity's…, Return a safe string representation showing owner and algorithm without…, Named private identity holding an ML-DSA-65 signing capability and associated…, Validate the owner name and ensure the internal signer is an MLDSA65 instance., alice_identity(), fixture (+5 more)

### Community 85 - "_OQSSignature"
Cohesion: 0.14
Nodes (8): _OQSSignature, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs signature context manager., Protocol for the liboqs Signature constructor callable., _SignatureFactory

### Community 86 - "identity.py"
Cohesion: 0.22
Nodes (6): Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, Private and public identities for PQC authentication., Named PQC parties with signing and pre-provisioned verification trust., Explicit pre-provisioned trust for public PQC identities., Register a public identity as trusted, raising an error if already present…

### Community 87 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 88 - ".__exit__"
Cohesion: 0.25
Nodes (5): BaseException, TracebackType, Release secret references when leaving a managed lifetime., Release secret references idempotently without claiming memory zeroization., Transfer raw KEM contributions once to the domain-owned hybrid capability.

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "test_key_schedule.py"
Cohesion: 0.09
Nodes (44): PQCSessionKeyDeriver, PQCOperationObserver, Derive the same key for either role using one shared transcript-bound schedule., Derive Alice's key only from a successful authenticated Phase 3 result., Derive Bob's key only from a successful authenticated Phase 4 result., Build explicit HKDF info for the Phase 5 session-key purpose., _session_key_info(), Self (+36 more)

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

### Community 101 - "QuantumSec Deployment Guide"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 102 - "BB84 security model"
Cohesion: 0.14
Nodes (13): AES-256-GCM data plane, Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Hybrid session composition, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication (+5 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "BaseRNG"
Cohesion: 0.06
Nodes (51): BaseRNG, ABC, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations., Generate binary choices using this simulator's bias/correlation model., Generate one or more uniformly distributed classical bits. (+43 more)

### Community 105 - "QuantumSec Web UI V1"
Cohesion: 0.33
Nodes (6): API, Development, Extension points, QuantumSec Web UI V1, Supported V1 features, Verification

### Community 106 - "SessionResult"
Cohesion: 0.10
Nodes (6): EstablishedKeyCapability, Self, Return whether this result no longer exposes live key material., Export accepted key bytes; QKD exact bit length remains in result metadata., Private export boundary for accepted key bytes with exact bit-length metadata., SessionResult

### Community 107 - "GlobalRNG"
Cohesion: 0.33
Nodes (4): GlobalRNG, Process-wide generator initialized from operating-system entropy., Return the shared entropy-seeded NumPy generator., test_global_rng_is_a_singleton()

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "AuthenticationFrame"
Cohesion: 0.11
Nodes (12): AuthenticationEvidence, AuthenticationFrame, AuthenticationVerification, Canonical authentication unit binding payload to anti-replay context., MLDSADirectionalAuthenticator, Sign as one provisioned party and verify through the receiver's trust store., _frame_bits(), NDArray (+4 more)

### Community 111 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

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

### Community 116 - "UnsupportedAlgorithmError"
Cohesion: 0.11
Nodes (19): Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return the active HQC provider instance required by a HIGH-profile session., Decapsulate an HQC ciphertext with this HIGH-profile session's private key., hqc(), ml_kem() (+11 more)

### Community 117 - "qkd/transcript.py"
Cohesion: 0.11
Nodes (22): Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), Authenticated public context binding every hybrid session input., Versioned, role-separated HMAC-SHA-384 Finished exchange for hybrid keys. (+14 more)

### Community 119 - "analysis/thesis_v1.py"
Cohesion: 0.07
Nodes (75): generate_all(), _number(), _numbers(), _plot_e1(), _plot_e2(), _plot_e3(), _plot_e4(), _plot_e5() (+67 more)

### Community 120 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release references to ephemeral private KEM instances to prevent subsequent…, Release the private KEM capabilities when leaving a managed lifetime.

### Community 121 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 122 - "validation.py"
Cohesion: 0.08
Nodes (50): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+42 more)

### Community 123 - "StrEnum"
Cohesion: 0.67
Nodes (3): CapabilityStatus, EstablishmentSource, StrEnum

### Community 125 - "EstablishedPQCSession"
Cohesion: 0.13
Nodes (8): EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key., Enter a managed lifetime for this established local session.

### Community 126 - "PQCParty"
Cohesion: 0.05
Nodes (74): OfferCreation, ProcessedServerOffer, PQCOperationObserver, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed., ServerKeyOfferProcessor (+66 more)

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 129 - "test_api.py"
Cohesion: 0.11
Nodes (4): parametrize, test_backend_gives_protocol_and_each_eve_stage_independent_rng_streams(), test_intercept_resend_configuration_rejects_invalid_fraction(), test_session_api_executes_every_current_public_profile()

### Community 130 - "QuantumSec Web Laboratory redesign"
Cohesion: 0.22
Nodes (8): Backend/API changes, Current-state audit, Event and data flow, Explicit non-goals, Implementation phases, Information architecture, QuantumSec Web Laboratory redesign, Retained and replaced

### Community 131 - "DepolarizingChannel"
Cohesion: 0.13
Nodes (21): DepolarizingChannel, ArrayLike, ComplexArray, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, Apply depolarizing noise to a single-qubit density matrix., assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state() (+13 more)

### Community 134 - "campaigns/thesis_v1.py"
Cohesion: 0.16
Nodes (26): build_campaign_plan(), CampaignPlan, CampaignPreset, _config(), _e2_conditions(), _e5_config(), execute_campaign(), _experiment_manifest() (+18 more)

### Community 136 - "RunWorkspace.tsx"
Cohesion: 0.20
Nodes (11): runSession(), OUTCOME_HEADINGS, RunWorkspace(), RunWorkspaceProps, run, useSessionRun(), LaboratoryPageProps, RunsPageProps (+3 more)

### Community 137 - "experiments/config.py"
Cohesion: 0.38
Nodes (8): _invalid_stage(), _number(), _optional_integer(), _postprocessing_from_public_dict(), Strict, versioned, secret-free experiment configuration., _reject_unknown(), _session_from_public_dict(), test_json_loader_rejects_duplicate_and_unknown_fields()

### Community 139 - "Thesis Campaign `thesis-v1.0.1`"
Cohesion: 0.40
Nodes (4): Interpretation boundary, Reproduction, Status, Thesis Campaign `thesis-v1.0.1`

### Community 140 - "schemas.py"
Cohesion: 0.17
Nodes (16): BaseModel, model_validator, AmplitudeDampingChannelConfiguration, ApiError, BitFlipChannelConfiguration, CompareRequest, DepolarizingChannelConfiguration, IdentityChannelConfiguration (+8 more)

### Community 141 - "CompositionSummary.tsx"
Cohesion: 0.15
Nodes (18): CompositionSummary(), CompositionSummaryProps, EventTone, ProtocolTrace(), ProtocolTraceProps, AuthenticationCard(), SecurityEvidence(), SecurityEvidenceProps (+10 more)

### Community 144 - "d1.py"
Cohesion: 0.15
Nodes (14): D1Record, _expect_invalid_tag(), _flip_first(), Secret-free executable D1 protected-session demonstration., Establish HYBRID-DIVERSE, transfer its key, and test AES-GCM rejection., run_d1(), TamperOutcome, _distribution_version() (+6 more)

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

### Community 147 - "exchange.py"
Cohesion: 0.13
Nodes (12): Exception, execute_authenticated_pqc_exchange(), PQCExchangeArtifacts, PQCExchangeRejected, Reusable execution of the existing mutually authenticated PQC phases 2--4., Execute signed offer/encapsulation/exchange/decapsulation without deriving keys., PQCOperationTimer, PQCOperationTimings (+4 more)

### Community 160 - "orchestration/profiles.py"
Cohesion: 0.11
Nodes (30): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationMetrics, AuthenticationState, AuthenticatorMetadata, ClassicalAuthenticationResult, DirectionalAuthenticator, ABC (+22 more)

### Community 166 - "oqs_backend.py"
Cohesion: 0.11
Nodes (20): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), oqs_runtime_versions(), OQSKeyPair, _OQSModule, OQSRuntimeVersions, Adapter isolating the liboqs-python signature API. (+12 more)

### Community 181 - "as_ket"
Cohesion: 0.12
Nodes (30): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+22 more)

### Community 186 - "KrausChannel"
Cohesion: 0.10
Nodes (19): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+11 more)

### Community 188 - "qber_by_basis"
Cohesion: 0.15
Nodes (19): QKD metric computations., _optional_probability(), ArrayLike, ndarray, qber(), qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics. (+11 more)

### Community 197 - "bb84.py"
Cohesion: 0.08
Nodes (33): Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., Map the QKD random-bit convention 0/1 to the Z/X basis. (+25 more)

### Community 270 - "_prepare_density_matrix"
Cohesion: 0.15
Nodes (12): _immutable_density(), ArrayLike, ComplexArray, Possibly intercept one qubit, then return a fresh transmitted state., _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix. (+4 more)

### Community 271 - "hybrid/runner.py"
Cohesion: 0.09
Nodes (27): AuthenticationOutcome, HybridPublicContext, hybrid_component_metadata_bytes(), hybrid_kem_label(), Return encoded bytes attributable to one component's non-secret…, Return the canonical hybrid label for a supported KEM algorithm., create_finished(), HybridFinishedMessage (+19 more)

### Community 272 - "amplify_privacy"
Cohesion: 0.17
Nodes (11): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, parametrize, test_privacy_amplification_agrees_and_respects_target_length() (+3 more)

### Community 273 - "analytical_qber"
Cohesion: 0.40
Nodes (5): analytical_qber(), AnalyticalQBER, Analytical BB84 error predictions for the E2 validation campaign., Expected Z-, X-, and uniform-basis aggregate QBER., Return the exact E2 prediction implied by the implemented channel.

### Community 274 - "qkd/runner.py"
Cohesion: 0.16
Nodes (10): MLDSAAuthenticationContext, Pre-provisioned bilateral ML-DSA identities and peer trust stores., QKD session orchestration and canonical public transcript contracts., QKDSessionSummary, QKDTraceEvent, Non-secret BB84 outcome metadata suitable for backend serialization., Profile-aware QKD runner that gates final-key release on authentication., StrEnum (+2 more)

### Community 275 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 279 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

## Knowledge Gaps
- **378 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+373 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1339 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `dm_from_ket`, `test_api.py`, `runtime.py`, `BaseRNG`, `SessionConfig`, `test_measures.py`, `QuantumChannel`, `reconcile_cascade`, `amplify_privacy`, `verify_reconciled_keys`, `adapters.py`, `BB84Protocol`, `estimate_qber_from_sample`, `test_data_plane.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `PQCProfile`, `PublicIdentity`, `TrustedIdentityStore`, `runtime.py`, `test_client_exchange.py`, `SessionConfig`, `test_party.py`, `.generate`, `orchestration/__init__.py`, `pqc/__init__.py`, `exchange.py`, `MLDSAIdentity`, `identity.py`, `test_key_schedule.py`, `test_key_confirmation.py`, `test_data_plane.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `QuantumSec TFM Goal` connect `QuantumSec TFM Goal` to `10. Security Model`, `EXPERIMENTS.md`, `13. Experiments`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `SeededRNG` (e.g. with `ExperimentRuntimeFactory` and `build_channel_pipeline()`) actually correct?**
  _`SeededRNG` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `SessionConfig` (e.g. with `QKDProfile` and `SessionProfile`) actually correct?**
  _`SessionConfig` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._