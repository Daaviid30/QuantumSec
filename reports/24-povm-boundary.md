# Tarea 24 — Preservar espacio para POVMs

Estado: completada como decisión arquitectónica.

Las APIs se llaman explícitamente `ProjectiveMeasurement`, `sample_projective_outcome` y `measure_projective`. No se creó una jerarquía genérica ni se reutilizó la validación idempotente de proyectores para efectos POVM.

La separación deja libre una futura implementación de efectos y operadores de medición cuando B92 aporte un caso de uso concreto, sin condicionar prematuramente el diseño actual.
