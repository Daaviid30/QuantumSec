# QuantumSec Web Laboratory

The web application is the view/controller for the implemented QuantumSec research laboratory. It
executes the real domain and orchestration layers; it does not reproduce quantum, cryptographic,
security-estimation, or data-protection logic in React.

## Product surfaces

- **Overview** — seven public security profiles, executable capabilities, research boundary, and
  backend readiness.
- **Laboratory** — profile selection, Guided/Research configuration, real execution, ordered trace,
  QKD/PQC/hybrid metrics, authentication, provenance, and the protected-message demonstration.
- **Runs** — bounded process-local public records and exact-configuration reruns.
- **Compare** — exactly two records with conservative QKD/PQC compatibility rules.

Campaign-scale experiment analysis remains in `experiments/analysis`; the browser does not recreate
an N-run dashboard.

## Current profiles

| Public profile | Establishment | Authentication | Web status |
|---|---|---|---|
| `QKD-ASSUMED` | BB84 | Authenticated classical channel assumed | **CURRENT** |
| `QKD-CLASSICAL-AUTH` | BB84 | One-time universal-hash/PSK construction | **CURRENT** |
| `QKD-PQC-AUTH` | BB84 | ML-DSA-65 transcript authentication | **CURRENT** |
| `PQC-BASE` | ML-KEM-768 | ML-DSA-65 | **CURRENT** |
| `PQC-DIVERSE` | ML-KEM-768 + HQC-3 | ML-DSA-65 | **CURRENT** |
| `HYBRID` | BB84 + ML-KEM-768 | Explicit QKD policy + ML-DSA-65 PQC auth | **CURRENT** |
| `HYBRID-DIVERSE` | BB84 + ML-KEM-768 + HQC-3 | Explicit QKD policy + ML-DSA-65 PQC auth | **CURRENT** |

`PQCProfile.LOW/HIGH` remain internal transcript identifiers and are not primary UI terminology.
HQC-3 is described as selected for NIST standardization, not as an already published standard.

## Architecture

```text
React / TypeScript product UI
    -> typed JSON / HTTP
FastAPI capabilities, schemas, and WebLaboratoryService
    -> ExperimentConfig + ExperimentRuntimeFactory
        -> orchestration.run_session
            -> qkd / pqc / hybrid domains
            -> public SessionResult, trace, categorized metrics, provenance
        -> immutable secret-safe ExperimentRecord

Opaque run ID -> backend-only ProtectedSession -> AES-256-GCM public result facts
```

The process-local run store retains at most 100 public records. Durable storage, authentication,
authorization, remote jobs, and production key custody are explicit non-goals of this research UI
phase.

## API

```text
GET  /api/health
GET  /api/capabilities
POST /api/sessions
GET  /api/runs
GET  /api/runs/{run_id}
POST /api/compare
POST /api/runs/{run_id}/protect

# retained compatibility route
POST /api/simulations/bb84
```

The session API returns normalized configuration, environment/provisioning metadata, terminal
result, ordered trace, categorized metrics, bounded Eve diagnostics, and data-plane availability.
It never returns private identities, shared KEM secrets, raw QKD final material, `K_SESSION`,
`K_CONFIRM`, or authentication secrets.

The protected-message endpoint consumes the backend-held session capability. It owns nonce
allocation, AAD, tag generation, encryption/decryption, and tamper rejection. React receives only
public sizes, status, and a bounded ciphertext preview.

## Measurement contract

- BB84 is a seeded NumPy logical-qubit simulation. Its software runtime is not physical QKD
  latency, secret-key rate, fiber throughput, device performance, or distance.
- PQC profiles execute real liboqs software operations. Their timings are comparable only under a
  documented compatible environment and require distributions for benchmark claims.
- Compare never ranks QKD simulation runtime against PQC handshake timing.
- Raw cryptographic, canonical protocol, and serialized transport byte layers remain distinct.

## Development

From the repository root:

```bash
uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
```

From `ui/frontend`:

```bash
npm ci
npm run dev
```

Vite serves `http://localhost:5173` and proxies `/api` to `http://127.0.0.1:8000`.

## Verification

```bash
uv run python -m ruff check .
uv run python -m ruff format --check .
uv run python -m pyright
uv run python -m pytest -q

cd ui/frontend
npm test -- --run
npm run typecheck
npm run build
```

See [`../TFM_GOAL.md`](../TFM_GOAL.md), [`../docs/structure.md`](../docs/structure.md), and
[`../docs/UI_REDESIGN.md`](../docs/UI_REDESIGN.md) for the academic, architectural, and product
contracts.
