# Informe de Revisión de Código Independiente: Orquestación de Sesiones, Runners PQC/QKD y Composición Híbrida (Fases 4 y 5)

**Fecha**: 7 de Septiembre de 2026  
**Alcance**: Commit `0383d72` (*"phase 3 review implemented & phase 4 & 5 (orchestation)"*) frente a la base `2d00da7`.  
**Módulos analizados**:
- **Capa común de orquestación**: `orchestration/config.py`, `orchestration/context.py`, `orchestration/profiles.py`, `orchestration/metrics.py`, `orchestration/trace.py`, `orchestration/result.py`, `orchestration/runner.py`.
- **Adaptadores y runners de dominio**:
  - QKD: `orchestration/qkd/session_runner.py`, `orchestration/qkd/runner.py`, `orchestration/qkd/result.py`.
  - PQC: `orchestration/pqc/runner.py`, `orchestration/pqc/exchange.py`.
- **Composición híbrida (Fase 5)**: `orchestration/hybrid/runner.py`, `orchestration/hybrid/finished.py`, `orchestration/hybrid/key_schedule.py`, `orchestration/hybrid/context.py`, `orchestration/hybrid/encoding.py`.
- **Integración PQC-Híbrida**: `pqc/protocol/hybrid_contributions.py`, `pqc/protocol/_shared_secret_state.py`.
- **Autenticación clásica QKD**: `orchestration/authentication/base.py`, `orchestration/authentication/execution.py`, `orchestration/authentication/ml_dsa.py`.
- **Suites de verificación**: `tests/test_orchestration/*`, `tests/test_pqc/test_hybrid_contributions.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han modificado archivos fuente durante la revisión, cumpliendo las directrices del rol.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría exhaustiva e independiente sobre la implementación de las Fases 4 y 5 de la arquitectura de **QuantumSec**, correspondiente a la creación de la capa unificada de orquestación de sesiones y la composición híbrida de material secreto cuántico y poscuántico:

1. **Fase 4 — Capa Común de Sesiones y Runners Especializados**:
   - Definición de 7 perfiles públicos normalizados (`QKD-ASSUMED`, `QKD-CLASSICAL-AUTH`, `QKD-PQC-AUTH`, `PQC-BASE`, `PQC-DIVERSE`, `HYBRID`, `HYBRID-DIVERSE`) con dimensiones ortogonales de establecimiento y autenticación.
   - Separación estricta entre configuración pública reproducible (`SessionConfig`) y contexto de ejecución con secretos efímeros y entidades aprovisionadas (`SessionExecutionContext`).
   - Contratos de trazabilidad ordenada e inmutable (`SessionTrace`, `SessionTraceEvent`, `SessionTraceBuilder`).
   - Contratos de resultado unificado y capacidad de clave establecida (`SessionResult`, `EstablishedKeyCapability`, `SecretProvenance`, `SessionAuthentication`).
   - Mapeo de métricas categorizadas que preserva la separación metodológica entre el tiempo de simulación cuántica BB84 y el tiempo de computación criptográfica clásica/poscuántica en CPU.
   - Adaptadores de ejecución (`run_qkd_session`, `run_pqc_session`) sobre un despachador unificado (`run_session`).

2. **Fase 5 — Composición Híbrida QKD + PQC**:
   - Capacidad de transferencia de un solo uso en el dominio PQC (`AuthenticatedKEMContributions`), que valida la autenticación del transcript antes de transferir los secretos compartidos de ML-KEM-768 y HQC-3, cerrando inmediatamente el estado interno de origen (`_shared_secret_state.py`).
   - Codificación canónica binaria no ambigua de componentes secretos (`canonical_hybrid_secret_input`), imponiendo orden canónico estricto ($K_{\text{QKD}}$, $SS_{\text{ML-KEM}}$, opcional $SS_{\text{HQC}}$), prefijos de longitud de 64 bits y empaquetado de bits QKD con comprobación de ceros en bits residuales.
   - Contexto público híbrido autenticado (`HybridPublicContext`) que enlaza de manera no ambigua identificador de sesión, versiones, algoritmos, y los digests SHA-384 de las transcripciones QKD y PQC.
   - Derivación de clave mediante HKDF-SHA-384 con separación criptográfica estricta de dominios (`SessionKey` y `ConfirmationKey`).
   - Protocolo Finished de confirmación mutua HMAC-SHA-384 en dos vuelos (Bob $\rightarrow$ Alice encadenada con `verify_data`), que retira inmediatamente la clave de confirmación una vez validada.

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades que permitan la fuga de secretos, la derivación no autenticada de claves o eludir el control de acceso a las capacidades de clave. |
| **HIGH** | 2 | Cláusula `except` con anomalía de sintaxis en `ml_dsa.py` que rompe compatibilidad con entornos estándar Python $\le 3.13$, y captura excesivamente estrecha (`except ValueError:`) en runners que deja escapar excepciones criptográficas del backend (`PQCError`) provocando caídas no controladas y dejando `SessionStatus.FAILED` como código muerto. |
| **MEDIUM** | 3 | Pérdida de todas las métricas híbridas intermedias cuando el protocolo aborta en la verificación Finished; ausencia de soporte de Gestor de Contexto (`__enter__`/`__exit__`) en `SessionResult` para la destrucción determinista de claves; y acoplamiento rígido por índice numérico en el etiquetado de KEMs. |
| **LOW** | 5 | Omisión de comprobación defensiva de tipo booleano en `HybridSecretComponent`; falta de validación de rango en versiones de transcripción en `HybridPublicContext.__post_init__`; uso de `assert` para validar precondiciones en `run_hybrid_session`; omisión de validación de tipo en `verify_finished`; y pérdida de los hashes de transcripción ya calculados en el resultado abortado. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `HIGH` | `orchestration/authentication/ml_dsa.py:92` | Sintaxis / Compatibilidad | Manejador `except PQCError, TypeError, ValueError:` sin paréntesis que genera `SyntaxError` en cualquier versión de Python $\le 3.13$ e incumple PEP 8. |
| **H-02** | `HIGH` | `orchestration/hybrid/runner.py:386`, `orchestration/pqc/runner.py:232` | Robustez / Manejo de Errores | Captura restringida exclusivamente a `ValueError` que deja escapar `PQCError`, `BackendOperationError` y `RuntimeError`, provocando caídas abruptas y dejando `SessionStatus.FAILED` como código muerto. |
| **M-01** | `MEDIUM` | `orchestration/hybrid/runner.py:321, 386-407` | Observabilidad / Métricas | La instancia `HybridSessionMetrics` se crea tras el Finished, provocando que si el Finished falla se retorne `metrics.hybrid = None` y se pierdan todos los tiempos y bytes de combinador y HKDF ya invertidos. |
| **M-02** | `MEDIUM` | `orchestration/result.py:125-235` (`SessionResult`) | Gestión de Recursos / API | `SessionResult` no implementa `__enter__` ni `__exit__`, impidiendo la gestión segura con `with run_session(...) as result:` y requiriendo un cierre manual que favorece la permanencia de claves en memoria. |
| **M-03** | `MEDIUM` | `orchestration/hybrid/runner.py:215` (`components`) | Diseño / Extensibilidad | Asignación de etiquetas de secretos basada rígidamente en `"SS_ML_KEM" if index == 2 else "SS_HQC"`, etiquetando erróneamente cualquier KEM adicional o reorganizado como HQC. |
| **L-01** | `LOW` | `orchestration/hybrid/encoding.py:26-38` | Validación Defensiva | `HybridSecretComponent` no rechaza valores booleanos en `position` y `bit_length` (`isinstance(True, int)` es `True`), a diferencia de otras clases defensivas del repositorio. |
| **L-02** | `LOW` | `orchestration/hybrid/context.py:34-60` | Validación de Tipos | `HybridPublicContext.__post_init__` no valida que `qkd_transcript_version` y `pqc_protocol_version` sean enteros sin signo en $[0, 65535]$, difiriendo el error a la serialización. |
| **L-03** | `LOW` | `orchestration/hybrid/runner.py:84-85` | Fiabilidad en Producción | Uso de `assert config.qkd_signal_count is not None` en código de librería, omitiéndose silenciosamente si el intérprete se ejecuta optimizado (`python -O`). |
| **L-04** | `LOW` | `orchestration/hybrid/finished.py:125-135` | Manejo de Tipos | `verify_finished` asume ciegamente la presencia de atributos del mensaje sin verificar `isinstance(message, HybridFinishedMessage)`, lanzando `AttributeError` ante objetos inesperados. |
| **L-05** | `LOW` | `orchestration/hybrid/runner.py:390-407` | Auditoría Forense | El resultado abortado en Finished no adjunta los hashes de transcripción QKD/PQC y del contexto en `public_context` pese a haber sido ya computados. |

---

## 3. Análisis Detallado de Hallazgos

### [H-01] Manejador de excepciones no parentizado en `ml_dsa.py` incompatible con Python $\le 3.13$

1. **Archivo y función afectada**:
   - Archivo: `orchestration/authentication/ml_dsa.py`
   - Función: `MLDSADirectionalAuthenticator.verify_evidence` (línea 92).

2. **Por qué es un problema**:
   En el commit auditado se modificó la línea 92 cambiando:
   ```python
   # Antes (canónico):
   except (PQCError, TypeError, ValueError):
   # Ahora:
   except PQCError, TypeError, ValueError:
   ```
   En Python 3 estándar (desde Python 3.0 hasta Python 3.13), la cláusula `except A, B, C:` genera un error de sintaxis irrecuperable: `SyntaxError: invalid syntax`. En la semántica histórica de Python 2, la coma se interpretaba como enlace a variable (`except ExceptionType, target:`). Aunque Python 3.14 introduce una relajación en el analizador sintáctico PEG para tuplas sin paréntesis en ciertas expresiones, escribir excepciones separadas por coma sin agrupar en tupla:
   - Incumple de forma flagrante la guía de estilo PEP 8.
   - Rompe la ejecución inmediata si el repositorio se instala o ejecuta en entornos con Python 3.11, 3.12 o 3.13 (versiones de producción y LTS actuales en la industria).
   - Genera incoherencia con el resto del proyecto, donde se emplea la sintaxis canónica (ej. `orchestration/authentication/execution.py:100`: `except (AuthenticationMaterialError, PQCError, TypeError, ValueError) as exc:`).

3. **Escenario donde falla**:
   Si un usuario, evaluador del TFM o canal de integración continua ejecuta la suite bajo Python 3.12 o 3.13, o si se pasa una herramienta estándar de linting/AST, el módulo no compila:
   ```text
     File "orchestration/authentication/ml_dsa.py", line 92
       except PQCError, TypeError, ValueError:
                      ^
   SyntaxError: invalid syntax
   ```

4. **Corrección propuesta**:
   Restaurar la tupla canónica de excepciones con paréntesis:
   ```python
   except (PQCError, TypeError, ValueError):
       return AuthenticationVerification(False, "ML-DSA signature verification failed.")
   ```

---

### [H-02] Captura excesivamente restrictiva (`except ValueError:`) que deja escapar excepciones criptográficas y operativas del backend

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/runner.py` -> `run_hybrid_session` (línea 386).
   - Archivo: `orchestration/pqc/runner.py` -> `run_pqc_session` (línea 232).

