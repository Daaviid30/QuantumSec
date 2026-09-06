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

                  pqc (independent sibling domain)
```

Target dependency flow:

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
|-- qkd/                        # CURRENT/PARTIAL: BB84 and classical post-processing
|-- pqc/                        # CURRENT: standalone authenticated PQC handshakes
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
|-- orchestration/              # PLANNED: profiles, session composition, auth policy
|-- data_protection/            # PLANNED: AES-256-GCM session payloads
`-- experiments/               # PLANNED: config/run/record/export/analyze
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

### 5.3 `qkd/` — CURRENT execution, PARTIAL security-decision path

Implemented flow:

```text
BB84 preparation
    -> ordered logical-qubit CPTP channels
    -> Bob measurement
    -> basis sifting
    -> sampled aggregate QBER and disclosure removal
    -> aggregate-QBER threshold
    -> Cascade reconciliation
    -> universal-hash reconciled-key verification
    -> asymptotic secret-length estimate
    -> Toeplitz privacy amplification
    -> final material or explicit abort
```

Implemented channels are Identity, Depolarizing, Bit Flip, Phase Flip, Pauli mixture, and Amplitude
Damping. They are logical-qubit models. Amplitude damping is relaxation, not photon loss.

The session exposes raw/sifted counts, sifting efficiency, diagnostic full-sifted aggregate QBER,
sampled aggregate QBER, disclosed positions, candidate size, Cascade leakage/corrections,
verification result/leakage, reconciled/final sizes, and final simulated material.

The following security limitations are architectural blockers:

- `e_Z` and `e_X` are not calculated or exposed.
- the QBER threshold and `asymptotic_bb84_secret_length()` use sampled aggregate QBER;
- the estimator assumes symmetric phase error, but asymmetric supported channels can violate it;
- no intercept-resend adversary exists;
- the classical transcript is assumed authenticated, not authenticated by code.

Consequently, `QKD-ASSUMED` is **PARTIAL** as a security profile even though the BB84 pipeline is
executable. Correction requires a theoretically justified phase-error model or conservative abort
outside the model's domain—not an undocumented `max(e_Z, e_X)` substitution.

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

### 5.5 `ui/` — CURRENT BB84 interface, PARTIAL TFM laboratory

Current backend routes:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The current request supports `n_signals`, a seed, and up to 12 ordered implemented channels.
Responses adapt real domain results and contain a UUID, software duration, outcome, summary,
post-processing details, distributions, and a bounded raw-transmission sample.

There are no PQC, QKD-authentication, Eve, hybrid, experiment, compare, or AES-GCM routes. The
frontend provides a BB84 builder and result workspace only.

### 5.6 `benchmarks/` — CURRENT, not the experiment engine

The existing benchmark measures projective sampling paths. It does not implement E1–E5 and must
not be presented as the TFM experimental framework.

## 6. Definitive profile architecture

| Public profile | Establishment source | Authentication policy | Status |
|---|---|---|---|
| `QKD-ASSUMED` | BB84 | Assumed authenticated classical channel | **PARTIAL** |
| `QKD-CLASSICAL-AUTH` | BB84 | Executed universal-hash/Wegman–Carter-style authentication | **PLANNED** |
| `QKD-PQC-AUTH` | BB84 | Executed ML-DSA-65 transcript authentication | **PLANNED** |
| `PQC-BASE` | ML-KEM-768 | ML-DSA-65 | **CURRENT** |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 | ML-DSA-65 | **CURRENT** |
| `HYBRID` | BB84 + ML-KEM-768 | Explicit policy recorded in the profile/result | **PLANNED** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 | Explicit policy recorded in the profile/result | **PLANNED** |

The profile contract must make these independent dimensions explicit:

- source and provenance of each establishment component;
- QKD authentication mechanism and whether it was assumed or executed;
- algorithms and exact internal PQC profile;
- transcript/encoding version;
- terminal outcome and reason;
- applicable metrics only.

## 7. Planned QKD authentication

### `QKD-CLASSICAL-AUTH`

