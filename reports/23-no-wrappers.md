# Tarea 23 — Posponer wrappers innecesarios

Estado: completada como decisión arquitectónica.

No se crearon `QuantumState`, `Ket`, `DensityMatrix`, `Projector` ni `ProbabilityVector`. Las entradas continúan aceptando `ArrayLike` y las salidas numéricas usan alias `NDArray`, manteniendo interoperabilidad directa con NumPy.

La única clase de dominio añadida representa una medición completa y prevalidada, que sí encapsula una invariantes y un ahorro de trabajo verificables.
