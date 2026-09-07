# Informe de Revisión de Código Independiente: QKD BB84 (Fases 1 y 2 del Escenario Final v1)

**Fecha**: 6 de Septiembre de 2026  
**Alcance**: Commits `2b6c75e` ("final stage v1 - phase 1 completed") y `8cdbf32` ("final stage v1 - phase 2 completed").  
**Módulos analizados**:
- **Fase 1**: Estimación de QBER por bases (`e_Z`, `e_X`, agregado), modelo de cota de error de fase asintótico (`max(e_Z, e_X)`) y muestreo estratificado con descarte de divulgados (`qkd/metrics/qber.py`, `qkd/metrics/security.py`, `qkd/postprocessing/parameter_estimation.py`, `qkd/protocols/bb84.py`, `docs/SECURITY_MODEL.md`).
- **Fase 2**: Adversario activo *Intercept-Resend* (Eve) desacoplado en el canal cuántico, diagnósticos agregados y exposición en API/UI (`qkd/channel/attacks/intercept_resend.py`, `qkd/channel/base.py`, `ui/backend/adapters.py`, `ui/backend/schemas.py`, `ui/backend/capabilities.py`, `ui/frontend/src/types/api.ts`).  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría exhaustiva e independiente sobre los dos últimos commits correspondientes a las Fases 1 y 2 del plan de culminación de la versión 1 de **QuantumSec**:

1. **Fase 1 (`2b6c75e` — Métricas por bases y corrección de la decisión de seguridad)**:
   - Sustitución de la suposición simétrica previa ($e_{ph} = \text{QBER}$) por la cota teórica conservadora de Shor-Preskill / códigos CSS: para un candidato que combina posiciones retenidas en $Z$ y $X$, los errores de bit en $X$ acotan los errores de fase en $Z$, y los errores de bit en $Z$ acotan los errores de fase en $X$, justificando formalmente $\text{phase\_error\_bound} = \max(e_Z, e_X)$.
   - Prevención demostrada de la sobre-extracción de bits secretos en canales asimétricos (ej. *Phase Flip Channel* donde $e_Z \approx 0$ y $e_X \approx p$, lo que antes permitía extraer erróneamente claves sobre estimaciones agregadas de $p/2$).
   - Muestreo estratificado sin reemplazo por base (`estimate_qber_from_sample`), garantizando que ambas bases contribuyen a la estimación y conservan posiciones candidatas, eliminando obligatoriamente todos los bits divulgados.
   - Separación estricta entre la tasa de error de bit de Cascade (`bit_error_rate = estimated_qber_aggregated`) y la cota de error de fase para amplificación de privacidad (`phase_error_bound`).

