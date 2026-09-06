# QuantumSec TFM Goal

This document is the definitive academic and technical contract for the Master's thesis. Code and
tests remain the source of truth for implementation status. The status vocabulary is strict:

- **CURRENT** — implemented and tested.
- **PARTIAL** — an executable part exists, but a required guarantee or capability is incomplete.
- **PLANNED** — required for the TFM, but not implemented.
- **FUTURE** — explicitly outside the TFM definition of done.

## 1. Thesis in One Sentence

QuantumSec is a modular and reproducible laboratory for executing, visualizing, and evaluating
quantum-safe session-establishment strategies based on QKD, post-quantum cryptography, and hybrid
QKD–PQC composition.

Provisional title:

- **ES:** *QuantumSec: evaluación experimental del coste y los supuestos de seguridad de
  estrategias de establecimiento de sesión quantum-safe basadas en QKD, PQC e hibridación*.
- **EN:** *QuantumSec: Experimental Evaluation of the Cost and Security Assumptions of QKD-, PQC-
  and Hybrid-Based Quantum-Safe Session Establishment*.

The title remains provisional until the experimental results are available.

## 2. Problem Statement

QKD, PQC, and hybrid approaches establish session material under different trust, channel,
authentication, and security assumptions. Their costs are also expressed through different
metrics. A numerical BB84 simulation cannot be treated as QKD hardware, while real liboqs
operations can be timed on a documented software and hardware platform. A useful comparison must
therefore preserve provenance, expose assumptions, and avoid collapsing incompatible quantities
into a single performance ranking.

The web is the interface to the laboratory, the protocols and primitives are the systems under
study, the experiments are the evaluation method, and the experimental results and conclusions
are the academic contribution.

## 3. Research Question

> What computational and communication costs are introduced by different quantum-safe
> session-establishment strategies based on QKD, PQC, and hybrid composition, and how do the
> channel model, authentication, and the presence of an adversary affect their behavior and the
> validity of their security guarantees?

Original Spanish formulation:

> ¿Qué coste computacional y de comunicación introducen distintas estrategias de establecimiento
> de sesión quantum-safe basadas en QKD, PQC e hibridación, y cómo afectan el modelo de canal, la
> autenticación y la presencia de un adversario a su comportamiento y a la validez de sus garantías
> de seguridad?

## 4. Research Subquestions

1. What computational and communication overhead does `PQC-DIVERSE` add to `PQC-BASE`, and which
   operations dominate it on the documented reference platform?
2. Does the BB84 simulator reproduce the analytical per-basis error predictions of each supported
   channel, and where is the current security estimator's domain of validity?
3. Once the planned ideal intercept-resend model is implemented, how do interception fraction,
   channel noise, and sampling affect QBER, final material, and abort probability?
4. What overhead and security assumptions distinguish assumed, classical/ITS, and PQC
   authentication of the QKD classical channel?
5. What marginal orchestration, byte, derivation, and confirmation overhead is introduced by the
   hybrid profiles without comparing simulated QKD runtime with real PQC timing?
6. Can the web laboratory communicate each profile's provenance, assumptions, compatible metrics,
   and outcome without presenting planned behavior as executed?

## 5. Hypotheses

- **H1:** `PQC-DIVERSE` overhead relative to `PQC-BASE` will be dominated by HQC-3 rather than by
  the structured combiner, HKDF, or key confirmation.
- **H2:** Under the planned ideal intercept-resend model, induced QBER will be approximately
  proportional to `0.25 f`, where `f` is the intercepted fraction.
- **H3:** Aggregated QBER is not a conservative phase-error estimate for every asymmetric channel
  supported by QuantumSec.
- **H4:** The marginal computational cost of structured combination, HKDF, and confirmation will be
  small relative to the KEM and signature primitives composing the session.
- **H5:** Executing authentication of the QKD classical channel will add measurable overhead while
  removing the external authentication assumption of the `QKD-ASSUMED` baseline.

These are working hypotheses, not results. They must be accepted, rejected, or qualified using the
recorded evidence.

## 6. General Objective

Design, implement, and experimentally evaluate a bounded, modular, reproducible laboratory for
quantum-safe session establishment using BB84, real PQC primitives, and explicit hybrid profiles.

## 7. Specific Objectives

1. Validate BB84 against analytical channel predictions using aggregated and per-basis QBER.
2. Implement and evaluate an explicit intercept-resend adversary with a configurable interception
   fraction.
3. Replace the current symmetric-error assumption with a theoretically justified phase-error
   model or fail conservatively outside its domain of validity.