2. **Por qué es un problema**:
   Los bloques de ejecución criptográfica de ambos runners están protegidos únicamente contra `ValueError`:
   ```python
   # orchestration/hybrid/runner.py:386
   except ValueError as exc:
       reason = str(exc)
       trace.append(SessionTraceSource.HYBRID, "confirmation", "failed", reason)
       ...
       return SessionResult(..., SessionStatus.ABORTED, ...)
   ```
   Sin embargo, las funciones invocadas internamente pueden emitir otros tipos de excepción:
   - `derive_hkdf_sha384` en `pqc/kdf/hkdf.py:46` captura fallos criptográficos y lanza `PQCError(f"HKDF key derivation failed: {exc}")`. `PQCError` hereda de `Exception`, **no** de `ValueError`.
   - `BackendOperationError` o `BackendUnavailableError` lanzados por fallos en llamadas nativas de `liboqs`.
   - `RuntimeError` lanzado por `release_final_keys()` si el estado QKD se invoca fuera de orden.
   - `TypeError` generado si un hook de transporte devuelve un tipo corrupto.

   Al no ser instancias de `ValueError`, estas excepciones escapan sin control, provocando que `run_session()` caiga con un trace de excepción no capturado en lugar de retornar un `SessionResult` seguro con clave retenida.
   Asimismo, `SessionStatus.FAILED = "failed"` (definido en `orchestration/result.py:18` para reflejar caídas operativas) no se utiliza en ningún lugar de la base de código, resultando en código muerto.

