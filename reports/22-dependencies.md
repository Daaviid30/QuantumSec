# Tarea 22 — Revisar dependencias

Estado: completada.

La descripción provisional de `pyproject.toml` se sustituyó por una descripción específica del proyecto. Una búsqueda del repositorio confirmó que Qiskit no se importa en el código actual, por lo que pasó de dependencia obligatoria al extra opcional `qiskit`.

`uv.lock` se regeneró correctamente. También se configuró Pyright para resolver el entorno `.venv`, permitiendo ejecutar el control de tipos sin falsos errores de imports.
