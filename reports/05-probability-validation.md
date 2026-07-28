# Tarea 5 — Validar probabilidades antes de recortar

Estado: completada.

La función interna de probabilidades de Born comprueba, en orden, parte imaginaria, finitud, valores menores que `-tol`, valores mayores que `1 + tol`, recorte de residuos pequeños, suma unitaria y normalización.

Las pruebas demuestran que `[-0.1, 1.1]` no queda oculto por `np.clip`, y cubren además exceso superior, suma incorrecta y probabilidades complejas.
