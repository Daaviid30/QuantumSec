# Informe de Revisión de Código Independiente: Módulo `pqc` (Autenticación del Iniciador y Encapsulamiento KEM)

> **Historical review snapshot.** Findings are dated and may have been resolved by later phases.
> Use code/tests, README.md, docs/structure.md, and TFM_GOAL.md for current status.

**Fecha**: 3 de Septiembre de 2026  
**Alcance**: Módulo `pqc/protocol/initiator.py`, integración con `pqc/protocol/messages.py`, `server_offer.py`, `party.py` y suite de pruebas `tests/test_pqc/test_initiator.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría técnica e independiente del nuevo componente del protocolo de handshake post-cuántico en **QuantumSec**: el procesamiento y autenticación en el lado del iniciador (Alice) de las ofertas de servidor y la posterior generación de respuestas de encapsulamiento KEM (`pqc/protocol/initiator.py`).

El análisis cubrió:
- **Flujo de Autenticación Previa**: Validación de la oferta firmada (`SignedServerKeyOffer`), verificación de que el firmante (Bob) esté pre-aprovisionado en el almacén de confianza (`TrustedIdentityStore`), comprobación de coherencia con el perfil (`LOW`/`HIGH`) y verificación de la firma digital ML-DSA-65 antes de cualquier operación KEM.
- **Encapsulamiento Condicionado**: Ejecución de la encapsulación **ML-KEM-768** (y opcionalmente **HQC-3**) únicamente tras verificar con éxito la autenticidad del responder.
- **Separación de Estados**: Aislamiento estricto entre el estado privado de secretos del iniciador (`InitiatorKEMState`) y la respuesta pública de texto cifrado (`EncapsulationResponse`).
- **Manejo de Estados de Retorno**: Objeto estructurado `ProcessedServerOffer` y enumeración `ServerOfferProcessingStatus`.
- **Suite de Pruebas**: Tests unitarios con mocks de espionaje para verificar que nunca se encapsula si la autenticación falla (`tests/test_pqc/test_initiator.py`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades críticas ni fugas de secretos compartidos en el flujo de encapsulación. |
| **HIGH** | 2 | Ausencia de métodos de serialización de transporte en `EncapsulationResponse` y ubicación desalineada de mensajes públicos en `initiator.py`. |
| **MEDIUM** | 2 | Asimetría de ciclo de vida (falta de método `close()` en `InitiatorKEMState`) y falta de API pública/método de derivación para consumir los secretos compartidos en futuras fases. |
| **LOW** | 2 | Duplicación del helper `_require_exact_bytes` frente a `messages.py` y asunción posicional en la validación del algoritmo ML-KEM. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `HIGH` | `pqc/protocol/initiator.py:86` (`EncapsulationResponse`) | Interfaces / Transporte | `EncapsulationResponse` carece de métodos `to_dict()` y `from_dict()`, impidiendo su serialización estándar para viajar por la red hacia Bob. |
| **H-02** | `HIGH` | `pqc/protocol/initiator.py:86` vs `messages.py` | Arquitectura / Diseño | `EncapsulationResponse` está definida en `initiator.py` en vez de `pqc/protocol/messages.py` junto con los demás mensajes de protocolo. |
| **M-01** | `MEDIUM` | `pqc/protocol/initiator.py:43` (`InitiatorKEMState`) | Seguridad / Ciclo de Vida | `InitiatorKEMState` carece de método de cierre/limpieza (`close()`, `is_closed`) a diferencia de `ResponderKEMState`. |
| **M-02** | `MEDIUM` | `pqc/protocol/initiator.py:43` (`InitiatorKEMState`) | Diseño / Extensibilidad | Los secretos compartidos están en atributos privados sin getter ni método de derivación de claves para la fase de KDF. |
| **L-01** | `LOW` | `pqc/protocol/initiator.py:25` (`_require_exact_bytes`) | Mantenibilidad / DRY | Duplicación de la lógica de validación de bytes ya existente en `pqc/protocol/messages.py:26` (`_require_bytes`). |
| **L-02** | `LOW` | `pqc/protocol/initiator.py:251` (`_offer_algorithms_match_profile`) | Robustez | Comprobación posicional rígida `definition.kem_algorithms[0]` en lugar de verificación de conjunto. |

---

## 3. Análisis Detallado de Hallazgos

### [H-01] Ausencia de métodos de serialización y transporte (`to_dict` / `from_dict`) en `EncapsulationResponse`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py`
   - Clase: `EncapsulationResponse` (líneas 86–140).

