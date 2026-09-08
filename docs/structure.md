# QuantumSec Architecture

This is the canonical architecture document. Source code and tests take precedence over target
diagrams. Academic scope, hypotheses, methodology, and the definition of done live in
[`../TFM_GOAL.md`](../TFM_GOAL.md).

## 1. Architectural purpose

QuantumSec is a modular and reproducible laboratory for executing, visualizing, and evaluating
QKD-, PQC-, and hybrid-based quantum-safe session-establishment strategies. Its architecture must:

1. keep QKD and PQC independently testable;
2. compose them only through an upper orchestration layer;
3. preserve the provenance, order, labels, lengths, and domains of secret inputs;
4. expose executed authentication separately from assumed authentication;
5. produce real configuration, trace, metric, result, and export records;
6. make implementation status visible to the API and UI; and
7. prevent incompatible QKD and PQC measurements from being treated as one performance axis.

Status terms are **CURRENT**, **PARTIAL**, **PLANNED**, and **FUTURE**, as defined in
[`../TFM_GOAL.md`](../TFM_GOAL.md).

## 2. Dependency invariants

Current dependency flow:

```text
ui/frontend -> ui/backend -> qkd -> quantum -> core

                         experiments
                              |
                              v
                         orchestration
                        /      |       \
                      qkd     pqc   data_protection
```

Target UI dependency flow:

```text
ui/frontend
    -> ui/backend
        -> orchestration
            -> qkd
            -> pqc
            -> data_protection
        -> experiments
            -> orchestration
```

The allowed direction is:

```text
core <- quantum <- qkd <- orchestration <- experiments / ui

                 pqc <- orchestration
data_protection <- orchestration
```

The invariants are:

- `core` has no domain dependencies.
- `quantum` may depend on `core`, but knows nothing about QKD or PQC.
- `qkd` may depend on `quantum` and `core`, but never imports `pqc`.
- `pqc` is a sibling domain and never imports `qkd`.
- `data_protection` owns only data-plane concepts and never imports `qkd`, `pqc`, or
  `orchestration`; the ownership-transfer adapter lives in `orchestration`.
- authentication policy and QKD–PQC composition belong above both domains.
- `experiments` records and invokes capabilities; it does not implement cryptography.
- `ui/backend` adapts typed contracts and does not hide domain logic in routes.
- `ui/frontend` renders backend capabilities, events, metrics, and status; it does not simulate
  protocol behavior.

## 3. Current and target tree

```text
QuantumSec/
|-- core/                       # CURRENT: constants, RNG, shared foundations
|-- quantum/                    # CURRENT: numerical quantum mathematics
|-- qkd/                        # CURRENT: BB84 and classical post-processing
|-- pqc/                        # CURRENT: standalone authenticated PQC handshakes
|-- orchestration/              # CURRENT: session layer and data-plane adapter
|-- data_protection/            # CURRENT: session-bound AES-256-GCM payload protection
|-- experiments/                # CURRENT: engine plus thesis-v1 campaign/record-only analysis
|-- ui/
|   |-- backend/                # CURRENT: BB84 HTTP adapter only
|   `-- frontend/               # CURRENT/PARTIAL: BB84 laboratory
|-- tests/                      # CURRENT: Python and UI tests
|-- benchmarks/                 # CURRENT: narrow projective-measurement benchmark
|-- reports/                    # HISTORICAL implementation records
|-- docs/
|   |-- reviews/                # HISTORICAL independent review snapshots
|   |-- structure.md            # CURRENT architecture source
|   `-- tasks.md                # CURRENT ordered implementation plan
`-- examples/experiments/       # CURRENT: small secret-free QKD and PQC configs
```

The names of planned packages may be refined when implementation begins; their dependency
boundaries may not.

## 4. Cross-cutting invariants

### Injected randomness

All modeled randomness is supplied through `BaseRNG`; deterministic simulations and tests use
`SeededRNG(seed=...)`. Real PQC operations use liboqs and operating-system cryptographic
randomness and are not made deterministic for experiments.

### Immutable results and defensive validation

Value/result objects use frozen slotted dataclasses where practical. Stored NumPy arrays are copied
and made read-only. Inputs use `ArrayLike`; outputs use explicit array aliases.

### Explicit status and capability discovery

A planned profile must not appear executable. The backend reports actual capabilities and the UI
enables controls only for those capabilities. Partial status includes a reason and must not be
collapsed into current/complete.

### Secret handling

Private keys, shared secrets, `K_SESSION`, and `K_CONFIRM` are not traces or experiment metrics.
Public messages and derived metadata may be serialized through explicit versioned mappings. Secret
state remains repr-safe and follows explicit lifecycle rules without claiming memory zeroization.

## 5. Implemented layers

### 5.1 `core/` — CURRENT

`core/rng.py` defines the `BaseRNG` boundary and seeded implementation used by simulations.
`core/constants.py` provides shared numerical tolerances. This layer must remain domain-neutral.

### 5.2 `quantum/` — CURRENT

This layer owns numerical state validation, pure/density-state conversion, linear algebra,
information measures, projectors, and projective measurement. It knows nothing about Alice, Bob,
BB84, QBER, authentication, KEMs, or session profiles.

### 5.3 `qkd/` — CURRENT execution and asymptotic security-decision path

Implemented flow:

```text
BB84 preparation
    -> ordered logical-qubit channel/adversary stages
    -> Bob measurement
    -> basis sifting
    -> basis-stratified Z/X QBER estimation and disclosure removal
    -> explicit mixed-basis phase-error bound and threshold
    -> Cascade reconciliation
    -> universal-hash reconciled-key verification
    -> asymptotic secret-length estimate
    -> Toeplitz privacy amplification
    -> final material or explicit abort
