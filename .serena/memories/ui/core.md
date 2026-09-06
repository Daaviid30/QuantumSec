# Capa ui/ (Web Laboratory & API)

- Estado actual: laboratorio BB84 funcional. PQC, híbrido, experimentos/comparación, Eve,
  autenticación QKD ejecutada y AES-256-GCM no tienen endpoints ni flujos frontend.
- Dependencia actual: `ui/frontend -> ui/backend -> qkd -> quantum -> core`. El backend no
  reimplementa lógica cuántica o de postprocesado.
- Rutas reales: `GET /api/health`, `GET /api/capabilities`,
  `POST /api/simulations/bb84`.
- Request BB84: `n_signals` 1..100000, semilla 0..2^32-1 y máximo 12 canales ordenados.
- Canales HTTP: Identity, Depolarizing, Bit Flip, Phase Flip, Pauli y Amplitude Damping.
- Resultados: UUID, semilla, duración de software, canal/configuración, tamaños y QBER agregado,
  postprocesado/abort, distribuciones y hasta 64 registros de transmisión.
- Objetivo TFM limitado a tres pantallas: Builder, Run y Compare exactamente dos runs. Protected
  Message aparece como strip en Run; no existe Quantum-Safe Explorer separado.
- Presentación de perfiles: QKD-ASSUMED, QKD-CLASSICAL-AUTH, QKD-PQC-AUTH, PQC-BASE,
  PQC-DIVERSE, HYBRID e HYBRID-DIVERSE; LOW/HIGH solo son identificadores internos.
- Regla: un control se activa solo cuando la capacidad real existe; no fabricar mensajes, trazas o
  métricas. Mostrar autenticación asumida frente a ejecutada y no comparar temporalmente QKD
  numérico con PQC real.
- Documentación fuente: `ui/README.md`, `docs/structure.md`, `TFM_GOAL.md`.