2. **Por qué es un problema**:
   `EncapsulationResponse` representa el mensaje público que Alice debe transmitir de vuelta a Bob a través de la red (o mediante la API HTTP de `ui/backend`) conteniendo los textos cifrados ML-KEM y HQC.
   Mientras que `ServerKeyOffer` y `SignedServerKeyOffer` cuentan con métodos estandarizados `to_dict()` y `from_dict()` con codificación Base64 en `pqc/protocol/messages.py`, `EncapsulationResponse` no dispone de ningún método de serialización ni deserialización.
   Cualquier capa de transporte o endpoint REST que necesite transmitir o recibir esta respuesta debe reimplementar manualmente el empaquetado, desempaquetado y validación de Base64 para los campos `session_id`, `ml_kem_ciphertext` y `hqc_ciphertext`.

3. **Escenario donde falla**:
   Al integrar el handshake en la API de FastAPI (`ui/backend`) o serializar la respuesta de Alice en formato JSON para enviarla a Bob a través de un socket:
   ```python
   response = processed_offer.public_encapsulation
   # response.to_dict() -> AttributeError: 'EncapsulationResponse' object has no attribute 'to_dict'
   ```

4. **Corrección propuesta**:
   Implementar `to_dict()` y `from_dict(cls, payload: Mapping[str, object]) -> Self` en `EncapsulationResponse`, codificando los campos binarios en Base64 de forma idéntica a `ServerKeyOffer`.

---

### [H-02] Ubicación desalineada de `EncapsulationResponse` fuera de `pqc/protocol/messages.py`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py` (líneas 86–140) y `pqc/protocol/messages.py`.

2. **Por qué es un problema**:
   `pqc/protocol/messages.py` está definido como el módulo de especificación de los mensajes públicos inmutables del protocolo de negociación.
   `ServerKeyOffer` y `SignedServerKeyOffer` residen en `messages.py`. Sin embargo, `EncapsulationResponse` (que es el mensaje de retorno simétrico) fue ubicada dentro de `initiator.py`.
   Esta dispersión rompe el principio de responsabilidad única y genera acoplamiento: un servidor (Bob) que deba deserializar y tipar la respuesta entrante de Alice debe importar `EncapsulationResponse` desde `pqc.protocol.initiator`, un módulo concebido exclusivamente para la lógica de procesamiento del cliente.

3. **Escenario donde falla**:
   En la fase de recepción del servidor (Bob), el módulo del servidor debe depender de submódulos del iniciador:
   ```python
   # En el módulo de responder/servidor:
   from pqc.protocol.initiator import EncapsulationResponse  # Acoplamiento conceptual inverso
   ```

4. **Corrección propuesta**:
   Mover la definición de `EncapsulationResponse` a `pqc/protocol/messages.py` (junto con `ServerKeyOffer` y `SignedServerKeyOffer`) y reexportarla desde `pqc/protocol/__init__.py`.

---

### [M-01] Asimetría de ciclo de vida: falta de liberación de secretos en `InitiatorKEMState`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py`
   - Clase: `InitiatorKEMState` (líneas 43–83).

2. **Por qué es un problema**:
   En `pqc/protocol/server_offer.py`, `ResponderKEMState` implementa un método `close()` y una propiedad `is_closed` que anula las referencias a las instancias KEM privadas una vez completada la sesión o en caso de aborto, mitigando la retención innecesaria de material secreto en memoria.
   En cambio, `InitiatorKEMState` es una `@dataclass(frozen=True)` que retiene permanentemente `_ml_kem_shared_secret` y `_hqc_shared_secret` como buffers inmutables sin ninguna capacidad de invalidación, cierre o limpieza explícita (`close()`).

3. **Escenario donde falla**:
   Sesiones de handshake abortadas o completadas donde las instancias de `InitiatorKEMState` permanecen en cachés de sesión o memorias de experimentos sin posibilidad de ser invalidadas explícitamente.

4. **Corrección propuesta**:
   Convertir `InitiatorKEMState` a una clase con gestión de estado de cierre (o añadir método `close()` / soporte para gestor de contexto `with`) análogo a `ResponderKEMState`.

---

### [M-02] Encapsulamiento hermético sin API para el consumo de secretos en `InitiatorKEMState`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py`
   - Clase: `InitiatorKEMState` (líneas 43–83).

2. **Por qué es un problema**:
   Los secretos derivados de la encapsulación (`_ml_kem_shared_secret` y `_hqc_shared_secret`) están almacenados exclusivamente en atributos privados (con prefijo de subrayado `_`).
   `InitiatorKEMState` no expone ninguna propiedad de lectura protegida (como una tupla de bytes `shared_secrets`), ni un método de exportación para KDF (como `export_secrets()` o `derive_key(...)`).
   Para que una fase posterior de derivación de claves (KDF / HKDF / combinación con QKD) pueda utilizar estos secretos, actualmente tendría que violar el encapsulamiento accediendo directamente a `state._ml_kem_shared_secret`.

