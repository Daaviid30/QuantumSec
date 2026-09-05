# Informe de Revisión de Código Independiente: Módulo `pqc` (Intercambio de Clave del Cliente y Desencapsulamiento en el Servidor)

> **Historical review snapshot.** Findings are dated and may have been resolved by later phases.
> Use code/tests, README.md, docs/structure.md, and TFM_GOAL.md for current status.

**Fecha**: 3 de Septiembre de 2026  
**Alcance**: Módulo `pqc/protocol/client_exchange.py`, `pqc/protocol/messages.py` (`ClientKeyExchange`, `SignedClientKeyExchange`), métodos de desencapsulamiento en `pqc/protocol/server_offer.py`, y suite de pruebas `tests/test_pqc/test_client_exchange.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha llevado a cabo una auditoría técnica e independiente de la cuarta fase del protocolo de negociación post-cuántico (handshake PQC) en **QuantumSec**, correspondiente al empaquetado y firma de la respuesta del cliente (Alice), y la subsiguiente verificación y desencapsulamiento seguro en el lado del servidor (Bob):
- **Capa `pqc/protocol/client_exchange.py`**:
  - Fábrica de intercambio (`ClientKeyExchangeFactory`): vinculación criptográfica a la oferta de Bob mediante hash SHA-384 del mensaje canónico previo (`server_offer_hash`) y firma digital ML-DSA-65 de Alice sin re-encapsulamiento redundante.
  - Procesador del servidor (`ClientKeyExchangeProcessor`): verificación previa exhaustiva (estado no cerrado, concordancia de sesión, concordancia de perfil, vinculación del hash de la oferta, correspondencia de algoritmos, procedencia del firmante en el almacén de confianza y validación de firma ML-DSA) antes de invocar la desencapsulación KEM.
  - Estado de secretos compartidos del servidor (`ResponderSharedSecretState`): almacenamiento hermético de secretos derivados con método de cierre/liberación idempotente (`close()`).
- **Capa `pqc/protocol/messages.py`**: Nuevas estructuras de mensajes inmutables (`ClientKeyExchange`, `SignedClientKeyExchange`), serialización canónica con separación de dominio (`QuantumSec/PQCHandshake/v1/ClientKeyExchange`) y mapeos de transporte Base64 (`to_dict` / `from_dict`).
- **Capa `pqc/protocol/server_offer.py`**: Métodos específicos `decapsulate_ml_kem()` y `decapsulate_hqc()` en `ResponderKEMState`, garantizando la invalidación de claves tras el éxito del handshake.
- **Suite de Pruebas**: Tests unitarios y de integración con backend real para verificar la correspondencia exacta de secretos compartidos, rechazo de firmantes no confiables, detección de firmas manipuladas, protección contra repetición (replay) y control de fugas de secretos (`tests/test_pqc/test_client_exchange.py`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades críticas ni fallos de seguridad en la verificación previa, vinculación del transcript (SHA-384) ni en la recuperación de secretos KEM. |
| **HIGH** | 0 | La arquitectura resuelve de forma impecable las observaciones de revisiones previas (métodos de desencapsulación, deserializadores de transporte y cierre de claves). |
| **MEDIUM** | 1 | Ausencia de `client_nonce` en `ClientKeyExchange` para inyección de entropía fresca bilateral en la futura fase de KDF. |
| **LOW** | 3 | Falta de soporte para gestores de contexto (`__enter__`/`__exit__`) en las clases de estado efímero, duplicación estructural entre `ResponderSharedSecretState` e `InitiatorKEMState`, y casos límite de estado de desencapsulación no cubiertos en pruebas. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | `MEDIUM` | `pqc/protocol/messages.py:398` (`ClientKeyExchange`) | Criptografía / Protocolo | `ClientKeyExchange` no incluye un `client_nonce` generado por Alice, dependiendo exclusivamente de la aleatoriedad del servidor para la entropía del transcript en la KDF. |
| **L-01** | `LOW` | `pqc/protocol/client_exchange.py:40`, `initiator.py:35`, `server_offer.py:19` | Ergonomía / Python | Las clases de estado efímero implementan `.close()` pero no implementan el protocolo de gestor de contexto (`__enter__` / `__exit__`). |
| **L-02** | `LOW` | `pqc/protocol/client_exchange.py:40` vs `initiator.py:35` | Mantenibilidad / DRY | `ResponderSharedSecretState` e `InitiatorKEMState` son estructuralmente idénticas en atributos, validaciones y métodos, duplicando código. |
| **L-03** | `LOW` | `tests/test_pqc/test_client_exchange.py` | Calidad de Tests | Faltan tests para llamadas a `decapsulate_hqc` en sesiones de perfil LOW y longitudes corruptas de `server_offer_hash` en `from_dict`. |

---

## 3. Análisis Detallado de Hallazgos

### [M-01] Ausencia de `client_nonce` en `ClientKeyExchange` para entropía bilateral en la KDF

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/messages.py`
   - Clases: `ClientKeyExchange` (líneas 398–536) y `SignedClientKeyExchange` (líneas 538–598).

