# Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 6: Confirmación de Claves, Mensajes Finished y Establecimiento de Sesión)

**Fecha**: 4 de Septiembre de 2026  
**Alcance**: Módulo `pqc/protocol/key_confirmation.py`, mensajes Finished (`pqc/protocol/messages.py`), actualizaciones en `key_schedule.py`, `transcript.py` y suite de pruebas `tests/test_pqc/test_key_confirmation.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha llevado a cabo una auditoría técnica e independiente de la **Fase 6 del protocolo de negociación post-cuántico (handshake PQC)** en **QuantumSec**, correspondiente a la confirmación explícita de claves mediante intercambio ordenado de mensajes Finished y la materialización final de la sesión establecida (`EstablishedPQCSession`):
- **Capa `pqc/protocol/key_confirmation.py`**:
  - Derivación de claves de confirmación (`PQCConfirmationKeyDeriver`): derivación separada por propósito mediante HKDF-SHA-384 con dominio `QuantumSec/PQCHandshake/v1/ConfirmationKey` y cierre seguro de los estados KEM intermedios.
  - Mensajes Finished encadenados y separados por rol (`PQCFinishedRole.RESPONDER` y `PQCFinishedRole.INITIATOR`): cálculo de `verify_data` mediante HMAC-SHA-384 sobre el transcript autenticado y encadenamiento del Finished de Bob en el de Alice (`previous_verify_data`).
  - Máquina de estados de confirmación (`PQCKeyConfirmation`): orden estricto (Bob envía Finished $\to$ Alice verifica y genera Finished encadenado $\to$ Bob verifica y genera prueba de confirmación mutua).
  - Materialización de sesión (`EstablishedPQCSession`): objeto seguro que posee la clave de sesión simétrica de 256 bits (`export_session_key()`), con control de ciclo de vida (`close()`, `is_closed`) y soporte para gestores de contexto `with`.
- **Capa `pqc/protocol/messages.py`**: DTO inmutable `PQCFinishedMessage`, serialización canónica con dominio `QuantumSec/PQCHandshake/v1/Finished` y serialización de transporte `to_dict()` / `from_dict()` con Base64.
- **Suite de Pruebas**: 31 tests unitarios y de integración exhaustivos cubriendo rechazo de Finished manipulados, prevención de reflexión de roles, protección contra repetición (replay) entre sesiones, aislamiento de claves de confirmación frente a claves de sesión y cierre automático de material criptográfico (`tests/test_pqc/test_key_confirmation.py`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades criptográficas ni riesgos de confusión de contexto en los cálculos de HMAC-SHA-384. |
| **HIGH** | 0 | El diseño e implementación criptográfica satisfacen con rigor los principios de seguridad de protocolos tipo TLS 1.3 / SIGMA. |
| **MEDIUM** | 1 | Asimetría en la materialización de sesión distribuida: `establish_local_session` exige un objeto `ConfirmedPQCHandshake` que solo Bob genera en su proceso local, bloqueando la instanciación de Alice en arquitecturas cliente-servidor distribuidas. |
| **LOW** | 3 | Falta de propiedad alias `session_key` en `EstablishedPQCSession`, semántica sobrecargada de `is_closed` en estados de confirmación, y ausencia de test de integración end-to-end con transporte puramente JSON. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | `MEDIUM` | `pqc/protocol/key_confirmation.py:576, 629` | Arquitectura / Distribución | `PQCKeyConfirmation.establish_local_session` requiere el token inmutable `ConfirmedPQCHandshake` que solo se produce en el lado de Bob, impidiendo a Alice materializar su sesión de forma desacoplada en procesos distribuidos. |
| **L-01** | `LOW` | `pqc/protocol/key_confirmation.py:523` (`EstablishedPQCSession`) | Ergonomía / API | `EstablishedPQCSession` solo expone `export_session_key()` y carece de la propiedad `@property session_key`. |
| **L-02** | `LOW` | `pqc/protocol/key_confirmation.py:645` | Claridad de Diseño | `establish_local_session` exige `state.is_closed == True` como precondición de éxito, reutilizando `close()` como estado de finalización en lugar de solo destrucción. |
| **L-03** | `LOW` | `tests/test_pqc/test_key_confirmation.py` | Calidad de Tests | Los tests ejecutan la confirmación compartiendo memoria in-process; falta un test end-to-end que ejecute las 6 fases serializando estrictamente a JSON/dict entre procesos desacoplados. |

---

## 3. Análisis Detallado de Hallazgos

### [M-01] Bloqueo en la materialización de sesión de Alice en procesos distribuidos

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/key_confirmation.py`
   - Métodos: `verify_responder_and_create_initiator` (líneas 576–599) y `establish_local_session` (líneas 629–676).