3. **Escenario donde falla**:
   Si durante una ejecución intensiva de derivación de claves bajo carga o en un entorno con un fallo puntual de memoria en liboqs, `derive_hkdf_sha384` lanza `PQCError`, el runner híbrido o PQC no lo atrapa. La aplicación superior o la API FastAPI experimenta un error 500 no controlado en lugar de recibir un `SessionResult` con `SessionStatus.FAILED` o `ABORTED`.

4. **Corrección propuesta**:
   Ampliar el manejador de excepciones para distinguir entre fallos de validación/protocolo y fallos operacionales de la infraestructura:
   ```python
   except ValueError as exc:
       reason = str(exc)
       trace.append(SessionTraceSource.HYBRID, "confirmation", "failed", reason)
       trace.append(SessionTraceSource.SESSION, "session", "aborted", reason)
       return SessionResult(
           ...,
           status=SessionStatus.ABORTED,
           abort_reason=reason,
           ...,
       )
   except (PQCError, RuntimeError, Exception) as exc:
       reason = f"Operational execution failure: {exc}"
       trace.append(SessionTraceSource.SESSION, "session", "failed", reason)
       return SessionResult(
           SESSION_RESULT_VERSION,
           exchange.transcript.session_id,
           config.profile,
           SessionStatus.FAILED,
           reason,
           (),
           SessionAuthentication(qkd_auth, _pqc_outcome(False)),
           trace.freeze(),
           SessionMetrics(orchestration_software_wall_time_ns=perf_counter_ns() - wall_start),
       )
   ```

