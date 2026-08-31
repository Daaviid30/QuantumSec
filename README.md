# QuantumSec

A modular, reproducible simulation platform for Quantum Key Distribution (QKD), quantum-channel
research, and the future evaluation of post-quantum authentication mechanisms.

The current release includes a functional BB84 engine and a dark-first web laboratory for composing
logical-qubit channels, running seeded simulations, and inspecting genuine simulation output.

## 📌 Overview

This project aims to bridge the gap between theoretical quantum cryptography and practical secure system design by focusing on a critical but often overlooked component:

> **The authentication of the classical channel in QKD systems under post-quantum threat models.**

While QKD provides information-theoretic security for key exchange, it relies on classical authentication mechanisms that are vulnerable to quantum attacks (e.g., Shor’s algorithm). This framework enables the evaluation of such mechanisms in realistic protocol scenarios.

---

## 🎯 Objectives

- Model QKD protocols (BB84, B92, E91) at a logical and operational level.
- Simulate the classical communication channel and its exposure to attacks (e.g., Man-in-the-Middle).
- Integrate and compare different authentication schemes:
  - Classical (MAC, ECDSA)
  - Post-Quantum (e.g., CRYSTALS-Dilithium)
  - Hybrid approaches
- Evaluate the impact of authentication on:
  - Communication overhead
  - Latency
  - Key generation rate
  - Scalability

## 🏗️ Architecture

The implemented dependency direction is:

```text
ui/frontend -> ui/backend -> qkd -> quantum -> core
```

`core` and the simulation packages never depend on `ui`. The web backend is an adapter over the
existing public APIs; it does not implement quantum behavior.


### Core Components

- **QKD Module**  
  Logical implementation of QKD protocols with clear phase separation.

- **Authentication Module**  
  Pluggable authentication schemes for securing the classical channel.

- **Mathematical Layer**  
  Lightweight abstractions for modeling quantum-like behavior.

- **Experiment Engine**  
  Enables reproducible evaluation and comparison across different configurations.

## 🧪 Current simulation scope

- complete BB84 preparation, transmission, projective measurement, sifting, and classical
  post-processing
- deterministic runs through the injected `SeededRNG`
- composable Identity, Depolarizing, Pauli, Bit Flip, Phase Flip, and Amplitude Damping channels
- per-position raw-result inspection, stage shrinkage, and security summaries in the Web UI

The complete session flow is:

```text
raw signals -> basis sifting -> sampled parameter estimation
            -> Cascade reconciliation -> universal-hash confirmation
            -> asymptotic length estimation -> Toeplitz privacy amplification
```

`BB84Result.qber` remains the QBER over all sifted bits for simulation diagnostics. Protocol
decisions use only a seeded random disclosed sample, and every disclosed position is removed from
both candidate keys. Cascade records one leakage bit per public Alice parity; key confirmation also
records its public tag length. Public Toeplitz seeds are not secret material and are not subtracted
from the key length.

The current length estimator is an **asymptotic BB84 model**, not a complete composable finite-key
security proof. It assumes a symmetric phase-error rate represented by sampled QBER and subtracts
actual simulated reconciliation and confirmation leakage exactly once. The classical channel is
assumed authenticated. PQC authentication remains an intentionally separate future QuantumSec
layer; without authentication, the simulator must not be interpreted as end-to-end secure QKD.

Optical loss, experiment sweeps, physical transmission timing/secret bits per second, production
LDPC reconciliation, PQC authentication, and QKDN functionality are not implemented yet.

## 🖥️ Web UI V1

Install the locked Python environment and frontend dependencies:

```bash
uv sync --dev
cd ui/frontend
npm ci
```

Run the two development services in separate terminals. Start the backend first and leave it
running. The backend command must be executed from the repository root:

```bash
uv run uvicorn ui.backend.main:app --reload --port 8000
```

```bash
cd ui/frontend
npm run dev
```

Wait for `Application startup complete`, then verify the backend at
`http://127.0.0.1:8000/api/health`. Open `http://localhost:5173` only after that check succeeds. The
Vite development server proxies `/api` to FastAPI on port `8000`; if the backend process is not
running, the frontend reports that it cannot connect. API documentation is available at
`http://127.0.0.1:8000/docs`.

See [`ui/README.md`](ui/README.md) for architecture, API contracts, tests, and extension points.

## ✅ Tests

```bash
uv run pytest
uv run ruff check .
cd ui/frontend
npm test
npm run build
```

---

## 🔐 Research Focus

The main research question addressed by this framework is:

> **How do post-quantum authentication mechanisms affect the security and operational performance of QKD systems?**

## 🎓 Academic Context

This project is developed as part of a Master's thesis focused on:

Post-Quantum Cryptography (PQC)
Quantum Key Distribution (QKD)
Secure system design under quantum threat models

It is designed to serve as a foundation for future research, including potential PhD work.

⚠️ Disclaimer

This framework is intended for research and educational purposes.
It does not aim to provide production-ready cryptographic implementations.

👤 Author

David Martín Castro
