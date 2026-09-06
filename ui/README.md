# QuantumSec Web Laboratory V1

The web application is the interface to the QuantumSec experimental laboratory. It is not the
scientific contribution by itself and it does not implement cryptographic or quantum logic.

The current release is a working BB84 configuration/results workspace. The definitive V1 target is
limited to **Builder**, **Run**, and **Compare**. There is no separate Quantum-Safe Explorer.

## Status

| Capability | Status |
|---|---|
| BB84 signal/seed/channel builder | **CURRENT** |
| BB84 execution, abort/result, charts, and raw inspector | **CURRENT** |
| Per-basis `e_Z/e_X` and corrected estimator | **PLANNED** |
| Eve interception fraction and adversary timeline | **PLANNED** |
| `QKD-ASSUMED` explicit authentication state | **PLANNED UI**; underlying assumption is current |
| Executed QKD classical/PQC authentication | **PLANNED** |
| `PQC-BASE`/`PQC-DIVERSE` domain handshakes | **CURRENT domain**, **PLANNED UI/API** |
| `HYBRID`/`HYBRID-DIVERSE` | **PLANNED** |
| Experiment records and two-run comparison | **PLANNED** |
| AES-256-GCM protected-message strip | **PLANNED** |

## Architecture

```text
React / TypeScript
    -> JSON / HTTP
FastAPI capabilities, schemas, routes, adapters
    -> current direct BB84 adapter
    -> planned orchestration / experiment services
        -> qkd
        -> pqc
        -> data protection
```

The frontend renders backend-reported capabilities, traces, metrics, assumptions, and outcomes. It
does not calculate QBER, simulate Eve, sign transcripts, combine secrets, derive keys, or encrypt
payloads. Controls remain disabled until the corresponding backend capability is executable.

## Current application

The BB84 request supports:

- `n_signals` from 1 to 100,000;
- an integer seed from 0 to 2^32−1;
- up to 12 ordered Identity, Depolarizing, Bit Flip, Phase Flip, Pauli, or Amplitude Damping
  channels; and
- real engine execution through `BB84Protocol`.

The response contains a request UUID, seed, software duration, channel/config snapshot, terminal
status, aggregate QBER, stage sizes, post-processing details, distributions, and at most 64 raw
transmission records. Post-processing parameters currently use domain defaults.

Current routes:

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

There are no API routes for per-basis QBER, Eve, executed QKD authentication, PQC sessions, hybrid
sessions, experiments, comparison, or AES-256-GCM.

The displayed final BB84 material is simulated research output, not an application encryption key.
The existing reconciled-key verification tag is not authentication of the classical channel.

## Screen 1 — Builder

Builder configures one run using a backend-reported profile.

Target profile selector:

| Public profile | UI composition | Status |
|---|---|---|
| `QKD-ASSUMED` | BB84; classical authentication assumed | **PARTIAL** |
| `QKD-CLASSICAL-AUTH` | BB84 plus executed classical/ITS authentication | **PLANNED** |
| `QKD-PQC-AUTH` | BB84 plus ML-DSA-65 transcript authentication | **PLANNED** |
| `PQC-BASE` | ML-KEM-768 + ML-DSA-65 | **CURRENT domain**, **PLANNED UI/API** |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 + ML-DSA-65 | **CURRENT domain**, **PLANNED UI/API** |
| `HYBRID` | BB84 + ML-KEM-768 + explicit authentication policy | **PLANNED** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 + explicit authentication policy | **PLANNED** |

The UI never exposes internal `LOW/HIGH` names. The backend may preserve
`PQCProfile.LOW/PQCProfile.HIGH` in existing transcripts and HKDF contexts.

QKD controls:

- signal count;
- seed;
- ordered channel and valid channel parameters; and
- Eve interception fraction once the adversary exists.

PQC algorithms are derived from the selected profile. Builder must not offer an arbitrary algorithm
picker that can generate unsupported combinations.

