# Tarea 1 — Mejorar `MeasurementResult`

Estado: completada.

Se actualizó `quantum/measures.py` con `frozen=True`, `slots=True` y `eq=False`. El campo `post_state` usa `field(repr=False)`, por lo que la representación ya no vuelca matrices potencialmente grandes.

La prueba dedicada verifica inmutabilidad, ausencia de `__dict__`, representación compacta y uso de la igualdad de identidad heredada. Las matrices de los resultados se comparan con `numpy.testing.assert_allclose`.
