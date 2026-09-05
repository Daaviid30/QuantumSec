# Informe de Revisión de Código Independiente: Módulo `pqc` (KEM y Handshake PQC)

> **Historical review snapshot.** Findings are dated and may have been resolved by later phases.
> Use code/tests, README.md, docs/structure.md, and TFM_GOAL.md for current status.

**Fecha**: 2 de Septiembre de 2026  
**Alcance**: Módulo `pqc/kem/` (`base.py`, `_oqs_provider.py`, `ml_kem.py`, `hqc.py`), `pqc/backends/oqs_kem_backend.py`, `pqc/profiles.py`, mensajes de protocolo (`pqc/protocol/messages.py`, `server_offer.py`) y suite de pruebas (`tests/test_pqc/test_kem/`, `test_profiles.py`, `test_server_offer.py`).  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha llevado a cabo una auditoría técnica e independiente de la extensión de **Mecanismos de Encapsulamiento de Claves (KEM)** y la mensajería del protocolo de negociación (handshake) post-cuántico en **QuantumSec**:
- **Capa `pqc/backends/oqs_kem_backend.py`**: Adaptador para las primitivas KEM de `liboqs-python`, gestión de ciclo de vida con gestores de contexto, caché de algoritmos habilitados y extracción de metadatos C.
- **Capa `pqc/kem/`**: Contratos abstractos (`base.py`), capa base compartida (`_oqs_provider.py`), e implementaciones concretas de **ML-KEM-768** (FIPS 203) (`ml_kem.py`) y **HQC-3** (algoritmo basado en códigos) (`hqc.py`).
- **Capa `pqc/profiles.py`**: Perfiles centrales de despliegue (`LOW` con ML-KEM-768 y `HIGH` combinando ML-KEM-768 + HQC-3).
- **Capa `pqc/protocol/`**: Mensajes serializables canónicos y autenticados (`ServerKeyOffer`, `SignedServerKeyOffer` en `messages.py`) y fábrica de ofertas de clave de servidor (`ServerKeyOfferFactory`, `ResponderKEMState` en `server_offer.py`).
- **Suite de Pruebas**: Tests unitarios y de integración con backend real para proveedores KEM, perfiles y ofertas autenticadas.

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades críticas ni fallos de seguridad en la encapsulación/desencapsulación o en el framing canónico de los mensajes. |
| **HIGH** | 1 | `ResponderKEMState` retiene claves privadas pero carece de método público `decapsulate()`, bloqueando la culminación del handshake en el lado del servidor. |
| **MEDIUM** | 1 | Serialización asimétrica: `ServerKeyOffer` cuenta con serialización canónica para firma, pero carece de deserializadores/parsers para transporte o red. |
| **LOW** | 4 | Falta de método explícito de limpieza/destrucción de claves efímeras en `ResponderKEMState`, metadatos de estandarización en prosa para HQC-3, tests límite de decapsulación alterada (IND-CCA2) ausentes, y re-exportación incompleta en `pqc/__init__.py`. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `HIGH` | `pqc/protocol/server_offer.py:18` (`ResponderKEMState`) | Diseño / Ciclo de Vida | `ResponderKEMState` retiene los objetos KEM privados pero no expone método `decapsulate()`, impidiendo derivar el secreto compartido al recibir la respuesta del cliente. |
| **M-01** | `MEDIUM` | `pqc/protocol/messages.py:40` (`ServerKeyOffer`) | Interfaces / Transporte | `ServerKeyOffer` y `SignedServerKeyOffer` carecen de métodos de deserialización (`from_dict`, `from_bytes`), dificultando su recepción desde la red o API HTTP. |
| **L-01** | `LOW` | `pqc/protocol/server_offer.py:18` | Seguridad / Memoria | Ausencia de método explícito de destrucción (`wipe`/`close`) de claves efímeras en `ResponderKEMState`. |
| **L-02** | `LOW` | `pqc/kem/hqc.py:27` (`hqc_3_metadata`) | Metadatos | Cadena de estandarización en lenguaje natural largo en lugar de identificador conciso. |
| **L-03** | `LOW` | `tests/test_pqc/test_kem/test_providers.py` | Calidad de Tests | Ausencia de tests para verificar el comportamiento de rechazo implícito (IND-CCA2) ante texto cifrado manipulado. |
| **L-04** | `LOW` | `pqc/__init__.py` | API Pública | `pqc/__init__.py` no reexporta las clases públicas de KEM (`MLKEM768`, `HQC3`, `KEMProvider`) ni los mensajes de oferta. |