---

### [M-01] Pérdida de métricas de trabajo híbrido ante abortos en la confirmación Finished

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/runner.py`
   - Función: `run_hybrid_session` (líneas 321–340 y 386–407).

2. **Por qué es un problema**:
   En `run_hybrid_session`, la variable `hybrid_metrics` se inicializa como `None` (línea 120) y únicamente se le asigna una instancia de `HybridSessionMetrics` en la línea 321, **después** de verificar con éxito los mensajes Finished de Bob y Alice.
   Si la verificación de Finished falla (línea 277 o 308):
   ```python
   if not responder_verified:
       raise ValueError("Responder hybrid Finished verification failed.")
   ```
   El flujo salta inmediatamente al bloque `except ValueError:`, donde se retorna:
   ```python
   SessionMetrics(
       qkd=qkd_metrics,
       pqc=pqc_metrics,
       ...,
       hybrid=hybrid_metrics, # <-- Sigue siendo None
       orchestration_software_wall_time_ns=perf_counter_ns() - wall_start,
   )
   ```
   A pesar de que el combinador se ejecutó con éxito (codificación de secretos, cálculo de sobrecarga de bytes), se derivaron las claves HKDF de sesión y confirmación (`hkdf_session_time_ns`, `hkdf_confirmation_time_ns`) y se midió el tiempo de cálculo del MAC Finished, **todas estas métricas se pierden irrevocablemente**.

3. **Escenario donde falla**:
   En la campaña de experimentos (ej. evaluando el coste de un ataque activo sobre el canal clásico durante la fase Finished), el objeto `SessionResult` resultante tiene `metrics.hybrid is None`. El investigador no puede medir el impacto en tiempo ni la sobrecarga en bytes de los secretos combinados antes de que ocurriera el aborto.

4. **Corrección propuesta**:
   Construir métricas parciales o registrar los contadores en una estructura intermedia antes de entrar al intercambio Finished, de modo que en el bloque de excepción se construya el `HybridSessionMetrics` correspondiente con los tiempos acumulados hasta el fallo:
   ```python
   except ValueError as exc:
       reason = str(exc)
       if hybrid_metrics is None and alice_input is not None:
           hybrid_metrics = HybridSessionMetrics(
               component_count=len(alice_components),
               component_metadata_bytes=tuple(hybrid_component_metadata_bytes(c) for c in alice_components),
               qkd_contribution_bits=qkd_bit_length,
               ml_kem_contribution_bytes=ml_bytes,
               hqc_contribution_bytes=hqc_bytes,
               canonical_combiner_input_bytes=len(alice_input),
               encoding_overhead_bytes=len(alice_input) - raw_bytes,
               public_context_bytes=len(public_context.canonical_bytes()),
               encoding_time_ns=encoding_time,
               hkdf_session_time_ns=hkdf_session_time,
               hkdf_confirmation_time_ns=hkdf_confirmation_time,
               finished_generation_time_ns=generation_time,
               finished_verification_time_ns=verification_time,
               finished_responder_bytes=len(responder_finished.canonical_bytes()) if responder_finished else 0,
               finished_initiator_bytes=0,
               derived_session_key_bits=256,
           )
   ```

---

### [M-02] `SessionResult` carece de interfaz de Gestor de Contexto (`__enter__` / `__exit__`)

1. **Archivo y función afectada**:
   - Archivo: `orchestration/result.py`
   - Clase: `SessionResult` (líneas 125–235).

2. **Por qué es un problema**:
   El contenedor interno de la clave, `EstablishedKeyCapability`, implementa el protocolo de gestor de contexto (`__enter__` y `__exit__`, líneas 58–62) para garantizar la destrucción segura de la referencia a la clave en memoria al abandonar el bloque `with`.
   Sin embargo, la clase expuesta públicamente al usuario en el punto de entrada `run_session()`, `SessionResult`, únicamente implementa un método explícito `close()`, omitiendo `__enter__` y `__exit__`.
   Esto impide el patrón idiomático y seguro:
   ```python
   with run_session(config, context) as session:
       key = session.export_session_key()
       # procesar datos protegidos
   # la clave queda automáticamente cerrada y retirada de memoria
   ```
   Si el consumidor olvida envolver el uso de `SessionResult` en un bloque `try ... finally: session.close()`, el material criptográfico plano reside indefinidamente en el heap de Python.

3. **Escenario donde falla**:
   Cualquier código de usuario o test que intente hacer `with run_session(cfg, ctx) as res:` falla inmediatamente con `AttributeError: __enter__`.

4. **Corrección propuesta**:
   Implementar los métodos del protocolo de gestor de contexto en `SessionResult`:
   ```python
   def __enter__(self) -> Self:
       return self

   def __exit__(
       self,
       exc_type: type[BaseException] | None,
       exc_val: BaseException | None,
       exc_tb: object,
   ) -> None:
       self.close()
   ```

---

### [M-03] Asignación rígida de etiquetas de algoritmos KEM por índice numérico en `run_hybrid_session`

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/runner.py`
   - Función interna: `run_hybrid_session.components` (línea 215).

