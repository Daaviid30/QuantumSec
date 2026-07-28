# Tarea 17 — Benchmark de rutas segura y rápida

Estado: completada.

Se añadió `benchmarks/benchmark_measurements.py`. La ejecución aislada con un qubit y una repetición produjo:

| Señales | Segura | Rápida | Validación de `rho` | `eigvalsh` aislado | Segura/rápida |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 0,105319 s | 0,050814 s | 0,044163 s | 0,004007 s | 2,073× |
| 10.000 | 1,063407 s | 0,515036 s | 0,486821 s | 0,041075 s | 2,065× |
| 100.000 | 10,591530 s | 5,322749 s | 4,679332 s | 0,426631 s | 1,990× |

La evidencia justifica las optimizaciones ya realizadas y no justifica todavía añadir JIT o una segunda implementación vectorizada. Comando reproducible: `python -m benchmarks.benchmark_measurements`.
