# Comandos sugeridos

Ejecutar desde la raíz de QuantumSec en PowerShell.

- Sincronizar entorno Python: `uv sync`
- Instalar también Qiskit cuando sea necesario: `uv sync --extra qiskit`
- Servidor Backend: `uv run uvicorn ui.backend.main:app --reload`
- Servidor Frontend: `npm run dev` (dentro de `ui/frontend`)
- Suite completa Python: `uv run python -m pytest -q`
- Suite Frontend: `npm test -- --run` (dentro de `ui/frontend`)
- Prueba BB84: `uv run python -m pytest tests/test_qkd/test_bb84.py -q`
- Prueba API UI: `uv run python -m pytest tests/test_ui/test_api.py -q`
- Lint Python: `uv run python -m ruff check .`
- Verificación de formato: `uv run python -m ruff format --check .`
- Aplicar formato cuando la tarea lo requiera: `uv run python -m ruff format .`
- Tipos Python: `uv run python -m pyright`
- Estado de cambios: `git status --short`
- Revisar parche: `git diff --check` y `git diff`
- Buscar rápido: `rg "patrón" ruta` y `rg --files`
- Actualizar el grafo tras cambios estructurales: `graphify . --update`
- Consultar el grafo de conocimiento: `graphify query "<pregunta>"`

Evitar `uv run pytest`/wrappers similares en esta máquina si Windows los bloquea; el patrón validado es `uv run python -m ...`.