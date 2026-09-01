# Agent Instructions & Tooling Guide (QuantumSec)

This document defines guidelines and the tool selection matrix for any AI agent working on the `QuantumSec` repository.

---

## 1. Tool Selection Matrix

Work efficiently by combining the available tools according to the task type. **Do not read large volumes of raw source files when Graphify or Serena can retrieve the relevant context immediately.**

| Need / Task | Primary Tool | Command / Action |
| :--- | :--- | :--- |
| **Global architecture, cross-module relationships, blast radius & impact analysis** | **Graphify** | `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"` |
| **Code navigation by symbols, exact references, and semantic AST refactoring** | **Serena** | `find_symbol`, `find_referencing_symbols`, `replace_symbol_body`, `get_symbols_overview` |
| **Project background, design conventions, and domain memories** | **Serena (Memories)** | `list_memories`, `read_memory` (reuse existing memories; **do not run onboarding again**) |
| **External library & API documentation (React, FastAPI, NumPy, SciPy, etc.)** | **Context7** | `resolve-library-id` followed by `query-docs` |
| **Test execution and quality gate validation** | **PowerShell / CLI** | `uv run pytest`, `npm test` (in `ui/frontend`), `ruff check` |
| **Graph maintenance after code modifications** | **Graphify** | `graphify update .` (incremental, AST-based, zero token cost) |

---

## 2. Specific Tooling Rules

### A. Graphify (`graphify-out/`)
- A precomputed knowledge graph exists in `graphify-out/` detailing community topology, god nodes, and cross-file dependencies.
- **Architectural queries**: Always execute `graphify query "<question>"` or `graphify path "<A>" "<B>"` first. They return concise, scoped subgraphs.
- **Avoid blind codebase reads**: If `graphify-out/wiki/index.md` exists, use it for high-level navigation before opening raw source files.
- **Incremental updates**: After modifying or refactoring code files, run `graphify update .` to keep `graph.json`, `graph.html`, and `GRAPH_REPORT.md` synchronized.
- **Do not rebuild from scratch**: Always use the existing graph and incremental updates (`--update`).

### B. Serena (Symbol Navigation & Memories)
- **Project memories**: Serena already has structured project knowledge stored in `.serena/memories/` (`conventions.md`, `core.md`, `qkd/core.md`, `quantum/core.md`, `tech_stack.md`, `task_completion.md`). **Do not re-run onboarding.**
- **Safe symbol-level editing**: Use Serena's AST tools (`find_symbol`, `replace_symbol_body`, `safe_delete_symbol`) to inspect and modify classes and functions while preserving syntax tree integrity.

### C. Context7 (External Documentation)
- Use **exclusively** to look up official, up-to-date documentation for third-party libraries, frameworks, SDKs, and APIs (e.g. FastAPI, Pydantic, TailwindCSS, React, Vitest, NumPy, SciPy, liboqs).
- Mandatory flow:
  1. `resolve-library-id` with the library name.
  2. `query-docs` with the obtained library ID and specific query concept.
- **Do not use Context7** for internal repository logic or refactoring custom project code.

---

## 3. Architectural Invariants & Project Rules

1. **Strict Layer Discipline (Acyclic Layering)**:
   $$\text{ui (backend/frontend)} \longrightarrow \text{qkd} \longrightarrow \text{quantum} \longrightarrow \text{core}$$
   - `core/`: Global constants (`DEFAULT_ATOL`), RNG abstractions (`BaseRNG`, `SeededRNG`), errors. Zero domain dependencies.
   - `quantum/`: Linear algebra, pure/density states (`dm_from_ket`), operators, projective measurements (`ProjectiveMeasurement`), CPTP channels (`QuantumChannel`). No knowledge of QKD.
   - `qkd/`: Protocols (BB84), sifting, error reconciliation (Cascade), parameter estimation, privacy amplification (Toeplitz), security bounds (QBER, Shor-Preskill).
   - `ui/`: FastAPI (`ui/backend`) and React/Vite/Tailwind (`ui/frontend`).
   - *Never invert the import flow.*

2. **Injected Randomness (Injected RNG)**:
   - Any function or class requiring randomness must receive a `BaseRNG` instance.
   - Deterministic simulations and tests must always use `SeededRNG(seed=...)`.
   - Never use unseeded, global RNG state in domain logic.

3. **Immutability & Defensive Validation**:
   - Value and result objects use `@dataclass(frozen=True, slots=True)`.
   - Stored NumPy arrays must be defensively copied and marked `flags.writeable = False` when part of immutable state objects.
   - Use `ArrayLike` for input signatures and explicit types (`ComplexArray`, `RealArray`, etc.) for outputs.

4. **Sources of Truth**:
   - `docs/structure.md` and codebase docstrings are the architectural sources of truth.
   - Implemented source code takes precedence over preliminary target proposals in `README.md`.

---

## 4. Mandatory Quality Gate

Before completing any task or refactor:
1. **Tests**: Run all relevant test suites with `uv run pytest` and `npm test` ensuring 100% pass rate.
2. **Lint & Types**: Ensure no linter warnings (`ruff check`) or TypeScript/Python type errors are introduced.
3. **Updated Graph**: Run `graphify update .` to register new AST nodes and relationships in the knowledge graph.
