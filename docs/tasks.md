# QuantumSec TFM Implementation Plan

This is the ordered implementation plan for the definitive thesis contract in
[`../TFM_GOAL.md`](../TFM_GOAL.md). Do not start a later phase by fabricating contracts or UI
behavior from an earlier unfinished phase.

## Current baseline

- [x] Acyclic `core -> quantum -> qkd` foundation with injected randomness.
- [x] Executable BB84 pipeline with implemented logical-qubit channels and explicit abort results.
- [x] Sampled aggregate QBER, disclosure removal, Cascade, reconciled-key verification, asymptotic
  extraction, and Toeplitz privacy amplification.
- [x] `PQC-BASE` (internal `LOW`) end-to-end handshake.
- [x] `PQC-DIVERSE` (internal `HIGH`) end-to-end handshake.
- [x] ML-DSA-65 identities/trust, authenticated transcript, structured KEM input,
  HKDF-SHA-384, separate `K_SESSION`/`K_CONFIRM`, and bilateral Finished.
- [x] Current BB84 FastAPI adapter and React workspace.

The existing QKD session is **PARTIAL** as a security profile: it assumes classical-channel
authentication and its aggregate-QBER estimator is not valid for every supported asymmetric
channel.

## Exact implementation order

### 1. Intercept-resend Eve

- [ ] Implement Eve above or within the QKD channel boundary without coupling `qkd` to `pqc`.
- [ ] Inject all Eve basis choices, interception decisions, measurements, and resends through
  `BaseRNG`.
- [ ] Support an interception fraction `f` and explicit disabled/`f=0` behavior.
- [ ] Trace Eve without exposing secret material.
- [ ] Validate `QBER ~= 0.25 f` under the stated ideal model across seeded repetitions.
- [ ] Expose Eve configuration and results through the BB84 API only after the domain path exists.

Exit condition: E3 can generate QBER and abort-probability curves against the analytical baseline.

### 2. Per-basis QBER and validation fixtures

- [ ] Preserve basis labels through parameter-estimation sampling.
- [ ] Add `e_Z`, `e_X`, sample sizes by basis, and aggregate QBER to immutable domain results.
- [ ] Define behavior when a basis has insufficient or zero disclosed observations.
- [ ] Expose the new metrics through the backend without changing their meaning.
- [ ] Add deterministic tests for Identity, Depolarizing, Bit Flip, Phase Flip, Pauli, and Amplitude
  Damping predictions.
- [ ] Reproduce and record the asymmetric Phase Flip discrepancy as a validation fixture.

Exit condition: E2 can observe the quantity that the security model requires instead of only an
aggregate.

### 3. Correct the BB84 security-decision model

- [ ] Identify and cite the phase-error relation for the exact implemented BB84 sampling/model.
- [ ] Specify which per-basis observation or justified bound feeds abort and secret-length logic.
- [ ] Fail conservatively when observations cannot support the bound or the channel/configuration
  is outside the model's declared validity.
- [ ] Do not substitute `max(e_Z, e_X)` without a theoretical argument.
- [ ] Add regression tests proving that the former asymmetric over-extraction cannot recur.
- [ ] Revalidate E2 fixtures after the correction and document before/cause/after.

Exit condition: Definition of Done item 2 is satisfied and `QKD-ASSUMED` is no longer partial for
the estimator reason.

### 4. Session, profile, trace, metric, and result contracts

- [ ] Add an upper orchestration layer that imports `qkd` and `pqc`; keep both domains independent.
- [ ] Implement public profile names while preserving internal `PQCProfile.LOW/HIGH` values.
- [ ] Represent establishment provenance and authentication as independent, explicit dimensions.
- [ ] Define versioned configuration, ordered trace, compatible metric, terminal result, and abort
  contracts.
- [ ] Ensure capability discovery distinguishes **CURRENT**, **PARTIAL**, and **PLANNED**.
- [ ] Prohibit secret values and private key material from trace/result serialization.

Exit condition: all later profiles can share one orchestration boundary without semantic loss.

### 5. Execute QKD authentication

#### 5a. `QKD-PQC-AUTH` — required first

- [ ] Define the canonical security-relevant BB84 classical transcript/messages.
- [ ] Reuse ML-DSA-65 identities and explicit pre-provisioned trust above the sibling domains.
- [ ] Sign and verify before any unauthenticated security-relevant data can be accepted.
- [ ] Add transcript/message tamper, wrong identity, missing signature, replay/context, and failure
  tests.
- [ ] Record operations, bytes, meaningful latency, trust assumptions, and outcome.

#### 5b. `QKD-CLASSICAL-AUTH` — required for the definitive comparison

- [ ] Specify a correct universal-hash/Wegman–Carter-style construction.
- [ ] Provide secret pre-shared authentication material and required key separation.
- [ ] Implement tag generation, verification, and explicit failure.
- [ ] Account for authentication-key consumption where the construction requires it.
- [ ] Test modified transcript/tag, wrong key, reuse constraints, and consumption accounting.

Exit condition: at least one QKD profile executes authentication; E4 compares both mechanisms only
if both constructions satisfy their contracts.

### 6. Hybrid session establishment

- [ ] Implement `HYBRID` from successful BB84 material and authenticated ML-KEM-768 material.
- [ ] Implement `HYBRID-DIVERSE` with the additional HQC-3 component.
- [ ] Define a hybrid-specific canonical encoding with labels, lengths, count, deterministic order,
  profile, provenance, and domain separation.