2. **Por qué es un problema**:
   En el flujo del protocolo de confirmación:
   - Alice llama a `PQCKeyConfirmation.verify_responder_and_create_initiator(alice_state, responder_finished)` y obtiene `initiator_finished: PQCFinishedMessage`.
   - Alice envía `initiator_finished` a Bob a través de la red (API HTTP / WebSocket).
   - Bob llama a `PQCKeyConfirmation.verify_initiator_and_confirm(bob_state, initiator_finished)` y obtiene el objeto `confirmed: ConfirmedPQCHandshake`.
   - Bob llama a `PQCKeyConfirmation.establish_local_session(confirmed, bob_state)` y obtiene su `EstablishedPQCSession`.
   
   Sin embargo, **Alice necesita materializar su propia `EstablishedPQCSession` en su máquina/proceso**:
   `establish_local_session` exige estrictamente un parámetro `confirmation: ConfirmedPQCHandshake`.
   `ConfirmedPQCHandshake` es un objeto en memoria que no puede ser instanciado por Alice (su `__post_init__` valida un token privado `_proof is _CONFIRMED_HANDSHAKE_PROOF`) ni puede ser transmitido por red (no tiene serialización `to_dict` / `from_dict`).
   En las pruebas unitarias (`test_key_confirmation.py`), Alice y Bob residen en el mismo proceso de Python y comparten la misma variable en memoria `confirmed`. Pero en un despliegue distribuido real, Alice no puede llamar a `establish_local_session` porque no tiene acceso al objeto `ConfirmedPQCHandshake` devuelto a Bob.

3. **Escenario donde falla**:
   En una arquitectura cliente-servidor distribuida:
   ```python
   # En el cliente (Alice):
   initiator_finished = PQCKeyConfirmation.verify_responder_and_create_initiator(
       alice_state,
       responder_finished_message,
   )
   # Alice envía initiator_finished al servidor por HTTP...
   # Ahora Alice necesita su sesión establecida:
   # alice_session = PQCKeyConfirmation.establish_local_session(???, alice_state)
   # ¡Alice no tiene ningún objeto ConfirmedPQCHandshake ni puede crearlo!
   ```

4. **Corrección propuesta**:
   Permitir que `verify_responder_and_create_initiator` devuelva también la confirmación para Alice, o crear un método `establish_initiator_session` que tome `(initiator_state, responder_finished)` (o generar `ConfirmedPQCHandshake` en el lado del iniciador una vez verificado el Finished del responder):
   ```python
   # Opción A: verify_responder_and_create_initiator devuelve (PQCFinishedMessage, ConfirmedPQCHandshake)
   # Opción B: establish_initiator_session(initiator_state)
   ```

---

### [L-01] Ausencia de propiedad `@property session_key` en `EstablishedPQCSession`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/key_confirmation.py`
   - Clase: `EstablishedPQCSession` (líneas 523–527).

2. **Por qué es un problema**:
   `DerivedSessionKeyState` y `EstablishedPQCSession` exponen el método `export_session_key() -> bytes`.
   Sin embargo, no ofrecen una propiedad de solo lectura `@property session_key`. En Python idiomático, los objetos que encapsulan claves suelen ofrecer tanto la propiedad de lectura como el método explícito de exportación.

3. **Escenario donde falla**:
   Consumidores en `ui/backend` o adaptadores de cifrado simétrico que acceden a `session.session_key` esperando una propiedad estándar.

4. **Corrección propuesta**:
   Añadir `@property def session_key(self) -> bytes: return self.export_session_key()` en `EstablishedPQCSession`.

---