---

## 3. Análisis Detallado de Hallazgos

### [H-01] `ResponderKEMState` retiene claves privadas pero carece de método `decapsulate()`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/server_offer.py`
   - Clase: `ResponderKEMState` (líneas 18–60).

2. **Por qué es un problema**:
   En el protocolo KEM de dos pasos (servidor/responder genera oferta con claves públicas efímeras $\to$ cliente/iniciador encapsula y devuelve texto cifrado $\to$ servidor desencapsula):
   `ServerKeyOfferFactory.create()` produce un objeto `ResponderKEMState` que almacena internamente las instancias privadas de KEM (`_ml_kem: MLKEM768` y opcionalmente `_hqc: HQC3`).
   Sin embargo, `ResponderKEMState` solo expone las propiedades públicas `ml_kem_public_key` y `hqc_public_key`, y **no tiene ningún método `decapsulate()`**.
   Dado que `_ml_kem` y `_hqc` son atributos privados, cuando el servidor recibe la respuesta del cliente con el texto cifrado, el código de capa superior no puede desencapsular el secreto compartido sin violar el encapsulamiento accediendo a atributos privados (`state._ml_kem.decapsulate(...)`).

3. **Escenario donde falla**:
   Al implementar el flujo completo de negociación entre un cliente y un servidor:
   ```python
   # 1. Servidor genera oferta:
   state, signed_offer = ServerKeyOfferFactory().create(responder=bob, profile=PQCProfile.LOW)
   
   # 2. Cliente recibe la oferta y encapsula:
   encap = MLKEM768.encapsulate(signed_offer.offer.ml_kem_public_key)
   # Cliente envía encap.ciphertext al servidor
   
   # 3. Servidor recibe el ciphertext pero no puede invocar decapsulate:
   # state.decapsulate(encap.ciphertext) -> AttributeError: 'ResponderKEMState' object has no attribute 'decapsulate'
   ```

4. **Corrección propuesta**:
   Añadir el método `decapsulate` en `ResponderKEMState` que despache a los KEMs subyacentes según el perfil:
   ```python
   def decapsulate(
       self,
       ml_kem_ciphertext: bytes,
       hqc_ciphertext: bytes | None = None,
   ) -> tuple[bytes, ...]:
       """Decapsulate received ciphertexts using this session's private KEM state."""
       ml_secret = self._ml_kem.decapsulate(ml_kem_ciphertext)
       if self.profile is PQCProfile.LOW:
           if hqc_ciphertext is not None:
               raise ValueError("LOW profile decapsulation does not accept HQC ciphertext.")
           return (ml_secret,)
       if hqc_ciphertext is None or self._hqc is None:
           raise ValueError("HIGH profile decapsulation requires an HQC ciphertext.")
       hqc_secret = self._hqc.decapsulate(hqc_ciphertext)
       return (ml_secret, hqc_secret)
   ```

---

### [M-01] Serialización asimétrica: ausencia de métodos de deserialización para `ServerKeyOffer`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/messages.py`
   - Clases: `ServerKeyOffer` (líneas 40–120) y `SignedServerKeyOffer` (líneas 123–138).

