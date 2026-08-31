# Stack técnico

- Python `>=3.14`; código y herramientas apuntan a Python 3.14.
- Gestión reproducible con uv: `pyproject.toml` + `uv.lock` + entorno `.venv`.
- Runtime: NumPy `>=2.5`, Matplotlib `>=3.11`, Rich `>=15`, SymPy `>=1.14`, tqdm `>=4.68.3`.
- Qiskit es un extra opcional (`qiskit`); el código actual no lo importa.
- Desarrollo: pytest `>=9.1.1`, Ruff `>=0.15.20`, Pyright `>=1.1.411`.
- Ruff: longitud 110, destino `py314`, comillas dobles, reglas E/F/I/UP/B.
- Pyright: modo `basic`, Python 3.14, entorno `.venv`, alcance `core/ quantum/ qkd/ tests/`.
- Serena: proyecto `QuantumSec`, backend LSP Python, UTF-8, raíz completa como workspace.
- Plataforma de desarrollo observada: Windows/PowerShell. La directiva de Control de aplicaciones bloquea algunos wrappers ejecutables; usar `uv run python -m <tool>` para las puertas de calidad.