# QuantumSec

- Framework de investigación y educación para simulaciones reproducibles de QKD y autenticación poscuántica; no es criptografía de producción.
- Dependencias por capas: `ui (backend/frontend) -> experiments -> qkd/pqc -> quantum -> core -> librerías externas`. Nunca invertir esta dirección ni acoplar directamente `qkd` con `pqc`.
- Invariantes transversales: RNG inyectado para QKD/física, CSPRNG de liboqs/SO para PQC, resultados reproducibles desde semilla/configuración, validación física explícita, inmutabilidad y pruebas de comportamiento analítico.
- Guía para agentes y matriz de herramientas: `AGENTS.md`.
- Infraestructura y límites de `core/`: `mem:infrastructure/core`.
- Matemática cuántica general y sus convenciones: `mem:quantum/core`.
- Dominio QKD, canales, BB84, filtrado, reconciliación y métricas: `mem:qkd/core`.
- Dominio PQC, firmas ML-DSA-65, KEMs ML-KEM-768/HQC-3, KDF/HKDF y protocolo de handshake: `mem:pqc/core`.
- Capa de interfaz de usuario y APIs Web: `mem:ui/core`.
- Stack, versiones y herramientas: `mem:tech_stack`.
- Comandos reproducibles para Windows/uv: `mem:suggested_commands`.
- Estilo, validación, tipos y pruebas: `mem:conventions`.
- Puertas de calidad obligatorias antes de terminar una tarea: `mem:task_completion`.
- `pqc/` cubre las 5 fases del handshake: (1) ML-DSA-65 y confianza explícita, (2) oferta efímera de Bob firmada, (3) autenticación de Bob por Alice y encapsulamiento KEM, (4) respuesta firmada de Alice (`ClientKeyExchange` con `client_nonce` y `server_offer_hash` SHA-384) y desencapsulamiento en Bob, y (5) transcript canónico autenticado (`PQCHandshakeTranscript`), combinación KEM y derivación de clave de sesión simétrica de 256 bits (`PQCSessionKeyDeriver`, `DerivedSessionKeyState`) mediante HKDF-SHA-384. Los mensajes de confirmación (Finished) pertenecen a la Fase 6.
- `docs/structure.md` es la fuente de verdad arquitectónica; `README.md` conserva parte de una visión objetivo antigua y puede mencionar directorios aún no implementados.
- `graphify-out/` contiene el mapa de relaciones. Tras cambios arquitectónicos o de símbolos, actualizar Graphify con `graphify update .`.
