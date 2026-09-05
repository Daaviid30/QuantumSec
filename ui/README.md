# QuantumSec Web Laboratory

The Web UI is the presentation and interaction layer of the QuantumSec experimental laboratory.
Its current release is a functional BB84 workspace; PQC, hybrid, experiment-comparison, and
protected-message workspaces are TFM targets and are not exposed as implemented features.

## Status summary

| Module | Status |
|---|---|
| BB84 Session Builder | CURRENT |
| Ordered logical-qubit channel editor | CURRENT |
| BB84 flow and results visualization | CURRENT |
| Raw transmission inspector | CURRENT |
| PQC handshake builder/visualizer | PLANNED |
| Hybrid profile builder/visualizer | PLANNED |
| Experiment runs and comparison | PLANNED |
| AES-256-GCM Protected Message Demo | PLANNED |
| Sourced Quantum-Safe Explorer | OPTIONAL TFM / FUTURE |

## Architecture

```text
React / TypeScript frontend
    -> JSON / HTTP
FastAPI schemas, routes, capabilities, and adapters
    -> current direct adapter
BB84Protocol + ChannelPipeline + SeededRNG
    ->
qkd -> quantum -> core
```

The UI does not implement measurement, channel, RNG, sifting, QBER, KEM, signature, KDF, or
encryption logic. Planned QKD–PQC composition belongs in an upper session-orchestration layer that
the backend will call; it must not be recreated in React or hidden inside route handlers.

## Current BB84 workspace

The current interface supports:

- BB84 with `n_signals` from 1 to 100,000;
- a reproducible integer seed from 0 to 2^32−1;
- up to 12 ordered Identity, Depolarizing, Bit Flip, Phase Flip, Pauli, or Amplitude Damping
  channels;
- real engine execution and explicit `completed`/`aborted` outcomes;
- raw/sifted counts, sifting efficiency, and diagnostic full-sifted QBER;
- sampled parameter estimation, candidate size, Cascade corrections/leakage, universal-hash
  verification/leakage, asymptotic extraction size, compression ratio, and final secret fraction;
- basis and measurement distributions;
- raw-to-final key-material shrinkage and educational inspection of a completed simulated key;
- the first 64 transmission positions from the actual domain result;
- capability discovery that disables unsupported protocols.

The current request does not expose the post-processing configuration: sample fraction, QBER abort
threshold, Cascade configuration, verification tag length, and security margin use domain defaults.
Amplitude damping is presented as qubit relaxation, not photon loss. Adapter-measured duration is
software simulation time and must not be labeled physical QKD latency or secret-key rate.

The displayed final key is simulator output for research/education. It is not application traffic
protection, and the classical QKD transcript is assumed authenticated.

## Current API

```text
GET  /api/health
GET  /api/capabilities
POST /api/simulations/bb84
```

The BB84 request uses a discriminated channel union. Pydantic rejects unknown fields, invalid
probabilities, and Pauli configurations where `px + py + pz > 1`. Responses are JSON-safe DTOs;
NumPy arrays do not cross the HTTP boundary.

There are currently no HTTP routes for PQC handshakes, QKD–PQC hybrid sessions, experiment runs,
comparison, or AES-256-GCM payload protection.

## Target TFM modules

### Session Builder

The builder will select a backend-reported security profile and expose only implemented parameters.
The target profile vocabulary is QKD Experimental, PQC (`LOW`), PQC Diversified (`HIGH`), Hybrid
QKD–PQC, and Hybrid Diversified. A profile remains disabled until its orchestration path exists.

Current QKD inputs that can be reused are BB84, raw signal count, seed, ordered channel model, and
implemented noise parameters. Future PQC controls must reflect the exact supported variants:
ML-KEM-768, ML-DSA-65, optional HQC-3 through `HIGH`, HKDF-SHA-384, and the implemented profile
contract. The UI must not offer arbitrary algorithms the backend cannot execute.

### Protocol / Handshake Visualizer

The visualizer will render ordered events emitted by real runs.

For BB84: preparation, channel application, measurement, sifting, sampled QBER, reconciliation,
verification, privacy amplification, and completion/abort.

For PQC: identity/trust, ephemeral key generation, signed `ServerKeyOffer`, verification,
encapsulation, signed `ClientKeyExchange`, verification, decapsulation, transcript construction,
canonical secret input, HKDF, `Finished_B`, `Finished_A`, and session establishment.

For hybrid profiles, the QKD and PQC branches may converge only when the hybrid orchestration and
combiner exist. The visualizer will not invent messages or imply that QKD alone authenticated the
classical channel.

### Results / Metrics

The results workspace will evolve from the current BB84 output to a versioned run record containing
only available measurements: status/abort, profile, phase/total software timings, byte counts,
algorithm dimensions, derived-key length, component provenance, QKD stage sizes and QBER, seed,
backend versions, and configuration snapshot. Comparison will operate on two or more stored run
records instead of rerunning logic inside chart components.

Secrets, private keys, KEM shared secrets, `K_SESSION`, and `K_CONFIRM` are not metrics and must not
be logged or serialized in experiment records.

### Protected Message Demo

After an established session exists, this workspace will show:

```text
KEY-ESTABLISHMENT PLANE
QKD / PQC / hybrid -> confirmed 256-bit K_SESSION

DATA-PROTECTION PLANE
plaintext -> AES-256-GCM -> nonce + ciphertext + tag
          -> Bob authenticated decrypt -> plaintext or tamper failure
```

Nonce generation/reuse controls and optional AAD binding to session/profile/transcript metadata
belong in backend domain code, not frontend JavaScript.

### Quantum-Safe Explorer

If included, the explorer will consume a structured, versioned catalog for BB84, QKD, ML-KEM,
ML-DSA, HQC, HKDF-SHA-384, AES-256-GCM, hybrid establishment, and combiners. Every standards claim
must include a source and “status as of” date. As of 2026-09-05, ML-KEM and ML-DSA are standardized
in NIST FIPS 203/204; HQC is selected for standardization, not described as a final FIPS standard.

## Development

Prerequisites:

- Python 3.14 and [`uv`](https://docs.astral.sh/uv/);
- Node.js 20.19+ (or 22.12+) and npm.

From the repository root:

```bash
uv sync --dev
cd ui/frontend
npm ci
```

Start the backend from the repository root and wait for `Application startup complete`:

```bash
uv run uvicorn ui.backend.main:app --reload --host 127.0.0.1 --port 8000
```

Verify `http://127.0.0.1:8000/api/health`. In a second terminal:

```bash
cd ui/frontend
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to `http://127.0.0.1:8000`; the backend must be
running on that port.

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

## Extension rules

- implement a domain/orchestration capability before adding its route and frontend control;
- report implemented/planned status from `/api/capabilities`;
- preserve typed request/response contracts and explicit adapters;
- render traces and metrics returned by the backend rather than synthesizing protocol behavior;
- keep QKD and PQC as sibling domains composed only above them.

See [`../TFM_GOAL.md`](../TFM_GOAL.md) for the academic contract and
[`../docs/structure.md`](../docs/structure.md) for the complete target architecture.
