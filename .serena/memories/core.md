# QuantumSec

- Framework de investigación y educación para simulaciones reproducibles de QKD y futura autenticación poscuántica; no es criptografía de producción.
- Dependencias por capas: `experiments -> qkd/pqc -> quantum -> core -> librerías externas`. Nunca invertir esta dirección ni acoplar directamente `qkd` con `pqc`.
- Invariantes transversales: RNG inyectado, resultados reproducibles desde semilla/configuración, validación física explícita y pruebas de comportamiento analítico.
- Infraestructura y límites de `core/`: `mem:infrastructure/core`.
- Matemática cuántica general y sus convenciones: `mem:quantum/core`.
- Dominio QKD, canales, BB84, filtrado y métricas: `mem:qkd/core`.
- Stack, versiones y herramientas: `mem:tech_stack`.
- Comandos reproducibles para Windows/uv: `mem:suggested_commands`.
- Estilo, validación, tipos y pruebas: `mem:conventions`.
- Puertas de calidad obligatorias antes de terminar una tarea: `mem:task_completion`.
- `pqc/`, `experiments/`, configuraciones y modelos ópticos son capas previstas; no fingir que existen ni mezclar su lógica en los módulos actuales.
- `docs/structure.md` es la fuente de verdad arquitectónica; `README.md` conserva parte de una visión objetivo antigua y puede mencionar directorios aún no implementados.
- `graphify-out/` contiene el mapa de relaciones. Tras cambios arquitectónicos o de símbolos, actualizar Graphify antes de depender del grafo.