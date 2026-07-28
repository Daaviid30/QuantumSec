# Tarea 3 — Crear `ProjectiveMeasurement`

Estado: completada.

Se añadió `ProjectiveMeasurement` a `quantum/measures.py`. La construcción rechaza colecciones vacías, exige un resultado por proyector, copia las entradas a `np.complex128`, valida el conjunto completo una sola vez y marca las copias como no escribibles.

Los proyectores y resultados quedan almacenados como tuplas. Las pruebas verifican conjuntos inválidos, copia defensiva, solo lectura, dimensión y número de resultados.