2. **Por qué es un problema**:
   En la construcción de la tupla de `HybridSecretComponent`, las etiquetas se asignan con la expresión ternaria:
   ```python
   values.extend(
       HybridSecretComponent(
           index,
           "SS_ML_KEM" if index == 2 else "SS_HQC",
           "pqc",
           algorithm,
           "raw-bytes",
           len(secret) * 8,
           secret,
       )
       for index, (algorithm, secret) in enumerate(kems, 2)
   )
   ```
   Esta lógica asume que todo componente con `index >= 3` es necesariamente HQC. Si en versiones futuras se incorpora un tercer algoritmo KEM (por ejemplo, Classic McEliece para paridad conservadora) o se evalúa un perfil donde solo se use un KEM distinto de ML-KEM, cualquier índice $\ge 3$ recibirá indiscriminadamente la etiqueta `"SS_HQC"`. Esto introduce un acoplamiento frágil dependiente de la posición en lugar de basarse en el identificador semántico del algoritmo.

3. **Escenario donde falla**:
   Si se expande la arquitectura para dar soporte a combinaciones con tres KEMs o se sustituye HQC por otro KEM de nivel 5, el segundo KEM recibe la etiqueta de metadatos `"SS_HQC"`, generando un fallo de validación en `canonical_hybrid_secret_input` o corrompiendo la semántica de la entrada canónica.