3. **Escenario donde falla**:
   Al implementar la siguiente fase de combinación de secretos o KDF:
   ```python
   state = processed_offer.initiator_state
   # Para pasar los secretos a la KDF:
   kdf_input = state._ml_kem_shared_secret  # Acceso forzado a atributo privado
   ```

4. **Corrección propuesta**:
   Proveer un método explícito (ej. `shared_secrets` como propiedad que devuelva una tupla de `bytes` o un método `export_shared_secrets()`) documentando su uso exclusivo para el motor de derivación de claves.

---

### [L-01] Duplicación del helper de validación `_require_exact_bytes`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py`
   - Función: `_require_exact_bytes` (líneas 25–30).

2. **Por qué es un problema**:
   `pqc/protocol/messages.py` ya define `_require_bytes(value, *, name, length=None)` (línea 26), que valida tipo `bytes`, longitud exacta y no-vacío.
   En `initiator.py` se reescribió una función privada idéntica bajo el nombre `_require_exact_bytes`.

3. **Escenario donde falla**:
   Mantenimiento redundante de helpers de validación de bajo nivel en submódulos del mismo paquete.

4. **Corrección propuesta**:
   Importar y reutilizar `_require_bytes` desde `pqc.protocol.messages` en `initiator.py`.

---

### [L-02] Asunción posicional en `_offer_algorithms_match_profile`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/initiator.py`
   - Función: `ServerKeyOfferProcessor._offer_algorithms_match_profile` (línea 253).

2. **Por qué es un problema**:
   La línea 253 realiza:
   ```python
   if offer.ml_kem_algorithm != definition.kem_algorithms[0]:
       return False
   ```
   Asume de manera rígida que el algoritmo ML-KEM siempre ocupa el índice `0` de la tupla `kem_algorithms`. Si en el futuro se parametriza o reordena la definición de perfiles, esta asunción posicional podría causar falsos rechazos.

3. **Escenario donde falla**:
   Modificaciones en la definición de perfiles donde el orden de los algoritmos KEM no sitúe ML-KEM en el primer índice.

4. **Corrección propuesta**:
   Comparar explícitamente mediante pertenencia o atributos semánticos de la definición del perfil.

---

## 4. Evaluación de Invariantes y Principios de Diseño

1. **Seguridad Criptográfica y Orden de Operaciones (Authenticate-then-Encapsulate)**:
   - **Cumplimiento**: **Excelente**.
   - `ServerKeyOfferProcessor.process` verifica estrictamente la firma digital de Bob y su pertenencia al almacén de confianza antes de invocar cualquier método de encapsulación KEM.
   - Las pruebas unitarias confirman mediante espías (`patch.object(MLKEM768, "encapsulate")`) que si el firmante no es de confianza o la firma está manipulada, **no se ejecuta ninguna operación de encapsulamiento**, previniendo ataques de sondeo o consumo innecesario de entropía.

2. **Separación Estricta de Secretos y Textos Cifrados**:
   - **Cumplimiento**: **Excelente**.
   - `EncapsulationResponse` contiene únicamente los textos cifrados públicos (`ml_kem_ciphertext`, `hqc_ciphertext`) y el `session_id`.
   - Los secretos compartidos residen exclusivamente en `InitiatorKEMState` y están protegidos con `repr=False`, evitando fugas accidentales en logs.

3. **Inmutabilidad y Robustez de Tipos**:
   - **Cumplimiento**: **Muy Bueno**.
   - `ProcessedServerOffer`, `InitiatorKEMState` y `EncapsulationResponse` utilizan `@dataclass(frozen=True, slots=True)` con validaciones rigurosas en `__post_init__` sobre tamaños de clave y coherencia de perfiles.

---

## 5. Conclusiones y Recomendaciones de Priorización

La implementación del lado del iniciador (Alice) en `initiator.py` es sólida, elegante y respeta fielmente el principio criptográfico de autenticación previa antes del encapsulamiento KEM.

Se sugiere abordar las mejoras en el siguiente orden de prioridad:
1. **Prioridad 1 (Arquitectura de Mensajería y Transporte)**:
   - Trasladar `EncapsulationResponse` a `pqc/protocol/messages.py` (**H-02**).
   - Implementar `to_dict()` y `from_dict()` en `EncapsulationResponse` (**H-01**).
2. **Prioridad 2 (Gestión de Ciclo de Vida y Extensibilidad)**:
   - Dotar a `InitiatorKEMState` de un método de cierre/invalidación de secretos (`close()`) (**M-01**).
   - Exponer un método formal para el consumo controlado de secretos compartidos hacia la KDF (**M-02**).
3. **Prioridad 3 (Limpieza y DRY)**:
   - Unificar `_require_exact_bytes` con `_require_bytes` de `messages.py` (**L-01**).
   - Flexibilizar la verificación de algoritmos en `_offer_algorithms_match_profile` (**L-02**).
