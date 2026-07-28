# Tarea 20 — Limpiar mensajes y ortografía

Estado: completada.

Se eliminaron `proyector`, `bi-dimensional`, `projecctor` y los usos inconsistentes de `hermitian`. Los errores nuevos incluyen, según corresponda, forma, dimensión, índice, traza, autovalor mínimo, desviación máxima o vector de probabilidades.

Los docstrings de predicados explican ahora qué entradas mal formadas devuelven `False` y cuáles pueden fallar durante una conversión incompatible. También se corrigió `PSI_MINUS`, que contenía un cuarto componente espurio y no estaba normalizado.
