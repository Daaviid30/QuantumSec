# Comandos sugeridos

Ejecutar desde la raíz de QuantumSec en PowerShell.

- Sincronizar entorno: `uv sync`
- Instalar también Qiskit cuando sea necesario: `uv sync --extra qiskit`
- Suite completa: `uv run python -m pytest -q`
- Prueba BB84: `uv run python -m pytest tests/test_qkd/test_bb84.py -q`
- Pruebas de un módulo: `uv run python -m pytest tests/test_quantum/test_measures.py -q`
- Lint: `uv run python -m ruff check .`
- Verificación de formato: `uv run python -m ruff format --check .`
- Aplicar formato cuando la tarea lo requiera: `uv run python -m ruff format .`
- Tipos: `uv run python -m pyright`
- Estado de cambios: `git status --short`
- Revisar parche: `git diff --check` y `git diff`
- Buscar rápido: `rg "patrón" ruta` y `rg --files`
- Actualizar el grafo tras cambios estructurales: `graphify . --update`
- Verificar referencias de memorias: `serena memories check`

Evitar `uv run pytest`/wrappers similares en esta máquina si Windows los bloquea; el patrón validado es `uv run python -m ...`.