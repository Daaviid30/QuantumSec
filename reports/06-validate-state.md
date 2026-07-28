# Tarea 6 — Añadir `validate_state`

Estado: completada.

`sample_projective_outcome()` y `measure_projective()` aceptan `validate_state: bool = True`. La ruta segura conserva la validación espectral completa; la rápida la omite expresamente, pero mantiene forma, dimensión, realidad, rango, finitud y normalización de probabilidades.

Una prueba sustituye la validación completa por una función que falla y confirma que la ruta rápida no la invoca.
