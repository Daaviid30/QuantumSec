# QuantumSec

- Identidad del TFM: laboratorio modular y reproducible para diseñar, ejecutar, visualizar y
  comparar establecimiento de sesiones quantum-safe mediante QKD, PQC y composición híbrida
  QKD–PQC.
- Estado actual: BB84 completo sobre canales lógicos; handshake PQC autónomo completo para
  `LOW`/`HIGH`; Web UI funcional solo para BB84.
- Trabajo TFM pendiente: orquestación híbrida, demo AES-256-GCM, contratos/ejecución de
  experimentos, ampliación del laboratorio web y campaña experimental.
- Fuera de alcance: protocolos QKD adicionales, QKDN, hardware, nuevas primitivas/pruebas formales,
  agentes LLM y optimización de producción.
- Dependencias actuales: `ui/frontend -> ui/backend -> qkd -> quantum -> core`; `pqc` es un
  dominio hermano independiente. `qkd` y `pqc` nunca se importan mutuamente.
- Arquitectura objetivo: `ui/experiments -> orchestration -> qkd,pqc,data_protection`. La
  composición ocurre solo en una capa superior todavía no implementada.
- RNG inyectado para QKD/física; CSPRNG de liboqs/SO para PQC. Reproducibilidad no significa forzar
  claves o firmas criptográficas deterministas.
- QKD asume canal clásico autenticado; el estimador BB84 es asintótico, no una prueba finite-key
  componible; el tiempo NumPy no representa hardware QKD.
- PQC actual: ML-KEM-768, ML-DSA-65 y HQC-3; `K_SESSION` y `K_CONFIRM` son 32 bytes y usan
  dominios HKDF-SHA-384 separados; Finished usa HMAC-SHA-384.
- `LOW` = PQC y `HIGH` = PQC diversificado. `HIGH` no es el futuro perfil híbrido QKD–PQC ni
  un combiner multi-KEM estandarizado.
- Fuentes de verdad: código/tests, `README.md`, `docs/structure.md` y `TFM_GOAL.md`.
- Memorias de detalle: `mem:infrastructure/core`, `mem:quantum/core`, `mem:qkd/core`,
  `mem:pqc/core`, `mem:ui/core`, `mem:tech_stack`, `mem:conventions`,
  `mem:suggested_commands`, `mem:task_completion`.
- Tras cambios de código: pruebas, Ruff, Pyright, frontend tests/typecheck/build y
  `graphify update .`.