### [L-02] Semántica sobrecargada de `is_closed` en estados de confirmación

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/key_confirmation.py`
   - Clase: `PQCConfirmationKeyState` y método `establish_local_session` (línea 645).

2. **Por qué es un problema**:
   En `PQCConfirmationKeyState`, invocar `close()` libera la clave de confirmación `_confirmation_key = None`.
   En `establish_local_session`:
   ```python
   if not state.is_closed or state._local_finished is None or state._peer_finished is None:
       raise RuntimeError("Local Finished exchange is incomplete.")
   ```
   La condición `not state.is_closed` (exigiendo que esté cerrado) resulta contraintuitiva, ya que en el resto del repositorio `is_closed == True` denota un objeto invalidado o destruido. Aquí se utiliza como indicador de que la clave de confirmación fue liberada con éxito tras la verificación.

3. **Escenario donde falla**:
   Confusión en el mantenimiento del código o interpretación de trazas de depuración donde un estado reporta `closed=True` antes de que la sesión se declare establecida.

4. **Corrección propuesta**:
   Renombrar o documentar explícitamente mediante una propiedad dedicada (ej. `@property def confirmation_key_retired(self) -> bool`) que la clave de confirmación es liberada preventivamente para proteger la sesión simétrica.

---

### [L-03] Ausencia de prueba de integración de transporte puro en las 6 fases

1. **Archivo y función afectada**:
   - Archivo: `tests/test_pqc/test_key_confirmation.py`.

2. **Por qué es un problema**:
   Las pruebas actuales verifican exhaustivamente la lógica criptográfica pasando objetos Python directamente entre Alice y Bob.
   No existe un test de integración que ejecute las 6 fases completas convirtiendo **cada mensaje** a JSON con `to_dict()` y restaurándolo con `from_dict()`, validando la interoperabilidad total a través de la capa de transporte.

3. **Escenario donde falla**:
   Discrepancias sutiles en los nombres de campos de serialización Base64 entre fases que no se manifiesten en llamadas directas en memoria.

4. **Corrección propuesta**:
   Añadir un test `test_full_handshake_pure_json_transport` en `test_key_confirmation.py` que serialice a JSON cada mensaje (`ServerKeyOffer`, `SignedClientKeyExchange`, `PQCFinishedMessage`).

---

## 4. Evaluación de Invariantes y Principios de Diseño Criptográfico

1. **Separación de Dominios e Independencia de Claves (Key Separation)**:
   - **Cumplimiento**: **Sobresaliente**.
   - `PQCConfirmationKeyDeriver` deriva `confirmation_key` con dominio `QuantumSec/PQCHandshake/v1/ConfirmationKey`, completamente disjunto de `QuantumSec/PQCHandshake/v1/SessionKey`.
   - Las pruebas (`test_confirmation_material_matches_and_is_separate_from_session_key`) demuestran que la clave de confirmación es completamente independiente y matemáticamente distinta de la clave de sesión de 256 bits.

2. **Encadenamiento y Prevención de Reflexión de Finished (Role Separation & Chaining)**:
   - **Cumplimiento**: **Sobresaliente**.
   - El mensaje Finished de Bob (`PQCFinishedRole.RESPONDER`) utiliza `previous_verify_data = b""`.
   - El mensaje Finished de Alice (`PQCFinishedRole.INITIATOR`) encadena obligatoriamente el `verify_data` de Bob (`previous_verify_data = responder_finished.verify_data`).
   - Los dominios HMAC incluyen explícitamente el rol (`b"responder"` vs `b"initiator"`), impidiendo cualquier ataque de reflexión o reordenamiento de vuelos.

3. **Ciclo de Vida y Zeroización Oportuna de Material Intermedio**:
   - **Cumplimiento**: **Excelente**.
   - Al derivar las claves de confirmación en la Fase 6, los estados KEM fuente (`InitiatorKEMState`, `ResponderSharedSecretState`) son cerrados inmediatamente (`secret_state.close()`), eliminando referencias a los secretos KEM en memoria.
   - Al verificar los Finished, las claves de confirmación son igualmente liberadas, dejando únicamente la clave simétrica de 256 bits en `EstablishedPQCSession`.

---

## 5. Conclusiones y Recomendaciones de Priorización

La Fase 6 culmina con éxito el diseño y la implementación del protocolo de negociación post-cuántico (handshake PQC) en **QuantumSec**. Con las 6 fases completadas, QuantumSec dispone de un protocolo criptográfico completo con autenticación mutua (ML-DSA-65), encapsulamiento KEM (ML-KEM-768 y HQC-3), derivación de clave de sesión con transcript binding (HKDF-SHA-384) y confirmación de clave mutua (HMAC-SHA-384).

Se recomienda priorizar:
1. **Prioridad 1 (Desacoplamiento para Entornos Distribuidos)**:
   - Ajustar el flujo de `PQCKeyConfirmation` para que el cliente (Alice) pueda generar su `ConfirmedPQCHandshake` / materializar su `EstablishedPQCSession` de forma autónoma sin depender de un objeto en memoria devuelto en el proceso del servidor (**M-01**).
2. **Prioridad 2 (Comodidad de API y Pruebas)**:
   - Añadir la propiedad `@property session_key` en `EstablishedPQCSession` (**L-01**).
   - Incorporar un test de integración de extremo a extremo que ejecute las 6 fases a través de serialización pura JSON/Base64 (**L-03**).