```

Implemented physical channels are Identity, Depolarizing, Bit Flip, Phase Flip, Pauli mixture, and
Amplitude Damping. `qkd/channel/attacks/` contains the seeded Intercept-Resend stage. Both satisfy
the same `QuantumChannel` contract and compose in one ordered `ChannelPipeline`. They are
logical-qubit models. Amplitude damping is relaxation, not photon loss.

The session exposes raw/sifted counts, sifting efficiency, estimated and diagnostic Z/X/aggregate
QBER, the phase-error bound, disclosed positions and bases, candidate size, Cascade
leakage/corrections, verification result/leakage, reconciled/final sizes, and final simulated
material.

The estimator no longer assumes basis symmetry. X observations bound phase errors for retained Z
positions and Z observations bound phase errors for retained X positions. Because the current
candidate mixes both subsets, `max(e_Z, e_X)` is their documented common upper bound. Aggregate
QBER remains descriptive and sizes Cascade; it cannot authorize privacy amplification as a phase
estimate. Missing per-basis data fails closed. `docs/SECURITY_MODEL.md` records the derivation.

`QKD-ASSUMED` is the **CURRENT** explicit assumption baseline. It never reports authentication as
verified. Executed authentication is available only through the upper-layer profiles described
below. The secret-length decision remains asymptotic, not a composable finite-key proof;
intercept-resend remains one bounded adversary model.

#### Verification is not authentication

`verify_reconciled_keys()` creates a seeded universal-hash comparison tag after Cascade. Its role
is to detect residual disagreement between Alice's and Bob's reconciled keys. It has no secret
authentication key, identity binding, authenticated transcript coverage, or channel-authentication
failure semantics. It must never be labeled a MAC or QKD classical-channel authentication.

### 5.4 `pqc/` — CURRENT standalone handshakes

Public-to-internal profile mapping:

```text
PQC-BASE    -> PQCProfile.LOW
PQC-DIVERSE -> PQCProfile.HIGH
```

The internal names remain because they are encoded into signed messages, transcript construction,
and HKDF context.

Implemented roles:

| Component | Responsibility |
|---|---|
| ML-KEM-768 | Key establishment |
| ML-DSA-65 | Authentication using pre-provisioned trust |
| HQC-3 | Additional KEM and cryptographic diversification |
| SHA-384 transcript | Public handshake binding |
| Structured KEM input | Explicit algorithm order, identifiers, lengths, and boundaries |
| HKDF-SHA-384 | Separate derivation of 32-byte `K_SESSION` and `K_CONFIRM` |
| Finished / HMAC-SHA-384 | Bilateral explicit key confirmation |

Implemented message flow:

```text
1. Alice and Bob create ML-DSA-65 identities and provision trust.
2. Bob creates ephemeral KEM keys and signs ServerKeyOffer.
3. Alice resolves and verifies Bob before encapsulation.
4. Alice encapsulates ML-KEM-768 and, for PQC-DIVERSE, HQC-3.
5. Alice binds the exact offer, signs ClientKeyExchange, and Bob verifies before decapsulation.
6. Both build the canonical transcript and structured KEM-secret input.
7. HKDF-SHA-384 derives K_SESSION and a domain-separated K_CONFIRM.
8. Finished_B and Finished_A confirm possession with role and transcript binding.
```

`canonical_kem_secret_input()` uses a fixed ML-KEM-then-HQC order, component count, identifiers,
and lengths. The transcript hash is the HKDF salt; `info` binds purpose, version, and internal
profile. This is a research diversity construction, not a standardized multi-KEM combiner or a
formal robust-combiner proof.

The implementation uses the parameter set exposed by liboqs 0.16.0 as `HQC-3`. Its documented
status as of 2026-09-05 is selected for standardization, not a final NIST standard.

### 5.5 `orchestration/` — CURRENT common session layer

This upper layer imports the independent `qkd` and `pqc` domains. `SessionConfig`,
`SessionExecutionContext`, `SessionTrace`, `SessionMetrics`, `SessionResult`, and `run_session()`
provide one versioned contract for all seven public profiles. QKD, PQC, and hybrid adapters remain
separate below the thin dispatcher. Runtime identities, authentication material, protocol engines,
and test transport boundaries never enter the serializable configuration. Failed authentication,
security aborts, and Finished failures always withhold final material. Data protection, experiment
records, and new UI routes remain outside this phase.

### 5.6 `ui/` — CURRENT BB84 interface, PARTIAL TFM laboratory

Current backend routes:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The current request supports `n_signals`, a seed, and up to 12 ordered physical or adversarial
stages. Responses adapt real domain results and contain a UUID, software duration, ordered stage
metadata, bounded attack diagnostics, outcome, post-processing details, distributions, and a
bounded raw-transmission sample.

There are no PQC, QKD-authentication, hybrid, experiment, compare, or AES-GCM routes. Eve is
available through the existing BB84 simulation route, but this phase adds no Eve UI. The frontend
provides a BB84 builder and result workspace only.

### 5.7 `benchmarks/` — CURRENT, not the experiment engine

The existing benchmark measures projective sampling paths. It does not implement E1–E5 and must
not be presented as the TFM experimental framework.

## 6. Definitive profile architecture

| Public profile | Establishment source | Authentication policy | Status |
|---|---|---|---|
| `QKD-ASSUMED` | BB84 | Assumed authenticated classical channel; not executed | **CURRENT baseline** |
| `QKD-CLASSICAL-AUTH` | BB84 | Executed one-time Toeplitz/Wegman–Carter-style authentication | **CURRENT** |
| `QKD-PQC-AUTH` | BB84 | Executed ML-DSA-65 transcript authentication | **CURRENT** |
| `PQC-BASE` | ML-KEM-768 | ML-DSA-65 | **CURRENT** |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 | ML-DSA-65 | **CURRENT** |
| `HYBRID` | BB84 + ML-KEM-768 | Explicit QKD policy + ML-DSA-65 PQC exchange authentication | **CURRENT** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 | Explicit QKD policy + ML-DSA-65 PQC exchange authentication | **CURRENT** |

The profile contract must make these independent dimensions explicit:

- source and provenance of each establishment component;
- QKD authentication mechanism and whether it was assumed or executed;
- algorithms and exact internal PQC profile;
- transcript/encoding version;
- terminal outcome and reason;
- applicable metrics only.

## 7. Current QKD authentication

### `QKD-CLASSICAL-AUTH`

This profile implements a complete construction, not merely the existing Toeplitz helper:

- pre-shared secret authentication material;
- a fresh secret Toeplitz selector and independent fresh one-time tag mask per checkpoint;
- canonical authenticated messages/transcript;
- tag generation and verification;
- explicit failure path; and
- exact accounting of `n + 2t - 1` consumed PSK bits for an `n`-bit frame and `t`-bit tag.

The current default is `t = 128`, giving a per-checkpoint substitution/forgery bound no larger
than `2^-128` under the stated XOR-universal Toeplitz-family and uniform-secret assumptions. The
implementation conservatively consumes both selector and mask material exactly once and claims no
key recycling. Byte tags are checked with `hmac.compare_digest`; this does not imply whole-Python
side-channel resistance. The PSK is provisioned before the session and is never derived from the
QKD key being authenticated.

### `QKD-PQC-AUTH`

This profile reuses real ML-DSA-65 identities and explicit pre-provisioned trust above `qkd` and
`pqc`. Alice and Bob each sign the canonical public-transcript checkpoint in their communication
direction; the peer resolves the signer through its existing trusted identity store. Identity
generation and public-key provisioning are outside per-session latency.

Both executed profiles authenticate the same complete public transcript. Its ordered events bind
Alice/Bob basis announcements, sifting positions, per-basis parameter-estimation positions/bases/
bits, every Cascade permutation and Alice/Bob root/binary parity (including look-back context),
the reconciled-key verification public seed and both comparison tags, and the privacy-amplification
public seed. Each event binds domain, version, session ID, direction, sequence number, message type,
payload length, and payload. The end-of-transcript bilateral checkpoint strategy may permit wasted
work or denial of service before verification, but the orchestrator never releases a final key
until every required checkpoint verifies.

## 8. Current intercept-resend adversary and corrected estimator

The intercept-resend component receives an interception fraction `f`. For intercepted signals Eve
chooses Z/X uniformly, measures the input density matrix, prepares the state implied by her own
outcome, and resends it to Bob. It is a stochastic `QuantumChannel` with an injected RNG and no
access to Alice/Bob protocol context. The API records its ordered stage metadata and aggregate
counts without serializing per-signal Eve events or secret material.

Per-basis estimation preserves disclosed and candidate basis labels and exposes `e_Z`, `e_X`, and
aggregate QBER. The current mixed-basis policy uses the larger per-basis estimate as a common
asymptotic phase-error bound and aborts when that bound is unavailable. Deterministic tests cover
the analytical predictions for all implemented channels. Seeded tests now validate the ideal
`QBER ~= 0.25 f` adversary baseline and symmetric Z/X disturbance. The multi-seed E3 experiment
campaign remains planned.

## 9. Current hybrid orchestration

```text
K_QKD
SS_ML_KEM       -> canonical hybrid component encoding
SS_HQC optional -> hybrid domain separation
                -> transcript/ciphertext binding where specified
                -> HKDF-SHA-384
                -> 32-byte K_SESSION
                -> explicit provenance and confirmation
