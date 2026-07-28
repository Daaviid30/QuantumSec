# Tarea 8 — Crear `Basis`

Estado: completada para el alcance actual.

Se creó `qkd/primitives/bases.py` con `Basis.Z`, `Basis.X` y `Basis.Y`, además de los adaptadores validados `basis_from_bit()` y `bases_from_bits()`. La API se exporta desde `qkd.primitives`, mientras `core.rng.random_basis()` continúa siendo binaria y genérica.

Las conversiones escalares y vectoriales, incluidos enteros NumPy y entradas inválidas, están cubiertas. Todavía no existe `bb84.py` en el repositorio, por lo que no había código de protocolo con números mágicos que migrar; la nueva API queda lista para usarlo desde su primera implementación.
