# Stack técnico

- Python `>=3.14`, entorno reproducible con `uv`, `pyproject.toml` y `uv.lock`.
- Runtime declarado: cryptography `>=50.0.1`, FastAPI `>=0.116`, liboqs-python `>=0.16`,
  NumPy `>=2.5`, Matplotlib `>=3.11`, Rich `>=15`, SymPy `>=1.14`, tqdm `>=4.68.3` y
  Uvicorn `>=0.35`.
- Qiskit `>=2.4.2` es extra opcional; el código actual no lo importa.
- Frontend declarado: React/React DOM `^19.2`, TypeScript `~6.0.2`, Vite `^8.0.10`,
  Tailwind CSS `^4.1.18`, Recharts `^3.1.2` y Lucide React `^0.548`.
- Desarrollo Python: pytest `>=9.1.1`, Ruff `>=0.15.20`, Pyright `>=1.1.411` y
  httpx `>=0.28.1`.
- Desarrollo frontend: Vitest `^4.0.18`, Testing Library y jsdom.
- Ruff: longitud 110, destino `py314`, reglas E/F/I/UP/B. Pyright: modo `basic`, Python 3.14.
- Graphify: grafo en `graphify-out/`; consultas de arquitectura y `graphify update .` tras
  cambios de código.
- Serena: navegación simbólica y memorias persistentes en `.serena/memories/`.
- Context7: documentación actual de librerías/APIs externas.
- Plataforma observada: Windows/PowerShell.
