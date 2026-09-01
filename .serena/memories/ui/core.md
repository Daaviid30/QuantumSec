# Capa ui/ (Web UI & API)

- Capa de presentación y servicios sobre `qkd/`, `quantum/` y `core/`.
- `ui/backend/`:
  - `main.py`: Aplicación FastAPI (`/api/v1`), middleware CORS, endpoints `/health`, `/capabilities`, `/simulate/bb84`.
  - `schemas.py`: Modelos Pydantic v2 con validación estricta (`StrictModel`), schemas de canales, configuración BB84 y resultados.
  - `capabilities.py`: Metadatos de canales disponibles (Identity, Pauli, BitFlip, PhaseFlip, Depolarizing, AmplitudeDamping, Kraus, Pipeline) y rangos válidos.
  - `adapters.py`: Puente entre las requests de la API y las clases de dominio (`BB84Protocol`, canales cuánticos, `SeededRNG`).
- `ui/frontend/`:
  - SPA React 19 + TypeScript + Vite 6 + TailwindCSS 4.
  - `src/components/layout/`: `AppShell`, `Header`, `Sidebar`, `QuantumMark`.
  - `src/components/simulation/`: `SimulationConfigurator`, `ChannelPipeline`, `ChannelCard`, `ProtocolSelector`, `QuantumFlow`, `SimulationControls`.
  - `src/components/results/`: `ResultsWorkspace`, `ResultsSummary`, `ResultsCharts`, `QubitInspector`, `ScientificDetails`.
  - `src/hooks/`: `useCapabilities`, `useSimulation`.
  - `src/api/client.ts`: Cliente HTTP tipado con manejo de errores `QuantumSecApiError`.
- Tests:
  - Backend: `tests/test_ui/test_api.py` (usando FastAPI `TestClient`).
  - Frontend: `ui/frontend/src/**/*.test.tsx` (Vitest + React Testing Library + jsdom).