# Revisión final independiente — Fase 7: Motor Experimental Reproducible V1

**Fecha de revisión:** 7 de septiembre de 2026  
**Correcciones verificadas:** 8 de septiembre de 2026  
**Commit base revisado:** `cf51da1bf07a1364cfb7ba4b2bc401bac955580e` (`phase 7 completed`)  
**Alcance:** `experiments/`, métricas QKD, builder neutral de canales, integración con `orchestration`, exportadores, CLI, ejemplos, tests y documentación.  
**Tipo de revisión:** arquitectura, comportamiento, reproducibilidad científica, ciclo de vida de secretos, integridad de artefactos y quality gates.

## 1. Dictamen

La Fase 7 queda funcionalmente cerrada para su alcance V1. La ruta canónica no expone material secreto, `experiments` permanece por encima de `orchestration`, y los tiempos QKD, PQC, autenticación e híbridos siguen separados.

La revisión original detectó siete incidencias. Todas se corrigieron y se protegieron con regresiones. En particular, E4 y HYBRID con autenticación Wegman–Carter completan una sesión ideal de 4.000 señales; los kinds incompatibles ya no pueden producir records engañosos; cada lote conserva su metodología; el entorno registra el dirty state de Git; y el límite record/export aplica schema estricto, valores JSON finitos y defensa contra campos secretos.

D1 continúa fuera del alcance de implementación de esta V1, tal como establece la especificación. El runner genérico ahora lo rechaza explícitamente para impedir que una sesión de establecimiento se etiquete falsamente como experimento de data plane.

### Resultado agregado

| Severidad | Detectadas | Abiertas | Resultado |
| :--- | :---: | :---: | :--- |
| **CRITICAL** | 0 | 0 | No se ha encontrado exfiltración automática de claves ni inversión de capas. |
| **HIGH** | 1 | 0 | H-01 corregida y validada en QKD y HYBRID con 4.000 señales. |
| **MEDIUM** | 3 | 0 | M-01, M-02 y M-03 corregidas. |
| **LOW** | 3 | 0 | L-01, L-02 y L-03 corregidas con validación y pruebas. |

**Decisión posterior a correcciones:** `GO` para preparar y ejecutar las campañas E1–E5. `D1` permanece `NOT IMPLEMENTED` por alcance y falla de forma explícita en el runner genérico.

---

## 2. Alcance inspeccionado

Se revisaron:

- [`experiments/config.py`](../../experiments/config.py): `ExperimentKind`, `ExperimentConfig`, round-trip y validación.
- [`experiments/environment.py`](../../experiments/environment.py): versiones, plataforma, CPU y Git.
- [`experiments/runtime.py`](../../experiments/runtime.py): RNG QKD, canales, identidades PQC y contextos de autenticación.
- [`experiments/runner.py`](../../experiments/runner.py): ejecución individual, cierre de secretos y lotes.
- [`experiments/record.py`](../../experiments/record.py): evidencia inmutable y schema público.
- [`experiments/export.py`](../../experiments/export.py): JSON/CSV y loaders de configuración.
- [`experiments/statistics.py`](../../experiments/statistics.py): mediana/IQR e intervalo Wilson.
- [`experiments/cli.py`](../../experiments/cli.py): comandos `run` y `batch`.
- [`qkd/channel/config.py`](../../qkd/channel/config.py): especificación neutral y builder de canales.
- [`orchestration/metrics.py`](../../orchestration/metrics.py), [`orchestration/qkd/result.py`](../../orchestration/qkd/result.py), [`orchestration/qkd/session_runner.py`](../../orchestration/qkd/session_runner.py) y [`orchestration/hybrid/runner.py`](../../orchestration/hybrid/runner.py): propagación de métricas QKD.
- [`tests/test_experiments/`](../../tests/test_experiments) y pruebas de integración relacionadas.
- [`docs/EXPERIMENTS.md`](../EXPERIMENTS.md), `README.md`, `TFM_GOAL.md`, `docs/structure.md`, `docs/tasks.md` y `AGENTS.md`.