```

The hybrid encoding is distinct from the PQC-only `canonical_kem_secret_input()`. It binds the
domain and version, public profile, component count, and each component's position, label, source,
algorithm, encoding, exact bit length, byte length, and length-prefixed secret bytes. Order is
strictly QKD, ML-KEM-768, then optional HQC-3. The QKD bitstring is big-endian packed with its exact
bit length, so padding cannot alias another input.

PQC phases 2–4 authenticate the signed offer and client exchange before the domain-owned single-use
`AuthenticatedKEMContributions` capability releases defensive secret copies. The source KEM states
close during transfer. The hybrid layer never reads PQC private fields and never mixes the pure-PQC
`K_SESSION`.

The public hybrid context binds the shared 16-byte session ID, hybrid and QKD profiles, canonical
QKD transcript hash/version, PQC transcript hash/protocol/internal profile, ordered algorithms, and
encoding/context versions. Its SHA-384 digest is the salt for independent 32-byte SessionKey and
ConfirmationKey HKDF calls. A hybrid-specific versioned HMAC-SHA-384 Finished exchange runs Bob
then Alice, with Alice's message chained to Bob's verify data. Only bilateral verification creates
the common established-key capability.

The security description is limited to the construction and assumptions actually implemented. A
computational KDF output is not automatically information-theoretically secure because one input
came from QKD, and no formal robust-combiner proof is claimed. QKD simulator time and real PQC
software-crypto time remain separate metric categories and are not presented as physical latency.

## 10. Current data-protection plane

```text
ESTABLISHMENT PLANE -> 256-bit K_SESSION
DATA PLANE          -> AES-256-GCM
                    -> nonce + ciphertext + 128-bit tag
                    -> plaintext or explicit authentication failure