2. **Por qué es un problema**:
   En un protocolo de negociación con autenticación mutua y derivación de claves (como TLS 1.3 o KEM-TLS):
   - El servidor envía `session_id`, `server_nonce`, su clave pública KEM y su firma digital.
   - El cliente envía `session_id`, `server_offer_hash`, los textos cifrados KEM y su firma digital.
   Actualmente, `ClientKeyExchange` vincula la oferta mediante `server_offer_hash` (SHA-384), pero no introduce un `client_nonce` explícito generado por Alice.
   Aunque la encapsulación KEM utiliza aleatoriedad interna del CSPRNG para el texto cifrado, la ausencia de un nonce explícito del cliente significa que el transcript del protocolo y los parámetros de contexto para la futura KDF dependen únicamente del `nonce` generado por el responder (Bob). Si el generador de números aleatorios del servidor estuviese sesgado o comprometido, la falta de entropía inyectada por Alice debilita la frescura explícita del intercambio.

3. **Escenario donde falla**:
   Al diseñar la función de derivación de claves (KDF/HKDF) en la Fase 5: la KDF habitualmente mezcla `server_nonce || client_nonce` en el contexto del key schedule para garantizar unicidad y protección contra repeticiones en ambos sentidos.

4. **Corrección propuesta**:
   Añadir un campo opcional o estándar `client_nonce: bytes = field(repr=False)` (de 32 bytes) a `ClientKeyExchange`, incorporándolo en `canonical_bytes()`, `to_dict()`, `from_dict()` y en la validación `__post_init__`.

---