2. **Fase 2 (`8cdbf32` — Adversario Intercept-Resend de Eve)**:
   - Implementación de `InterceptResendAttack` como etapa estocástica desacoplada en `ChannelPipeline`, heredando de `QuantumChannel` sin acceder a información privada de Alice ni Bob.
   - Parámetro de intercepción estocástica $f \in [0.0, 1.0]$ y verificación analítica de la perturbación inducida $\text{QBER} \approx 0.25 f$ bajo canal ideal.
   - Aislamiento estricto de diagnósticos en `AttackDiagnostics` (conteos de señales vistas, interceptadas, bases y resultados de Eve), sin exponer secuencias de claves ni decisiones de aborto al adversario.
   - Integración completa en FastAPI (`ui/backend/`) y tipado en frontend (`ui/frontend/`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades que comprometan la seguridad cuántica del protocolo ni sobre-extracciones de clave. |
| **HIGH** | 0 | El modelo de error de fase corrige con rigor el fallo asimétrico previo y el adversario Intercept-Resend está completamente desacoplado del protocolo. |
| **MEDIUM** | 1 | Compartición de la misma instancia de `BaseRNG` entre Eve y Bob en el backend, desincronizando la secuencia de medición de Bob en simulaciones donde Eve intercepta. |
| **LOW** | 5 | Inconsistencia de firma en `BB84PostprocessingConfig` (`phase_error_abort_threshold`), estado mutable acumulativo sin método `reset()` en `InterceptResendAttack`, convención de redondeo en `_explicit_stratified_counts`, potencial confusión en UI entre `estimated_qber` y `phase_error_bound`, y ausencia de test unitario de purificación de estados mezcla en Eve. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | `MEDIUM` | `ui/backend/adapters.py:111-116` | Modelado Físico / RNG | La misma instancia de `SeededRNG` se inyecta concurrentemente en `InterceptResendAttack` y `BB84Protocol`, acoplando el avance del PRNG de Bob a las intercepciones de Eve. |
| **L-01** | `LOW` | `qkd/protocols/bb84.py:228-275` (`BB84PostprocessingConfig`) | Usabilidad de API | `BB84PostprocessingConfig` no acepta `phase_error_abort_threshold` como argumento en `__init__`, obligando a usar el nombre legado `qber_abort_threshold`. |
| **L-02** | `LOW` | `qkd/channel/attacks/intercept_resend.py:86` (`InterceptResendAttack`) | Mantenibilidad / Diseño | `InterceptResendAttack` acumula contadores diagnósticos internos de forma mutable sin exponer un método `reset()`, falseando métricas si la instancia se reutiliza entre ejecuciones. |
| **L-03** | `LOW` | `qkd/postprocessing/parameter_estimation.py:36` (`_explicit_stratified_counts`) | Casos Borde | Uso de `round()` con regla de redondeo al par bancario en la asignación de bits por base, introduciendo asimetrías dependientes de la paridad en muestras impares. |
| **L-04** | `LOW` | `ui/backend/schemas.py:177` (`PostprocessingSummary`) | Claridad Semántica | Exposición duplicada de `estimated_qber` y `estimated_qber_aggregated`, pudiendo inducir a componentes de UI a mostrar QBER agregado como condición de aborto en lugar de `phase_error_bound`. |
| **L-05** | `LOW` | `tests/test_qkd/test_channel/test_intercept_resend.py` | Cobertura de Tests | Falta de test unitario verificando la proyección de estados mezcla (ej. $\rho = I/2$) hacia estados puros retransmitidos tras la medición de Eve. |

---

## 3. Análisis Detallado de Hallazgos

### [M-01] Acoplamiento del flujo PRNG de Bob por la inyección compartida de `BaseRNG` en Eve

1. **Archivo y función afectada**:
   - Archivo: `ui/backend/adapters.py`
   - Función: `run_bb84` (líneas 111–116).
   - Componentes relacionados: `qkd/protocols/bb84.py:448-460` y `qkd/channel/attacks/intercept_resend.py:143-156`.

2. **Por qué es un problema**:
   En `ui/backend/adapters.py`:
   ```python
   rng = SeededRNG(request.seed)
   channels = tuple(build_channel(configuration, rng=rng) for configuration in request.channels)
   pipeline = ChannelPipeline(channels)
   session = BB84Protocol(channel=pipeline, rng=rng).run_session(request.n_signals)
   ```
   La misma instancia física `rng` es compartida por `InterceptResendAttack` y `BB84Protocol`.
   En el bucle de transmisión cuántica (`bb84.py:448-460`), para cada señal $i$:
   - Primero se invoca `self.channel.apply(...)`. Si Eve intercepta (con probabilidad $f$), Eve consume números pseudoaleatorios de `self._rng` (decisión de Bernoulli, elección de base `random_basis`, y muestreo de Born en `sample_projective_outcome`).
   - Inmediatamente después, Bob mide el estado recibido utilizando `self.rng`.
   
   Al compartir la misma secuencia de PRNG:
   - Cuando Eve intercepta la señal $i$, consume valores del generador, alterando los números aleatorios que recibirá Bob tanto para su medición en la señal $i$ como en todas las señales posteriores $i+1, \dots, N$.
   - Físicamente, Alice, Bob y Eve son entidades independientes con sus propias fuentes de entropía física/detectores. En un simulador experimental, las decisiones estocásticas de Eve no deberían alterar el estado interno del generador del detector de Bob en señales no interceptadas.

3. **Escenario donde falla**:
   Al realizar estudios comparativos de sensibilidad o ablación para aislar la perturbación física cuántica de Eve frente al ruido del detector: variar la fracción de intercepción $f$ o cambiar la semilla de Eve desalinea por completo las decisiones de medición de Bob en señales idénticas, impidiendo un análisis causal paso a paso de los mismos estados cuánticos.

4. **Corrección propuesta**:
   Derivar o crear un generador independiente para los adversarios en `adapters.py` (ej. mediante `SeedSequence.spawn` o asignando `SeededRNG(seed + 1000)` a las etapas de ataque), desacoplando los sorteos estocásticos de Eve del canal de detección de Bob y del post-procesamiento de Alice/Bob.

---

### [L-01] Parámetro `phase_error_abort_threshold` no admitido en el constructor de `BB84PostprocessingConfig`

1. **Archivo y función afectada**:
   - Archivo: `qkd/protocols/bb84.py`
   - Clase: `BB84PostprocessingConfig` (líneas 228–275).

2. **Por qué es un problema**:
   La Fase 1 transformó conceptualmente el criterio de aborto de seguridad: ya no se aborta por QBER agregado, sino por la cota de error de fase ($\text{phase\_error\_bound} > \text{threshold}$).
   En `BB84PostprocessingConfig` se añadió la propiedad:
   ```python
   @property
   def phase_error_abort_threshold(self) -> float:
       return self.qber_abort_threshold
   ```
   Sin embargo, el campo en el `@dataclass` sigue llamándose exclusivamente `qber_abort_threshold`. Si un usuario o script intenta configurar la sesión con la terminología rigurosa del modelo (`BB84PostprocessingConfig(phase_error_abort_threshold=0.08)`), Python eleva una excepción `TypeError` por argumento inesperado.

3. **Escenario donde falla**:
   ```python
   config = BB84PostprocessingConfig(phase_error_abort_threshold=0.09)
   # TypeError: BB84PostprocessingConfig.__init__() got an unexpected keyword argument 'phase_error_abort_threshold'
   ```

4. **Corrección propuesta**:
   Permitir `phase_error_abort_threshold: float | None = None` como argumento opcional en el constructor (o mediante un método de factoría), asignándolo a `qber_abort_threshold` para permitir la transición sin romper retrocompatibilidad.

---

### [L-02] Acumulación de estado mutable sin método `reset()` en `InterceptResendAttack`

1. **Archivo y función afectada**:
   - Archivo: `qkd/channel/attacks/intercept_resend.py`
   - Clase: `InterceptResendAttack` (líneas 78–169).

2. **Por qué es un problema**:
   `InterceptResendAttack` mantiene contadores acumulativos internos (`_n_signals_seen`, `_n_intercepted`, `_eve_z_measurements`, etc.) que son actualizados en cada llamada a `apply()`.
   A diferencia del resto de canales de `qkd/channel/` que son operadores puros e inmutables, esta clase retiene estado. Si un usuario instancia un ataque y ejecuta múltiples simulaciones `bb84.run(1000)` reutilizando el mismo objeto de canal o pipeline, los diagnósticos no reflejan la última ejecución sino el acumulado histórico, sin que exista un método `reset()` para reiniciar los contadores.

3. **Escenario donde falla**:
   En scripts de benchmarking, barridos de parámetros o notebooks interactivos:
   ```python
   eve = InterceptResendAttack(0.5, rng)
   protocol = BB84Protocol(eve, rng)
   res1 = protocol.run(1000)   # eve.diagnostics.n_signals_seen == 1000
   res2 = protocol.run(1000)   # eve.diagnostics.n_signals_seen == 2000 (acumulado no deseado)
   ```

4. **Corrección propuesta**:
   Añadir un método `reset()` en `InterceptResendAttack`:
   ```python
   def reset(self) -> None:
       """Reset all internal cumulative diagnostic counters to zero."""
       self._n_signals_seen = 0
       self._n_intercepted = 0
       self._eve_z_measurements = 0
       self._eve_x_measurements = 0
       self._eve_zero_outcomes = 0
       self._eve_one_outcomes = 0
   ```

---

### [L-03] Asimetría de muestreo en `_explicit_stratified_counts` debida al redondeo al par

1. **Archivo y función afectada**:
   - Archivo: `qkd/postprocessing/parameter_estimation.py`
   - Función: `_explicit_stratified_counts` (línea 36).

2. **Por qué es un problema**:
   El cálculo de las posiciones a divulgar en la base $Z$ emplea:
   ```python
   disclose_z = int(round(sample_size * n_z / (n_z + n_x)))
   ```
   En Python 3, `round()` aplica la regla de redondeo bancario al entero par más cercano. Cuando $n_z = n_x$ y el tamaño de muestra `sample_size` es impar (por ejemplo $n_z=10, n_x=10, \text{sample\_size}=5$), el producto es $2.5$, que se redondea a $2$ (par), asignando $2$ a $Z$ y $3$ a $X$. Si la muestra es $7$, $7 \times 0.5 = 3.5$, que se redondea a $4$, asignando $4$ a $Z$ y $3$ a $X$. Esto produce pequeñas alternancias en la base predominante en función de la paridad matemática del cociente.

3. **Escenario donde falla**:
   En pruebas estadísticas ultra-estrictas de simetría de muestreo con muestras impares pequeñas.

4. **Corrección propuesta**:
   Documentar explícitamente el uso de redondeo al par o implementar una regla determinista simétrica si se requiere perfecta invariancia ante permutaciones de bases.

---

### [L-04] Potencial ambigüedad de métricas de decisión en el esquema de la API Web

1. **Archivo y función afectada**:
   - Archivo: `ui/backend/schemas.py`
   - Clases: `SimulationMetrics` (líneas 161–166) y `PostprocessingSummary` (líneas 173–180).

2. **Por qué es un problema**:
   En `PostprocessingSummary` se exponen simultáneamente:
   - `estimated_qber`: valor idéntico a `estimated_qber_aggregated`.
   - `phase_error_bound`: cota efectiva utilizada para autorizar la extracción de clave y calcular el tamaño secreto.
   
   Si un cliente frontend o un consumidor de la API REST visualiza `estimated_qber = 0.07` y observa `status: "aborted"`, puede interpretar que la simulación falló incorrectamente porque el QBER estaba por debajo del umbral del 11%, ignorando que el aborto fue provocado por `phase_error_bound = 0.14 > 0.11` debido a un canal asimétrico.

3. **Escenario donde falla**:
   Visualizadores del frontend que rendericen la tarjeta de estado mostrando únicamente `estimated_qber` junto al umbral de aborto.

4. **Corrección propuesta**:
   Asegurar en la documentación OpenAPI y en los componentes de interfaz que `phase_error_bound` se identifique explícitamente como la variable de control del aborto de seguridad, etiquetando `estimated_qber` como métrica exclusiva de configuración de Cascade.

---

### [L-05] Ausencia de prueba unitaria de colapso y purificación de estados mezcla en Eve

1. **Archivo y función afectada**:
   - Archivo: `tests/test_qkd/test_channel/test_intercept_resend.py`.

2. **Por qué es un problema**:
   Los tests de `InterceptResendAttack` verifican entradas con estados puros ($|0\rangle, |+\rangle$).
   Sin embargo, un canal físico previo en el pipeline (como `DepolarizingChannel` o `AmplitudeDampingChannel`) introduce estados mezcla con pureza $\text{Tr}(\rho^2) < 1$.
   Cuando Eve intercepta un estado mezcla, su medición proyectiva colapsa el estado y retransmite un estado BB84 completamente puro ($\text{Tr}(\rho^2) = 1$). Aunque matemáticamente `sample_projective_outcome` soporta matrices de densidad arbitrarias, no existe un test unitario que compruebe explícitamente la purificación física resultante de la retransmisión de Eve ante entradas mezcla como $\rho = I/2$.

3. **Escenario donde falla**:
   Falta de aserción explícita de pureza en tests ante composiciones de canales ruidosos seguidos de intercepción.

4. **Corrección propuesta**:
   Añadir un test `test_intercept_resend_purifies_mixed_input_states` en `test_intercept_resend.py`:
   ```python
   def test_intercept_resend_purifies_mixed_input_states():
       attack = InterceptResendAttack(1.0, SeededRNG(42))
       maximally_mixed = np.eye(2, dtype=np.complex128) / 2.0
       output = attack.apply(maximally_mixed)
       purity = float(np.real(np.trace(output @ output)))
       assert purity == pytest.approx(1.0, abs=1e-8)
   ```

---

## 4. Evaluación de Invariantes y Principios de Diseño Cuántico/Criptográfico

1. **Justificación Matemática de la Cota de Fase (Shor-Preskill / Códigos CSS)**:
   - **Evaluación**: **Sobresaliente**.
   - La implementación de $\text{phase\_error\_bound} = \max(e_Z, e_X)$ resuelve definitivamente la vulnerabilidad conceptual previa en canales asimétricos.
   - Al combinar las posiciones candidatas de $Z$ y $X$ en un único pool para Cascade y amplificación de privacidad, la tasa de error de fase media real es $\bar{e}_{ph} = \frac{n_Z e_X + n_X e_Z}{n_Z + n_X}$.
   - Puesto que $\max(e_Z, e_X) \ge \bar{e}_{ph}$ y la entropía binaria $h_2(p)$ es estrictamente creciente en $[0, 0.5]$, la cota adoptada garantiza que la compresión de privacidad aplicada mediante matrices de Toeplitz es un límite superior seguro para la información accesible a Eve.
   - Se demostró con tests de regresión (`test_asymmetric_phase_flip_does_not_use_aggregate_qber_as_phase_error`) que el ataque asimétrico por *Phase Flip* aborta limpiamente sin extraer bits no justificados.

2. **Muestreo Estratificado y Descarte Obligatorio**:
   - **Evaluación**: **Excelente**.
   - `estimate_qber_from_sample` muestrea de manera independiente y sin reemplazo dentro de cada base.
   - Se valida defensivamente que ambas bases aporten al menos una posición divulgada y retengan al menos una posición candidata; de lo contrario, la sesión aborta formalmente por insuficiencia muestral.
   - Todos los bits divulgados son eliminados de las claves de Alice y Bob antes de iniciar Cascade, eliminando cualquier riesgo de reutilización de material revelado.

3. **Arquitectura y Desacoplamiento del Adversario Intercept-Resend**:
   - **Evaluación**: **Excelente**.
   - `InterceptResendAttack` se implementa como un `QuantumChannel` composable en `ChannelPipeline`. No introduce bifurcaciones `if attack:` en el protocolo BB84 ni viola la jerarquía de capas.
   - La etapa sólo recibe matrices de densidad $\rho$; no tiene acceso a las elecciones de base de Alice ni a las futuras bases de Bob.
   - Cumple con alta fidelidad la ley física analítica $\text{QBER} \approx 0.25 f$, comprobada mediante pruebas estadísticas deterministas con $12\,000$ señales.
   - Con $f = 0.0$, el canal no consume aleatoriedad y replica con precisión de bit la ejecución libre de ataque.

---

## 5. Conclusiones y Recomendaciones de Priorización

Las Fases 1 y 2 del escenario final v1 representan un avance sustancial en la madurez científica y el rigor formal de **QuantumSec**:
- Se cerró la brecha de seguridad en canales asimétricos adoptando la cota teórica de Shor-Preskill.
- Se incorporó un modelo de adversario activo explícito y comprobable contra predicciones analíticas.
- La suite completa de 597 pruebas unitarias y de integración en Python y 6 pruebas en Vitest se ejecuta con éxito al 100%.

Se recomienda priorizar las mejoras detectadas en el siguiente orden:
1. **Prioridad 1 (Desacoplamiento Estocástico)**:
   - Derivar una semilla o generador independiente para el adversario en `adapters.py` para desacoplar el flujo de aleatoriedad de Eve del detector de Bob (**M-01**).
2. **Prioridad 2 (Ergonomía de API y Estado de Canales)**:
   - Habilitar `phase_error_abort_threshold` como argumento directo en el constructor de `BB84PostprocessingConfig` (**L-01**).
   - Añadir método `reset()` en `InterceptResendAttack` para facilitar su uso en campañas experimentales repetidas (**L-02**).
3. **Prioridad 3 (Cobertura y Documentación)**:
   - Incorporar el test de purificación de estados mezcla en `test_intercept_resend.py` (**L-05**).
   - Clarificar en la UI que `phase_error_bound` es la única variable que determina el aborto de seguridad (**L-04**).
