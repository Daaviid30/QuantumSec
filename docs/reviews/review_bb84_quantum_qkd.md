# Informe de Revisión de Código Independiente: Módulos `quantum` y `qkd` (BB84)

**Fecha**: 1 de Septiembre de 2026  
**Alcance**: Módulos `quantum/`, `qkd/`, integración con `core/rng.py` y suites de prueba asociadas (`tests/test_quantum/`, `tests/test_qkd/`).  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría estricta e independiente de la base de código de **QuantumSec** centrada en la pila fundacional de simulación cuántica y el protocolo **BB84**:
- **Capa `quantum/`**: Álgebra lineal cuántica (`linalg.py`), validaciones físicas (`validation.py`), estados puros y ensambles (`states.py`), medidas proyectivas de von Neumann / Lüders (`measures.py`), y métricas de información cuántica (`information.py`).
- **Capa `qkd/`**: Primitivas cuánticas (`states.py`, `operations.py`, `bases.py`, `measurements.py`), canales cuánticos CPTP e ideales (`channel/`), métricas (`qber.py`, `security.py`), post-procesado clásico (`sifting.py`, `parameter_estimation.py`, `reconciliation.py`, `verification.py`, `universal_hashing.py`, `privacy_amplification.py`) y el orquestador del protocolo (`protocols/bb84.py`).
- **Infraestructura de soporte**: Generación de números aleatorios (`core/rng.py`) y suites de prueba unitarias e integración (`tests/`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades críticas de ejecución o fallos que invaliden completamente la matemática fundamental de BB84. |
| **HIGH** | 3 | Rigidez en validación compleja (`np.isreal`), mutabilidad de constantes cuánticas globales y ruptura de LSP en `QRNGSimulator`. |
| **MEDIUM** | 3 | Inconsistencia de interfaz en funciones booleanas `is_*`, duplicación de helpers de validación y potenciales lazos en reconciliación límite. |
| **LOW** | 5 | Rendimiento de bucle escalar en `BB84Protocol.run`, archivo `errors.py` desalineado con la documentación, diccionarios globales mutables, precisión flotante en estimación y casos de prueba límite ausentes. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `HIGH` | `quantum/validation.py:12` (`_error_probability_state`) | Numérico / Tolerancia | `np.isreal` rechaza componentes imaginarias residuales ($<10^{-16}j$) por falta de tolerancia. |
| **H-02** | `HIGH` | `qkd/primitives/states.py`, `operations.py` | Seguridad / Invariantes | Arrays globales (`KET0`, `X`, etc.) no están marcados como de solo lectura (`writeable=False`). |
| **H-03** | `HIGH` | `core/rng.py:52` (`QRNGSimulator`) | Diseño / LSP | `QRNGSimulator.gen` delega al generador base, ignorando sesgo y correlación en llamadas polimórficas. |
| **M-01** | `MEDIUM` | `quantum/validation.py` (`is_*` vs `validate_*`) | Interfaces / Diseño | `is_quantum_state` y afines lanzan `ValueError` ante arrays malformados en vez de devolver `False`. |
| **M-02** | `MEDIUM` | `qkd/postprocessing/`, `metrics/` | Mantenibilidad / DRY | Cuádruple duplicación de helpers para validación de vectores binarios e índices. |
| **M-03** | `MEDIUM` | `qkd/postprocessing/reconciliation.py:211` | Robustez / Algoritmos | Reconciliación Cascade carece de cota máxima de iteraciones en el bucle de look-back. |
| **L-01** | `LOW` | `qkd/protocols/bb84.py:383` (`BB84Protocol.run`) | Rendimiento | Bucle escalar en Python puro para la transmisión y medida de $N$ qubits. |
| **L-02** | `LOW` | `quantum/errors.py` vs `docs/structure.md` | Documentación | Módulo de excepciones vacío a pesar de estar referenciado en la arquitectura. |
| **L-03** | `LOW` | `qkd/primitives/measurements.py:19` | Invariantes | Diccionario `MEASUREMENTS_BY_BASIS` mutable a nivel de módulo. |
| **L-04** | `LOW` | `qkd/postprocessing/parameter_estimation.py:54` | Numérico | Comparación estricta por desigualdad (`!=`) entre números de punto flotante en `__post_init__`. |
| **L-05** | `LOW` | `tests/test_qkd/test_reconciliation.py` | Calidad de Tests | Ausencia de tests parametrizados para longitudes no potencia de 2 y look-back multinivel forzado. |

---

## 3. Análisis Detallado de Hallazgos

### [H-01] Rechazo de vectores de probabilidad por ruido numérico imaginario (`np.isreal`)

1. **Archivo y función afectada**:
   - Archivo: `quantum/validation.py`
   - Función: `_error_probability_state(probs: ArrayLike, tol: float = DEFAULT_ATOL)` (línea 14), afectando a `is_probability_state` y `validate_probability_state`.

2. **Por qué es un problema**:
   La función verifica si las probabilidades son reales mediante `if not np.all(np.isreal(probabilities)):`. En NumPy, `np.isreal` comprueba la igualdad exacta `imag == 0`. Si una distribución de probabilidades proviene de una operación matricial compleja previa (por ejemplo, cálculo de valores esperados $\text{Tr}(P \rho)$ o autovalores en álgebra de estados cuánticos), es habitual que quede un residuo numérico de precisión de máquina (ej. $10^{-17}j$).
   Mientras que la no-negatividad y la suma unitaria sí respetan la tolerancia `tol`, la parte imaginaria es rechazada estrictamente sin tolerancia.

3. **Escenario donde falla**:
   Al validar un vector generado dinámicamente con parte imaginaria sub-épsilon:
   ```python
   p = np.array([0.5 + 1e-17j, 0.5 - 1e-17j], dtype=np.complex128)
   validate_probability_state(p)  # Lanza ValueError: Probability entries must be real.
   ```

4. **Corrección propuesta**:
   Comprobar que la magnitud de la parte imaginaria no exceda `tol`, en consonancia con el resto de validaciones del módulo:
   ```python
   if np.any(np.abs(np.imag(probabilities)) > tol):
       return f"Probability entries must be real. Got {probabilities}."
   ```

---

### [H-02] Arrays constantes globales mutables en primitivas QKD

1. **Archivo y función afectada**:
   - Archivos: `qkd/primitives/states.py` (líneas 5–15) y `qkd/primitives/operations.py` (líneas 5–8).
   - Constantes: `KET0`, `KET1`, `PLUS`, `MINUS`, `PLUS_I`, `MINUS_I`, `PHI_PLUS`, `PHI_MINUS`, `PSI_PLUS`, `PSI_MINUS`, `X`, `Y`, `Z`, `H`.

2. **Por qué es un problema**:
   Los arrays de NumPy son estructuras mutables por defecto. Las constantes a nivel de módulo no tienen activada la bandera `flags.writeable = False`. Cualquier función, test o script externo que modifique un elemento in-place (por ejemplo, `state = KET0; state[0] = 0.0` o `np.dot(X, ..., out=X)`) mutará la constante globalmente para todo el proceso de ejecución de Python, provocando efectos colaterales silenciosos y corrupción de simulaciones posteriores.

3. **Escenario donde falla**:
   ```python
   from qkd.primitives.states import KET0
   KET0[0] = 0.0  # Modifica KET0 globalmente; todas las ejecuciones de BB84 posteriores fallarán o darán resultados incorrectos.
   ```

4. **Corrección propuesta**:
   Marcar de forma explícita todos los arrays constantes como de solo lectura al inicializar los módulos:
   ```python
   # En qkd/primitives/states.py
   for _arr in (KET0, KET1, PLUS, MINUS, PLUS_I, MINUS_I, PHI_PLUS, PHI_MINUS, PSI_PLUS, PSI_MINUS):
       _arr.flags.writeable = False

   # En qkd/primitives/operations.py
   for _arr in (X, Y, Z, H):
       _arr.flags.writeable = False
   ```

---

### [H-03] `QRNGSimulator` no propaga sesgo ni correlación a través de la interfaz `BaseRNG`

1. **Archivo y función afectada**:
   - Archivo: `core/rng.py`
   - Clase: `QRNGSimulator` (líneas 52–96).

2. **Por qué es un problema**:
   `QRNGSimulator` hereda de `BaseRNG`, cuya propiedad abstracta obligatoria es `gen -> np.random.Generator`. Sin embargo, `QRNGSimulator.gen` devuelve simplemente `self.base_rng.gen` (el generador no sesgado subyacente). La lógica de sesgo (`bias_prob`) y correlación markoviana (`correlation`) solo está implementada en el método auxiliar `generate_raw_bits(size)`.
   Cualquier consumidor polimórfico de la arquitectura (como `sample_projective_outcome`, `BB84Protocol.run`, `random_bit` o `random_basis`) que reciba un `rng: BaseRNG` accede directamente a `rng.gen.choice` o `rng.gen.integers`. Como resultado, al inyectar un `QRNGSimulator`, el protocolo ejecuta una simulación perfecta e ideal, ignorando por completo el sesgo físico configurado.

3. **Escenario donde falla**:
   ```python
   # Simulación de ataque o imperfección física con QRNG defectuoso:
   qrng = QRNGSimulator(SeededRNG(42), bias_prob=0.95, correlation=0.3)
   protocol = BB84Protocol(IdentityChannel(), rng=qrng)
   res = protocol.run(1000)
   # Las bases y bits de Alice siguen siendo 50/50 uniformes porque BB84Protocol llama a rng.gen.integers.
   ```

4. **Corrección propuesta**:
   - Proporcionar métodos de generación de bits y elecciones en la interfaz `BaseRNG` (ej. `rng.random_bits(size)` y `rng.choice(outcomes, p)`), de modo que `QRNGSimulator` pueda sobreescribirlos.
   - Alternativamente, documentar que `QRNGSimulator` no debe usarse como generador general de `BaseRNG` mientras no implemente un `BitGenerator` personalizado de NumPy.

---

### [M-01] Inconsistencia en contratos de funciones de predicado `is_*` frente a entradas malformadas

1. **Archivo y función afectada**:
   - Archivo: `quantum/validation.py`
   - Funciones: `is_normalized_state`, `is_quantum_state`, `is_probability_state` frente a `is_unitary`, `is_density_matrix`, `is_projector`.

2. **Por qué es un problema**:
   En Python, una función de tipo predicado (`is_*`) debe devolver `True` o `False` para cualquier entrada evaluable, reservando el lanzamiento de excepciones para tipos fundamentalmente incompatibles si no se pueden coercer.
   En `validation.py`, `is_unitary(np.zeros((2, 3)))` y `is_density_matrix(np.zeros((2, 3)))` capturan dimensiones incorrectas y devuelven `False`. En cambio, `is_normalized_state(np.zeros((2, 2)))` y `is_quantum_state(np.zeros((2, 2)))` invocan `linalg.as_ket()`, la cual lanza un `ValueError` no capturado.
   Esto rompe la consistencia del API y la expectativa del usuario sobre las funciones de inspección booleana.

3. **Escenario donde falla**:
   ```python
   is_density_matrix(np.zeros((2, 2)))   # Devuelve False (correcto)
   is_quantum_state(np.zeros((2, 2)))     # Lanza ValueError: A ket must have shape (n,) or (n, 1). Got shape=(2, 2).
   ```

4. **Corrección propuesta**:
   En `_error_normalized_state` y `_error_probability_state`, encapsular la conversión de ket de forma segura:
   ```python
   def _error_normalized_state(psi: ArrayLike, tol: float = DEFAULT_ATOL) -> str | None:
       try:
           state = linalg.as_ket(psi)
       except ValueError as error:
           return str(error)
       norm_squared = float(np.sum(np.abs(state) ** 2))
       if not np.isclose(norm_squared, 1.0, atol=tol, rtol=0.0):
           return f"A quantum-state ket must have unit norm. Got norm_squared={norm_squared}."
       return None
   ```

---

### [M-02] Duplicación redundante de funciones de validación de vectores binarios e índices

1. **Archivo y función afectada**:
   - Archivos:
     - `qkd/postprocessing/_validation.py` (`copy_binary_vector`, `copy_indices`)
     - `qkd/postprocessing/sifting.py` (`_copy_binary_vector`, `_copy_indices`)
     - `qkd/metrics/qber.py` (`_binary_vector`)
     - `qkd/protocols/bb84.py` (`_copy_binary_vector`)

2. **Por qué es un problema**:
   Existen cuatro implementaciones casi idénticas de validación y copia defensiva de vectores binarios de bits en submódulos vecinos.
   Esto viola el principio DRY y causa pequeñas divergencias de comportamiento (por ejemplo, `_binary_vector` en `qber.py` no asigna `flags.writeable = False`, a diferencia de `copy_binary_vector` en `_validation.py`).

3. **Escenario donde falla**:
   Cualquier cambio o ajuste en los tipos enteros aceptados (ej. compatibilidad con tipos booleanos de NumPy o mensajes de error) requerirá modificaciones sincronizadas en cuatro archivos independientes.

4. **Corrección propuesta**:
   Eliminar las funciones privadas `_copy_binary_vector` y `_copy_indices` en `sifting.py`, `qber.py` y `bb84.py`, importando las versiones canónicas de `qkd.postprocessing._validation`.

---

### [M-03] Ausencia de límite de iteraciones / salvaguarda en bucle de look-back de Cascade

1. **Archivo y función afectada**:
   - Archivo: `qkd/postprocessing/reconciliation.py`
   - Función: `reconcile_cascade` (líneas 211–240).

2. **Por qué es un problema**:
   En la reconciliación Cascade, cuando se corrige un error en un bloque, se identifican todos los bloques afectados en otras pasadas y se encolan en `pending`. En escenarios con tasas de error atípicas o configuraciones anómalas con múltiples pasadas (ej. `passes=8`), el proceso de look-back puede reencolar repetidamente bloques. Aunque en teoría converge, la ausencia de un límite máximo de iteraciones de salvaguarda (`max_iterations`) expone al simulador a bloqueos o degradación de rendimiento ante claves sintéticas degeneradas.

3. **Escenario donde falla**:
   Ejecución de reconciliación en simulaciones de estrés con QBER muy elevado ($>30\%$) y claves grandes sin aborto previo por umbral de seguridad.

4. **Corrección propuesta**:
   Introducir un contador de seguridad en el bucle `while pending:` que lance una excepción descriptiva (`RuntimeError("Cascade look-back exceeded maximum iteration limit.")`) si se supera un múltiplo razonable del número de bloques.

---

### [L-01] Overhead de bucle escalar en `BB84Protocol.run`

1. **Archivo y función afectada**:
   - Archivo: `qkd/protocols/bb84.py`
   - Función: `BB84Protocol.run` (líneas 383–395).

2. **Por qué es un problema**:
   La simulación de la transmisión de $N$ qubits ejecuta un bucle `for` en Python puro que realiza $N$ llamadas individuales a `self.channel.apply()` y `sample_projective_outcome()`. Para valores grandes de $N$ ($N \ge 10^5$), la sobrecarga del intérprete de Python y la constante asignación/recolección de memoria para matrices $2\times 2$ ralentiza sensiblemente los barridos de parámetros en experimentos.

3. **Escenario donde falla**:
   Experimentos de Monte Carlo que requieran simular $10^6$ señales para análisis asintótico de tasas de clave.

4. **Corrección propuesta**:
   Mantener la interfaz actual para extensibilidad y añadir en el futuro un camino optimizado/vectorizado para canales estándar de un solo qubit (operando sobre tensores de estados `(N, 2, 2)`).

---

### [L-02] Módulo `quantum/errors.py` vacío y desalineación con `docs/structure.md`

1. **Archivo y función afectada**:
   - Archivo: `quantum/errors.py` (líneas 1–2).
   - Documentación: `docs/structure.md` (línea 211).

2. **Por qué es un problema**:
   La documentación de arquitectura indica que `quantum/errors.py` contiene `QuantumStateError` y `QuantumOperatorError`. Sin embargo, el archivo solo contiene un docstring reservado y todas las funciones de `quantum/` lanzan `ValueError`.

3. **Escenario donde falla**:
   Módulos superiores o usuarios que intenten capturar excepciones de dominio según la especificación de `structure.md`.

4. **Corrección propuesta**:
   Declarar formalmente las clases de excepción heredando de `ValueError` en `quantum/errors.py` o actualizar `docs/structure.md` para reflejar el uso de excepciones estándar.

---

### [L-03] Diccionario global mutable `MEASUREMENTS_BY_BASIS`

1. **Archivo y función afectada**:
   - Archivo: `qkd/primitives/measurements.py`
   - Objeto: `MEASUREMENTS_BY_BASIS` (líneas 19–23).

2. **Por qué es un problema**:
   `MEASUREMENTS_BY_BASIS` es un diccionario estándar de Python. Aunque sus valores son instancias inmutables de `ProjectiveMeasurement`, el diccionario en sí puede ser mutado (`MEASUREMENTS_BY_BASIS[Basis.Z] = None`), alterando el comportamiento global del protocolo.

3. **Escenario donde falla**:
   Reasignación accidental en scripts de prueba o experimentación interactiva en notebooks.

4. **Corrección propuesta**:
   Envolver el diccionario con `types.MappingProxyType` para garantizar inmutabilidad estructural:
   ```python
   from types import MappingProxyType
   MEASUREMENTS_BY_BASIS = MappingProxyType({
       Basis.Z: MEASUREMENT_Z,
       Basis.X: MEASUREMENT_X,
       Basis.Y: MEASUREMENT_Y,
   })
   ```

---

### [L-04] Comparación estricta de punto flotante en `ParameterEstimationResult`

1. **Archivo y función afectada**:
   - Archivo: `qkd/postprocessing/parameter_estimation.py`
   - Función: `ParameterEstimationResult.__post_init__` (línea 54).

2. **Por qué es un problema**:
   Se valida que `estimated_qber == qber(alice_disclosed, bob_disclosed)` mediante comparación estricta (`!=`). Si un usuario o componente deserializa o calcula `estimated_qber` con ligera imprecisión flotante (ej. $1/3$ vs $0.3333333333333333$), la validación fallará inesperadamente.

3. **Escenario donde falla**:
   Reconstrucción de objetos `ParameterEstimationResult` a partir de datos serializados (JSON/YAML) donde la representación de punto flotante pierde el último bit de precisión.

4. **Corrección propuesta**:
   Usar `math.isclose(estimated_qber, qber(...), abs_tol=1e-12)` o `DEFAULT_ATOL`.

---

### [L-05] Cobertura de pruebas insuficiente en casos límite de Cascade

1. **Archivo y función afectada**:
   - Archivo: `tests/test_qkd/test_reconciliation.py`

2. **Por qué es un problema**:
   Aunque los tests actuales cubren escenarios con ruido aleatorio y canales ideales con éxito, no existen tests con vectores de error artificialmente sintetizados para forzar la recursión multinivel del look-back (pasada 3 -> pasada 2 -> pasada 1) ni claves con longitudes primas impares pequeñas ($N=7, 11, 13$).

3. **Escenario donde falla**:
   Regresiones no detectadas en la indexación de bloques en tamaños impares o condiciones de carrera en el reencolado de Cascade.

4. **Corrección propuesta**:
   Añadir casos de prueba deterministas con patrones de error específicos conocidos y longitudes no estándar en `test_reconciliation.py`.

---

## 4. Evaluación de Invariantes y Principios de Diseño

1. **Disciplina Estricta de Capas (Acyclic Layering)**:
   - **Cumplimiento**: **Excelente**.
   - `core/` no importa nada del dominio cuántico ni QKD.
   - `quantum/` no conoce nada de BB84, Alice, Bob ni QBER.
   - `qkd/` consume limpiamente `quantum/` y `core/` sin importar `pqc` ni `ui`.

2. **Aleatoriedad Inyectada (Injected RNG)**:
   - **Cumplimiento**: **Muy Bueno**.
   - Todas las funciones del protocolo y de medida reciben `BaseRNG`.
   - Salvo por la limitación identificada en `QRNGSimulator` (hallazgo **H-03**), no se detecta estado global no reproducible en la lógica de dominio.

3. **Inmutabilidad y Copia Defensiva**:
   - **Cumplimiento**: **Muy Bueno**.
   - Los objetos de resultado (`BB84Result`, `ReconciliationResult`, `PrivacyAmplificationResult`, etc.) utilizan `@dataclass(frozen=True, slots=True, eq=False)` y configuran `flags.writeable = False` en sus arrays internos.
   - Es necesario extender esta protección a las constantes globales (hallazgos **H-02** y **L-03**).

4. **Precisión Matemática y Criptográfica**:
   - El hashing universal mediante convolución FFT sobre matrices de Toeplitz (`universal_hashing.py`) es matemáticamente impecable y evita materializar matrices densas $M \times N$.
   - La deducción de fuga de información en Cascade y confirmación es conservadora y rigurosa.

---

## 5. Conclusiones y Próximos Pasos Recomendados

La implementación de los módulos `quantum/`, `qkd/` y el protocolo `BB84` demuestra un nivel alto de rigor científico, excelente estructuración matemática y una estricta separación de responsabilidades.

Se recomienda abordar las correcciones en el siguiente orden de prioridad:
1. **Prioridad 1 (Inmediata)**:
   - Ajustar `_error_probability_state` en `quantum/validation.py` para usar tolerancia en la parte imaginaria (**H-01**).
   - Bloquear la mutabilidad de arrays constantes en `qkd/primitives/states.py` y `operations.py` (**H-02**).
   - Alinear `QRNGSimulator` con el flujo de aleatoriedad inyectada (**H-03**).
2. **Prioridad 2 (Mantenibilidad y Robustez)**:
   - Normalizar la captura de excepciones en funciones `is_*` de `quantum/validation.py` (**M-01**).
   - Unificar funciones duplicadas de validación de vectores binarios en `qkd/postprocessing/_validation.py` (**M-02**).
   - Añadir salvaguarda de iteraciones en Cascade (**M-03**).
3. **Prioridad 3 (Detalles menores y rendimiento)**:
   - Blindar `MEASUREMENTS_BY_BASIS` con `MappingProxyType` (**L-03**).
   - Ajustar `isclose` en `ParameterEstimationResult` (**L-04**).
   - Añadir casos de prueba dirigidos para longitudes impares en Cascade (**L-05**).
