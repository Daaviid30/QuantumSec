# QuantumSec TFM Goal

## 1. Thesis in One Sentence

QuantumSec designs and evaluates a reproducible laboratory that integrates QKD, PQC, and hybrid
QKD–PQC session-establishment strategies while making their security assumptions, behavior, and
operational overhead directly comparable.

## 2. Problem Statement

Quantum-safe key establishment spans technologies with different primitives, trust models,
maturity, and measurable costs. QKD can generate shared secret material but requires an
authenticated classical channel; PQC KEMs establish computationally protected shared secrets and
signatures provide identity authentication; hybrid schemes must compose these outputs without
hiding provenance or overstating security. Existing demonstrations are often isolated and measured
under incompatible assumptions. The TFM therefore needs one bounded architecture and methodology
that can execute, trace, visualize, and compare representative paths end to end.

## 3. Research Question

How can implemented QKD and PQC session-establishment paths, together with explicitly specified
hybrid compositions of their secret material, be integrated into a common reproducible laboratory
to compare their behavior, security assumptions, and operational overhead?

## 4. Research Subquestions

1. Which common configuration, trace, metric, and result contracts permit fair comparison without
   treating simulated QKD timing as physical-system performance?
2. How do the implemented PQC and diversified PQC profiles differ in computational and
   communication overhead?
3. How can QKD-derived and PQC-derived secret material be combined with explicit encoding, domain
   separation, provenance, and key confirmation while avoiding unsupported security claims?
4. How effectively can a web laboratory communicate the distinction between key establishment and
   authenticated application-data protection?

## 5. General Objective

Design, implement, and experimentally evaluate a modular laboratory for reproducible quantum-safe
session establishment using BB84, implemented PQC primitives, and bounded hybrid QKD–PQC profiles.

## 6. Specific Objectives

1. Preserve and validate the implemented BB84 path from state preparation through privacy
   amplification and explicit abort outcomes.
2. Demonstrate the implemented mutually authenticated `LOW` and `HIGH` PQC handshakes using exact
   algorithm and transcript bindings.
3. Define and implement unified security profiles without introducing direct `qkd`/`pqc` coupling.
4. Specify and implement a domain-separated hybrid secret input that retains component provenance
   before HKDF-SHA-384 derives a 256-bit `K_SESSION`.
5. Use the established `K_SESSION` in an AES-256-GCM protected-message demonstration with nonce and
   tamper-handling tests.
6. Produce reproducible experiment records and compare the principal QKD, PQC, and hybrid paths
   using available metrics.
7. Extend the web laboratory to configure, execute, trace, and visualize the principal TFM
   scenarios without exposing unsupported options.

## 7. Thesis Contribution

- **Engineering:** a modular integration boundary, explicit security profiles, common session
  results, and an end-to-end data-protection demonstration.
- **Experimental:** measured comparison of BB84 behavior, PQC profiles, hybrid overhead, and the
  final protected-session flow.
- **Methodological:** a reproducible `CONFIG -> RUN -> TRACE -> METRICS -> RESULT -> COMPARE`
  process with explicit assumptions and provenance.
- **Educational/visual:** an interface that shows what each primitive contributes and separates
  establishment from payload encryption.

## 8. What QuantumSec Is

QuantumSec is research and educational software for logical-qubit BB84 simulation, standalone PQC
handshakes, planned QKD–PQC composition, reproducible experiments, and protocol visualization. It
uses real PQC backend operations while treating the QKD path as a seeded numerical model. It is a
laboratory for integration and evaluation, not a new cryptographic primitive.

## 9. What QuantumSec Is NOT

QuantumSec is not commercial QKD hardware, a physical-network simulator, a production security
product, a new QKD/PQC algorithm, a proof that hybrid combination is automatically robust, or a
claim of unconditional end-to-end security. It does not equate QKD with encryption, a KEM with
application-data encryption, a signature with key establishment, HKDF with encryption, or NumPy
execution time with physical QKD latency or secret-key rate.

## 10. Security Model

- **QKD assumptions:** BB84 is modeled over logical qubits and configured CPTP channels. Security
  decisions use sampled QBER; the current length estimator is asymptotic, not a composable
  finite-key proof.
- **Authenticated classical channel:** the BB84 classical transcript is currently assumed
  authenticated. Standalone simulation does not supply that mechanism.
- **PQC authentication:** ML-DSA-65 identities are trusted only through explicit pre-provisioning.
  Both `ServerKeyOffer` and `ClientKeyExchange` are signed and verified before KEM operations that
  depend on peer authenticity.
- **KEM assumptions:** `LOW` uses ML-KEM-768; `HIGH` uses ML-KEM-768 and HQC-3. Successful KEM
  operations produce independent shared-secret inputs for the configured profile.
- **Hybrid diversification:** planned profiles combine successful QKD and PQC material in an upper
  layer with labels, lengths, domain separation, and provenance.
- **Combiner limitations:** the current PQC encoding and planned hybrid construction support
  integration research. The TFM does not present a new formal robust-combiner proof and does not
  claim that one secure input automatically guarantees the output.
