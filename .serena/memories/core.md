# QuantumSec

- Framework de investigación y educación para simulaciones reproducibles de QKD y futura autenticación poscuántica; no es criptografía de producción.
- Dependencias por capas: `ui (backend/frontend) -> experiments -> qkd/pqc -> quantum -> core -> librerías externas`. Nunca invertir esta dirección ni acoplar directamente `qkd` con `pqc`.
- Invariantes transversales: RNG inyectado, resultados reproducibles desde semilla/configuración, validación física explícita, inmutabilidad y pruebas de comportamiento analítico.
- Guía para agentes y matriz de herramientas: `AGENTS.md`.
- Infraestructura y límites de `core/`: `mem:infrastructure/core`.
- Matemática cuántica general y sus convenciones: `mem:quantum/core`.
- Dominio QKD, canales, BB84, filtrado, reconciliación y métricas: `mem:qkd/core`.
- Capa de interfaz de usuario y APIs Web: `mem:ui/core`.
- Stack, versiones y herramientas: `mem:tech_stack`.
- Comandos reproducibles para Windows/uv: `mem:suggested_commands`.
- Estilo, validación, tipos y pruebas: `mem:conventions`.
- Puertas de calidad obligatorias antes de terminar una tarea: `mem:task_completion`.
- `pqc/` contiene Fases 1-3: ML-DSA-65, identidades/confianza, perfiles LOW/HIGH, KEM efímeros ML-KEM-768/HQC-3, oferta canónica firmada y procesamiento de Alice con autenticación previa obligatoria. `InitiatorKEMState` conserva los secretos solo localmente y permite liberar sus referencias con `close()`; no exporta secretos hasta que la fase KDF defina el contrato. `EncapsulationResponse` vive en `protocol/messages.py`, contiene únicamente ciphertexts públicos y soporta transporte dict/Base64 validado. Bob aún no recibe, autentica ni decapsula la respuesta a nivel de protocolo. Sigue siendo hermano de `qkd/`; el handshake completo y la integración QKD/PQC no existen aún.
- `docs/structure.md` es la fuente de verdad arquitectónica; `README.md` conserva parte de una visión objetivo antigua y puede mencionar directorios aún no implementados.
- `graphify-out/` contiene el mapa de relaciones. Tras cambios arquitectónicos o de símbolos, actualizar Graphify con `graphify update .`.