```

`orchestration.open_data_plane()` accepts only an established 256-bit `SESSION_KEY`, constructs a
public `DataPlaneContext`, transfers the key into `ProtectedSession`, and retires the source
`SessionResult` capability. It supports `PQC-BASE`, `PQC-DIVERSE`, `HYBRID`, and
`HYBRID-DIVERSE`. QKD-only `QKD_BITSTRING` results are rejected because no application-key schedule
for their variable-length output is currently defined.

`data_protection/` has no dependency on establishment domains. `ProtectedSession` uses
`cryptography`'s `AESGCM` with exactly 32-byte keys. Each 96-bit nonce is a four-byte direction
discriminator (`00000001` for Alice-to-Bob or `00000002` for Bob-to-Alice) followed by an unsigned
64-bit big-endian monotonic sequence. Allocation is lock-protected; the final sequence value is
usable once and the counter never wraps.

Canonical AAD is the length-prefixed `QuantumSec/DataPlane/v1/AAD` domain, version, length-prefixed
canonical `DataPlaneContext`, direction, uint64 sequence, declared application-AAD byte count, and
length-prefixed application AAD. The context binds session ID, public profile, `SessionResult`
version, key type/size, and typed public session-context entries. `ProtectedRecord` stores only
public transport metadata, nonce, ciphertext, and the full 128-bit tag; it provides deterministic
length-prefixed `canonical_bytes()` / `from_bytes()` transport framing. Public-context map entries
are ordered by UTF-8 key bytes before hashing. `InvalidTag` propagates unchanged and no plaintext is
returned on authentication failure.

## 11. Experiment architecture

```text
ExperimentConfig
    -> ExperimentRuntimeFactory -> SessionExecutionContext (runtime-only secrets)
        -> ExperimentRunner -> run_session()
            -> public SessionResult + ordered Trace + categorized SessionMetrics
                -> immutable ExperimentRecord
                    -> versioned JSON/analysis-ready CSV
                        -> record-only summaries, figures, report, and integrity audit