- **Key confirmation:** the current PQC handshake derives a separate 32-byte `K_CONFIRM` and uses
  role-separated, chained HMAC-SHA-384 Finished messages. BB84's universal-hash verification is a
  separate post-reconciliation mechanism.
- **Data plane:** AES-256-GCM is planned to consume the established 32-byte `K_SESSION`; it will use
  non-repeating nonces per key, authenticate optional session metadata as AAD, and reject modified
  ciphertext or tags.

## 11. Security Profiles

| Profile | Components | Purpose | Current status |
|---|---|---|---|
| QKD Experimental | BB84 final material; authenticated classical channel as an explicit assumption | Study QKD channel and post-processing behavior | CURRENT standalone path; PLANNED unified profile |
| PQC (`LOW`) | ML-KEM-768 + ML-DSA-65 | Authenticated PQC establishment | CURRENT |
| PQC Diversified (`HIGH`) | ML-KEM-768 + HQC-3 + ML-DSA-65 | Diverse KEM integration and overhead | CURRENT |
| Hybrid QKD–PQC | BB84 material + ML-KEM-768 + explicit authentication policy | Integrate QKD and standardized PQC establishment | PLANNED |
| Hybrid Diversified | BB84 material + ML-KEM-768 + HQC-3 + explicit authentication policy | Evaluate added diversity and overhead | PLANNED |

As of **2026-09-05**, ML-KEM and ML-DSA are standardized by NIST in FIPS 203 and FIPS 204. HQC
was selected for standardization on 2025-03-11; QuantumSec does not describe it as a final FIPS
standard. `LOW` and `HIGH` are project profile names, not NIST categories.

## 12. Experimental Methodology

Every experiment follows a versioned record from configuration to comparison. Modeled randomness
uses injected seeds; cryptographic operations retain secure backend randomness and record backend
metadata instead of forcing deterministic keys. Repeated runs separate warm-up effects where
needed and report distributions rather than a single favorable measurement.

The planned campaign contains:

1. **PQC profile comparison:** compare `LOW` and `HIGH` handshake timing and communication sizes.
2. **BB84 channel behavior:** vary implemented noise parameters and study QBER, sifting, final
   material, efficiency, leakage, and aborts.
3. **Hybrid key establishment:** verify functional integration and measure overhead for QKD +
   ML-KEM-768, with optional HQC-3 diversification.
4. **End-to-end secure session:** derive `K_SESSION`, protect a payload with AES-256-GCM, verify
   decryption, and demonstrate authentication failure after tampering.

## 13. Key Metrics

- terminal success/abort status and reason;
- phase and total timings, clearly labeled as software measurements;
- bytes exchanged and public-key, ciphertext, and signature sizes;
- QKD raw, sifted, disclosed, candidate, reconciled, and final sizes;
- diagnostic and sampled QBER, sifting efficiency, leakage, and final secret fraction;
- derived-key length, profile, component provenance, run ID, seed, and configuration snapshot.

Secret values are not experiment metrics.

## 14. TFM Deliverables

- modular QuantumSec software;
- reproducible experiment definitions and records;
- comparative results, tables, and figures;
- a web laboratory for the principal scenarios;
- accurate architecture, security-model, usage, and scope documentation;
- the Master's thesis and defense demonstration.

## 15. Definition of Done

The TFM is complete only when:

- the QKD path is demonstrable from preparation through final material or justified abort;
- the `LOW` and `HIGH` PQC paths are demonstrable through mutual Finished confirmation;
- QKD–PQC hybrid integration is demonstrable without direct sibling-package coupling;
- both sides derive the expected 256-bit `K_SESSION` under the implemented profile contract;
- the AES-256-GCM protected-message demo decrypts valid data and rejects tampering;
- the web laboratory runs and visualizes the principal QKD, PQC, hybrid, and data-plane scenarios;
- reproducible experiments emit versioned configurations, traces, metrics, and comparable results;
- the experimental evidence is sufficient to answer the research question and document
  limitations honestly.

## 16. Out of Scope

- multiple additional QKD protocols unless all required work is already complete;
- QKD networks, routing, and quantum repeaters;
- production or commercial QKD hardware;
- a new formal cryptographic security proof;
- new PQC algorithms;
- LLM or autonomous agents;
- production optimization, certification, or deployment hardening;
- full physical simulation of commercial devices.

## 17. Future Work

- E91, B92, and BBM92;
- QKDN topology, routing, repeaters, and key management;
- physical QKD device and optical-loss integration;
- additional PQC algorithms and security profiles;
- richer combiners and formal verification;
- larger cross-platform benchmarking;
- deployment and interoperability research.

## 18. Proposed Thesis Title

**English:** *QuantumSec: Design and Evaluation of a Reproducible Laboratory for Quantum-Safe
Session Establishment Based on QKD, PQC, and Hybrid Strategies*

**Español:** *QuantumSec: Diseño y evaluación de un laboratorio reproducible para el
establecimiento de sesiones quantum-safe basado en QKD, PQC y estrategias híbridas*

Standards references: [NIST FIPS 203](https://csrc.nist.gov/pubs/fips/203/final),
[NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), and
[NIST HQC selection](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption).