2. **Por qué es un problema**:
   `ServerKeyOffer` implementa `canonical_bytes()`, un método riguroso y determinista que genera el preimage de firma con separación de dominio.
   Sin embargo, no se proporciona ningún método inverso o de serialización estructurada (como `to_dict()` y `from_dict()`, o `from_canonical_bytes()`), a diferencia de `PublicIdentity` en `identity.py`.
   Cuando un cliente recibe la oferta a través de una API REST (FastAPI en `ui/backend`) o un socket de red en formato JSON/dict, no existe un mecanismo estandarizado en el modelo de dominio para reconstruir las instancias de `ServerKeyOffer` y `SignedServerKeyOffer`, obligando a reimplementar la decodificación y validación de Base64 en cada consumidor.

3. **Escenario donde falla**:
   En el endpoint de backend de la interfaz de usuario o en adaptadores de red, al parsear un payload HTTP entrante que contiene una oferta firmada.

4. **Corrección propuesta**:
   Implementar `to_dict()` y `from_dict(cls, payload: Mapping[str, object])` en `ServerKeyOffer` y `SignedServerKeyOffer`, codificando en Base64 los campos binarios (`session_id`, `nonce`, `ml_kem_public_key`, `hqc_public_key`, `signature`), manteniendo paridad con `PublicIdentity`.

---