La revisión se apoyó en inspección de código, Graphify, suite completa, smokes de los siete perfiles y reproducciones negativas específicas.

---

## 3. Arquitectura y propiedades verificadas

```text
examples / CLI
      |
      v
 experiments
   | config + public records
   | runtime-only provisioning
   v
 orchestration
   |----------|----------|
   v          v          v
  qkd        pqc      hybrid
   |
   v
 quantum -> core

 data_protection <- adaptador superior especializado
```

Graphify confirma:

```text
ExperimentRunner -> ExperimentRunner.run() -> run_session()
```

No existe ruta dirigida inversa desde `run_session` hacia `ExperimentRunner`, el informe global no detecta ciclos de importación y `ExperimentRunner` no aparece entre los diez nodos más conectados.

### Aspectos correctamente resueltos

1. `experiments` no importa schemas Pydantic de `ui`.
2. UI y experiments reutilizan el builder neutral de `qkd.channel`.
3. Los stages QKD conservan el orden y Eve recibe un RNG determinista separado por dominio.
4. Las identidades PQC se crean antes de `run_session()` y se reutilizan dentro de una factoría.
5. El material Wegman–Carter es runtime-only y fresco por ejecución; el defecto encontrado afecta a su capacidad, no a su confidencialidad.
6. `SessionResult.to_public_dict()` se copia antes de cerrar la capacidad viva.
7. `SessionResult.close()` se ejecuta en `finally` tras obtener un resultado.
8. Los abortos del protocolo producen records válidos.
9. La ruta canónica no exporta `K_SESSION`, PSK, secretos KEM, claves privadas ML-DSA ni claves QKD crudas.
10. Las métricas QKD estimadas y los diagnósticos del simulador permanecen diferenciados.
11. No existe `quantum_safe_latency` ni se suman relojes QKD y PQC.
12. El CSV deja vacías las métricas no aplicables y usa JSON canónico para estructuras anidadas.

---

## 4. Tabla de hallazgos

| ID | Severidad | Estado | Resolución |
| :--- | :--- | :---: | :--- |
| **H-01** | HIGH | **RESUELTA** | La capacidad Wegman–Carter crece con señales y pases Cascade, se registra en bytes por dirección y su almacenamiento permanece empaquetado. Regresiones QKD/HYBRID a 4.000 señales. |
| **M-01** | MEDIUM | **RESUELTA** | Validación mínima kind/perfil/stages y bloqueo temprano de D1 en el runner genérico. |
| **M-02** | MEDIUM | **RESUELTA** | `BatchProvenance` versionado conserva `batch_run_id`, shuffle, order seed y warm-ups en JSON/CSV. |
| **M-03** | MEDIUM | **RESUELTA** | `ExperimentEnvironment` registra `git_worktree_dirty: bool | None`. |
| **L-01** | LOW | **RESUELTA** | Cobertura CLI de batch JSON/CSV, shuffle, warm-up, destino ausente y JSON inválido/duplicado. |
| **L-02** | LOW | **RESUELTA** | Schema raíz exacto, árbol público validado, UUID4 canónico, campos secretos prohibidos y `allow_nan=False`. |
| **L-03** | LOW | **RESUELTA** | Matriz positiva de los siete stages y extremos estadísticos añadidos. |

---

## 5. Hallazgos detallados

### [H-01] La PSK Wegman–Carter por defecto es insuficiente

**Estado: RESUELTA.** La factoría reserva ahora, por dirección, el máximo entre el mínimo configurado y `signal_count * 128 * (cascade_passes + 1)` bytes. La capacidad pública queda registrada sin revelar el material y `PreSharedAuthenticationMaterial` conserva los secretos como bytes empaquetados, desempaquetando únicamente el tramo consumido. Las regresiones E4 y HYBRID con 4.000 señales terminan `established`.

El análisis siguiente conserva la reproducción original que motivó la corrección.

