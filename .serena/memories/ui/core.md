# Capa ui/ (Web Laboratory & API)

- Estado actual: laboratorio BB84 funcional. PQC, híbrido, experimentos/comparación y AES-256-GCM
  no tienen endpoints ni flujos frontend.
- Dependencia actual: `ui/frontend -> ui/backend -> qkd -> quantum -> core`. El backend no
  reimplementa lógica cuántica o de postprocesado.
- Rutas reales: `GET /api/health`, `GET /api/capabilities`,
  `POST /api/simulations/bb84`.
- Request BB84: `n_signals` 1..100000, semilla 0..2^32-1 y máximo 12 canales ordenados.
- Canales HTTP soportados: Identity, Depolarizing, Bit Flip, Phase Flip, Pauli y Amplitude Damping.
  `KrausChannel` es infraestructura pública Python, no una opción directa de la API.
- Resultados: UUID, semilla, duración de software, canal/configuración, tamaños y QBER,
  postprocesado/abort, distribuciones y hasta 64 registros de transmisión.
- Frontend: React 19.2, TypeScript 6, Vite 8, Tailwind 4, Recharts y Lucide.
- Componentes actuales: configurador BB84, editor de pipeline, vista de flujo, controles,
  resultados/gráficas, inspector y detalle científico.
- Objetivo TFM: Session Builder por perfiles, visualizador de eventos reales, resultados y
  comparación, Protected Message Demo y catálogo quantum-safe versionado/citado.
- Regla: un control se activa solo cuando la capacidad real existe en backend; no fabricar mensajes,
  trazas o métricas.
- Documentación fuente: `ui/README.md`, `docs/structure.md`, `TFM_GOAL.md`.