```

The five required experiments and D1 are specified in
[`../TFM_GOAL.md §13`](../TFM_GOAL.md#13-experiments). The measurement-category rule and statistical
requirements are centralized in
[`../TFM_GOAL.md §12`](../TFM_GOAL.md#12-experimental-methodology).

The V1 experiment layer is **CURRENT**. It records environment, versions, profile, normalized
round-trippable config, applicable seed, versioned batch provenance, randomized condition order,
Git dirty-worktree state, trace, public byte sizes,
applicable timings, QKD protocol estimates/diagnostics, and outcome. It never serializes secret
values and closes each generic `SessionResult` after copying public evidence. Its exact contracts,
CLI, seed policy, batch behavior, and export schemas are documented in
[`EXPERIMENTS.md`](EXPERIMENTS.md).

`experiments/campaigns/thesis_v1.py` owns only the fixed campaign matrix and execution workflow;
`experiments/analysis/thesis_v1.py` and `plots.py` read the exported raw records and never import or
execute cryptographic sessions. The THESIS dataset was executed as `thesis-v1.0.1` under
`results/thesis_v1/` with 1,111 records and 13 required figures. The dependency direction remains
`analysis/campaigns -> experiments -> orchestration -> domains`.

## 12. Web Laboratory V1

The current implementation uses four restrained navigation surfaces while preserving the bounded
Builder / Run / Compare thesis workflow:

1. **Overview** — seven public profile summaries, implemented capability groups, backend readiness,
   and the QKD/PQC measurement boundary.
2. **Laboratory** — the profile-aware Builder and Run workflow: Guided/Research controls, QKD signal
   count, seed, ordered channel/Eve stages, profile-derived PQC components, real ordered trace,
   authentication, provenance, compatible metrics, outcome, and the protected-message strip when a
   backend-held `K_SESSION` capability exists.
3. **Runs** — bounded process-local public records, normalized configuration and environment
   provenance, exact-configuration rerun, and two-record selection.
4. **Compare** — exactly two run records; configuration diff, components, assumptions, compatible
   metrics, byte layers, outcome, and security notes.

For `QKD-ASSUMED`, Run must display:

```text
CLASSICAL AUTHENTICATION
ASSUMED — NOT EXECUTED
```

There is no separate Quantum-Safe Explorer or campaign-scale web dashboard. Contextual profile
content identifies component role, security assumption, profile contribution, and normative status.

## 13. Quality and maintenance

Before completion of any implementation refactor:

```text
uv run pytest
uv run ruff check .
uv run pyright

cd ui/frontend
npm test
npm run typecheck
npm run build
```

After code changes, run `graphify update .`. Documentation reviews must also search the live
documents and UI capability text for obsolete profile names, unsupported performance claims,
authentication ambiguity, HQC overclaims, and stale planned/current status.

Normative status references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST HQC selection](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).
