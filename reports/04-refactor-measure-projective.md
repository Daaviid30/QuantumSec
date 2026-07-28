# Tarea 4 — Refactorizar `measure_projective()`

Estado: completada.

La API recibe ahora un `ProjectiveMeasurement` prevalidado. Se retiraron de la ruta por señal las conversiones y validaciones de proyectores; permanecen la conversión de `rho`, la compatibilidad dimensional, las probabilidades físicas, el muestreo y la actualización de Lüders.

También se añadió una protección explícita si una fuente aleatoria defectuosa selecciona un resultado de probabilidad numéricamente nula. Existe una prueba específica para esta defensa.
