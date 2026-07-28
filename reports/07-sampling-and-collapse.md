# Tarea 7 — Separar muestreo y colapso

Estado: completada.

Se implementó `sample_projective_outcome()` sin productos de colapso. `measure_projective()` reutiliza ese resultado, recupera el proyector por `sample.index` y solo entonces calcula y normaliza `P @ rho @ P`.

Las pruebas comparan ambas rutas con semillas iguales, verifican colapso físico y demuestran repetibilidad inmediata de la misma medición.
