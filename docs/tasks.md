# QuantumSec TFM Roadmap

This roadmap tracks the closed TFM scope defined in [`../TFM_GOAL.md`](../TFM_GOAL.md). Detailed
historical implementation checklists have been retired because their completed milestones no
longer described the project's current direction.

Status date: **2026-09-05**.

## Completed / current

- [x] Acyclic `core -> quantum -> qkd` foundation with injected simulation randomness.
- [x] Immutable quantum state, measurement, validation, and information primitives.
- [x] BB84 preparation, transmission, projective measurement, and basis sifting.
- [x] Identity, Depolarizing, Bit Flip, Phase Flip, Pauli, and Amplitude Damping channels.
- [x] Sampled QBER estimation with disclosed-position removal and explicit aborts.
- [x] Cascade reconciliation with recorded parity leakage.
- [x] Universal-hash post-reconciliation verification with recorded tag leakage.
- [x] Asymptotic BB84 length estimation and FFT Toeplitz privacy amplification.
- [x] ML-DSA-65 identities and explicit pre-provisioned trust.
- [x] ML-KEM-768 and HQC-3 providers through liboqs.
- [x] `LOW` (ML-KEM-768) and `HIGH` (ML-KEM-768 + HQC-3) PQC profiles.
- [x] Signed `ServerKeyOffer` and `ClientKeyExchange` with verify-before-KEM behavior.
- [x] Canonical authenticated transcript and profile-aware KEM-secret encoding.
- [x] HKDF-SHA-384 derivation of a 32-byte `K_SESSION`.
- [x] Separate 32-byte `K_CONFIRM` and bilateral role-bound HMAC-SHA-384 Finished messages.
- [x] Role-local established PQC session handles with explicit secret lifecycle.
- [x] FastAPI/React BB84 laboratory with real results, capability discovery, charts, and inspection.

## Remaining TFM implementation work

### 1. Unified session contracts and profiles

- [ ] Define configuration, trace, metrics, and result types shared by orchestration and the UI.
- [ ] Map current `LOW` to PQC and `HIGH` to PQC Diversified without renaming domain APIs.
- [ ] Represent QKD Experimental without pretending its assumed authenticated channel was executed.
- [ ] Preserve algorithm/backend versions and component provenance.

### 2. QKD–PQC hybrid integration

- [ ] Add an upper orchestration layer that consumes public QKD and PQC results.
- [ ] Define a hybrid-specific canonical secret input with component labels, lengths, fixed ordering,
  provenance, and domain separation.
- [ ] Implement Hybrid QKD–PQC (BB84 + ML-KEM-768).
- [ ] Implement Hybrid Diversified (BB84 + ML-KEM-768 + HQC-3).
- [ ] Bind the final derivation to the selected profile and appropriate transcript/session context.
- [ ] Define and test final key confirmation without making a formal robust-combiner claim.

### 3. AES-256-GCM protected-message demo

- [ ] Consume the established 32-byte `K_SESSION`; do not derive application encryption from a
  public or unconfirmed value.
- [ ] Generate nonces securely and prevent nonce reuse under the same key.
- [ ] Support appropriate AAD, potentially binding session/profile/transcript metadata.
- [ ] Demonstrate encrypt/decrypt and explicit authentication failure after ciphertext/tag changes.
- [ ] Keep payload protection in a separate layer from KEM, signature, QKD, and KDF code.

### 4. Experiment engine

- [ ] Implement `CONFIG -> RUN -> TRACE -> METRICS -> RESULT -> COMPARE` records.
- [ ] Capture deterministic simulation seeds and immutable configuration snapshots.
- [ ] Record secure PQC backend versions without forcing deterministic cryptographic randomness.
- [ ] Export versioned JSON/CSV and thesis-ready aggregate tables/figures.
- [ ] Implement the four bounded experiments below.

| Experiment | Comparison | Required evidence |
|---|---|---|
| PQC profiles | `LOW` vs `HIGH` | phase/total timings, bytes, key/ciphertext/signature sizes, success |
| BB84 channels | implemented channel parameters | sampled QBER, sizes, leakage, efficiency, aborts |
| Hybrid establishment | QKD + ML-KEM vs diversified hybrid | functional agreement, provenance, overhead |
| End-to-end session | established key to AES-256-GCM | decrypt success, tamper failure, session metadata |

### 5. Web laboratory

- [ ] Extend capability discovery with implemented security-profile status.
- [ ] Build a profile-aware Session Builder using only supported backend parameters.
- [ ] Add a real-event protocol/handshake visualizer for QKD, PQC, and hybrid runs.
- [ ] Add experiment result persistence/selection and multi-run comparison.
- [ ] Add the Protected Message Demo with a clear establishment/data-plane boundary.
- [ ] Add a versioned, sourced Quantum-Safe Explorer only if it supports the thesis workflow.

### 6. Experimental campaign and thesis

- [ ] Freeze experiment versions, configurations, environments, and measurement methodology.
- [ ] Execute repeated runs and report distributions and limitations.
- [ ] Separate software timing from any claim about physical QKD equipment.
- [ ] Analyze results against the research question and subquestions.
- [ ] Complete the defense flow: QKD, PQC, hybrid, AES-GCM, comparison, conclusions.

## Quality gates for every implementation block

```bash
uv run pytest
uv run ruff check .
uv run pyright

cd ui/frontend
npm test
npm run typecheck
npm run build
```

After code changes, run `graphify update .` to synchronize the repository knowledge graph.

## Future work — not required for the TFM

- B92, E91, and BBM92;
- optical/device-level QKD and hardware integration;
- QKDN, routing, and repeaters;
- additional PQC algorithms;
- richer or formally verified combiners;
- LLM/autonomous agents;
- production optimization, certification, and large-scale deployment.

## Definition of done

The checklist above is complete only when the executable QKD, PQC, hybrid, AES-GCM, experiment, and
web paths satisfy Section 15 of [`../TFM_GOAL.md`](../TFM_GOAL.md). Documentation-only profile names
or mocked UI events do not satisfy that contract.
