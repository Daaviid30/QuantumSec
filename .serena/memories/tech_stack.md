# Stack técnico

- Backend Python `>=3.14`; código y herramientas apuntan a Python 3.14.
- Gestión reproducible con uv: `pyproject.toml` + `uv.lock` + entorno `.venv`.
- Runtime Python: NumPy `>=2.5`, Matplotlib `>=3.11`, Rich `>=15`, SymPy `>=1.14`, tqdm `>=4.68.3`, FastAPI `>=0.115`, Pydantic `>=2.10`, Uvicorn `>=0.34`, liboqs-python (backend PQC), cryptography (HKDF/hashes).
- Frontend: Node.js, React 19, TypeScript 5.8, Vite 6, Tailwind CSS 4, Lucide React, Recharts.
- Qiskit es un extra opcional (`qiskit`); el código actual no lo importa.
- Desarrollo Python: pytest `>=9.1.1`, Ruff `>=0.15.20`, Pyright `>=1.1.411`, httpx `>=0.28`.
- Desarrollo Frontend: Vitest 4, `@testing-library/react`, `@testing-library/jest-dom`, jsdom.
- Tooling de Agentes:
  - **Graphify**: Knowledge graph en `graphify-out/` para arquitectura global y análisis de impacto (`graphify query`, `graphify update .`).
  - **Serena**: Navegación AST por símbolos (`find_symbol`, `replace_symbol_body`) y memorias en `.serena/memories/`.
  - **Context7**: Documentación oficial de APIs externas (`resolve-library-id`, `query-docs`).
- Ruff: longitud 110, destino `py314`, comillas dobles, reglas E/F/I/UP/B.
- Pyright: modo `basic`, Python 3.14, entorno `.venv`, alcance `core/ quantum/ qkd/ pqc/ ui/backend/ tests/`.
- Serena: proyecto `QuantumSec`, backend LSP Python, UTF-8, raíz completa como workspace.
- Plataforma de desarrollo observada: Windows/PowerShell (`uv run python -m <tool>` para comandos directos).