### [L-01] Ausencia de soporte para el protocolo de Context Manager (`with`) en estados efímeros

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/client_exchange.py` (`ResponderSharedSecretState`, líneas 40–102), `pqc/protocol/initiator.py` (`InitiatorKEMState`, líneas 35–96), `pqc/protocol/server_offer.py` (`ResponderKEMState`, líneas 19–106).

2. **Por qué es un problema**:
   Todas estas clases implementan un método `.close()` y una propiedad `.is_closed` para liberar las referencias a claves privadas o secretos compartidos. No obstante, ninguna implementa los métodos mágicos estándar de Python `__enter__` y `__exit__`.
   El uso del gestor de contexto (`with state: ...`) es el patrón estándar en Python para asegurar la liberación garantizada de recursos o material sensible de memoria incluso en presencia de excepciones no controladas.

3. **Escenario donde falla**:
   Si un consumidor intenta gestionar el ciclo de vida de forma idiomática:
   ```python
   with responder_state:
       # procesamiento
   # AttributeError: __enter__
   ```

4. **Corrección propuesta**:
   Implementar `__enter__(self) -> Self: return self` y `__exit__(self, exc_type, exc_val, exc_tb) -> None: self.close()` en las tres clases de estado.

---

### [L-02] Duplicación estructural entre `ResponderSharedSecretState` e `InitiatorKEMState`

1. **Archivo y función afectada**:
   - Archivos: `pqc/protocol/client_exchange.py` (líneas 40–102) e `pqc/protocol/initiator.py` (líneas 35–96).

2. **Por qué es un problema**:
   `ResponderSharedSecretState` e `InitiatorKEMState` poseen atributos idénticos (`session_id`, `profile`, `_ml_kem_shared_secret`, `_hqc_shared_secret`, `_closed`), validaciones idénticas en `__post_init__`, y métodos `.close()` e `.is_closed` con exactamente la misma semántica.
   Mantener dos definiciones idénticas en archivos separados duplica el mantenimiento y aumenta el riesgo de divergencias no intencionadas en futuras extensiones (por ejemplo, al añadir la API de exportación para KDF).

3. **Escenario donde falla**:
   Cualquier refactorización en el formato de los secretos compartidos o en la integración con la KDF requerirá duplicar los cambios y sus pruebas en ambos submódulos.

4. **Corrección propuesta**:
   Extraer una clase base común en `pqc/protocol/` (ej. `_KEMSharedSecretStateBase` o `KEMSharedSecretState`) de la cual hereden o sean alias `InitiatorKEMState` y `ResponderSharedSecretState`, o unificarlas formalmente bajo `KEMSharedSecretState`.

---

### [L-03] Casos límite de decapsulación y deserialización no cubiertos en pruebas

1. **Archivo y función afectada**:
   - Archivo: `tests/test_pqc/test_client_exchange.py`.

2. **Por qué es un problema**:
   La suite de pruebas actual es muy completa (19 tests exhaustivos), pero carece de pruebas unitarias específicas para:
   1. Invocar `responder_state.decapsulate_hqc(...)` en una sesión con perfil `LOW` (comprobando que lanza `RuntimeError` por ausencia de instancia HQC).
   2. Deserializar con `ClientKeyExchange.from_dict(...)` un payload cuyo `server_offer_hash` codificado en Base64 tenga una longitud incorrecta (distinta de 48 bytes).

3. **Escenario donde falla**:
   Regresiones no detectadas en los controles de consistencia interna de `ResponderKEMState` o en el validador de `ClientKeyExchange`.

4. **Corrección propuesta**:
   Añadir tests en `test_client_exchange.py` que ejerciten estas dos ramas de error.

---

## 4. Evaluación de Invariantes y Principios de Diseño

1. **Vinculación Criptográfica del Transcript (Transcript Binding)**:
   - **Cumplimiento**: **Excelente**.
   - `ClientKeyExchangeFactory` calcula `server_offer_hash = sha384(offer.canonical_bytes()).digest()`, atando criptográficamente la respuesta de Alice a la oferta exacta de Bob.
   - `ClientKeyExchangeProcessor` comprueba este hash en tiempo constante mediante `hmac.compare_digest` antes de cualquier operación KEM, previniendo ataques de sustitución de oferta (*offer substitution*) y confusión de sesiones (*cross-session binding attacks*).

2. **Orden Estricto de Seguridad (Verify-then-Decapsulate)**:
   - **Cumplimiento**: **Excelente**.
   - `ClientKeyExchangeProcessor.process` ejecuta 11 validaciones secuenciales de seguridad (perfil, sesión, correspondencia de oferta, hash del transcript, algoritmo de firma, búsqueda en el almacén de confianza y verificación de firma digital ML-DSA-65) **antes** de invocar `decapsulate_ml_kem()` o `decapsulate_hqc()`.
   - Las pruebas unitarias confirman mediante espías que ninguna función de desencapsulación es invocada si falla cualquiera de estas etapas.

3. **Gestión Idempotente y Cierre de Claves Efímeras**:
   - **Cumplimiento**: **Excelente**.
   - Tras el éxito de todas las desencapsulaciones requeridas, `responder_state.close()` libera inmediatamente las referencias a las instancias privadas de KEM (`_ml_kem = None`, `_hqc = None`), impidiendo la reutilización de claves en ataques de repetición (*replay*).

4. **Separación de Separadores de Dominio y Serialización Canónica**:
   - **Cumplimiento**: **Excelente**.
   - `CLIENT_KEY_EXCHANGE_DOMAIN_SEPARATOR` (`QuantumSec/PQCHandshake/v1/ClientKeyExchange`) es completamente independiente de `SERVER_KEY_OFFER_DOMAIN_SEPARATOR`, garantizando la imposibilidad de reutilizar firmas de ofertas como respuestas de intercambio (*cross-protocol signature collision*).

---

## 5. Conclusiones y Recomendaciones de Priorización

La implementación de la Fase 4 del protocolo KEM en `client_exchange.py`, `messages.py` y `server_offer.py` alcanza un nivel sobresaliente de madurez, seguridad criptográfica y diseño defensivo. Resuelve íntegramente las necesidades de autenticación mutua, vinculación canónica y recuperación segura de secretos compartidos entre Alice y Bob.

Se recomienda priorizar las siguientes acciones:
1. **Prioridad 1 (Preparación para la KDF)**:
   - Evaluar la inclusión de un `client_nonce` en `ClientKeyExchange` para asegurar aleatoriedad bilateral en el key schedule de la Fase 5 (**M-01**).
2. **Prioridad 2 (Refactorización y DRY)**:
   - Unificar o extraer una clase base común para `InitiatorKEMState` y `ResponderSharedSecretState` (**L-02**).
   - Añadir soporte para gestores de contexto `with` en las clases de estado efímero (**L-01**).
3. **Prioridad 3 (Cobertura de Pruebas)**:
   - Añadir pruebas para invocaciones erróneas de `decapsulate_hqc` en perfil LOW y validación de longitud de hash en `from_dict` (**L-03**).
