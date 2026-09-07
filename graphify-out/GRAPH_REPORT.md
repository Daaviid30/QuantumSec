# Graph Report - QuantumSec  (2026-09-07)

## Corpus Check
- 288 files · ~117,147 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2920 nodes · 7003 edges · 151 communities (123 shown, 23 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 303 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `793ff22a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- MLDSA65
- adapters.py
- test_initiator.py
- QuantumSec Serena Root Memory
- devDependencies
- ProjectiveMeasurement Class
- asymptotic_bb84_secret_length
- test_client_exchange.py
- BackendOperationError
- constants.py
- compilerOptions
- ResultsWorkspace.tsx
- dm_from_ket
- QuantumChannel
- hybrid/runner.py
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- InterceptResendAttack
- KrausChannel
- 3. Análisis Detallado de Hallazgos
- SeededRNG
- estimate_qber_from_sample
- .generate
- BB84SessionResult
- identity.py
- client.ts
- compilerOptions
- AppShell.tsx
- SessionResult
- AuthenticationEvidence
- SimulationConfigurator.tsx
- test_key_schedule.py
- PQCProfile
- authentication/base.py
- Adaptive Agents for QKD
- BaseRNG
- bb84.py
- BB84Result
- HybridPublicContext
- qkd/transcript.py
- ProtectedSession
- SimulatorPage.tsx
- PQCParty
- QuantumSec Web UI V1
- postprocessing/__init__.py
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
- BB84Protocol
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- SessionConfig
- UnsupportedAlgorithmError
- information.py
- ChannelPipeline
- copy_binary_vector
- ExperimentRecord
- PublicIdentity
- oqs_backend.py
- .__exit__
- _require_bytes
- SessionProfile
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- _OQSKEM
- test_server_offer.py
- pqc/core.md
- 3. Análisis Detallado de Hallazgos
- 3. Análisis Detallado de Hallazgos
- Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)
- QuantumSec TFM Goal
- 3. Análisis Detallado de Hallazgos
- runtime.py
- schemas.py
- BB84 security model
- Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)
- TrustedIdentityStore
- qber_by_basis
- orchestration/__init__.py
- .__exit__
- ui/core.md
- 3. Análisis Detallado de Hallazgos
- MLDSAAuthenticationContext
- capabilities.py
- verify_reconciled_keys
- export.py
- test_authentication.py
- _new_kem
- 13. Experiments
- AuthenticatedQKDSessionResult
- dm_from_ensemble
- experiments/__init__.py
- .apply
- validation.py
- 10. Security Model
- EXPERIMENTS.md
- wegman_carter.py
- PQCHandshakeTranscript
- .apply
- .apply
- test_api.py
- WegmanCarterAuthenticationContext
- DepolarizingChannel
- experiments/config.py
- .apply
- experiments/runner.py
- test_states.py
- ._active_ml_kem
- test_config.py
- amplify_privacy
- SignedServerKeyOffer
- BB84SessionStatus
- _InvalidOutputChannel
- EncapsulationResponse
- .__exit__
- _KEMSharedSecretStateBase
- _top_level_imports
- ._active_hqc
- health
- _final_key_string
- .__enter__

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 127 edges
2. `PQCParty` - 80 edges
3. `BB84Protocol` - 63 edges
4. `SignedServerKeyOffer` - 62 edges
5. `SessionConfig` - 55 edges
6. `PQCProfile` - 53 edges
7. `IdentityChannel` - 44 edges
8. `run_hybrid_session()` - 42 edges
9. `dm_from_ket()` - 42 edges
10. `BaseRNG` - 41 edges

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

## Communities (151 total, 23 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.08
Nodes (28): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking…, Validate that the input value is a byte string, raising a TypeError if it is…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs. (+20 more)

### Community 1 - "adapters.py"
Cohesion: 0.14
Nodes (22): ChannelSummary, post, _bb84_basis_value(), _channel_summary(), BB84SimulationRequest, BB84SimulationResponse, Adapters between typed HTTP data and the QuantumSec simulation domain., Narrow the general QKD Basis enum to BB84's two supported bases. (+14 more)

### Community 2 - "test_initiator.py"
Cohesion: 0.16
Nodes (22): Authenticate Bob's offer before producing Alice's KEM encapsulations., Verify a trusted responder and encapsulate only after authentication., ServerKeyOfferProcessor, FixtureRequest, parametrize, Tests for Alice-side authenticated processing of server KEM offers., _require_success(), test_alice_processing_never_decapsulates() (+14 more)

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
Nodes (29): InitiatorKEMState, Alice-local KEM secrets created only after authenticating the responder. Raw-…, _create_flow(), _Phase4Flow, _private_initiator_state(), _process(), parametrize, Tests for authenticated Alice responses and Bob-side KEM decapsulation. (+21 more)

### Community 8 - "BackendOperationError"
Cohesion: 0.05
Nodes (44): OQSKEMBackend, OQSKEMDetails, Adapter isolating the liboqs-python key-encapsulation API., Extract and validate a required metadata field from the liboqs algorithm…, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, Query and return validated metadata and buffer dimensions for a KEM algorithm…, Decapsulate a ciphertext using the provided secret key via liboqs to recover…, Immutable data structure storing algorithm parameters and buffer dimensions… (+36 more)

### Community 9 - "constants.py"
Cohesion: 0.14
Nodes (27): Project-wide numerical constants with no domain-layer dependencies., as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray (+19 more)

### Community 10 - "compilerOptions"
Cohesion: 0.08
Nodes (25): DOM, DOM.Iterable, ES2022, src, @testing-library/jest-dom, vite/client, vitest/globals, compilerOptions (+17 more)

### Community 11 - "ResultsWorkspace.tsx"
Cohesion: 0.16
Nodes (19): Panel(), PanelProps, SectionHeading(), SectionHeadingProps, StatusPill(), StatusPillProps, QubitInspector(), QubitInspectorProps (+11 more)

### Community 12 - "dm_from_ket"
Cohesion: 0.07
Nodes (44): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), _born_probabilities(), measure_projective() (+36 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.06
Nodes (47): _prepare_density_matrix(), ABC, ArrayLike, ComplexArray, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for composable channel stages acting on density matrices. A stage may…, Apply the channel to a density matrix. (+39 more)

### Community 14 - "hybrid/runner.py"
Cohesion: 0.07
Nodes (46): Enum, Exception, Establishment-to-data-plane adapter with explicit session-key ownership…, _hybrid_public_context_entries(), _pqc_outcome(), _qkd_outcome(), Orchestrate authenticated QKD and raw authenticated PQC contributions., Establish a hybrid key only after both source protocols and hybrid Finished… (+38 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.08
Nodes (29): CascadeConfig, CascadePassStatistics, CascadePublicEvent, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp (+21 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.06
Nodes (56): _compute_finished_verify_data(), _confirmation_key_info(), ConfirmedPQCHandshake, _finished_mac_input(), PQCConfirmationKeyDeriver, PQCConfirmationKeyState, PQCKeyConfirmation, Compute one Finished value with the standard-library HMAC-SHA-384 primitive. (+48 more)

### Community 17 - "api.ts"
Cohesion: 0.11
Nodes (20): futureSteps, mainSteps, QuantumFlow(), QuantumFlowProps, labels, SimulationControls(), SimulationControlsProps, AdversaryCapability (+12 more)

### Community 18 - "InterceptResendAttack"
Cohesion: 0.12
Nodes (16): Explicit adversarial stages for ordered QKD channel pipelines., AttackDiagnostics, InterceptResendAttack, Return an immutable simulator-only snapshot of cumulative counters., Reset aggregate counters without rewinding the injected RNG stream., Small immutable snapshot of simulator-only attack observations., Measure selected signals in a random BB84 basis and resend fresh states. The…, parametrize (+8 more)

### Community 19 - "KrausChannel"
Cohesion: 0.12
Nodes (16): Return a finite scalar probability in the closed unit interval., _validate_probability(), KrausChannel, ArrayLike, ComplexArray, A completely positive trace-preserving map validated at construction., Build a channel from a non-empty complete set of Kraus operators., Return the Hilbert-space dimension acted on by the channel. (+8 more)

### Community 20 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.14
Nodes (13): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1), [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`, [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack` (+5 more)

### Community 21 - "SeededRNG"
Cohesion: 0.12
Nodes (31): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+23 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.10
Nodes (20): _copy_bb84_bases(), estimate_qber_from_sample(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade., Return the common asymptotic bound used for mixed-basis candidates. In the… (+12 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (12): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+4 more)

### Community 25 - "identity.py"
Cohesion: 0.07
Nodes (26): Private and public identities for PQC authentication., Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Verify a signature against the message using this public identity's algorithm…, ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital… (+18 more)

### Community 26 - "client.ts"
Cohesion: 0.27
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), runBB84Simulation(), useCapabilities(), useSimulation(), SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.16
Nodes (12): App(), AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection (+4 more)

### Community 29 - "SessionResult"
Cohesion: 0.11
Nodes (6): _authentication_dict(), Self, Return whether this result no longer exposes live key material., Export accepted key bytes; QKD exact bit length remains in result metadata., SessionResult, SessionTrace

### Community 30 - "AuthenticationEvidence"
Cohesion: 0.14
Nodes (10): AuthenticationEvidence, AuthenticationVerification, AuthenticatorMetadata, DirectionalAuthenticator, ABC, Generate and verify evidence for one authenticated communication direction., MLDSADirectionalAuthenticator, ML-DSA-65 authentication of canonical QKD classical transcript checkpoints. (+2 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "test_key_schedule.py"
Cohesion: 0.06
Nodes (61): _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), derive_hkdf_sha384() (+53 more)

### Community 33 - "PQCProfile"
Cohesion: 0.05
Nodes (55): PQCProfile, PQCProfileDefinition, profile_definition(), StrEnum, Central QuantumSec deployment profiles for PQC handshakes., Enumeration of QuantumSec handshake profiles defining selected algorithm suites., Immutable algorithm suite specification for a QuantumSec PQC profile., Return the configured KEM names in canonical protocol order. (+47 more)

### Community 34 - "authentication/base.py"
Cohesion: 0.21
Nodes (14): assumed_authentication_result(), Explicit non-executed authentication result for the QKD baseline profile., AuthenticationMetrics, AuthenticationState, ClassicalAuthenticationResult, StrEnum, Common contracts for executed or explicitly assumed QKD classical…, authenticate_transcript_checkpoints() (+6 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BaseRNG"
Cohesion: 0.10
Nodes (20): BaseRNG, GlobalRNG, ABC, ndarray, random_basis(), random_bit(), Injectable random-number sources for reproducible simulations., Generate binary choices using this simulator's bias/correlation model. (+12 more)

### Community 37 - "bb84.py"
Cohesion: 0.09
Nodes (30): Seeded stochastic intercept-resend attack for logical-qubit BB84 signals., bases_from_bits(), Basis, basis_from_bit(), ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases., Map the QKD random-bit convention 0/1 to the Z/X basis. (+22 more)

### Community 38 - "BB84Result"
Cohesion: 0.10
Nodes (11): _optional_probability(), QBERByBasis, Immutable aggregate and BB84 basis-conditioned error metrics., BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting. (+3 more)

### Community 39 - "HybridPublicContext"
Cohesion: 0.11
Nodes (16): HybridPublicContext, create_finished(), HybridFinishedMessage, HybridFinishedRole, _mac_input(), StrEnum, Versioned, role-separated HMAC-SHA-384 Finished exchange for hybrid keys., verify_finished() (+8 more)

### Community 40 - "qkd/transcript.py"
Cohesion: 0.08
Nodes (30): Encode replay-relevant context without the authenticated payload., length_prefixed(), Canonical binary encoding helpers for upper-layer session protocols., Encode a non-negative integer at a fixed width., Encode bytes with an unsigned 64-bit big-endian length., unsigned(), QKD session orchestration and canonical public transcript contracts., StrEnum (+22 more)

### Community 41 - "ProtectedSession"
Cohesion: 0.05
Nodes (64): decrypt_aes_256_gcm(), encrypt_aes_256_gcm(), Strict AES-256-GCM primitive adapter backed by pyca/cryptography., Encrypt bytes and return ciphertext and the full 128-bit GCM tag separately., Authenticate then decrypt, propagating cryptography.exceptions.InvalidTag…, _validated_inputs(), canonical_data_plane_aad(), DataPlaneContext (+56 more)

### Community 42 - "SimulatorPage.tsx"
Cohesion: 0.32
Nodes (10): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage() (+2 more)

### Community 43 - "PQCParty"
Cohesion: 0.10
Nodes (27): Raised when an operation requires an identity from a peer not found in the…, UnknownTrustedPeerError, PQCParty, Self, Protocol participant holding a private signing identity and a trusted peer…, Validate that the party identity and trusted peer store instances are valid., Create a new party instance initialized with a fresh ML-DSA-65 signing identity., Return the owner name of this party's private identity. (+19 more)

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

### Community 50 - "AuthenticationFrame"
Cohesion: 0.21
Nodes (9): AuthenticationFrame, Canonical authentication unit binding payload to anti-replay context., _frame_bits(), NDArray, uint8, Authenticate one direction with fresh Toeplitz-selector and mask bits., Atomically reserve fresh bits for one unique authenticated frame context., WegmanCarterDirectionalAuthenticator (+1 more)

### Community 52 - "ExperimentConfig"
Cohesion: 0.20
Nodes (12): ExperimentConfig, One normalized instruction for an experimental session execution., Run ordered configurations sequentially, optionally shuffling reproducibly.…, run_batch(), e3_config(), experiment_runner(), fixture, qkd_config() (+4 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "BB84Protocol"
Cohesion: 0.09
Nodes (49): AuthenticationContext, AuthenticationTransportHook, Run BB84 and authenticate its public transcript according to ``profile``., run_qkd_profile(), _session_identifier(), IdentityChannel, Channel that returns an independent copy of the input state., BB84PostprocessingConfig (+41 more)

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
Cohesion: 0.12
Nodes (40): Normalized public configuration; runtime secrets belong in a separate context., SessionConfig, Non-serializable provisioned parties, QKD engine, secrets, and test boundaries., SessionExecutionContext, open_data_plane(), Transfer one established 256-bit session key into an AES-GCM runtime capability., Dispatch a normalized session config to its domain-specific adapter., run_session() (+32 more)

### Community 79 - "UnsupportedAlgorithmError"
Cohesion: 0.14
Nodes (19): Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., hqc(), ml_kem() (+11 more)

### Community 80 - "information.py"
Cohesion: 0.16
Nodes (23): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+15 more)

### Community 81 - "ChannelPipeline"
Cohesion: 0.15
Nodes (18): ChannelPipeline, ArrayLike, ComplexArray, Apply an immutable sequence of channels in order. An empty pipeline is defined…, Apply each component from first to last without mutating the input., test_empty_pipeline_is_an_identity_without_aliasing_input(), test_pipeline_composes_bit_and_phase_flips_in_order(), test_pipeline_composes_identity_channels() (+10 more)

### Community 82 - "copy_binary_vector"
Cohesion: 0.09
Nodes (35): Aggregate and per-basis quantum bit error rate metrics., Sampled QBER estimation with mandatory removal of disclosed key positions., Toeplitz-universal privacy amplification for reconciled QKD keys., generate_toeplitz_seed(), ArrayLike, NDArray, uint8, Efficient binary Toeplitz universal hashing for QKD post-processing. (+27 more)

### Community 83 - "ExperimentRecord"
Cohesion: 0.17
Nodes (7): ExperimentKind, StrEnum, ExperimentRecord, _freeze(), _freeze_mapping(), Immutable, versioned public evidence produced by one experiment run., _thaw()

### Community 84 - "PublicIdentity"
Cohesion: 0.06
Nodes (29): MLDSAIdentity, PublicIdentity, Self, Export the non-secret public identity suitable for peer trust stores., Generate an ML-DSA-65 signature over message bytes using this identity's…, Verify a message signature against an explicitly provided public identity., Return a safe string representation showing owner and algorithm without…, Immutable public verification identity associating an owner name with public… (+21 more)

### Community 85 - "oqs_backend.py"
Cohesion: 0.07
Nodes (26): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, OQSRuntimeVersions, _OQSSignature, BaseException (+18 more)

### Community 86 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the session-key reference idempotently without claiming memory…, Release the session key when leaving a managed lifetime.

### Community 87 - "_require_bytes"
Cohesion: 0.07
Nodes (15): Validate that the given identity name is a non-empty string and return its…, _validated_identity_name(), EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed. (+7 more)

### Community 88 - "SessionProfile"
Cohesion: 0.15
Nodes (27): canonical_hybrid_secret_input(), _expected_algorithms(), hybrid_component_metadata_bytes(), hybrid_kem_label(), HybridSecretComponent, Unambiguous encoding of independently established QKD and KEM contributions., Return encoded bytes attributable to one component's non-secret…, Return the canonical hybrid label for a supported KEM algorithm. (+19 more)

### Community 90 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.12
Nodes (16): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Recomendaciones de Priorización, [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto, [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`, Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica) (+8 more)

### Community 91 - "_OQSKEM"
Cohesion: 0.12
Nodes (10): _KEMFactory, _OQSKEM, _OQSModule, BaseException, Protocol, Self, TracebackType, Protocol defining the interface for a liboqs KeyEncapsulation context manager. (+2 more)

### Community 92 - "test_server_offer.py"
Cohesion: 0.14
Nodes (22): OfferCreation, bob(), high_creation(), low_creation(), fixture, FixtureRequest, parametrize, Tests for ephemeral responder state and authenticated ServerKeyOffer messages. (+14 more)

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

### Community 100 - "runtime.py"
Cohesion: 0.29
Nodes (4): ExperimentRuntime, Runtime-only provisioning for experiment configurations., Public description of provisioning policy; it never contains key material., RuntimeProvisioning

### Community 101 - "schemas.py"
Cohesion: 0.18
Nodes (16): BaseModel, model_validator, AmplitudeDampingChannelConfiguration, ApiError, AttackDiagnosticsSummary, BitFlipChannelConfiguration, DepolarizingChannelConfiguration, IdentityChannelConfiguration (+8 more)

### Community 102 - "BB84 security model"
Cohesion: 0.14
Nodes (13): AES-256-GCM data plane, Analytical channel expectations, BB84 security model, Classical-channel authentication profiles, Hybrid session composition, Intercept-resend threat model, Key and parameter-estimation model, ML-DSA-65 checkpoint authentication (+5 more)

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - "TrustedIdentityStore"
Cohesion: 0.09
Nodes (17): Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, Generate a new named private ML-DSA-65 signing identity with fresh…, Named PQC parties with signing and pre-provisioned verification trust., Return the explicit store of trusted peer identities configured for this party., Explicit pre-provisioned trust for public PQC identities., Thread-safe in-memory registry mapping peer names to pre-provisioned trusted…, Initialize an empty trusted identity store. (+9 more)

### Community 105 - "qber_by_basis"
Cohesion: 0.20
Nodes (15): QKD metric computations., ArrayLike, ndarray, qber(), qber_by_basis(), Return the differing-bit fraction for two aligned non-empty binary keys. An…, Return Z, X, and aggregate QBER without inventing absent-basis values., parametrize (+7 more)

### Community 106 - "orchestration/__init__.py"
Cohesion: 0.13
Nodes (18): Versioned public configuration for common QuantumSec session execution., Runtime-only capabilities kept separate from reproducible public configuration., Authenticated public context binding every hybrid session input., Upper-layer composition of independent QKD and PQC domain modules., CapabilityStatus, EstablishmentSource, StrEnum, qkd_profile_definition() (+10 more)

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.13
Nodes (14): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Aspectos Positivos y Fortalezas del Diseño, 5. Recomendaciones de Calidad, Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6), [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`, [L-02] Validación tardía de `session.is_closed` en `open_data_plane` (+6 more)

### Community 110 - "MLDSAAuthenticationContext"
Cohesion: 0.15
Nodes (7): AuthenticationSessionRegistry, AuthenticationSessionReplayError, RuntimeError, Raised when a session identifier is reused within persistent authentication…, Thread-safe replay registry that contains identifiers, never authentication…, MLDSAAuthenticationContext, Pre-provisioned bilateral ML-DSA identities and peer trust stores.

### Community 111 - "capabilities.py"
Cohesion: 0.18
Nodes (16): ParameterCapability, get_capabilities(), _probability(), project_version(), CapabilitiesResponse, Capability discovery backed by the features that exist in the repository., Return the installed project version with a source-tree fallback., Describe implemented and planned features without implying future support. (+8 more)

### Community 112 - "verify_reconciled_keys"
Cohesion: 0.21
Nodes (10): ArrayLike, Immutable public key-agreement verification data and protocol decision., Return the number of public Alice tag bits., Verify reconciled-key agreement using public Toeplitz-universal hash tags. The…, VerificationResult, verify_reconciled_keys(), test_different_keys_fail_for_deterministic_hash_setup(), test_equal_keys_verify_and_tag_leakage_is_tracked() (+2 more)

### Community 113 - "export.py"
Cohesion: 0.16
Nodes (23): ArgumentParser, main(), _parser(), Minimal command-line interface for reproducible QuantumSec runs., _canonical_cell(), _csv_value(), dumps_csv(), dumps_json() (+15 more)

### Community 114 - "test_authentication.py"
Cohesion: 0.30
Nodes (16): _frame(), _ml_dsa_authenticator(), parametrize, test_ml_dsa_rejects_missing_signature(), test_ml_dsa_rejects_modified_or_cross_context_frame(), test_ml_dsa_rejects_modified_signature(), test_ml_dsa_rejects_unknown_identity(), test_ml_dsa_rejects_wrong_public_identity() (+8 more)

### Community 115 - "_new_kem"
Cohesion: 0.15
Nodes (12): _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMEncapsulation, OQSKEMKeyPair, Initialize and return a new liboqs KeyEncapsulation instance for the specified…, Generate a fresh key pair for the specified KEM algorithm using liboqs., Encapsulate a secret against the public key via liboqs, returning ciphertext… (+4 more)

### Community 116 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

### Community 117 - "AuthenticatedQKDSessionResult"
Cohesion: 0.21
Nodes (7): AuthenticatedQKDSessionResult, _optional_key_copy(), NDArray, uint8, Return defensive immutable copies only for an accepted session., Serialize bounded public metadata, never transcript payloads or key material., Terminal QKD decision; key fields exist only after all required checks pass.

### Community 118 - "dm_from_ensemble"
Cohesion: 0.29
Nodes (7): dm_from_ensemble(), ArrayLike, ComplexArray, Construct a density matrix from a finite ensemble of pure states. Parameters…, Validate that a ket represents a normalized pure quantum state., validate_quantum_state(), test_validate_quantum_state()

### Community 119 - "experiments/__init__.py"
Cohesion: 0.23
Nodes (12): Reproducible, secret-free experimental execution for QuantumSec., median_iqr(), Small statistical summaries required by the first experiment campaigns., Summarize finite values with NumPy's linear percentile convention., Return the two-sided Wilson score interval (not Clopper-Pearson exact)., TimingSummary, wilson_interval(), WilsonInterval (+4 more)

### Community 120 - ".apply"
Cohesion: 0.50
Nodes (4): _immutable_density(), ArrayLike, ComplexArray, Possibly intercept one qubit, then return a fresh transmitted state.

### Community 122 - "validation.py"
Cohesion: 0.09
Nodes (47): _error_density_matrix(), _error_normalized_state(), _error_probability_state(), _error_projective_measurement(), _error_projector(), _error_unitary(), is_density_matrix(), is_normalized_state() (+39 more)

### Community 123 - "10. Security Model"
Cohesion: 0.40
Nodes (5): 10. Security Model, Adversary boundary, PQC and hybrid boundary, QBER and secret-length model, QKD boundary

### Community 124 - "EXPERIMENTS.md"
Cohesion: 0.15
Nodes (11): Batch and statistics, CLI, Configuration, Environment and record schema, Metrics and exports, Reproducible Experiment Engine V1, Runtime and secret lifecycle, test_environment_snapshot_contains_reproducibility_context() (+3 more)

### Community 125 - "wegman_carter.py"
Cohesion: 0.28
Nodes (8): AuthenticationMaterialError, AuthenticationMaterialExhaustedError, AuthenticationMaterialReuseError, RuntimeError, One-time universal-hash authentication for QKD classical checkpoints. The…, Base error for unsafe or unavailable authentication material., Raised before a tag operation that would exceed the provisioned PSK., Raised when a frame context attempts to consume authentication bits twice.

### Community 126 - "PQCHandshakeTranscript"
Cohesion: 0.08
Nodes (19): AuthenticatedKEMContributions, issue_initiator_hybrid_contributions(), issue_responder_hybrid_contributions(), Consumable capability issued only for an authenticated exact PQC transcript., Return defensive secret copies once and retire the capability., Consume Alice's state only after its authenticated transcript binding validates., Consume Bob's state only after its authenticated transcript binding validates., _transcript() (+11 more)

### Community 127 - ".apply"
Cohesion: 0.32
Nodes (5): ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply Pauli noise to a single-qubit density matrix., Apply bit-flip noise to a single-qubit density matrix.

### Community 128 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 130 - "WegmanCarterAuthenticationContext"
Cohesion: 0.11
Nodes (8): PreSharedAuthenticationMaterial, Self, Bilateral, direction-separated PSK material for one or more QKD sessions., Provision matching but independent copies for each communication direction., Consumable PSK bit stream whose contents are never exposed or serialized., WegmanCarterAuthenticationContext, test_psk_representation_never_contains_secret(), test_wegman_carter_context_enforces_directional_key_separation()

### Community 131 - "DepolarizingChannel"
Cohesion: 0.14
Nodes (20): DepolarizingChannel, ArrayLike, ComplexArray, Single-qubit channel ``E(rho) = (1 - p) rho + p I/2``. The parameter satisfies…, Apply depolarizing noise to a single-qubit density matrix., assert_valid_qubit_density_matrix(), parametrize, test_amplitude_damping_extremes_and_fixed_ground_state() (+12 more)

### Community 132 - "experiments/config.py"
Cohesion: 0.57
Nodes (7): _integer(), _number(), _optional_integer(), _postprocessing_from_public_dict(), Strict, versioned, secret-free experiment configuration., _reject_unknown(), _session_from_public_dict()

### Community 133 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Return the same physical state without aliasing the input array.

### Community 134 - "experiments/runner.py"
Cohesion: 0.20
Nodes (9): _distribution_version(), ExperimentEnvironment, _git_commit(), _quantumsec_version(), Best-effort environment snapshots that contextualize experimental evidence., Copy public evidence before the caller closes the live session capability., Thin observer around the common session runner., oqs_runtime_versions() (+1 more)

### Community 135 - "test_states.py"
Cohesion: 0.43
Nodes (5): parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 136 - "._active_ml_kem"
Cohesion: 0.33
Nodes (3): Return the active ML-KEM provider instance or raise RuntimeError if state is…, Return the public ML-KEM encapsulation key associated with this responder…, Decapsulate an ML-KEM ciphertext with this session's private key.

### Community 137 - "test_config.py"
Cohesion: 0.21
Nodes (12): _invalid_stage(), config_from_json(), configs_from_json(), load_config_json(), _loads_without_duplicate_keys(), Path, test_config_rejects_obvious_ambiguities(), test_config_round_trip_preserves_normalized_meaning() (+4 more)

### Community 138 - "amplify_privacy"
Cohesion: 0.17
Nodes (11): amplify_privacy(), PrivacyAmplificationResult, ArrayLike, Immutable final keys and public Toeplitz seed metadata., Hash both reconciled keys to an explicitly derived target length., Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, parametrize, test_privacy_amplification_agrees_and_respects_target_length() (+3 more)

### Community 139 - "SignedServerKeyOffer"
Cohesion: 0.07
Nodes (31): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeFactory, Package and sign Alice's already-created Phase 3 public encapsulation response., Bind a successful Phase 3 response to Bob's exact offer and sign it as Alice., ProcessedServerOffer, StrEnum, Authentication outcome produced before any Alice-side response is sent., Alice-side authentication outcome and optional private/public KEM outputs. (+23 more)

### Community 140 - "BB84SessionStatus"
Cohesion: 0.33
Nodes (5): BB84SessionStatus, StrEnum, Terminal state of a complete BB84 session., A basis average must not authorize extraction on an asymmetric channel., test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error()

### Community 141 - "_InvalidOutputChannel"
Cohesion: 0.40
Nodes (4): _InvalidOutputChannel, ArrayLike, ComplexArray, test_bb84_validates_the_injected_channels_output_by_default()

### Community 142 - "EncapsulationResponse"
Cohesion: 0.16
Nodes (13): _decode_base64_field(), EncapsulationResponse, Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Unsigned public KEM ciphertext message prepared for the next phase., Serialize this public response to a JSON-compatible mapping., Restore and validate a public response from a transport mapping. (+5 more)

### Community 143 - ".__exit__"
Cohesion: 0.32
Nodes (5): BaseException, TracebackType, Release the confirmation key when leaving its managed lifetime., Close the owned session-key state idempotently., Close the session key when leaving the managed lifetime.

### Community 144 - "_KEMSharedSecretStateBase"
Cohesion: 0.12
Nodes (11): _KEMSharedSecretStateBase, BaseException, Self, TracebackType, Release secret references when leaving a managed lifetime., Internal validated storage shared by initiator and responder secret states., Return whether the private shared-secret references were released., Release secret references idempotently without claiming memory zeroization. (+3 more)

### Community 145 - "_top_level_imports"
Cohesion: 0.80
Nodes (4): Path, test_data_protection_is_independent_from_establishment_domains(), test_qkd_and_pqc_remain_independent_lower_domains(), _top_level_imports()

### Community 154 - "health"
Cohesion: 0.50
Nodes (4): get, HealthResponse, health(), HealthResponse

### Community 156 - "_final_key_string"
Cohesion: 0.50
Nodes (4): _final_key_string(), NDArray, uint8, Serialize a completed simulator key as a binary string for inspection.

## Knowledge Gaps
- **295 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+290 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1199 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SeededRNG` connect `SeededRNG` to `test_api.py`, `adapters.py`, `runtime.py`, `BaseRNG`, `BB84Protocol`, `amplify_privacy`, `SessionConfig`, `dm_from_ket`, `QuantumChannel`, `BB84SessionStatus`, `_InvalidOutputChannel`, `reconcile_cascade`, `export.py`, `InterceptResendAttack`, `ChannelPipeline`, `copy_binary_vector`, `verify_reconciled_keys`, `estimate_qber_from_sample`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `DerivedSessionKeyState` connect `SignedServerKeyOffer` to `test_key_schedule.py`, `PQCProfile`, `test_key_confirmation.py`, `.__exit__`, `_require_bytes`, `PQCHandshakeTranscript`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `PQCParty` connect `PQCParty` to `test_key_schedule.py`, `PQCProfile`, `test_initiator.py`, `runtime.py`, `test_client_exchange.py`, `TrustedIdentityStore`, `orchestration/__init__.py`, `SignedServerKeyOffer`, `SessionConfig`, `hybrid/runner.py`, `test_key_confirmation.py`, `PublicIdentity`, `test_server_offer.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `SeededRNG` (e.g. with `ExperimentRuntimeFactory` and `build_channel_pipeline()`) actually correct?**
  _`SeededRNG` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `BB84Protocol` (e.g. with `BaseRNG` and `Basis`) actually correct?**
  _`BB84Protocol` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 11 INFERRED edges - model-reasoned connections that need verification._