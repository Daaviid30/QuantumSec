# Convenciones

- Paquetes y módulos en minúsculas; nombres explícitos. Evitar `utils.py`, `helpers.py` o `math.py` cuando oculten responsabilidades.
- Imports respetan capas: `core` no conoce dominio; `quantum` no conoce QKD; `qkd` puede importar `quantum` y `core`.
- Toda aleatoriedad entra como `BaseRNG`; pruebas y experimentos reproducibles usan `SeededRNG`. No introducir RNG global oculto.
- Entradas numéricas aceptan `ArrayLike`; salidas materializadas usan aliases de `quantum/types.py` y dtypes NumPy explícitos.
- No crear wrappers `Ket`, `DensityMatrix`, `QuantumState`, `Projector` o `ProbabilityVector` sin invariantes/coste evitado demostrables.
- `DEFAULT_ATOL` vive en `core/constants.py`; no dispersar tolerancias mágicas.
- Validación pública clara: pares `is_*`/ `validate_*` cuando aplica; mensajes incluyen el detalle numérico o estructural útil.
- Objetos de valor/canales favorecen `@dataclass(frozen=True, slots=True)`; arrays almacenados se copian defensivamente y se protegen contra mutación.
- Funciones privadas con prefijo `_`; propiedades triviales y APIs públicas tienen docstrings concisos estilo NumPy. Reservar documentación larga para decisiones científicas.
- Mantener nombres explícitos `ProjectiveMeasurement`, `sample_projective_outcome`, `measure_projective`; una futura API POVM será separada.
- Tests reflejan el árbol fuente, usan pytest, incluyen casos inválidos, límites/tolerancias y resultados analíticos. No afirmar igualdad estadística exacta en canales ruidosos.
- APIs públicas deben reexportarse de forma deliberada desde el `__init__.py` de su paquete; evitar capas wrapper sin comportamiento.
- Errores de contrato suelen ser `ValueError`; incompatibilidades de tipo estructural usan `TypeError`; los tests pueden fijar fragmentos relevantes del mensaje.