- [ ] Bind transcript/ciphertext context where required by the final protocol specification.
- [ ] Derive a 32-byte `K_SESSION` with HKDF-SHA-384 and preserve explicit provenance.
- [ ] Define final confirmation semantics and distributed-session limitations.
- [ ] Add order, omission, duplication, profile mismatch, boundary, sensitivity, authentication
  failure, QKD abort, KEM failure, and Finished failure tests.
- [ ] State only the security claim justified by the construction; do not claim a new robust
  combiner proof or automatic information-theoretic security.

Exit condition: `HYBRID` and `HYBRID-DIVERSE` work end to end.

### 7. AES-256-GCM protected session

- [ ] Consume only an established 32-byte `K_SESSION`.
- [ ] Use 96-bit nonces with enforced uniqueness per key/session policy.
- [ ] Use the full 128-bit authentication tag.
- [ ] Bind appropriate session/profile/transcript metadata as AAD.
- [ ] Return plaintext only after successful authentication.
- [ ] Test valid round-trip and modified ciphertext, tag, AAD, nonce policy, and wrong-key failure.

Exit condition: D1 demonstrates the establishment/data-plane boundary and all tampering is rejected.

### 8. Minimal experiment engine

- [ ] Implement `CONFIG -> RUN -> RECORD -> EXPORT -> ANALYZE`.
- [ ] Capture run ID, profile, normalized config, seed where applicable, Python, NumPy, liboqs,
  wrapper, CPU, OS, backend versions, ordered condition, trace, metrics, and outcome.
- [ ] Export versioned JSON and analysis-ready CSV without secrets.
- [ ] Support randomized condition order and discarded warm-up for PQC timing.
- [ ] Report median/IQR and justified distribution summaries.
- [ ] Report justified binomial intervals for QBER/proportions.
- [ ] Distinguish raw cryptographic, canonical protocol, and serialized transport sizes.

Exit condition: all five experiments can be reproduced from saved configurations and records.

### 9. Execute the experimental campaign

- [ ] **E1 — PQC Cost Decomposition:** `PQC-BASE` versus `PQC-DIVERSE`, minimum 30 and preferably
  50 runs; persistent identity provisioning separate.
- [ ] **E2 — BB84 Model Validation:** analytical versus simulated per-basis/aggregate error,
  sifting, final material, and abort behavior.
- [ ] **E3 — Eve / Intercept-Resend:** vary `f`; measure QBER, per-basis error, abort probability,
  and final material.
- [ ] **E4 — QKD Authentication Cost:** assumed baseline versus correctly executed authentication
  profiles.
- [ ] **E5 — Hybrid Marginal Overhead:** provenance, component sizes, orchestration bytes,
  combiner/HKDF/confirmation cost, outcome, and negative tests.
- [ ] **D1 — Protected Session:** capture successful AES-GCM flow and tamper-rejection matrix.

The measurement-category and statistics rules are centralized in
[`../TFM_GOAL.md §12`](../TFM_GOAL.md#12-experimental-methodology).

### 10. Web Laboratory V1

- [ ] **Builder:** supported profile selector; signal count, seed, channel/parameters, Eve fraction;
  profile-derived PQC components; contextual cards.
- [ ] **Run:** real Alice/Bob/Eve trace, explicit authentication state, compatible metrics,
  outcome, and protected-message strip.
- [ ] Show `CLASSICAL AUTHENTICATION — ASSUMED / NOT EXECUTED` for `QKD-ASSUMED`.
- [ ] **Compare:** exactly two saved runs with configuration diff, components, assumptions,
  compatible metrics, bytes, outcome, and security notes.
- [ ] Prevent direct temporal comparison between numerical BB84 and real PQC operations.
- [ ] Add small, static/versioned, sourced component cards with a status-as-of date.
- [ ] Remove the separate Quantum-Safe Explorer concept; do not build N-run web analytics.
- [ ] Add backend, frontend, accessibility, loading/error, and unsupported-capability tests.

Exit condition: Builder, Run, and Compare render actual backend records without invented behavior.

### 11. Thesis analysis and freeze

- [ ] Freeze experiment/config/schema versions and the reference environment.
- [ ] Generate tables and figures from exported records.
- [ ] Accept, reject, or qualify H1–H5.
- [ ] Answer every research question with evidence or an explicit limitation.
- [ ] Document threats to validity, security boundaries, and non-claims.
- [ ] Confirm that the provisional title still matches the results before finalizing it.

## Final documentation audit

Before declaring the TFM complete, search live documentation, API capability text, and UI copy for:

- old research questions centered on integration rather than measurable cost;
- public `LOW/HIGH` terminology instead of `PQC-BASE/PQC-DIVERSE`;
- QKD runtime presented as physical latency, secret-key rate, distance, or fiber throughput;
- HQC described as a final NIST standard;
- assumed authentication presented as executed;
- the reconciled-key verification tag presented as a channel MAC;
- Eve or per-basis QBER presented as current before implementation;
- aggregate QBER presented as valid for every supported channel;
- AES-GCM or hybrid orchestration presented as current before implementation;
- a separate Quantum-Safe Explorer or N-run dashboard;
- incompatible metrics compared on one axis; and
- obsolete roadmap or status text.

## Quality gate

```text
uv run pytest
uv run ruff check .
uv run pyright

cd ui/frontend
npm test
npm run typecheck
npm run build
```

After code changes, run `graphify update .`.
