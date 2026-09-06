# Graph Report - QuantumSec  (2026-09-06)

## Corpus Check
- 214 files · ~89,321 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2173 nodes · 4575 edges · 126 communities (100 shown, 22 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 218 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9542f9c2`
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
- _OQSKEM
- compilerOptions
- ResultsWorkspace.tsx
- test_measures.py
- QuantumChannel
- as_ket
- reconcile_cascade
- test_key_confirmation.py
- api.ts
- KrausChannel
- test_noise.py
- dm_from_ket
- SeededRNG
- estimate_qber_from_sample
- .generate
- BB84SessionResult
- registry.py
- client.ts
- compilerOptions
- AppShell.tsx
- test_server_offer.py
- test_bb84.py
- SimulationConfigurator.tsx
- PQCHandshakeTranscript
- PQCProfile
- qber_by_basis
- Adaptive Agents for QKD
- BaseRNG
- bb84.py
- BB84Result
- SimulatorPage.tsx
- PublicIdentity
- BitFlipChannel
- ChannelPipeline.tsx
- test_initiator.py
- QuantumSec Web UI V1
- sift_keys
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
- constants.py
- QuantumSec Conventions Memory
- quantumsec
- QuantumSec Two-Service Web Architecture
- QuantumSec Project Structure and Architectural Blueprint
- identity.py
- UnsupportedAlgorithmError
- Revisión independiente del TFM — QuantumSec
- amplify_privacy
- .create
- oqs_kem_backend.py
- PQCParty
- oqs_backend.py
- .__exit__
- .__exit__
- GlobalRNG
- backends/__init__.py
- 3. Análisis Detallado de Hallazgos
- PQCConfirmationKeyState
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
- .apply
- _prepare_density_matrix
- operations.py
- .__exit__
- ui/core.md
- Recommended Changes to TFM_GOAL.md
- Clasificación
- .run
- EstablishedPQCSession
- Security Concerns / Overclaims
- 13. Experiments
- .apply
- Executive Assessment
- .__enter__
- Scope Matrix
- 10. Security Model
- Problems I Found
- Recommended Research Question
- Up to Three Improvements Worth Adding
- .__enter__
- Recommended Security Profiles

## God Nodes (most connected - your core abstractions)
1. `SeededRNG` - 86 edges
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

## Communities (126 total, 22 thin omitted)

### Community 0 - "MLDSA65"
Cohesion: 0.09
Nodes (27): MonkeyPatch, OQSSignatureBackend, Low-level adapter managing liboqs signature contexts, key generation, signing,…, MLDSA65, Self, Return a safe string representation with public key length without leaking…, Validate that the input value is a byte string, raising a TypeError if it is…, ML-DSA-65 (NIST FIPS 204) digital signature provider backed by liboqs. (+19 more)

### Community 1 - "adapters.py"
Cohesion: 0.06
Nodes (61): BaseModel, ChannelSummary, get, HealthResponse, model_validator, ParameterCapability, post, _bb84_basis_value() (+53 more)

### Community 2 - "validation.py"
Cohesion: 0.06
Nodes (73): _as_square_matrix(), fidelity(), _prepare_pair(), _psd_matrix_sqrt(), purity(), ArrayLike, ComplexArray, Quantum-information metrics for density matrices. (+65 more)

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
Cohesion: 0.11
Nodes (35): _decode_base64_field(), Self, Restore and validate an offer from its JSON-compatible mapping., Deserialize a signed server key offer from a dictionary without verifying…, Restore and validate a client exchange from a transport mapping., Decode a Base64-encoded string into raw bytes, raising ValueError if the data…, Deserialize a signed client exchange without authenticating its signature., Ensure all required transport keys exist in the provided payload dictionary. (+27 more)

### Community 8 - "BackendOperationError"
Cohesion: 0.06
Nodes (37): OQSKEMBackend, Low-level adapter managing liboqs KeyEncapsulation contexts and cryptographic…, BackendOperationError, Domain errors for post-quantum cryptographic operations., Raised when an active post-quantum cryptography backend fails during execution., KEMEncapsulation, KEMMetadata, KEMProvider (+29 more)

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
Cohesion: 0.07
Nodes (41): Any, _elapsed(), main(), Benchmark safe and fast projective sampling paths for one-qubit signals., Print best-of-repeat wall times for the requested signal counts., run_benchmark(), _born_probabilities(), measure_projective() (+33 more)

### Community 13 - "QuantumChannel"
Cohesion: 0.18
Nodes (13): ABC, QuantumChannel, Base interface and shared input handling for quantum channels., Interface for deterministic channels acting on density matrices., Ideal quantum channel., Public quantum-channel API for QKD simulations., Reusable operator-sum representation of CPTP quantum channels., Single-qubit amplitude-damping noise. (+5 more)

### Community 14 - "as_ket"
Cohesion: 0.15
Nodes (26): as_ket(), inner_product(), normalize(), outer_product(), probabilities_from_ket(), ArrayLike, ComplexArray, RealArray (+18 more)

### Community 15 - "reconcile_cascade"
Cohesion: 0.09
Nodes (27): CascadeConfig, CascadePassStatistics, _initial_block_size(), _parity(), _PassLayout, ArrayLike, intp, NDArray (+19 more)

### Community 16 - "test_key_confirmation.py"
Cohesion: 0.10
Nodes (40): ConfirmedPQCHandshake, PQCKeyConfirmation, Capability produced only after both role-separated Finished MACs verify., Enforce the Bob-Finished, Alice-Finished, mutual-confirmation order., Create Bob's first Finished flight exactly once., Verify Bob before creating Alice's chained Finished response., Verify Alice's chained Finished and produce mutual-confirmation proof., Materialize one role-local session only from the completed Finished exchange. (+32 more)

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
Cohesion: 0.19
Nodes (16): ChannelPipeline, Apply an immutable sequence of channels in order. An empty pipeline is defined…, dm_from_ensemble(), dm_from_ket(), ArrayLike, ComplexArray, Construction helpers for quantum density matrices., Construct the pure-state density matrix ``|psi><psi|``. (+8 more)

### Community 21 - "SeededRNG"
Cohesion: 0.10
Nodes (36): QRNGSimulator, random_unitary(), Generate a Haar-distributed random unitary using QR decomposition., Deterministic PRNG for reproducible simulations and tests., Return the generator initialized with this instance's seed., Simulate a physical QRNG with bias and Markovian correlation., Return the generator supplied by the base random source., SeededRNG (+28 more)

### Community 22 - "estimate_qber_from_sample"
Cohesion: 0.09
Nodes (20): _copy_bb84_bases(), estimate_qber_from_sample(), _explicit_stratified_counts(), ParameterEstimationResult, ArrayLike, ndarray, Return aggregate sampled QBER as a backwards-compatible alias., Return the aggregate sampled bit-error rate used to configure Cascade. (+12 more)

### Community 24 - "BB84SessionResult"
Cohesion: 0.06
Nodes (12): BB84SessionResult, intp, NDArray, uint8, Return Bob's measured outcomes under the raw-key naming convention., Return raw positions where Alice and Bob selected the same basis., Return Alice's key after basis reconciliation., Return Bob's key after basis reconciliation. (+4 more)

### Community 25 - "registry.py"
Cohesion: 0.08
Nodes (23): ABC, Self, Backend-independent signature contracts and metadata., Immutable specification and buffer dimensions for a post-quantum digital…, Validate metadata text fields and ensure category and buffer sizes are positive…, Abstract base contract defining post-quantum digital signature operations., Generate a fresh signing key pair using secure cryptographic backend randomness., Return the public algorithm metadata and key/signature buffer dimensions. (+15 more)

### Community 26 - "client.ts"
Cohesion: 0.25
Nodes (10): getCapabilities(), getHealth(), QuantumSecApiError, requestJson(), App(), useCapabilities(), root, SimulatorPageProps (+2 more)

### Community 27 - "compilerOptions"
Cohesion: 0.14
Nodes (13): node, vite.config.ts, vitest.config.ts, compilerOptions, allowImportingTsExtensions, composite, module, moduleResolution (+5 more)

### Community 28 - "AppShell.tsx"
Cohesion: 0.21
Nodes (10): AppShell(), AppShellProps, Header(), HeaderProps, QuantumMark(), NavigationItem, NavigationSection, sections (+2 more)

### Community 29 - "test_server_offer.py"
Cohesion: 0.17
Nodes (19): OfferCreation, bob(), high_creation(), low_creation(), fixture, Tests for ephemeral responder state and authenticated ServerKeyOffer messages., test_bob_signs_canonical_offer_with_existing_identity(), test_canonical_serialization_is_deterministic_and_domain_separated() (+11 more)

### Community 30 - "test_bb84.py"
Cohesion: 0.06
Nodes (48): IdentityChannel, ArrayLike, ComplexArray, Channel that returns an independent copy of the input state., Return the same physical state without aliasing the input array., BB84PostprocessingConfig, BB84Protocol, BB84SessionStatus (+40 more)

### Community 31 - "SimulationConfigurator.tsx"
Cohesion: 0.24
Nodes (8): ResultsWorkspace(), ProtocolSelector(), ProtocolSelectorProps, SimulationConfigurator(), SimulationConfiguratorProps, capabilitiesFixture, resultFixture, ProtocolCapability

### Community 32 - "PQCHandshakeTranscript"
Cohesion: 0.17
Nodes (5): PQCHandshakeTranscript, Encode the exact signed server and client messages in fixed protocol order., Return the public SHA-384 digest of this canonical authenticated transcript., Immutable authenticated public context shared by Alice and Bob., Serialize this public transcript to a JSON-compatible mapping.

### Community 33 - "PQCProfile"
Cohesion: 0.05
Nodes (54): _length_prefixed(), Internal canonical binary encoding primitives shared across PQC domains., Prefix bytes with an unsigned 32-bit big-endian length., canonical_kem_secret_input(), Unambiguous profile-aware encoding of independently established KEM secrets., Encode LOW/HIGH KEM secrets with fixed algorithm order and explicit boundaries.…, _validated_secret(), Canonical KEM input construction and HKDF primitives for QuantumSec. (+46 more)

### Community 34 - "qber_by_basis"
Cohesion: 0.16
Nodes (18): _optional_probability(), ArrayLike, ndarray, qber(), qber_by_basis(), QBERByBasis, Aggregate and per-basis quantum bit error rate metrics., Immutable aggregate and BB84 basis-conditioned error metrics. (+10 more)

### Community 35 - "Adaptive Agents for QKD"
Cohesion: 0.36
Nodes (10): Adaptive Agents for QKD, Adaptive Channel Agent, Experiment Orchestrator Agent, Layer-Local Agent Placement, Multi-Agent QKDN Coordination, Observe-Decide-Act Loop, Protocol Controller Agent, QKDN Routing Agent (+2 more)

### Community 36 - "BaseRNG"
Cohesion: 0.07
Nodes (46): BaseRNG, ABC, Injectable random-number sources for reproducible simulations., Return the underlying NumPy generator., Common interface for random sources backed by a NumPy generator., Classical QKD post-processing algorithms and immutable transcripts., Sampled QBER estimation with mandatory removal of disclosed key positions., PrivacyAmplificationResult (+38 more)

### Community 37 - "bb84.py"
Cohesion: 0.10
Nodes (26): Enum, bases_from_bits(), Basis, basis_from_bit(), integer, ndarray, Named basis conventions used by QKD protocols., Standard single-qubit measurement bases. (+18 more)

### Community 38 - "BB84Result"
Cohesion: 0.11
Nodes (8): BB84Result, Return Alice's BB84 bases aligned with the sifted key., Return the number of quantum signals sent by Alice., Return the number of positions retained after sifting., Return the fraction of raw positions retained after sifting., Return aggregate simulator-diagnostic QBER over the complete sifted key. This…, Return simulator-only Z, X, and aggregate full-sifted QBER., Immutable raw and sifted material produced by one complete BB84 run.

### Community 39 - "SimulatorPage.tsx"
Cohesion: 0.47
Nodes (6): runBB84Simulation(), useSimulation(), createChannelDraft(), serializeChannels(), validateChannels(), SimulatorPage()

### Community 40 - "PublicIdentity"
Cohesion: 0.10
Nodes (12): PublicIdentity, Export the non-secret public identity suitable for peer trust stores., Verify a message signature against an explicitly provided public identity., Immutable public verification identity associating an owner name with public…, Verify a signature against the message using this public identity's algorithm…, Serialize this public identity into a JSON-compatible dictionary with…, Return this party's public identity for distribution and registration in peer…, Add a peer's public identity to this party's trusted store with optional… (+4 more)

### Community 41 - "BitFlipChannel"
Cohesion: 0.12
Nodes (14): BitFlipChannel, PauliChannel, PhaseFlipChannel, ArrayLike, ComplexArray, Apply phase-flip noise to a single-qubit density matrix., Apply an incoherent mixture of the single-qubit Pauli operators. The identity…, Return the implied identity probability. (+6 more)

### Community 42 - "ChannelPipeline.tsx"
Cohesion: 0.50
Nodes (6): ChannelCard(), ChannelCardProps, ChannelPipeline(), ChannelPipelineProps, ChannelCapability, ChannelDraft

### Community 43 - "test_initiator.py"
Cohesion: 0.18
Nodes (21): Authenticate Bob's offer before producing Alice's KEM encapsulations., ServerKeyOfferProcessor, Restore and validate a public response from a transport mapping., FixtureRequest, parametrize, Tests for Alice-side authenticated processing of server KEM offers., _require_success(), test_alice_processing_never_decapsulates() (+13 more)

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
Cohesion: 0.12
Nodes (17): MLDSAIdentity, Self, Generate a new named private ML-DSA-65 signing identity with fresh…, Return public algorithm metadata and key lengths for this identity's ML-DSA-65…, Generate an ML-DSA-65 signature over message bytes using this identity's…, Return a safe string representation showing owner and algorithm without…, Deserialize and validate a public identity from a JSON-compatible dictionary…, Named private identity holding an ML-DSA-65 signing capability and associated… (+9 more)

### Community 52 - "SignedServerKeyOffer"
Cohesion: 0.04
Nodes (63): Post-quantum identity, authentication, KEM, and key-establishment primitives., ClientKeyExchangeFactory, ClientKeyExchangeProcessingStatus, ClientKeyExchangeProcessor, ProcessedClientKeyExchange, StrEnum, Authenticated Alice-to-Bob KEM response processing for staged PQC handshakes., Package and sign Alice's already-created Phase 3 public encapsulation response. (+55 more)

### Community 53 - "3. Análisis Detallado de Hallazgos"
Cohesion: 0.11
Nodes (18): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño, 5. Conclusiones y Próximos Pasos Recomendados, [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`), [H-02] Arrays constantes globales mutables en primitivas QKD, [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG` (+10 more)

### Community 54 - "quantum.information Module"
Cohesion: 0.50
Nodes (4): quantum.information Module, Report: Quantum Information Measures, Quantum Information Test Suite, Report: Quantum Information Tests

### Community 55 - "QuantumSec Web UI Architecture"
Cohesion: 0.67
Nodes (4): QuantumSec UI HTML Entry Point, BB84 Simulation REST API, QuantumSec Web UI V1 Documentation, QuantumSec Web UI Architecture

### Community 70 - "constants.py"
Cohesion: 0.31
Nodes (6): Project-wide numerical constants with no domain-layer dependencies., parametrize, test_dm_from_ensemble(), test_dm_from_ensemble_rejects_invalid_inputs(), test_dm_from_ket(), test_dm_from_ket_rejects_invalid_quantum_states()

### Community 71 - "QuantumSec Conventions Memory"
Cohesion: 0.20
Nodes (10): Cryptographic Helper Functions, RNG Architecture Design Principles, QuantumSec RNG Architecture Manual, Core Design Principles and Boundary Rules, QuantumSec Conventions Memory, Layered Dependency Discipline, Injected RNG Convention, Validation Policy and Error Types (+2 more)

### Community 73 - "QuantumSec Two-Service Web Architecture"
Cohesion: 0.40
Nodes (6): QuantumSec Two-Service Web Architecture, QuantumSec Deployment Guide, PQC liboqs Windows & Linux Toolchain, Production Systemd & Nginx Deployment, Query: Web UI Construction Prompt, QuantumSec Web Laboratory

### Community 74 - "QuantumSec Project Structure and Architectural Blueprint"
Cohesion: 0.18
Nodes (14): BB84 Classical Post-Processing Pipeline Spec, CPTP Noise vs Optical Loss Architectural Separation, QuantumSec Project Structure and Architectural Blueprint, ProjectiveMeasurement & Sampling Refactor Spec, Quantum Channel & BB84 Foundation Milestone, Quantum Information Metrics Specification, QuantumSec Development Task Roadmap, Query: Initial Bitstring Length & BB84 Signals (+6 more)

### Community 75 - "identity.py"
Cohesion: 0.17
Nodes (6): Private and public identities for PQC authentication., Validate that the given identity name is a non-empty string and return its…, Validate owner, algorithm, and public key buffer dimensions, storing an…, Validate the owner name and ensure the internal signer is an MLDSA65 instance., _validated_identity_name(), Return the trusted public identity for an owner, raising…

### Community 79 - "UnsupportedAlgorithmError"
Cohesion: 0.09
Nodes (23): Raised when a requested post-quantum algorithm is unsupported or disabled in…, UnsupportedAlgorithmError, HQC3, Ephemeral HQC-3 key encapsulation provider backed by liboqs for NIST Category 3…, Return cached algorithm metadata and expected key/ciphertext dimensions for…, MLKEM768, Ephemeral ML-KEM-768 key encapsulation provider backed by liboqs., Return cached algorithm metadata and expected key/ciphertext dimensions for ML-… (+15 more)

### Community 80 - "Revisión independiente del TFM — QuantumSec"
Cohesion: 0.17
Nodes (11): 6,5 / 10, Documentation Problems, Fuentes, Métricas medidas de referencia, Nota de procedimiento, Proposed Thesis Title, Revisión independiente del TFM — QuantumSec, Strongest Thesis Contribution (+3 more)

### Community 81 - "amplify_privacy"
Cohesion: 0.25
Nodes (9): amplify_privacy(), ArrayLike, Hash both reconciled keys to an explicitly derived target length., Run BB84 through estimation, Cascade, verification, and extraction. Legitimate…, parametrize, test_privacy_amplification_agrees_and_respects_target_length(), test_privacy_amplification_handles_zero_target_explicitly(), test_privacy_amplification_rejects_invalid_target() (+1 more)

### Community 82 - ".create"
Cohesion: 0.25
Nodes (8): Self, Create a new party instance initialized with a fresh ML-DSA-65 signing identity., test_factory_rejects_failed_phase3_result(), alice(), bob(), high_offer(), low_offer(), fixture

### Community 83 - "oqs_kem_backend.py"
Cohesion: 0.08
Nodes (26): Exception, _ensure_kem_algorithm_enabled(), _load_oqs(), _new_kem(), OQSKEMDetails, OQSKEMEncapsulation, OQSKEMKeyPair, _OQSModule (+18 more)

### Community 84 - "PQCParty"
Cohesion: 0.06
Nodes (33): Raised when an operation requires an identity from a peer not found in the…, Raised when adding an identity for an existing peer without overwrite…, TrustedIdentityConflictError, UnknownTrustedPeerError, PQCParty, Named PQC parties with signing and pre-provisioned verification trust., Protocol participant holding a private signing identity and a trusted peer…, Validate that the party identity and trusted peer store instances are valid. (+25 more)

### Community 85 - "oqs_backend.py"
Cohesion: 0.07
Nodes (22): _ensure_signature_algorithm_enabled(), _load_oqs(), _new_signature(), OQSKeyPair, _OQSModule, _OQSSignature, BaseException, Protocol (+14 more)

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

### Community 91 - "PQCConfirmationKeyState"
Cohesion: 0.08
Nodes (17): _compute_finished_verify_data(), PQCConfirmationKeyState, Compute one Finished value with the standard-library HMAC-SHA-384 primitive., Require a live Phase 5 key state bound to the exact Phase 6 transcript., Private role-local Phase 6 key and Finished state machine., Return whether the private confirmation-key reference was released., Return whether this state has released its role-local confirmation key., Return whether this role completed its local send/verify Finished work. (+9 more)

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
Cohesion: 0.08
Nodes (49): derive_hkdf_sha384(), Thin validated adapter around cryptography's HKDF-SHA-384 implementation., Derive one domain-separated key with a fresh one-shot HKDF-SHA-384 instance.…, _validated_bytes(), _validated_salt(), PQCConfirmationKeyDeriver, Derive a private role-local confirmation key from authenticated Phase 5 state., Build explicit HKDF info for the Phase 5 session-key purpose. (+41 more)

### Community 102 - "BB84 security model"
Cohesion: 0.25
Nodes (7): Analytical channel expectations, BB84 security model, Key and parameter-estimation model, Phase-error relation, Reference, Secret-length and abort policy, Security boundary and remaining limitations

### Community 103 - "Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)"
Cohesion: 0.18
Nodes (10): 1. Resumen Ejecutivo y Alcance, 2. Tabla Resumen de Hallazgos, 3. Análisis Detallado de Hallazgos, 4. Evaluación de Invariantes y Principios de Diseño Criptográfico, 5. Conclusiones y Recomendaciones de Priorización, Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico), [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`, [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF (+2 more)

### Community 104 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply depolarizing noise to a single-qubit density matrix.

### Community 105 - "_prepare_density_matrix"
Cohesion: 0.13
Nodes (12): _prepare_density_matrix(), ArrayLike, ComplexArray, Apply the channel to a density matrix., Convert a channel input and enforce cheap structural invariants., ArrayLike, ComplexArray, Build a channel from a non-empty complete set of Kraus operators. (+4 more)

### Community 106 - "operations.py"
Cohesion: 0.50
Nodes (3): _immutable(), ndarray, Named single-qubit operators commonly used by QKD protocols.

### Community 107 - ".__exit__"
Cohesion: 0.33
Nodes (4): BaseException, TracebackType, Release the private KEM capabilities when leaving a managed lifetime., Release references to ephemeral private KEM instances to prevent subsequent…

### Community 109 - "Recommended Changes to TFM_GOAL.md"
Cohesion: 0.22
Nodes (9): §11 — Security Profiles — REESCRIBIR (tabla), §12 — Methodology — REESCRIBIR (añadir el bloque estadístico), §15 — Definition of Done — REESCRIBIR, §3 — Research Question — REESCRIBIR, §4 — Subquestions — REESCRIBIR, §7 — Contribution — REESCRIBIR, AÑADIR §19 — Threats to Validity, AÑADIR §20 — Related Work Positioning (+1 more)

### Community 110 - "Clasificación"
Cohesion: 0.22
Nodes (9): Clasificación, Minimum Web Laboratory, Pantallas para una defensa de 10-15 min, Protected Message Demo, Protocol Visualizer, Quantum-Safe Explorer, Results / Metrics, Session Builder (+1 more)

### Community 112 - ".run"
Cohesion: 0.20
Nodes (10): integer, ndarray, random_basis(), random_bit(), Generate binary choices using this simulator's bias/correlation model., Generate one or more uniformly distributed classical bits., Generate generic binary choices for adaptation by the QKD layer., Generate binary choices, allowing specialized RNGs to override their model. (+2 more)

### Community 113 - "EstablishedPQCSession"
Cohesion: 0.13
Nodes (8): EstablishedPQCSession, Self, Enter a managed lifetime for this private confirmation-key state., Role-local session-key handle available only after mutual Finished verification., Return true because this type exists only after mutual confirmation., Return whether the owned session-key state was closed., Explicitly export the established role-local symmetric session key., Enter a managed lifetime for this established local session.

### Community 115 - "Security Concerns / Overclaims"
Cohesion: 0.29
Nodes (7): AES-GCM (aún no implementado — requisitos para cuando se haga), Combinador híbrido — el punto más delicado, HQC, Key confirmation, PQC, QKD, Security Concerns / Overclaims

### Community 116 - "13. Experiments"
Cohesion: 0.29
Nodes (7): 13. Experiments, D1 — End-to-End Protected Session Demo, E1 — PQC Cost Decomposition, E2 — BB84 Model Validation, E3 — Eve / Intercept-Resend, E4 — QKD Authentication Cost, E5 — Hybrid Marginal Overhead

### Community 117 - ".apply"
Cohesion: 0.50
Nodes (3): ArrayLike, ComplexArray, Apply amplitude damping to a single-qubit density matrix.

### Community 119 - "Executive Assessment"
Cohesion: 0.40
Nodes (5): 1. La pregunta de investigación no es empírica, 2. No existe adversario en ninguna parte del código, 3. Existe un fallo real en el modelo de seguridad de QKD, no documentado, Executive Assessment, Veredicto resumido

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

## Knowledge Gaps
- **304 isolated node(s):** `quantumsec`, `name`, `private`, `version`, `type` (+299 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 960 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `QuantumChannel` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `Basis` (4× useful, score=2.893288868) _(code changed — re-verify)_
- `BaseRNG` (3× useful, score=2.16957619)
- `BB84Protocol` (2× useful, score=1.447957891) _(code changed — re-verify)_
- `SeededRNG` (2× useful, score=1.447745854)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Basis` connect `bb84.py` to `adapters.py`, `qber_by_basis`, `BaseRNG`, `BB84Result`, `sift_keys`, `estimate_qber_from_sample`, `test_bb84.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `SeededRNG` connect `SeededRNG` to `adapters.py`, `BaseRNG`, `BitFlipChannel`, `test_measures.py`, `reconcile_cascade`, `amplify_privacy`, `estimate_qber_from_sample`, `test_bb84.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `BB84SessionResult` connect `BB84SessionResult` to `BaseRNG`, `bb84.py`, `reconcile_cascade`, `amplify_privacy`, `estimate_qber_from_sample`, `test_bb84.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `SeededRNG` (e.g. with `test_supported_channels_match_analytical_per_basis_qber()` and `test_bb84_rejects_non_positive_or_non_integer_signal_counts()`) actually correct?**
  _`SeededRNG` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PQCParty` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCParty` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PQCProfile` (e.g. with `canonical_kem_secret_input()` and `ClientKeyExchangeProcessor`) actually correct?**
  _`PQCProfile` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignedServerKeyOffer` (e.g. with `ClientKeyExchangeFactory` and `ClientKeyExchangeProcessor`) actually correct?**
  _`SignedServerKeyOffer` has 8 INFERRED edges - model-reasoned connections that need verification._