4. Execute at least one real authentication mechanism for the QKD classical transcript and expose
   its trust and key-consumption assumptions.
5. Evaluate the implemented mutually authenticated PQC handshakes under stable public profile
   names while preserving their internal transcript identifiers.
6. Compose independently produced QKD and PQC material above the sibling domains with canonical
   encoding, provenance, domain separation, and deterministic ordering.
7. Derive a 256-bit `K_SESSION`, demonstrate AES-256-GCM payload protection, and reject tampering.
8. Produce versioned, reproducible experiment records and a web workflow for building, running,
   and comparing exactly two runs.

## 8. Contributions

- **Principal — experimental:** quantify the cost and behavior of successive quantum-safe
  guarantees under one architecture and methodology: executed QKD authentication, PQC
  authentication, KEM diversification, and hybrid QKD–PQC composition.
- **Validation:** compare BB84 behavior with analytical predictions and an explicit adversary. The
  discovery of the aggregated-QBER symmetry limitation is treated as a validation result:
  `THEORY -> MODEL -> EXPERIMENT -> DISCREPANCY -> ASSUMPTION IDENTIFIED -> CORRECTION ->
  REVALIDATION`.
- **Engineering:** preserve acyclic QKD/PQC domains and add upper orchestration, configuration,
  profile, trace, metric, result, and reproducibility contracts.
- **Visualization:** make the protocol, adversary, authentication, assumptions, derivation,
  metrics, and profile differences visible. The UI supports the research; it is not the principal
  scientific contribution.

QuantumSec does not claim a new QKD protocol, PQC primitive, or formal hybrid-combiner proof.

## 9. QuantumSec Definition

QuantumSec is a research laboratory, not primarily an educational site, algorithm collection,
isolated QKD simulator, or demonstration that QKD and PQC can merely be combined. It contains:

- a seeded numerical logical-qubit BB84 path;
- real PQC operations through liboqs;
- planned upper-layer QKD–PQC session composition;
- a reproducible experiment method; and
- a planned three-screen web interface to configure, observe, and compare runs.

## 10. Security Model

### QKD boundary

BB84 requires an authenticated classical channel. The current code assumes that authentication and
does not execute it. Its existing universal-hash verification step only detects whether reconciled
keys disagree; it is not a MAC and must not be described as channel authentication.

The planned authentication profiles must state which messages or canonical transcript are
authenticated, the identity or pre-shared-key provisioning model, key separation, tag/signature
generation and verification, failure behavior, and authentication-material consumption where
applicable. A Toeplitz hash alone is not a Wegman–Carter MAC.

### QBER and secret-length limitation

The current BB84 result exposes aggregated QBER only. Parameter estimation and
`asymptotic_bb84_secret_length()` use the sampled aggregate under a symmetric phase-error
assumption. Supported asymmetric channels can violate that assumption—for example, phase flip can
produce approximately `e_Z = 0`, `e_X = p`, while the aggregate is near `p/2`. The current
secret-length/security-decision path is therefore **PARTIAL** until it exposes `e_Z` and `e_X` and
uses a theoretically justified phase-error estimate, or explicitly aborts outside the justified
model. `max(e_Z, e_X)` must not be adopted without that justification.

### Adversary boundary

Intercept-resend Eve is **PLANNED**. Eve will intercept a fraction `f`, choose a basis, measure,
prepare, and resend. Under the ideal assumptions used by the experiment, the expected induced QBER
is approximately `0.25 f`. This is one concrete experimental model for validating a central BB84
property, not a complete QKD adversary model.

### PQC and hybrid boundary

ML-KEM-768 performs key establishment, ML-DSA-65 performs authentication, HQC-3 adds a distinct KEM
component for diversification, HKDF-SHA-384 derives keys, Finished/HMAC-SHA-384 confirms possession,
and AES-256-GCM will protect application data. These roles are not interchangeable.

The hybrid construction will not be described as automatically secure whenever one input remains
secure. The TFM does not provide a new formal proof. If information-theoretic QKD material is fed
through a KDF whose security is computational, the resulting hybrid key is described under that
computational model; it does not automatically retain information-theoretic security.

## 11. Profiles

Public documentation and UI use these names. `PQCProfile.LOW` and `PQCProfile.HIGH` remain internal
protocol/transcript identifiers to avoid changing existing derived keys and wire contracts.

