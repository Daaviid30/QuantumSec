# Finalización de tareas

1. Preservar cambios ajenos: revisar `git status --short` antes de editar y trabajar alrededor de un árbol sucio.
2. Durante la implementación, ejecutar las pruebas dirigidas del módulo afectado con `uv run python -m pytest <ruta> -q`.
3. Antes de entregar, ejecutar exactamente:
   - `uv run python -m ruff check .`
   - `uv run python -m ruff format --check .`
   - `uv run python -m pyright`
   - `uv run python -m pytest -q`
4. Revisar `git diff --check` y el diff final; confirmar que no hay archivos o cambios fuera de alcance.
5. Si cambiaron símbolos, imports o arquitectura y existe `graphify-out/`, ejecutar `graphify . --update`.
6. Si cambiaron memorias Serena, ejecutar `serena memories check`.
7. Informar resultados exactos, incluidas pruebas omitidas o bloqueos; no declarar éxito basándose solo en una edición.
8. No añadir dependencias obligatorias sin uso real; actualizar `pyproject.toml` y `uv.lock` juntos cuando corresponda.

Puertas verificadas durante onboarding: 328 tests, Ruff limpio, 48 archivos formateados y Pyright 0 errores/0 advertencias.