4. **Corrección propuesta**:
   Vincular las etiquetas al nombre canónico del algoritmo mediante un diccionario declarativo:
   ```python
   _KEM_ALGORITHM_LABELS = {
       ML_KEM_768_ALGORITHM: "SS_ML_KEM",
       HQC_3_ALGORITHM: "SS_HQC",
   }
   # Dentro de components():
   label = _KEM_ALGORITHM_LABELS.get(algorithm, f"SS_{algorithm.replace('-', '_')}")
   ```

---

### [L-01] Omisión de rechazo explícito de booleanos en `HybridSecretComponent.__post_init__`

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/encoding.py`
   - Clase: `HybridSecretComponent` (líneas 26–38).

2. **Por qué es un problema**:
   En Python, `bool` es una subclase de `int`, por lo que `isinstance(True, int)` es verdadero. La validación en `HybridSecretComponent`:
   ```python
   if self.position <= 0:
       raise ValueError("position must be positive.")
   ```
   permite que `position=True` (evaluado como 1) y `bit_length=True` (evaluado como 1) superen la validación sin levantar excepción.
   En cambio, en otras clases del paquete (ej. `EstablishedKeyCapability` en `result.py:34` y `SessionTraceEvent` en `trace.py:26`) se comprueba rigurosamente:
   ```python
   if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position <= 0:
   ```

3. **Escenario donde falla**:
   Instanciar `HybridSecretComponent(position=True, ...)` no genera error de tipo en el constructor, violando las invariantes de validación defensiva del proyecto.

4. **Corrección propuesta**:
   Añadir la comprobación de tipo estricta para `position` y `bit_length` en `__post_init__`:
   ```python
   if isinstance(self.position, bool) or not isinstance(self.position, int) or self.position <= 0:
       raise ValueError("position must be a positive integer.")
   if isinstance(self.bit_length, bool) or not isinstance(self.bit_length, int):
       raise TypeError("bit_length must be an integer.")
   ```

---

### [L-02] Falta de validación anticipada de versiones en `HybridPublicContext.__post_init__`

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/context.py`
   - Clase: `HybridPublicContext` (líneas 34–60).

2. **Por qué es un problema**:
   Los campos `qkd_transcript_version` y `pqc_protocol_version` no son verificados en `__post_init__`. Si se suministra un número negativo, un valor superior a $2^{16}-1$ o un tipo no entero, la instancia se construye exitosamente. El error solo se manifiesta tardíamente cuando se invoca `canonical_bytes()`, que a su vez llama a `unsigned(..., width=2)`.

3. **Escenario donde falla**:
   Construir `HybridPublicContext(..., qkd_transcript_version=-1, ...)` se ejecuta sin error inmediato, rompiendo el principio de fallo temprano (*fail-fast*) en la frontera de construcción de objetos de valor inmutables.

4. **Corrección propuesta**:
   Añadir en `__post_init__`:
   ```python
   for name in ("qkd_transcript_version", "pqc_protocol_version"):
       val = getattr(self, name)
       if isinstance(val, bool) or not isinstance(val, int) or not (0 <= val <= 0xFFFF):
           raise ValueError(f"{name} must be an unsigned 16-bit integer.")
   ```

---