| Public profile | Secret / key establishment | Authentication | Purpose | Status |
|---|---|---|---|---|
| `QKD-ASSUMED` | BB84 | Authenticated classical channel assumed | Baseline QKD model | **PARTIAL** — BB84 executes; authentication is not executed and the estimator needs correction |
| `QKD-CLASSICAL-AUTH` | BB84 | Planned universal-hash/Wegman–Carter-style construction with pre-shared authentication material | Executed classical/ITS authentication | **PLANNED** |
| `QKD-PQC-AUTH` | BB84 | ML-DSA-65 with pre-provisioned identities over a specified classical transcript | Executed PQC authentication | **PLANNED** |
| `PQC-BASE` | ML-KEM-768 | ML-DSA-65 | Post-quantum establishment | **CURRENT** as internal `LOW` |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 | ML-DSA-65 | Cryptographic diversification | **CURRENT** as internal `HIGH` |
| `HYBRID` | BB84 + ML-KEM-768 | Explicit, recorded authentication policy | Hybrid secret provenance | **PLANNED** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 | Explicit, recorded authentication policy | Diversified hybrid establishment | **PLANNED** |

HQC-3 means the parameter set exposed by liboqs 0.16.0 as `HQC-3`. As of 2026-09-05, HQC is
**selected for standardization**, not a published NIST standard. ML-KEM and ML-DSA are standardized
as FIPS 203 and FIPS 204.

## 12. Experimental Methodology

Every experiment follows `CONFIG -> RUN -> RECORD -> EXPORT -> ANALYZE` and records a run ID,
normalized configuration, applicable seed, Python and NumPy versions, liboqs and wrapper versions,
CPU, OS, profile, backend metadata, ordered condition, trace, metrics, and outcome. Secret values,
private keys, shared secrets, `K_SESSION`, and `K_CONFIRM` are never exported as metrics.

For PQC timing, discard warm-up, randomize condition order, use at least 30 runs and preferably 50,
and report distributions with median and IQR; p10/p90 may supplement them. Persistent identity
generation is a provisioning cost and is measured separately from the handshake.

For QBER and other proportions, report an appropriate binomial confidence interval and justify the
chosen confidence level. Use Mann–Whitney, Clopper–Pearson, or any other statistical procedure only
when it answers the stated question and its assumptions are documented.

### Fundamental measurement rule

The QKD route is a numerical simulation, not real QKD hardware. Its NumPy runtime is not physical
secret-key rate, device latency, fiber throughput, or reachable distance, and it must not be timed
against ML-KEM, ML-DSA, or HQC. Simulation time may characterize the software or compare simulator
configurations only. The PQC route executes real cryptographic operations through liboqs; its
operation and handshake timings may compare PQC profiles only on the documented hardware/software
environment. Other documents should reference this rule instead of duplicating it.

Communication measurement distinguishes raw cryptographic sizes, canonical protocol sizes, and
serialized transport sizes.

## 13. Experiments

### E1 — PQC Cost Decomposition

Compare `PQC-BASE` and `PQC-DIVERSE`. Measure ephemeral KEM key generation, sign, verify,
encapsulate, decapsulate, transcript hashing, combiner, HKDF, Finished generation/verification, and
total handshake. Measure persistent identity generation separately. Report the three size layers
defined in the methodology and do not extrapolate beyond the reference environment.

### E2 — BB84 Model Validation

For each supported channel, compare simulated `e_Z`, `e_X`, aggregated QBER, sifting efficiency,
final material, and abort behavior with the applicable analytical formulas. Include the asymmetric
case that exposed the current estimator limitation and document prior behavior, cause, correction,
and revalidation. The aim is model validation, not the trivial claim that more noise raises QBER.

### E3 — Eve / Intercept-Resend

Vary interception fraction `f`; measure QBER, `e_Z`, `e_X`, `P(abort)`, and `n_final`. Compare
with the ideal `QBER ~= 0.25 f` prediction under its stated assumptions. Principal figures are QBER
and abort probability versus `f`.

### E4 — QKD Authentication Cost

Compare `QKD-ASSUMED`, `QKD-CLASSICAL-AUTH`, and `QKD-PQC-AUTH`, but treat the first only as an
assumption baseline. For executed profiles, measure authentication bytes, operations, meaningful
latency, failures, consumed authentication material, and introduced assumptions. Include a
qualitative comparison of guarantee types.

### E5 — Hybrid Marginal Overhead

Compare `PQC-BASE`, `PQC-DIVERSE`, `HYBRID`, and `HYBRID-DIVERSE` using component provenance and
sizes, additional orchestration bytes, combiner/HKDF/confirmation cost, outcome, and negative tests.
Do not compare BB84 simulation time with liboqs time. Determine whether orchestration cost is
material relative to the constituent primitives.

### D1 — End-to-End Protected Session Demo

Demonstrate `K_SESSION -> AES-256-GCM -> protected payload`, successful decryption, and rejection
of modified ciphertext, tag, or AAD. This is a functional closure, not a scientific discovery.

