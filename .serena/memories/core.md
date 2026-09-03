# QuantumSec

- Framework de investigación y educación para simulaciones reproducibles de QKD y autenticación poscuántica; no es criptografía de producción.
- Dependencias por capas: `ui (backend/frontend) -> experiments -> qkd/pqc -> quantum -> core -> librerías externas`. Nunca invertir esta dirección ni acoplar directamente `qkd` con `pqc`.
- Invariantes transversales: RNG inyectado para QKD/física, CSPRNG de liboqs/SO para PQC, resultados reproducibles desde semilla/configuración, validación física explícita, inmutabilidad y pruebas de comportamiento analítico.
- Guía para agentes y matriz de herramientas: `AGENTS.md`.
- Infraestructura y límites de `core/`: `mem:infrastructure/core`.
- Matemática cuántica general y sus convenciones: `mem:quantum/core`.
- Dominio QKD, canales, BB84, filtrado, reconciliación y métricas: `mem:qkd/core`.
- Dominio PQC, firmas ML-DSA-65, KEMs ML-KEM-768/HQC-3 y protocolo de handshake: `mem:pqc/core`.
- Capa de interfaz de usuario y APIs Web: `mem:ui/core`.
- Stack, versiones y herramientas: `mem:tech_stack`.
- Comandos reproducibles para Windows/uv: `mem:suggested_commands`.
- Estilo, validación, tipos y pruebas: `mem:conventions`.
- Puertas de calidad obligatorias antes de terminar una tarea: `mem:task_completion`.
- `pqc/` cubre las 4 fases del handshake: (1) ML-DSA-65 y confianza explícita, (2) oferta efímera de Bob firmada, (3) autenticación de Bob por Alice y encapsulamiento KEM, y (4) respuesta firmada de Alice con vinculación SHA-384 (`ClientKeyExchange`) y verificación-antes-de-desencapsular en Bob. Alice y Bob obtienen secretos KEM idénticos y liberan sus claves efímeras con `close()`. La combinación de secretos, KDF/HKDF, mensajes Finished y sesión pertenecen a la Fase 5.
- `docs/structure.md` es la fuente de verdad arquitectónica; `README.md` conserva parte de una visión objetivo antigua y puede mencionar directorios aún no implementados.
- `graphify-out/` contiene el mapa de relaciones. Tras cambios arquitectónicos o de símbolos, actualizar Graphify con `graphify update .`.