### [L-03] Uso de sentencias `assert` para la validación de precondiciones en `run_hybrid_session`

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/runner.py`
   - Función: `run_hybrid_session` (líneas 84–85).

2. **Por qué es un problema**:
   En las líneas 84–85 se evalúa:
   ```python
   assert config.qkd_signal_count is not None
   assert config.qkd_authentication_profile is not None
   ```
   Si el entorno de ejecución ejecuta Python con el flag `-O` (*optimize*), el intérprete ignora y elimina por completo todas las sentencias `assert`. Las comprobaciones de seguridad y consistencia en código de producción de una biblioteca criptográfica nunca deben depender de `assert`.

3. **Escenario donde falla**:
   Ejecución del servicio con `python -O`, donde una configuración manipulada o incompleta elude la aserción y desencadena errores de tipo inesperados en funciones internas.

4. **Corrección propuesta**:
   Sustituir por comprobaciones explícitas:
   ```python
   if config.qkd_signal_count is None:
       raise ValueError("Hybrid execution requires a positive qkd_signal_count.")
   if config.qkd_authentication_profile is None:
       raise ValueError("Hybrid execution requires an explicit qkd_authentication_profile.")
   ```

---

### [L-04] `verify_finished` no valida el tipo del mensaje entrante antes de acceder a sus atributos

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/finished.py`
   - Función: `verify_finished` (líneas 125–135).

2. **Por qué es un problema**:
   En `verify_finished`, la función comienza evaluando:
   ```python
   metadata_matches = (
       message.version == HYBRID_FINISHED_VERSION
       and message.session_id == context.session_id
       ...
   )
   ```
   Si se le pasa un objeto ajeno (o `None`, proveniente de un hook de transporte defectuoso), el código falla con `AttributeError: 'NoneType' object has no attribute 'version'` en lugar de retornar `False` o levantar un `TypeError` controlado.

3. **Escenario donde falla**:
   Un hook de red mal implementado o corrupto que devuelva `None` o un diccionario causa un crash no controlado por `AttributeError`.

4. **Corrección propuesta**:
   Comprobar el tipo al inicio de la función:
   ```python
   if not isinstance(message, HybridFinishedMessage):
       return False
   ```

---

### [L-05] Omisión de hashes de transcripción en `public_context` cuando la sesión híbrida aborta tras el cómputo

1. **Archivo y función afectada**:
   - Archivo: `orchestration/hybrid/runner.py`
   - Función: `run_hybrid_session` (líneas 390–407).

2. **Por qué es un problema**:
   Cuando la sesión híbrida aborta durante la fase de Finished (línea 386), el `SessionResult` devuelto se construye sin especificar `public_context`, por lo que toma el valor por defecto `()`.
   Sin embargo, en ese punto del flujo, tanto el `qkd_transcript_hash`, como el `pqc_transcript_hash` y el propio `public_context.context_hash` ya habían sido calculados de forma exitosa y determinista en la línea 232. Descartar estos identificadores impide la trazabilidad y la correlación forense del intento fallido en los sistemas de auditoría externa y en las pruebas de penetración.

3. **Escenario donde falla**:
   Al auditar sesiones abortadas en los experimentos de seguridad, el diccionario `result.to_public_dict()["public_context"]` está vacío, impidiendo verificar contra qué transcripciones específicas se produjo el fallo de HMAC.

4. **Corrección propuesta**:
   Pasar la tupla de metadatos públicos en el retorno de la excepción si `public_context` ya había sido instanciado:
   ```python
   public_context_entries = (
       ()
       if public_context is None
       else (
           ("hybrid_context_hash_sha384", public_context.context_hash.hex()),
           ("qkd_transcript_hash_sha384", public_context.qkd_transcript_hash.hex()),
           ("pqc_transcript_hash_sha384", public_context.pqc_transcript_hash.hex()),
           ("hybrid_encoding_version", public_context.encoding_version),
           ("hybrid_context_version", public_context.version),
       )
   )
   return SessionResult(
       ...,
       public_context=public_context_entries,
   )
   ```

---

## 4. Aspectos Positivos y Fortalezas del Diseño

