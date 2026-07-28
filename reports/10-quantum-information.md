# Tarea 10 — Crear `quantum/information.py`

Estado: completada.

La pureza salió de `quantum/measures.py`. El nuevo módulo contiene `purity`, `trace_distance`, `fidelity` y `von_neumann_entropy`, todas con validación opcional y comprobaciones numéricas explícitas.

La fidelidad adopta en todo el proyecto la convención de Uhlmann al cuadrado. Su raíz PSD usa `np.linalg.eigh`, rechaza negatividad significativa, recorta únicamente residuos tolerables y hermitiza los intermedios numéricos.
