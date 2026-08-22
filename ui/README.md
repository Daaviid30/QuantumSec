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
- raw/sifted counts, sifting efficiency, QBER, and adapter-measured execution time
- Alice/Bob basis distributions and Bob measurement outcome distribution
- a bounded inspector containing the first 64 positions from the actual `BB84Result`
- capability discovery for implemented and planned product areas

Amplitude damping is described as qubit relaxation, not photon loss. Unsupported protocols and
post-processing stages remain disabled.

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

From the repository root:

```bash
uv sync --dev
uv run uvicorn ui.backend.main:app --reload --port 8000
```

In another terminal:

```bash
cd ui/frontend
npm install
npm run dev
```

The frontend is served at `http://localhost:5173`; Vite proxies `/api` to
`http://127.0.0.1:8000`.

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