## 14. Metrics

- **QKD:** `e_Z`, `e_X`, aggregated QBER, binomial interval, sifting efficiency, candidate material,
  final calculated length, final secret fraction, abort/continue, abort probability, channel and
  adversary sensitivity, and explicit security-model assumptions.
- **PQC:** per-operation and total handshake distributions, provisioning cost, raw cryptographic
  sizes, canonical protocol sizes, serialized transport sizes, success/failure, and backend/profile
  metadata.
- **Authentication:** mechanism, authenticated transcript/messages, bytes, operations, failures,
  trust model, and consumed authentication material where applicable.
- **Hybrid:** component provenance, deterministic ordering, encoding/label/length overhead,
  combiner/HKDF/confirmation cost, derived-key length, outcome, and negative-test coverage.
- **Data protection:** key/nonce/tag sizes and acceptance or rejection of valid/tampered inputs.

Metrics are shown only where meaningful for the profile. Incompatible QKD and PQC timings are never
summed, ranked, or placed on a common performance axis.

## 15. Deliverables

- validated and corrected BB84 experiment path with per-basis metrics and Eve;
- executed QKD authentication and the two current PQC profiles;
- hybrid and hybrid-diverse session orchestration with explicit provenance;
- AES-256-GCM protected-message demonstration;
- versioned experiment configurations, records, exports, analysis, and figures for E1–E5;
- Web Laboratory V1 with Builder, Run, and two-run Compare screens;
- contextual, versioned component cards with sources and a status-as-of date; and
- thesis text that answers every research question with evidence or an explicit limitation.

## 16. Definition of Done

The TFM is not complete until:

1. BB84 returns a justified result or abort.
2. `e_Z` and `e_X` are calculated and secret-length estimation is theoretically justified or fails
   conservatively.
3. Intercept-resend Eve is executable and produces a curve comparable with theory.
4. `PQC-BASE` works end to end.
5. `PQC-DIVERSE` works end to end.
6. At least one QKD profile executes authentication rather than assuming it.
7. Classical and PQC QKD authentication are compared if both are implemented correctly.
8. `HYBRID` works end to end.
9. `HYBRID-DIVERSE` works end to end.
10. `K_SESSION` is 256 bits and records explicit provenance.
11. AES-256-GCM protects data and rejects tampering.
12. `CONFIG -> RUN -> RECORD -> EXPORT` works.
13. E1–E5 are reproducible.
14. Web Laboratory V1 provides Builder, Run, and Compare.
15. Contextual cards show the role and dated status of components.
16. Every research question is answered by results or explicit limitations.

## 17. Out of Scope

E91, B92, BBM92, QKDN, quantum repeaters, hardware-QKD modeling, physical fiber secret-key-rate
prediction, dark counts, decoy states, photon-number splitting, additional PQC algorithms, LLM
agents, advanced dashboards, N-run web analytics, a dynamic standards crawler, a formal proof of
the hybrid combiner, full finite-key composable security, and production deployment/certification
are excluded.

## 18. Future Work

Future research may replace the simulated QKD source with a standards-shaped key-delivery boundary,
study physical/optical models and additional adversaries, extend finite-key security, add QKD
protocols or PQC algorithms, analyze other combiners, and evaluate production/distributed
deployments. None is required to answer the current research question.

## 19. Threats to Validity

- **Construct validity:** numerical BB84 runtime is not hardware performance; liboqs timing is
  platform-specific; byte-count layers must not be conflated.
- **Internal validity:** RNG seeds, warm-up, execution order, background load, sampling fraction,
  channel assumptions, and implementation versions can affect measurements.
- **External validity:** logical single-qubit channels omit optical loss, detectors, dark counts,
  decoy states, devices, networks, and production transports.
- **Conclusion validity:** small samples, inappropriate averages, unsupported tests, or aggregate
  QBER can hide relevant behavior. Report distributions and justified intervals.
- **Security validity:** intercept-resend is not a complete adversary model; the estimator is
  currently partial; authentication and hybrid guarantees are limited to what is executed and
  documented.

## 20. Related Work Positioning

QuantumSec is positioned as an experimental integration and validation laboratory. Its novelty is
not the existence of BB84, ML-KEM, ML-DSA, HQC, HKDF, AES-GCM, or hybridization. Its target
contribution is controlled measurement of cost and assumptions across representative strategies,
validation against analytical behavior, correction and revalidation of the discovered
model-assumption violation, and a reproducible interface for inspecting those results.

Normative status references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST's HQC selection announcement](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).