### [L-01] Ausencia de método explícito de destrucción/limpieza de claves efímeras

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/server_offer.py`
   - Clase: `ResponderKEMState` (líneas 18–60).

2. **Por qué es un problema**:
   Las claves KEM generadas por el servidor son estrictamente efímeras (para una única sesión). `ResponderKEMState` no implementa un método `close()`, `wipe()` o gestor de contexto para eliminar explícitamente las referencias a las claves secretas en memoria una vez completada la decapsulación o si la sesión expira/aborta.

3. **Escenario donde falla**:
   En un servidor con alta concurrencia donde sesiones abortadas o inactivas acumulan objetos `ResponderKEMState` en memoria hasta que el recolector de basura de Python los libera.

4. **Corrección propuesta**:
   Añadir un método `close()` o soporte de context manager en `ResponderKEMState` que anule las referencias internas `_ml_kem` y `_hqc` y marque el estado como consumido.

---

### [L-02] Cadena de estandarización en prosa larga en `hqc.py`

1. **Archivo y función afectada**:
   - Archivo: `pqc/kem/hqc.py`
   - Función: `hqc_3_metadata` (línea 27).

2. **Por qué es un problema**:
   El campo `standardization` contiene `"NIST selected for standardization; FIPS not yet finalized"`. Mientras que en `MLKEM768` y `MLDSA65` se utilizan códigos estandarizados concisos (`"NIST FIPS 203"`, `"NIST FIPS 204"`), el uso de una oración descriptiva dificulta comparaciones programáticas directas.

3. **Escenario donde falla**:
   Exportadores de metadatos o generadores de tablas de benchmark en `experiments/` que esperan identificadores concisos de estándares.

4. **Corrección propuesta**:
   Utilizar un identificador más homogéneo, como `"NIST Round 4 Selection"` o `"NIST Draft"`.

---

### [L-03] Ausencia de tests para propiedades IND-CCA2 ante texto cifrado manipulado

1. **Archivo y función afectada**:
   - Archivo: `tests/test_pqc/test_kem/test_providers.py`.

2. **Por qué es un problema**:
   Los tests actuales verifican la decapsulación exitosa (`shared_secret == decapsulated`). No obstante, no se comprueba explícitamente la propiedad IND-CCA2 de rechazo implícito (transformada Fujisaki-Okamoto): si se altera un bit del `ciphertext`, `decapsulate()` debe devolver un secreto compartido determinista pero completamente diferente (sin lanzar excepción y sin igualar al secreto original).

3. **Escenario donde falla**:
   Potenciales regresiones en el comportamiento de decapsulación de liboqs que no sean detectadas por la suite de pruebas.

4. **Corrección propuesta**:
   Añadir un test en `test_providers.py` que muta el ciphertext y comprueba que `provider.decapsulate(corrupted_ct) != original_secret`.

---

### [L-04] Re-exportación incompleta en `pqc/__init__.py`

1. **Archivo y función afectada**:
   - Archivo: `pqc/__init__.py` (líneas 1–20).

2. **Por qué es un problema**:
   `pqc/__init__.py` reexporta `PQCProfile`, `ServerKeyOfferFactory`, `MLDSAIdentity`, `PQCParty`, `PublicIdentity` y `TrustedIdentityStore`. Sin embargo, no reexporta los proveedores KEM (`MLKEM768`, `HQC3`, `KEMProvider`) ni los mensajes (`ServerKeyOffer`, `SignedServerKeyOffer`), obligando a realizar importaciones desde submódulos internos (`pqc.kem`, `pqc.protocol`).

3. **Escenario donde falla**:
   Inconsistencia en la experiencia de desarrollo al consumir la API pública del paquete `pqc`.

4. **Corrección propuesta**:
   Reexportar de manera uniforme los proveedores y tipos de mensajes públicos en `pqc/__init__.py`.

---

## 4. Evaluación de Invariantes y Principios de Diseño

1. **Diseño Criptográfico de KEM (Separación Encapsulate / Decapsulate)**:
   - **Cumplimiento**: **Excelente**.
   - `KEMProvider.encapsulate` está modelado correctamente como `@classmethod` sobre la clave pública, permitiendo encapsular sin instanciar claves privadas (corrigiendo el patrón anterior de firmas).
   - `decapsulate` requiere la instancia con clave secreta.

2. **Framing Canónico y Separación de Dominio**:
   - **Cumplimiento**: **Excelente**.
   - `ServerKeyOffer.canonical_bytes()` aplica prefijos de longitud (`>I`), versión de protocolo (`>H`), separador de dominio explícito (`QuantumSec/PQCHandshake/v1/ServerKeyOffer`) y codificación determinista de variantes de perfil (`\x00` vs `\x01`). Esto previene ataques de maleabilidad, canonicalización y confusión de protocolos.

3. **Protección de Material Secreto y Representación**:
   - **Cumplimiento**: **Excelente**.
   - `KEMEncapsulation`, `OQSKEMProvider`, `ResponderKEMState` y `SignedServerKeyOffer` marcan `repr=False` en secretos, claves privadas y textos cifrados.
   - `__repr__` expone únicamente longitudes y nombres de algoritmo, evitando fugas en logs o trazas de depuración.

4. **Rendimiento e Integración FFI (liboqs)**:
   - **Cumplimiento**: **Muy Bueno**.
   - Se implementó `@lru_cache` para la carga del módulo `oqs` y `@cache` para la verificación de algoritmos habilitados (`_ensure_kem_algorithm_enabled`), eliminando la sobrecarga FFI reiterativa detectada en revisiones previas.
   - Los gestores de contexto `with kem:` garantizan la liberación de memoria nativa C (`OQS_KEM_free`).

---

## 5. Conclusiones y Recomendaciones de Priorización

La incorporación de KEM (ML-KEM-768 y HQC-3) y el modelado de ofertas autenticadas de servidor demuestran un diseño técnico de alta calidad, robusto y conforme a los estándares NIST FIPS 203 y FIPS 204.

Se sugiere abordar las mejoras en el siguiente orden:
1. **Prioridad 1 (Ciclo de Vida del Handshake)**:
   - Añadir el método `decapsulate(...)` en `ResponderKEMState` para permitir al servidor procesar la respuesta del cliente (**H-01**).
2. **Prioridad 2 (Interoperabilidad y Transporte)**:
   - Implementar `to_dict()` y `from_dict()` en `ServerKeyOffer` y `SignedServerKeyOffer` (**M-01**).
3. **Prioridad 3 (Refinamientos y Pruebas)**:
   - Incorporar método de cierre/limpieza de claves efímeras en `ResponderKEMState` (**L-01**).
   - Añadir test de rechazo implícito IND-CCA2 ante texto cifrado corrupto (**L-03**).
   - Homogeneizar exportaciones en `pqc/__init__.py` (**L-04**).