En [`experiments/runtime.py:87-92`](../../experiments/runtime.py#L87), la capacidad de cada secreto direccional se calcula así:

```python
signal_count = definition.qkd_signal_count or 0
material_bytes = max(self._minimum_psk_bytes, signal_count * 32)
qkd_authentication = WegmanCarterAuthenticationContext.from_shared_secrets(
    alice_to_bob_secret=token_bytes(material_bytes),
    bob_to_alice_secret=token_bytes(material_bytes),
)
```

La cantidad consumida no depende solo del número de señales. Wegman–Carter autentica un frame que contiene el transcript canónico completo. Su coste incluye mensaje, selector Toeplitz y máscara; el transcript incluye bases, índices de sifting, muestras, permutaciones y eventos Cascade.

#### Reproducción real

```text
experiment_kind = E4
profile = QKD-CLASSICAL-AUTH
qkd_signal_count = 4000
seed = 2026
pipeline = identity
runtime_factory = defaults
```

Resultado:

```text
status: aborted
transcript_bytes: 188510
required: 1509527 bits
remaining: 1024000 bits
abort_reason:
  Classical authentication failed: Authentication evidence generation failed:
  Insufficient fresh pre-shared authentication material
```

BB84 ideal produce material final; el aborto no representa ruido, ataque ni fallo criptográfico de verificación. Es una insuficiencia del laboratorio.

#### Impacto

- Invalida medidas E4 con tamaños mayores que los smokes pequeños.
- Puede afectar a HYBRID cuando selecciona `QKD-CLASSICAL-AUTH`.
- Convierte un error de aprovisionamiento en outcome protocolario `ABORTED`.
- Sesga la probabilidad de aborto y la comparación Wegman–Carter/ML-DSA.
- El test actual del motor usa 512 señales y no alcanza el umbral.

#### Corrección requerida en la revisión original (aplicada)

1. Eliminar la heurística no demostrada `signal_count * 32`.
2. Definir una cota conservadora demostrable a partir de señales y postprocesado, o exigir una capacidad pública explícita en el plan y validarla antes de medir.
3. Registrar solo la capacidad aprovisionada —nunca su valor— en `RuntimeProvisioning`.
4. Tratar este agotamiento como `execution_error`/`FAILED`, no como aborto de seguridad.
5. Añadir regresiones QKD y HYBRID con autenticación clásica, 4.000 señales y Cascade activo.

Este hallazgo bloqueaba E4 hasta aplicar y verificar la corrección descrita arriba.

### [M-01] `ExperimentKind` puede mentir sobre lo ejecutado

**Estado: RESUELTA.** `ExperimentConfig` exige QKD para E2/E3/E4, un stage `intercept_resend` para E3 y componente PQC para E1/E5/D1. `ExperimentRunner` rechaza D1 antes de construir runtime hasta que exista el runner especializado del data plane.

`ExperimentConfig.__post_init__()` valida seed, stages y perfil por separado, pero no usa `experiment_kind` para evitar contradicciones obvias. `ExperimentRunner.run()` tampoco despacha por tipo ni aplica guardas. Las referencias muestran que el kind se consume únicamente como etiqueta del record/exportación.

#### Reproducción real

```text
ExperimentKind.E3_INTERCEPT_RESEND + SessionProfile.PQC_BASE -> established
ExperimentKind.D1_PROTECTED_SESSION + SessionProfile.PQC_BASE -> established
```

En el primer caso no hubo BB84, Eve ni QBER. En el segundo no hubo transferencia al data plane ni AES-256-GCM. El artefacto declara respectivamente E3 y D1.

#### Impacto

No rompe criptografía, pero sí la integridad semántica del dataset. Un filtro posterior por `experiment_kind` puede incorporar filas ajenas y producir tablas científicamente falsas.

#### Corrección requerida en la revisión original (aplicada)

No hace falta una mega-matriz. Bastan invariantes obvias:

- E2, E3 y E4 requieren componente QKD.
- E3 requiere al menos un stage `intercept_resend`.
- E1 y E5 requieren el componente PQC aplicable a su diseño.
- D1 se rechaza en `ExperimentRunner` hasta que exista el runner que abra el data plane antes del cierre.

Si se desea flexibilidad futura, las guardas pueden vivir en validadores por kind o runners especializados. Lo inadmisible es generar silenciosamente un record falso.

### [M-02] El dataset no conserva la metodología del lote

**Estado: RESUELTA.** Todos los records retenidos de un batch comparten un `BatchProvenance` inmutable y versionado con UUID4, `shuffle`, `order_seed` y `warmup_runs`; `execution_order_index` exige esa procedencia. JSON y CSV exportan los campos.

`run_batch()` recibe `shuffle`, `order_seed` y `warmup_runs`, pero cada record solo conserva `execution_order_index`. No hay identificador de lote, manifest ni metadata del plan.

Para PQC, el número de warm-ups puede cambiar la distribución de tiempos por cachés, carga de bibliotecas y asignador. Dos artefactos con configs idénticas pueden proceder de cero o veinte warm-ups sin poder distinguirse.

`execution_order_index` reconstruye el orden si se conserva el lote completo, pero no indica:

- si el orden fue aleatorizado;
- qué `order_seed` lo produjo;
- cuántas ejecuciones se descartaron;
- qué records pertenecían al mismo lote tras combinar CSVs.

#### Corrección requerida en la revisión original (aplicada)

Añadir, por record o mediante un manifest versionado:

```text
batch_run_id
shuffle
order_seed
warmup_runs
execution_order_index
```

Esto no es un framework de campañas; es procedencia mínima del método ya expuesto por V1.

El warm-up QKD actual **no es automático**: solo ocurre con `warmup_runs > 0`. Ejecutar una config QKD cuando el usuario lo pide explícitamente no contradice la especificación. El problema es no registrar esa decisión.

### [M-03] El SHA Git no demuestra que se ejecutó ese código exacto

**Estado: RESUELTA.** La captura best-effort ejecuta `rev-parse HEAD` y `status --porcelain`, y registra tanto `git_commit_sha` como `git_worktree_dirty`. Fuera de un repositorio ambos pueden permanecer `None` sin abortar la ejecución.

`ExperimentEnvironment` contiene `git_commit_sha`, pero `_git_commit()` solo ejecuta `git rev-parse HEAD`. No captura si el árbol está limpio.

Si se modifica `qkd/`, `orchestration/` o `experiments/` sin commit y se inicia una campaña, todos los records siguen atribuyendo la ejecución al SHA anterior. La combinación config + seed + entorno + commit deja entonces de identificar el código real.

#### Corrección requerida en la revisión original (aplicada)

Añadir:

```text
git_worktree_dirty: bool | None
```

Opcionalmente puede incluirse un hash del diff o del árbol relevante. No debe almacenarse el diff textual, que podría contener información no destinada al artefacto. Para datasets finales la CLI debería advertir o rechazar un árbol de fuentes modificado.

### [L-01] Cobertura incompleta de la CLI

**Estado: RESUELTA.** Las pruebas cubren batch con JSON y CSV, shuffle/seed/warm-up, ausencia de destino y configuración JSON duplicada o inválida.

La única prueba de CLI cubre `run config.json --output record.json`. No hay prueba automatizada de:

- `batch` con JSON, CSV o ambos;
- `--shuffle --order-seed`;
- `--warmup-runs`;
- ausencia de destinos;
- seed de orden inválida;
- JSON malformado, claves duplicadas y errores de escritura a través de la CLI.

`run_batch()` sí tiene prueba directa de shuffle/warm-up, pero eso no cubre `argparse`, loaders y exportadores. Se recomienda un `test_cli.py` con happy paths y errores esperados, manteniendo visibles los fallos inesperados de programación.

### [L-02] El límite record/export confía en mappings arbitrarios

**Estado: RESUELTA.** El constructor valida los schemas raíz exactos de result/trace/metrics, recorre el árbol público, rechaza tipos no serializables, floats no finitos y nombres de campos secretos. Los exportadores usan JSON estricto con `allow_nan=False`.

La ruta normal es segura: `ExperimentRecord.from_session_result()` toma el serializer público, separa trace/metrics y congela copias. Sin embargo, el constructor público acepta cualquier `Mapping[str, object]`, y `dumps_json()`/`dumps_csv()` no aplican una allowlist adicional.

Así, un record manual puede contener campos ajenos; una regresión inferior se propagaría sin barrera; y un float no finito manual se serializaría como `NaN`/`Infinity`, que no es JSON estricto. No se observó una fuga en la ruta canónica, por eso la severidad es baja.

Se recomienda validar el schema exacto, limitar la construcción a una factoría controlada, rechazar nombres prohibidos como defensa en profundidad y usar `allow_nan=False`.

### [L-03] Huecos menores de tests del contrato público

**Estado: RESUELTA.** Se añadieron casos positivos para los siete tipos de stage, percentiles pares, extremos Wilson, una sola observación y rechazo de booleanos/NaN/infinitos.

Los canales subyacentes tienen buena suite y UI ejercita varias combinaciones. Falta una prueba parametrizada directa de `QKDChannelStageSpec -> build_channel_stage` para los siete tipos, incluidos casos positivos de `amplitude_damping` y `pauli`.

En estadísticas faltan regresiones para:

- Wilson con `successes = 0` y `successes = trials`;
- Wilson con una observación;
- `median_iqr` con cardinalidad par;
- rechazo visible de `NaN`, infinitos y booleanos.

Las implementaciones inspeccionadas son correctas; el hallazgo es de protección frente a regresiones.

---

## 6. Diagnósticos del borrador anterior descartados

La primera versión del informe contenía falsos positivos que no deben convertirse en tareas funcionales.

### Punto fijo de `experiment_record_json_bytes`

Solo cambia un entero ASCII dentro de una estructura JSON fija. La recurrencia es:

```text
siguiente_tamaño = C + número_de_dígitos(tamaño_actual)
```

Para un objeto finito converge. En un record PQC real se observó:

```text
5251 -> 5254 -> 5254
```

No es correcto llamarlo coste cuadrático ni riesgo actual de loop infinito. Puede acotarse por higiene, pero es una optimización informativa.

### Serialización JSON al producir CSV

El CSV incluye `artifact.experiment_record_json_bytes`; mientras exista esa columna debe resolverse el tamaño. Se puede cachear y evitar búsquedas redundantes, pero no es trabajo completamente innecesario.

### Warm-ups QKD

El default es cero y solo se ejecutan por petición explícita, tal como exige la especificación. Debe registrarse el plan, no ignorar unilateralmente configs solicitadas.

### Captura de `RuntimeError` en CLI

La especificación exige que programming errors permanezcan visibles. Capturar todo `RuntimeError` con `argparse` escondería invariantes rotos. Solo deben traducirse excepciones operativas específicas.

### Uso de `assert`

Los asserts observados estrechan invariantes ya validados por dataclasses inmutables. Quitar asserts con `python -O` no crea un objeto soportado con campos ausentes. `cast()` o guardas explícitas mejorarían claridad, pero no se demostró un fallo real.

---

## 7. Reproducibilidad y secretos

### QKD

- seed obligatorio y de 64 bits;
- `SeededRNG` para BB84;
- streams de Eve separados por SHA-256, seed raíz e índice de stage;
- orden de canales conservado;
- misma config + seed reproduce outcome y métricas protocolarias;
- run ID, timestamp y timings cambian correctamente.

### PQC

- no se falsea determinismo de liboqs;
- seed `None` en perfiles PQC-only;
- se reproducen perfil, algoritmos, schema y método, no ciphertexts, firmas, IDs ni tiempos;
- identidades persistentes fuera de los cronómetros de sesión.

### Auditoría de secretos

```text
ExperimentConfig (público)
        |
        v
ExperimentRuntimeFactory (PSK, private identities, KEM state)
        |
        v
run_session() -> SessionResult con capacidad viva
        |
        v
to_public_dict() -> ExperimentRecord copia/congela
        |
        v
SessionResult.close()
        |
        v
JSON / CSV
```

No se encontró un camino automático de secretos hacia los artefactos. La prueba sentinel Wegman–Carter pasa para JSON/CSV, `established_key` solo contiene tipo/longitud y provenance solo metadata pública. L-02 es defensa en profundidad, no una fuga actual.

---

## 8. Métricas, JSON, CSV y estadística

`QKDSessionMetrics` expone correctamente:

```text
estimated_qber_z / estimated_qber_x / estimated_qber_aggregated
phase_error_bound
n_raw / n_sifted / n_disclosed / n_candidate / n_reconciled / n_final
sifting_efficiency / final_secret_fraction
diagnostic_full_sifted_qber
diagnostic_qber_z / diagnostic_qber_x / diagnostic_qber_aggregated
transcript_bytes / simulation_time_ns
```

Las estimaciones proceden del muestreo; los diagnósticos de la sifted key completa están marcados como tales. PQC conserva los nombres reales de fase y no los renombra como primitivas que no se midieron.

JSON es UTF-8, indentado, versionado y con loaders estrictos para configuraciones. CSV tiene una fila por run, union schema, columnas dotted, JSON canónico para anidados y celdas vacías cuando no aplica.

`median_iqr` usa percentiles lineales de NumPy y `wilson_interval` implementa Wilson bilateral con `NormalDist`, sin añadir SciPy ni un framework analítico prematuro.

El CSV incluye `metrics.orchestration_software_wall_time_ns`. La campaña debe tratarlo expresamente como diagnóstico software, nunca latencia física ni magnitud para sumar/comparar con PQC.

---

## 9. Definition of Done agrupada

| Área | Estado | Observación |
| :--- | :---: | :--- |
| Arquitectura superior `experiments -> orchestration` | PASS | Sin inversión ni ciclos. |
| Config versionada, inmutable, normalizada y round-trip | PASS | Unknown/duplicate fields rechazados. |
| Seed QKD/PQC | PASS | Determinismo modelado separado de entropía criptográfica. |
| Pipeline QKD ordenado y neutral respecto a UI | PASS | Builder compartido. |
| Runtime separado de config/secretos | PASS | Ruta canónica secret-free. |
| PQC identities fuera del timing | PASS | Lazy y reutilizadas por factoría. |
| PSK Wegman–Carter suficiente | PASS | QKD y HYBRID establecidos a 4.000 señales. |
| Environment mínimo | PASS | Incluye commit y dirty state best-effort. |
| Record UUID4, UTC, inmutable y público | PASS | Copias y cierre de capacidad. |
| Coherencia `ExperimentKind` | PASS | Guardas mínimas y D1 bloqueado en el runner genérico. |
| QKD metrics E2/E3 | PASS | Estimated/diagnostic separados. |
| Abort como outcome válido | PASS | Abortos protocolarios se registran; la regresión artificial desapareció. |
| JSON/CSV secret-free canónico | PASS | Schema defensivo y JSON estricto. |
| Batch y shuffle reproducible | PASS | Procedencia versionada completa por record. |
| Warm-up explícito/descartado | PASS | Se descarta y se registra su cantidad. |
| Median/IQR y Wilson | PASS | Extremos y entradas no finitas cubiertos. |
| CLI y ejemplos | PASS | Run y batch cubiertos, incluidos errores esperados. |
| Separación de timings | PASS | Sin `quantum_safe_latency`. |
| Quality gates | PASS | Evidencia en sección 10. |
| D1 end-to-end | **NOT IMPLEMENTED** | Fuera del alcance V1; el genérico ya lo rechaza claramente. |

---

## 10. Evidencia de validación

### Python

```text
uv run pytest -q
782 passed, 1 warning
```

La advertencia procede de `fastapi.testclient`/Starlette, no de Fase 7.

```text
uv run pytest tests/test_experiments -q
46 passed

uv run ruff check .
All checks passed!

uv run pyright
0 errors, 0 warnings, 0 informations
```

### Frontend

```text
npm test -- --run
3 test files passed, 6 tests passed

npm run typecheck
PASS

npm run build
PASS — 2258 modules transformed
```

### Smoke de los siete perfiles

Con 512 señales donde aplica:

```text
QKD-ASSUMED          established
QKD-CLASSICAL-AUTH   established
QKD-PQC-AUTH         established
PQC-BASE             established
PQC-DIVERSE          established
HYBRID               established
HYBRID-DIVERSE       established
```

El mismo smoke validó siete records JSON, siete filas CSV, metadata común de lote y ausencia de nombres de campos secretos prohibidos.

### Regresiones de las incidencias

```text
E4 / QKD-CLASSICAL-AUTH / identity / 4000 señales
-> established

E5 / HYBRID + QKD-CLASSICAL-AUTH / identity / 4000 señales
-> established

E3 / PQC-BASE
-> configuración rechazada

D1 / PQC-BASE
-> runner genérico rechaza y dirige al runner especializado futuro
```

### Graphify

```text
2988 nodes
7118 edges
143 communities
import cycles: none
ExperimentRunner -> run() -> run_session()
reverse directed path: none
```

`ExperimentConfig` aparece como octavo god node con 43 aristas; `ExperimentRunner` sigue fuera del top 10. No se detectaron inversiones de dependencia.

---

## 11. Preparación por experimento

| Experimento | Estado | Motivo |
| :--- | :---: | :--- |
| **E1 — PQC cost** | **READY** | Records, métricas, batch y CLI disponibles. |
| **E2 — BB84 validation** | **READY** | Métricas protocolarias y diagnósticas diferenciadas. |
| **E3 — Intercept-resend** | **READY** | La configuración exige QKD y stage de Eve. |
| **E4 — QKD authentication** | **READY** | Wegman–Carter y ML-DSA disponibles; regresión a 4.000 señales verde. |
| **E5 — Hybrid overhead** | **READY** | Categorías QKD/PQC/híbrida separadas; regresión clásica verde. |
| **D1 — protected session** | **NOT IMPLEMENTED** | Requiere runner especializado futuro, según el alcance original. |

Ya se puede preparar y ejecutar la campaña E1–E5. Antes de producir el dataset definitivo conviene hacer commit de estas correcciones para que los records indiquen `git_worktree_dirty = false`. D1 no debe incluirse hasta implementar su runner especializado.

---

## 12. Correcciones aplicadas

1. **H-01:** capacidad Wegman–Carter escalada, publicada como cantidad y almacenada de forma empaquetada.
2. **M-01:** invariantes kind/perfil/stages y bloqueo del D1 genérico.
3. **M-02:** procedencia de lote versionada y exportable.
4. **M-03:** dirty state Git best-effort.
5. **L-01/L-03:** matriz ampliada de CLI, stages y estadística.
6. **L-02:** schema público defensivo y JSON estricto.

Se repitieron:

```text
uv run pytest
uv run ruff check .
uv run pyright
frontend tests/typecheck/build
graphify update .
smoke JSON/CSV sin secretos
E4 QKD-CLASSICAL-AUTH >= 4000 señales
HYBRID + QKD-CLASSICAL-AUTH >= 4000 señales
```

## 13. Conclusión

El diseño central respeta capas, conserva métricas existentes, separa configuración pública de capacidades secretas y mantiene verde la base de código. Las siete incidencias de la revisión quedaron corregidas sin rehacer la arquitectura ni ampliar el motor hacia una plataforma analítica.

**Veredicto final posterior a correcciones:** Fase 7 V1 aprobada y lista para preparar datasets reproducibles de E1–E5. D1 permanece conscientemente pendiente de su runner especializado y no puede etiquetarse por accidente mediante el runner genérico.
