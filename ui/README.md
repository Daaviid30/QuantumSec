# QuantumSec Web UI V1

QuantumSec Web UI is a research-oriented interface over the existing simulation engine. It is split
into a typed FastAPI adapter and a React application:

```text
frontend
   ↓ JSON / HTTP
ui/backend
   ↓ explicit adapters
BB84Protocol + ChannelPipeline + SeededRNG
   ↓
qkd / quantum / core
```

The simulation packages do not import the UI. No measurement, channel, RNG, sifting, or QBER logic is
duplicated in TypeScript or in the HTTP route layer.

## Supported V1 features

- BB84 with a configurable positive signal count and deterministic seed
- ordered pipelines containing Identity, Depolarizing, Bit Flip, Phase Flip, Pauli, and Amplitude
  Damping channels
- raw/sifted counts, diagnostic full-key QBER, and adapter-measured execution time
- sampled parameter estimation, Cascade leakage, universal-hash confirmation, asymptotic secret
  length estimation, and FFT Toeplitz privacy amplification summaries
- Alice/Bob basis distributions and Bob measurement outcome distribution
- raw-to-final key-material shrinkage and an expandable final simulated key for completed sessions
- a bounded inspector containing the first 64 positions from the actual `BB84Result`
- capability discovery for implemented and planned product areas

Amplitude damping is described as qubit relaxation, not photon loss. Unsupported protocols remain
disabled. The post-processing summary reports secure aborts as ordinary session outcomes.
The displayed key is educational simulator output and must not be used as production key material;
large public Toeplitz seeds remain internal to the backend.

## API

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The BB84 request uses a discriminated channel union. Pydantic validates probability ranges and the
Pauli constraint `px + py + pz <= 1` before an adapter instantiates the engine classes. Responses are
JSON-safe DTOs; NumPy values and arrays never cross the HTTP boundary directly.

## Development

### Prerequisites

- Python 3.14 and [`uv`](https://docs.astral.sh/uv/)
- Node.js 20.19+ (or 22.12+) and npm

### First-time setup

Run these commands from the repository root:

```bash
uv sync --dev
cd ui/frontend
npm ci
```

### Start the application

The frontend and backend are separate development servers. Start the backend first and keep both
terminals open.

1. In the first terminal, from the **repository root**, start FastAPI:

   ```bash
   uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

   Wait until Uvicorn prints `Application startup complete`. Check that it responds by opening
   `http://127.0.0.1:8000/api/health`; the response should contain `"status":"ok"`.

2. In a second terminal, start Vite:

   ```bash
   cd ui/frontend
   npm run dev
   ```

3. Open `http://localhost:5173`.

The browser sends requests to `/api`. While using `npm run dev`, Vite proxies those requests to
`http://127.0.0.1:8000`, so the backend must remain running on port `8000`.

### If the frontend cannot connect to the backend

- Check `http://127.0.0.1:8000/api/health` first. If it does not load, start or restart Uvicorn.
- Run the Uvicorn command from the repository root, not from `ui/frontend`; Python needs the root on
  its import path to resolve `ui`, `qkd`, `quantum`, and `core`.
- Make sure no other process is using ports `8000` or `5173`. Vite uses a strict port and will stop
  instead of silently choosing another one.
- Use the exact ports above. The proxy target is configured in `ui/frontend/vite.config.ts`.
- If dependencies are missing, rerun `uv sync --dev` at the root and `npm ci` inside
  `ui/frontend`.

## Verification

```bash
uv run pytest
uv run ruff check .

cd ui/frontend
npm test
npm run typecheck
npm run build
```

## Extension points

- add a new protocol to the engine, then add its request adapter and capability entry
- add a public `QuantumChannel`, then add one schema branch and explicit adapter mapping
- activate planned frontend phases only when `/api/capabilities` reports them implemented
- introduce experiment orchestration as a separate upper layer instead of looping inside protocol or
  UI components
