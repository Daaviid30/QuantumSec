# Graph Report - QuantumSec  (2026-09-07)

## Corpus Check
- 267 files · ~110,681 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2770 nodes · 6540 edges · 151 communities (111 shown, 36 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 296 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `44671a7c`
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
- BackendOperationError
- as_ket
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- orchestration/__init__.py
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- InterceptResendAttack
- test_noise.py
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- ParameterEstimationResult
- .generate
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- exchange.py
- AuthenticationFrame
- SimulationConfigurator.tsx
- test_key_schedule.py
- PQCProfile
- authentication/base.py
- Adaptive Agents for QKD
- BaseRNG
- bb84.py
- BB84Result
- hybrid/runner.py
- qkd/transcript.py
- ProtectedSession
- SimulatorPage.tsx
- SignedServerKeyOffer
- QuantumSec Web UI V1
- sift_keys
- Graphify Knowledge Graph Integration Rules
- Q: How should the BB84 core integrate with QuantumSec architecture?
- Q: Explícame cómo se utilizan las principales cosas y conceptos de BB84 y si Graphify, Serena y Context7 ayudaron
- Q: y cuantos bits forman el bitstring del inicio?? porque nolo puedo marcar no? como configuro el panel de serena para que en la siguiente tarea optimices y trabajes como nunca??
- AuthenticationMaterialError
- ResizeObserverMock
- ml_kem_768_metadata
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
- run_qkd_profile
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- SessionConfig
- test_providers.py
- information.py
- BB84Protocol
- postprocessing/__init__.py
- PQCConfirmationKeyState
- MLDSAIdentity
- oqs_backend.py
- .__exit__
- EstablishedPQCSession
- test_hybrid_primitives.py
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- oqs_kem_backend.py
- ServerKeyOfferFactory
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- PQCFinishedMessage
- .verify
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- PQCParty
- qber_by_basis
- SessionProfileDefinition
- .__exit__
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- MLDSAAuthenticationContext
- _OQSKEM
- verify_reconciled_keys
- estimate_qber_from_sample
- test_authentication.py
- NDArray
- 13. Experiments
- orchestration/profiles.py
- dm_from_ensemble
- OQSSignatureBackend
- _require_bytes
- ClientKeyExchange
- 10. Security Model
- ReconciliationResult
- .__repr__
- .canonical_bytes
- .apply
- .apply
- BB84PostprocessingConfig
- WegmanCarterAuthenticationContext
- .apply
- .generate
- .apply
- .apply
- dm_from_ket
- ._active_ml_kem
- .__repr__
- .metadata
- protocol/__init__.py
- .__post_init__
- .public_key
- test_full_six_phase_handshake_crosses_pure_json_transport
- .sign
- .verify
- _top_level_imports
- .metadata
- _RegisteredSignature
- .diagnostic_full_sifted_qber
- .estimated_qber
- .total_public_leakage

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 122 edges
2. `PQCParty` - 78 edges
3. `SignedServerKeyOffer` - 62 edges
4. `BB84Protocol` - 61 edges
5. `PQCProfile` - 51 edges
6. `IdentityChannel` - 44 edges
7. `run_hybrid_session()` - 42 edges
8. `dm_from_ket()` - 42 edges
9. `BaseRNG` - 39 edges
10. `ServerKeyOfferProcessor` - 39 edges

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

## Communities (151 total, 36 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.15
Nodes (16): MLDSA65, Self, Return a safe string representation with public key length without leaking…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs., Generate a fresh ML-DSA-65 key pair via liboqs and return a new provider…, Return the immutable ML-DSA-65 public key., fixture, Real-backend tests for ML-DSA-65 signatures. (+8 more)

### Community 1 - "adapters.py"
Cohesion: 0.05
Nodes (68): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, parametrize (+60 more)

### Community 2 - "validation.py"
Cohesion: 0.10
Nodes (43): _error_density_matrix(), _error_normalized_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state(), is_projective_measurement() (+35 more)

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
Cohesion: 0.08
Nodes (29): BackendOperationError, Domain errors for post-quantum cryptographic operations., Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation, KEMMetadata, KEMProvider, ABC, Backend-independent key-encapsulation contracts and metadata. (+21 more)

### Community 9 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "test_measures.py"
Cohesion: 0.06
Nodes (42): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), Project-wide numerical constants with no domain-layer dependencies., _born_probabilities() (+34 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.05
Nodes (50): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., Small immutable snapshot of simulator-only attack observations., _prepare_density_matrix(), ABC, ArrayLike, ComplexArray (+42 more)

### Community 14 - "orchestration/__init__.py"
Cohesion: 0.07
Nodes (30): Versioned public configuration for common QuantumSec session execution., Runtime-only capabilities kept separate from reproducible public configuration., Establishment-to-data-plane adapter with explicit session-key ownership…, Upper-layer composition of independent QKD and PQC domain modules., PQCAuthenticationMetrics, PQCSessionMetrics, QKDSessionMetrics, Profile-compatible metrics that keep unlike timing categories separate. (+22 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.14
Nodes (21): CascadeConfig, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray, uint8 (+13 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.19
Nodes (25): Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., _derive_confirmation_states(), _exchange_finished(), _flipped(), _Phase6States, parametrize, Tests for Phase 6 role-separated Finished key confirmation. (+17 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "InterceptResendAttack"
Cohesion: 0.11
Nodes (20): InterceptResendAttack, Return an immutable simulator-only snapshot of cumulative counters., Reset aggregate counters without rewinding the injected RNG stream., Measure selected signals in a random BB84 basis and resend fresh states. The…, Simulate preparation, transmission, measurement, sifting, and QBER data., parametrize, test_attack_diagnostics_can_be_reset_without_rewinding_the_rng(), test_full_interception_resends_a_pure_state_from_a_mixed_input() (+12 more)

### Community 19 - "test_noise.py"
Cohesion: 0.18
Nodes (16): AmplitudeDampingChannel, Standard single-qubit amplitude damping with ``0 <= gamma <= 1``. This CPTP…, assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state(), test_amplitude_damping_matches_analytical_superposition_result(), test_amplitude_damping_rejects_invalid_gamma(), test_depolarizing_channel_fixes_maximally_mixed_state() (+8 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.13
Nodes (29): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+21 more)

### Community 22 - "ParameterEstimationResult"
Cohesion: 0.13
Nodes (6): ParameterEstimationResult, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the…, Immutable basis-aware transcript and remaining candidate material., test_parameter_estimation_accepts_round_trip_qber_with_tiny_float_error()

### Community 25 - "registry.py"
Cohesion: 0.18
Nodes (14): ABC, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Abstract base contract defining post-quantum digital signature operations., Return the public algorithm metadata and key/signature buffer dimensions., SignatureMetadata, SignatureProvider, Post-quantum digital-signature providers. (+6 more)

### Community 26 - "client.ts"
Cohesion: 0.27
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), useCapabilities(), useSimulation(), SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.16
Nodes (12): App(), AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection (+4 more)

### Community 29 - "exchange.py"
Cohesion: 0.10
Nodes (18): Exception, execute_authenticated_pqc_exchange(), PQCExchangeArtifacts, PQCExchangeRejected, Reusable execution of the existing mutually authenticated PQC phases 2--4., Execute signed offer/encapsulation/exchange/decapsulation without deriving keys., PQC adapters owned by the upper orchestration layer., Run the unchanged PQC handshake and adapt its established capability. (+10 more)

### Community 30 - "AuthenticationFrame"
Cohesion: 0.12
Nodes (18): AuthenticationEvidence, AuthenticationFrame, AuthenticationVerification, AuthenticatorMetadata, DirectionalAuthenticator, ABC, Generate and verify evidence for one authenticated communication direction., Canonical authentication unit binding payload to anti-replay context. (+10 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "test_key_schedule.py"
Cohesion: 0.08
Nodes (51): derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), Bob-local KEM secrets recovered after authenticating Alice's response. Raw-…, ResponderSharedSecretState, PQCConfirmationKeyDeriver (+43 more)

### Community 33 - "PQCProfile"
Cohesion: 0.07
Nodes (37): Enum, Internal canonical binary encoding primitives shared across PQC domains., PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites. (+29 more)

### Community 34 - "authentication/base.py"
Cohesion: 0.21
Nodes (14): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationMetrics, AuthenticationState, ClassicalAuthenticationResult, StrEnum, Common contracts for executed or explicitly assumed QKD classical…, authenticate_transcript_checkpoints() (+6 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BaseRNG"
Cohesion: 0.08
Nodes (24): BaseRNG, GlobalRNG, ABC, integer, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations. (+16 more)

### Community 37 - "bb84.py"
Cohesion: 0.09
Nodes (28): Deterministic basis reconciliation for QKD raw keys., bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases. (+20 more)

### Community 38 - "BB84Result"
Cohesion: 0.10
Nodes (11): _optional_probability(), QBERByBasis, Immutable aggregate and BB84 basis-conditioned error metrics., BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting. (+3 more)

### Community 39 - "hybrid/runner.py"
Cohesion: 0.08
Nodes (32): HybridPublicContext, hybrid_component_metadata_bytes(), hybrid_kem_label(), Return encoded bytes attributable to one component's non-secret…, Return the canonical hybrid label for a supported KEM algorithm., create_finished(), HybridFinishedMessage, HybridFinishedRole (+24 more)

### Community 40 - "qkd/transcript.py"
Cohesion: 0.11
Nodes (20): Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), Authenticated public context binding every hybrid session input., _bases_payload() (+12 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "SignedServerKeyOffer"
Cohesion: 0.10
Nodes (34): Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ProcessedServerOffer, StrEnum, Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., Authentication outcome produced before any Alice-side response is sent., Alice-side authentication outcome and optional private/public KEM outputs., Return whether Bob was authenticated and encapsulation completed. (+26 more)

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

### Community 50 - "AuthenticationMaterialError"
Cohesion: 0.25
Nodes (8): AuthenticationMaterialError, AuthenticationMaterialExhaustedError, AuthenticationMaterialReuseError, RuntimeError, Base error for unsafe or unavailable authentication material., Raised before a tag operation that would exceed the provisioned PSK., Raised when a frame context attempts to consume authentication bits twice., Atomically reserve fresh bits for one unique authenticated frame context.

### Community 52 - "ml_kem_768_metadata"
Cohesion: 0.13
Nodes (18): _length_prefixed(), Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), Canonical KEM input construction and HKDF primitives for QuantumSec., hqc_3_metadata() (+10 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "run_qkd_profile"
Cohesion: 0.17
Nodes (24): AuthenticationContext, AuthenticationTransportHook, Validate runtime authentication capabilities before starting QKD work., Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), validate_qkd_authentication_context(), _imports_top_level() (+16 more)

### Community 71 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "SessionConfig"
Cohesion: 0.13
Nodes (36): Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., Dispatch a normalized session config to its domain-specific adapter., run_session() (+28 more)

### Community 79 - "test_providers.py"
Cohesion: 0.10
Nodes (20): HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-…, Return the active HQC provider instance required by a HIGH-profile session., Decapsulate an HQC ciphertext with this HIGH-profile session's private key. (+12 more)

### Community 80 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 81 - "BB84Protocol"
Cohesion: 0.11
Nodes (33): IdentityChannel, Channel that returns an independent copy of the input state., DepolarizingChannel, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, BB84Protocol, Run BB84 with an injected random source and density-matrix channel. Alice's…, test_common_runner_executes_all_qkd_profiles(), test_session_result_context_manager_closes_established_key() (+25 more)

### Community 82 - "postprocessing/__init__.py"
Cohesion: 0.06
Nodes (53): Aggregate and per-basis quantum bit error rate metrics., Classical QKD post-processing algorithms and immutable transcripts., _copy_bb84_bases(), Sampled QBER estimation with mandatory removal of disclosed key positions., amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Toeplitz-universal privacy amplification for reconciled QKD keys. (+45 more)

### Community 83 - "PQCConfirmationKeyState"
Cohesion: 0.11
Nodes (13): _compute_finished_verify_data(), _finished_mac_input(), PQCConfirmationKeyState, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released., Return whether this state has released its role-local confirmation key., Return whether this role completed its local send/verify Finished work. (+5 more)

### Community 84 - "MLDSAIdentity"
Cohesion: 0.06
Nodes (31): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without…, Validate that the given identity name is a non-empty string and return its… (+23 more)

### Community 85 - "oqs_backend.py"
Cohesion: 0.07
Nodes (26): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), oqs_runtime_versions(), OQSKeyPair, _OQSModule, OQSRuntimeVersions, _OQSSignature (+18 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "EstablishedPQCSession"
Cohesion: 0.13
Nodes (10): EstablishedPQCSession, BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key. (+2 more)

### Community 88 - "test_hybrid_primitives.py"
Cohesion: 0.21
Nodes (21): canonical_hybrid_secret_input(), _expected_algorithms(), HybridSecretComponent, Unambiguous encoding of independently established QKD and KEM contributions., Encode secret contributions in mandatory QKD, ML-KEM, optional HQC order., SessionProfile, _component(), _context() (+13 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "oqs_kem_backend.py"
Cohesion: 0.08
Nodes (28): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMBackend, OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule (+20 more)

### Community 92 - "ServerKeyOfferFactory"
Cohesion: 0.06
Nodes (37): OfferCreation, ClientKeyExchangeProcessor, Authenticate Alice and validate session binding before Bob decapsulates., Verify Alice's response and only then recover Bob's matching KEM secrets., Serialize this public offer to a JSON-compatible mapping., Immutable message containing responder ephemeral KEM public keys and handshake…, ServerKeyOffer, Self (+29 more)

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

### Community 100 - "PQCFinishedMessage"
Cohesion: 0.11
Nodes (13): ConfirmedPQCHandshake, PQCKeyConfirmation, Self, Enter a managed lifetime for this private confirmation-key state., Capability produced only after both role-separated Finished MACs verify., Enter a managed lifetime for this established local session., Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Verify Alice's chained Finished and produce mutual-confirmation proof. (+5 more)

### Community 102 - "BB84 security model"
Cohesion: 0.14
Nodes (13): AES-256-GCM data plane, Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Hybrid session composition, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication (+5 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "PQCParty"
Cohesion: 0.05
Nodes (49): Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PublicIdentity, Immutable public verification identity associating an owner name with public…, Serialize this public identity into a JSON-compatible dictionary with…, PQCParty (+41 more)

### Community 105 - "qber_by_basis"
Cohesion: 0.20
Nodes (15): QKD metric computations., ArrayLike, ndarray, qber(), qber_by_basis(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, Return Z, X, and aggregate QBER without inventing absent-basis values., parametrize (+7 more)

### Community 106 - "SessionProfileDefinition"
Cohesion: 0.29
Nodes (4): Return all executable profiles in stable public-enum order., session_capabilities(), SessionProfileDefinition, test_all_seven_public_capabilities_are_current_and_stably_ordered()

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "MLDSAAuthenticationContext"
Cohesion: 0.15
Nodes (7): AuthenticationSessionRegistry, AuthenticationSessionReplayError, RuntimeError, Raised when a session identifier is reused within persistent authentication…, Thread-safe replay registry that contains identifiers, never authentication…, MLDSAAuthenticationContext, Pre-provisioned bilateral ML-DSA identities and peer trust stores.

### Community 111 - "_OQSKEM"
Cohesion: 0.14
Nodes (8): _KEMFactory, _OQSKEM, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager., Protocol for the liboqs KeyEncapsulation constructor callable.

### Community 112 - "verify_reconciled_keys"
Cohesion: 0.39
Nodes (7): ArrayLike, Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked(), test_verification_default_tag_tracks_32_bits_of_public_leakage(), test_verification_seed_and_tags_reproduce_with_equal_rng_state()

### Community 113 - "estimate_qber_from_sample"
Cohesion: 0.25
Nodes (13): estimate_qber_from_sample(), ArrayLike, ndarray, Disclose a stratified BB84 sample and remove it from both keys. Sampling is…, parametrize, test_odd_explicit_sample_breaks_equal_basis_ties_with_the_injected_rng(), test_parameter_estimation_explicit_sample_size_preserves_alignment(), test_parameter_estimation_fails_closed_without_valid_data_for_both_bb84_bases() (+5 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.30
Nodes (16): _frame(), _ml_dsa_authenticator(), parametrize, test_ml_dsa_rejects_missing_signature(), test_ml_dsa_rejects_modified_or_cross_context_frame(), test_ml_dsa_rejects_modified_signature(), test_ml_dsa_rejects_unknown_identity(), test_ml_dsa_rejects_wrong_public_identity() (+8 more)

### Community 115 - "NDArray"
Cohesion: 0.21
Nodes (7): intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation.

### Community 116 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

### Community 117 - "orchestration/profiles.py"
Cohesion: 0.09
Nodes (24): CapabilityStatus, EstablishmentSource, StrEnum, qkd_profile_definition(), QKDProfile, QKDProfileDefinition, Public session profiles with orthogonal establishment and authentication…, Return explicit, public authentication duties for capability discovery. (+16 more)

### Community 118 - "dm_from_ensemble"
Cohesion: 0.18
Nodes (11): dm_from_ensemble(), ArrayLike, ComplexArray, Construct a density matrix from a finite ensemble of pure states. Parameters…, _error_probability_state(), is_probability_state(), Return whether an input is a finite probability distribution., Validate a finite, real, non-negative probability distribution. (+3 more)

### Community 119 - "OQSSignatureBackend"
Cohesion: 0.20
Nodes (8): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, Generate a signature over message bytes using the given algorithm and secret…, Verify a signature against the message and public key using the liboqs backend., test_backend_load_failure_has_domain_error(), test_enabled_algorithm_check_is_cached(), test_unsupported_backend_algorithm_has_domain_error()

### Community 120 - "_require_bytes"
Cohesion: 0.25
Nodes (5): Validate that the input value is a byte string, raising a TypeError if it is…, Validate ML-DSA-65 key buffer sizes and store immutable defensive copies of the…, Generate an ML-DSA-65 signature over message bytes using the private signing…, Verify an ML-DSA-65 signature against the message and public verification key., _require_bytes()

### Community 122 - "ClientKeyExchange"
Cohesion: 0.29
Nodes (4): ClientKeyExchange, Immutable public KEM ciphertext message bound to Bob's exact signed offer., Validate the protocol binding and profile-specific ciphertext fields., Serialize this public client exchange to a JSON-compatible mapping.

### Community 123 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 124 - "ReconciliationResult"
Cohesion: 0.29
Nodes (3): Immutable corrected key and conservative public parity transcript size., Return the conservative leakage: one bit per disclosed Alice parity., ReconciliationResult

### Community 125 - ".__repr__"
Cohesion: 0.20
Nodes (3): Decapsulate an incoming ciphertext using this provider instance's private key., Return a safe string representation showing buffer lengths without exposing…, Return the immutable public encapsulation key bytes.

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 128 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 129 - "BB84PostprocessingConfig"
Cohesion: 0.12
Nodes (12): BB84PostprocessingConfig, BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., Configuration for BB84 post-processing under assumed channel authentication.…, Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, QKD protocol implementations., A basis average must not authorize extraction on an asymmetric channel. (+4 more)

### Community 130 - "WegmanCarterAuthenticationContext"
Cohesion: 0.11
Nodes (8): PreSharedAuthenticationMaterial, Self, Bilateral, direction-separated PSK material for one or more QKD sessions., Provision matching but independent copies for each communication direction., Consumable PSK bit stream whose contents are never exposed or serialized., WegmanCarterAuthenticationContext, test_psk_representation_never_contains_secret(), test_wegman_carter_context_enforces_directional_key_separation()

### Community 131 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 133 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 135 - "dm_from_ket"
Cohesion: 0.10
Nodes (24): ChannelPipeline, ArrayLike, ComplexArray, Apply an immutable sequence of channels in order. An empty pipeline is defined…, Apply each component from first to last without mutating the input., Reusable standard projective measurements for QKD protocols., _immutable(), ndarray (+16 more)

### Community 136 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

### Community 139 - "protocol/__init__.py"
Cohesion: 0.05
Nodes (44): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeProcessingStatus, ProcessedClientKeyExchange, StrEnum, Bob-side authentication, binding, and decapsulation outcome., Bob-side result containing private KEM output only after successful…, Return whether Alice was authenticated and all required KEMs were decapsulated., AuthenticatedKEMContributions (+36 more)

### Community 142 - "test_full_six_phase_handshake_crosses_pure_json_transport"
Cohesion: 0.14
Nodes (18): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a public response from a transport mapping., Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature. (+10 more)

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

## Knowledge Gaps
- **289 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+284 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1154 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `BB84PostprocessingConfig`, `adapters.py`, `BaseRNG`, `run_qkd_profile`, `SessionConfig`, `test_measures.py`, `reconcile_cascade`, `verify_reconciled_keys`, `BB84Protocol`, `InterceptResendAttack`, `estimate_qber_from_sample`, `postprocessing/__init__.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `test_key_schedule.py`, `PQCProfile`, `test_client_exchange.py`, `protocol/__init__.py`, `SignedServerKeyOffer`, `SessionConfig`, `orchestration/__init__.py`, `test_key_confirmation.py`, `MLDSAIdentity`, `ServerKeyOfferFactory`, `exchange.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `BB84Protocol` connect `BB84Protocol` to `BB84PostprocessingConfig`, `adapters.py`, `BaseRNG`, `bb84.py`, `run_qkd_profile`, `SessionConfig`, `orchestration/__init__.py`, `InterceptResendAttack`, `orchestration/profiles.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `SeededRNG` (e.g. with `test_qkd_only_profiles_require_an_explicit_application_key_schedule()` and `test_authenticated_ideal_bb84_completes()`) actually correct?**
  _`SeededRNG` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._