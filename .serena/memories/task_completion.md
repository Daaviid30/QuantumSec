# Finalización de tareas

1. Preservar cambios ajenos: revisar `git status --short` antes de editar y trabajar alrededor de un árbol sucio.
2. Durante la implementación, ejecutar las pruebas dirigidas del módulo afectado con `uv run python -m pytest <ruta> -q`.
3. Antes de entregar, ejecutar exactamente:
   - `uv run python -m ruff check .`
   - `uv run python -m ruff format --check .`
   - `uv run python -m pyright`
   - `uv run python -m pytest -q`
   - `npm test -- --run` (en `ui/frontend/` si se modificó la interfaz o tipos compartidos).
4. Revisar `git diff --check` y el diff final; confirmar que no hay archivos o cambios fuera de alcance.
5. Si cambiaron símbolos, imports o arquitectura y existe `graphify-out/`, ejecutar `graphify . --update`.
6. Si cambiaron memorias Serena, verificar coherencia entre ellas.
7. Informar resultados exactos, incluidas pruebas omitidas o bloqueos; no declarar éxito basándose solo en una edición.
8. No añadir dependencias obligatorias sin uso real; actualizar `pyproject.toml` y `uv.lock` (o `package.json` y `package-lock.json`) juntos cuando corresponda.

Puertas de calidad verificadas tras la revisión de PQC Fase 5: 511 tests Python pasando, Ruff limpio y Pyright sin errores. La interfaz no cambió en esta fase; su última validación registrada mantiene 6 tests Vitest pasando.