This profile requires a complete construction, not merely the existing Toeplitz helper:

- pre-shared secret authentication material;
- separation between hash-selection and one-time/tag-protection material as required;
- canonical authenticated messages/transcript;
- tag generation and verification;
- explicit failure path; and
- accounting for consumed authentication material where applicable.

It remains **PLANNED** until all properties are executable and tested.

### `QKD-PQC-AUTH`

This profile reuses ML-DSA-65 identities and explicit pre-provisioned trust above `qkd` and `pqc`.
The design must define which classical messages or canonical transcript are signed and when
verification occurs. A decorative signature over a final summary is not equivalent to
authenticating all security-relevant exchanges.

## 8. Planned adversary and corrected estimator

The intercept-resend component receives an interception fraction `f`. For intercepted signals Eve
chooses a basis, measures, prepares the measured state, and resends it to Bob. Its trace records
whether Eve acted and the relevant modeled event without leaking final secret material.

Per-basis estimation must preserve enough basis/position information to expose `e_Z`, `e_X`, and
aggregate QBER. The security policy must identify which observed quantity bounds phase error under
the implemented BB84 model and what happens when no justified bound is available. The validation
suite must cover analytical channel predictions and the `QBER ~= 0.25 f` ideal adversary case.

## 9. Planned hybrid orchestration

```text
K_QKD
SS_ML_KEM       -> canonical hybrid component encoding
SS_HQC optional -> hybrid domain separation
                -> transcript/ciphertext binding where specified
                -> HKDF-SHA-384
                -> 32-byte K_SESSION
                -> explicit provenance and confirmation
```

The hybrid encoding is distinct from the current PQC-only `canonical_kem_secret_input()`. It must
specify canonical encoding, labels, lengths, deterministic order, profile, domain separation,
provenance, and binding inputs. Boundary, order, profile-mismatch, omission, duplication, and
sensitivity tests are mandatory.

The security description is limited to the construction and assumptions actually implemented. A
computational KDF output is not automatically information-theoretically secure because one input
came from QKD.

## 10. Planned data-protection plane

```text
ESTABLISHMENT PLANE -> 256-bit K_SESSION
DATA PLANE          -> AES-256-GCM
                    -> nonce + ciphertext + 128-bit tag
                    -> plaintext or explicit authentication failure
```

The implementation requires a 96-bit nonce, uniqueness under each key, full authentication tag,
appropriate session metadata as AAD, successful valid decryption, rejection of modified
ciphertext/tag/AAD, and no partial plaintext on failure.

## 11. Experiment architecture

```text
ExperimentConfig
    -> Runner
        -> SessionResult + ordered Trace
            -> MetricRecord
                -> versioned JSON/CSV export
                    -> analysis and figures
```

The five required experiments and D1 are specified in
[`../TFM_GOAL.md §13`](../TFM_GOAL.md#13-experiments). The measurement-category rule and statistical
requirements are centralized in
[`../TFM_GOAL.md §12`](../TFM_GOAL.md#12-experimental-methodology).

The experiment layer records environment, versions, profile, config, applicable seed, randomized
condition order, trace, public byte sizes, applicable timings, QKD metrics, and outcome. It never
serializes secret values.

## 12. Web Laboratory V1

The target is limited to three screens:

1. **Builder** — supported profile selector; QKD signal count, seed, channel/parameters, and Eve
   fraction; profile-derived PQC components; small contextual/versioned cards.
2. **Run** — real Alice/Bob/Eve timeline; explicit authentication state; KEM, combiner, HKDF,
   Finished, compatible metrics, outcome, and protected-message strip when `K_SESSION` exists.
3. **Compare** — exactly two run records; configuration diff, components, assumptions, compatible
   metrics, bytes, outcome, and security notes.

For `QKD-ASSUMED`, Run must display:

```text
CLASSICAL AUTHENTICATION
ASSUMED — NOT EXECUTED
```

There is no separate Quantum-Safe Explorer. Small contextual cards answer what a component is, its
role, security assumption, profile contribution, and dated normative status, with a reference.

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