### Contextual cards

Cards are small, contextual, static/versioned, dated, sourced, and shown only when relevant. They
answer what the component is, its role, its security assumption, what it adds to the profile, and
its normative status.

Examples:

```text
ML-KEM-768
KEM · key establishment
FIPS 203 · STANDARDIZED

ML-DSA-65
Signature · authentication
FIPS 204 · STANDARDIZED

HQC-3
Code-based KEM · diversification
liboqs 0.16.0 name
SELECTED FOR STANDARDIZATION

BB84
QKD · quantum key distribution
Requires an authenticated classical channel
```

Every standards claim includes a source and status-as-of date. As of 2026-09-05, HQC is selected
for standardization and is not presented as a published NIST standard.

## Screen 2 — Run

Run visualizes events emitted by the actual execution:

- Alice/Bob timeline and quantum transmission;
- Eve interception/measurement/resend when enabled;
- sifting, per-basis/aggregate QBER, security decision, and final material for QKD;
- authentication mechanism, coverage, verification, and failure;
- KEM generation/encapsulation/decapsulation for applicable profiles;
- structured combination, HKDF, Finished, and session outcome; and
- a protected-message strip when an established `K_SESSION` exists.

For `QKD-ASSUMED`, the screen displays:

```text
CLASSICAL AUTHENTICATION
ASSUMED — NOT EXECUTED
```

Executed profiles display the real mechanism and authenticated transcript/messages. A final
decorative signature must not be visualized as full transcript authentication.

Only profile-appropriate metrics appear. The QKD/PQC measurement-category rule is centralized in
[`../TFM_GOAL.md §12`](../TFM_GOAL.md#12-experimental-methodology).

## Screen 3 — Compare

Compare accepts exactly two saved run records. It shows:

- configuration differences;
- components and provenance;
- authentication and security assumptions;
- compatible metrics and byte layers;
- PQC timing distributions when both sides support a valid timing comparison;
- QKD per-basis QBER, key-material, and abort metrics when applicable;
- terminal outcomes; and
- security notes and limitations.

`PQC-BASE` versus `PQC-DIVERSE` supports direct timing comparison on one reference environment.
QKD versus PQC supports qualitative assumptions and each route's own metrics, never a comparison
such as “3 seconds versus 16 milliseconds.”

No N-run web dashboard is required. Campaign-scale analysis and figures are produced from exported
records outside the V1 interface.

## Protected-message strip

When a run produces `K_SESSION`, Run may show:

```text
ESTABLISHMENT PLANE -> 256-bit K_SESSION
DATA PLANE          -> AES-256-GCM -> protected payload
```

The backend owns nonce uniqueness, the full tag, AAD binding, decryption, and authentication
failure. React never receives or stores raw `K_SESSION`.

## Result and trace rules

- render ordered events returned by the backend; do not invent protocol messages;
- include explicit assumed/executed authentication state;
- keep secret values, private keys, KEM shared secrets, `K_SESSION`, and `K_CONFIRM` out of JSON
  records and browser state;
- preserve run ID, profile, config, versions, applicable seed, provenance, metrics, and outcome;
- label software duration as simulator runtime, not physical QKD performance; and
- never sum or rank incompatible measurements.

## Development

From the repository root:

```bash
uv sync --dev
cd ui/frontend
npm ci
```

Start the backend from the repository root:

```bash
uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Then start the frontend from `ui/frontend`:

```bash
npm run dev
```

Vite serves `http://localhost:5173` and proxies `/api` to `http://127.0.0.1:8000`.

## Verification

```bash
uv run pytest
uv run ruff check .
uv run pyright

cd ui/frontend
npm test
npm run typecheck
npm run build
```

See [`../TFM_GOAL.md`](../TFM_GOAL.md) for the academic contract and
[`../docs/structure.md`](../docs/structure.md) for the domain/orchestration boundaries.