1. **Disciplina de Capas Acíclicas Impecable (Acyclic Layering)**:
   - La arquitectura respeta estrictamente:
     $$\text{orchestration} \longrightarrow \{\text{qkd}, \text{pqc}\} \longrightarrow \text{quantum} \longrightarrow \text{core}$$
   - Ni `qkd` ni `pqc` importan jamás `orchestration` ni se conocen entre sí.
   - El test arquitectónico automatizado en `tests/test_orchestration/test_architecture_boundaries.py` verifica formalmente la ausencia de importaciones indebidas recorriendo el AST de todos los ficheros del repositorio.

2. **Codificación Canónica Libre de Ambigüedad (`canonical_hybrid_secret_input`)**:
   - Orden canónico inviolable: 1. $K_{\text{QKD}}$, 2. $SS_{\text{ML-KEM}}$, 3. $SS_{\text{HQC}}$ (opcional).
   - El empaquetado big-endian de bits de QKD exige la especificación exacta de la longitud en bits (`bit_length`) y verifica activamente que los bits no utilizados del byte final sean exactamente ceros (`unused_mask`), eliminando ataques de colisión o reinterpretación por padding.
   - Cada campo cuenta con prefijo de longitud de 64 bits en big-endian (`pack(">Q", ...)`), previniendo ataques de extensión de longitud o confusión de campos contiguos.

3. **Separación Criptográfica de Claves e Inviolabilidad de Dominio**:
   - HKDF-SHA-384 se invoca con prefijos de dominio diferenciados (`QuantumSec/HybridSession/v1/SessionKey` frente a `QuantumSec/HybridSession/v1/ConfirmationKey`) y utiliza como salt el digest SHA-384 de todo el contexto público (`context_hash`).
   - El material secreto combinado es completamente independiente de las claves generadas por el handshake puro de PQC, impidiendo ataques de reutilización cruzada de claves.

4. **Retirada Inmediata y Defensiva de Material Secreto**:
   - La transferencia de secretos desde PQC hacia la composición híbrida mediante `_consume_hybrid_components()` retira y anula inmediatamente las referencias en el estado de origen KEM (`self.close()`), impidiendo reutilizaciones accidentales o doble consumo.
   - Las claves de confirmación se destruyen inmediatamente tras la verificación Finished mediante `retire_confirmation_key()`.
   - La capacidad de clave final `EstablishedKeyCapability` protege el acceso directo a los bytes, exigiendo la invocación explícita de `export()` y ofreciendo un método de cierre `close()`.

5. **Rigurosa Separación Metodológica de Métricas**:
   - Se mantiene una separación conceptual absoluta entre el tiempo de simulación del canal cuántico BB84 (`simulation_time_ns`) y el tiempo de computación criptográfica clásica en software (`crypto_software_time_ns` y `orchestration_software_wall_time_ns`). En ningún momento se suman ambos relojes para representar una falsa latencia física global, cumpliendo escrupulosamente los requisitos metodológicos del TFM.

---

## 5. Recomendaciones de Testing y Calidad

1. **Añadir pruebas unitarias de robustez ante excepciones del backend**:
   - Simular un fallo en `derive_hkdf_sha384` (inyectando `BackendOperationError` o `PQCError`) para verificar que el runner captura la excepción y no cae con error no controlado.
2. **Ampliar tests de validación defensiva en constructores**:
   - Añadir tests que intenten instanciar `HybridSecretComponent` con `position=True`, `position=-1`, `bit_length=True` y `secret=b""`, comprobando que todos son rechazados.
3. **Verificar el Gestor de Contexto en `SessionResult`**:
   - Incorporar un test unitario que verifique que `with run_session(...) as session: session.export_session_key()` funciona y que al salir del bloque `session.is_closed` es `True` y `session.export_session_key()` levanta `RuntimeError`.
4. **Validación de la corrección sintáctica en `ml_dsa.py`**:
   - Asegurar que la tupla de excepciones en `ml_dsa.py:92` se corrija para garantizar que herramientas como `flake8`, `mypy`, `pyright` y versiones de Python $\le 3.13$ acepten el código sin advertencias ni errores sintácticos.
