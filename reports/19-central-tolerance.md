# Tarea 19 — Centralizar la tolerancia

Estado: completada.

`core/constants.py` define `DEFAULT_ATOL = 1e-10` sin importar capas de dominio. Los módulos cuánticos y las pruebas existentes obtienen de allí su tolerancia por defecto.

Una búsqueda completa confirma que el literal solo queda declarado en ese archivo central.
