# Informe de Revisión de Código Independiente: Módulo `pqc` (Fase 5: Derivación de Claves de Sesión con KDF y Transcript Canónico)

**Fecha**: 4 de Septiembre de 2026  
**Alcance**: Módulo `pqc/kdf/` (`combiner.py`, `hkdf.py`), `pqc/_encoding.py`, `pqc/protocol/transcript.py`, `pqc/protocol/key_schedule.py`, `pqc/protocol/_shared_secret_state.py`, y suite de pruebas `tests/test_pqc/test_key_schedule.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría técnica e independiente de la **Fase 5 del protocolo de negociación post-cuántico (handshake PQC)** en **QuantumSec**, correspondiente a la formalización del transcript canónico, la combinación inequívoca de secretos KEM y la derivación determinista de claves de sesión simétricas de 256 bits mediante HKDF-SHA-384:
- **Capa `pqc/kdf/`**:
  - Combinador canónico de secretos KEM (`canonical_kem_secret_input` en `combiner.py`): codificación determinista con prefijos de longitud de 32 bits, dominio de separación explícito (`QuantumSec/PQCHandshake/v1/KEMSecretInput`), orden fijo de algoritmos (ML-KEM-768 primero, HQC-3 segundo) y sensibilidad posicional y de componentes.
  - Adaptador HKDF-SHA-384 (`derive_hkdf_sha384` en `hkdf.py`): integración sobre la primitiva nativa de `cryptography` con validación estricta de parámetros.
- **Capa `pqc/protocol/transcript.py`**:
  - `PQCHandshakeTranscript`: agregación inmutable y validación cruzada de los dos mensajes autenticados (`SignedServerKeyOffer` y `SignedClientKeyExchange`), serialización canónica con separador de dominio (`QuantumSec/PQCHandshake/v1/Transcript`) y cálculo del hash de transcript de 384 bits (`transcript_hash`), utilizado como sal (*salt*) en la KDF.
- **Capa `pqc/protocol/key_schedule.py`**:
  - Derivador de claves de sesión (`PQCSessionKeyDeriver`): métodos `derive_initiator` y `derive_responder` que vinculan estrictamente los resultados previos autenticados (Fases 3 y 4) con el transcript público, ejecutando la derivación bajo el contexto de propósito `_session_key_info` (protocol_version + profile).
  - Estado de clave de sesión (`DerivedSessionKeyState`): contenedor de 256 bits con protección en `__repr__`, control de ciclo de vida (`close()`, `is_closed`) y soporte para gestores de contexto `with`.
- **Capa `pqc/protocol/_shared_secret_state.py`**:
  - Refactorización de `_KEMSharedSecretStateBase`: unificación de la lógica común entre `InitiatorKEMState` y `ResponderSharedSecretState`, implementando soporte para context manager (`__enter__`/`__exit__`) y construcción protegida de inputs para la KDF (`_build_kdf_input()`).
- **Suite de Pruebas**: 22 tests unitarios y de integración exhaustivos que cubren derivación bilateral simétrica, sensibilidad a mutaciones de un bit, separación por perfiles, inyección de `client_nonce`, restricciones de estado cerrado y protección contra fugas de memoria en representaciones (`tests/test_pqc/test_key_schedule.py`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se identificaron vulnerabilidades criptográficas ni fallos en la separación de dominios o en el cálculo de preimages de HKDF. |
| **HIGH** | 0 | La arquitectura implementa con rigor matemático los estándares FIPS 203, FIPS 204 y RFC 5869 (HKDF). |
| **MEDIUM** | 1 | `DerivedSessionKeyState` almacena la clave de sesión en un campo privado sin proveer un método público o propiedad controlada para su consumo en cifradores simétricos o composición con QKD. |
| **LOW** | 2 | Ausencia de métodos de serialización `to_dict`/`from_dict` en `PQCHandshakeTranscript` y validación estricta de sal no vacía en el adaptador genérico `derive_hkdf_sha384`. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | `MEDIUM` | `pqc/protocol/key_schedule.py:48` (`DerivedSessionKeyState`) | Interfaces / Usabilidad | `DerivedSessionKeyState` carece de propiedad pública o método de exportación (`session_key`/`export_session_key()`), obligando a usar atributos privados para consumir la clave simétrica derivada. |
| **L-01** | `LOW` | `pqc/protocol/transcript.py:17` (`PQCHandshakeTranscript`) | Interfaces / Transporte | `PQCHandshakeTranscript` no implementa `to_dict()` ni `from_dict()`, dificultando la persistencia estructurada o auditoría del transcript en formato JSON. |
| **L-02** | `LOW` | `pqc/kdf/hkdf.py:15` (`derive_hkdf_sha384`) | Validación / Estándares | `derive_hkdf_sha384` rechaza sales vacías (`salt=b""`), cuando la especificación RFC 5869 permite sales nulas o vacías. |

---

## 3. Análisis Detallado de Hallazgos

### [M-01] Ausencia de método público de acceso a `_session_key` en `DerivedSessionKeyState`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/key_schedule.py`
   - Clase: `DerivedSessionKeyState` (líneas 48–113).

2. **Por qué es un problema**:
   `DerivedSessionKeyState` es el artefacto terminal producido por la derivación de la Fase 5. Su objetivo fundamental es suministrar la clave simétrica de 256 bits (32 bytes) resultante del handshake a cifradores simétricos (ej. AES-GCM, ChaCha20-Poly1305 en `ui/backend`), o a combinadores híbridos con claves cuánticas de QKD en `experiments/`.
   Sin embargo, el campo `_session_key` se mantiene como atributo privado con prefijo de subrayado sin exponer ninguna propiedad pública (como `session_key`) ni método (como `export_session_key()`).
   Actualmente, la propia suite de pruebas (`test_key_schedule.py:121`) debe recurrir a `object.__getattribute__(alice_key_state, "_session_key")` para leer la clave. Cualquier consumidor legítimo en capas superiores se verá forzado a acceder a campos privados o utilizar introspección.

3. **Escenario donde falla**:
   Al instanciar un canal de datos cifrado o componer la clave con QKD:
   ```python
   session_state = deriver.derive_initiator(...)
   # Intento de uso en un cifrador AES-GCM o combinador OTP/KDF:
   cipher = AESGCM(session_state.session_key)
   # AttributeError: 'DerivedSessionKeyState' object has no attribute 'session_key'
   ```

4. **Corrección propuesta**:
   Añadir una propiedad `session_key` (o método `export_session_key()`) en `DerivedSessionKeyState` que valide que el estado no esté cerrado y devuelva los bytes de la clave:
   ```python
   @property
   def session_key(self) -> bytes:
       """Return the derived 256-bit symmetric session key."""
       if self._closed or self._session_key is None:
           raise RuntimeError("Derived session key state is closed.")
       return self._session_key
   ```

---

### [L-01] Ausencia de serialización `to_dict` / `from_dict` en `PQCHandshakeTranscript`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/transcript.py`
   - Clase: `PQCHandshakeTranscript` (líneas 17–120).

2. **Por qué es un problema**:
   `PQCHandshakeTranscript` agrega los dos mensajes firmados del protocolo (`SignedServerKeyOffer` y `SignedClientKeyExchange`), los cuales disponen ambos de métodos `to_dict()` y `from_dict()`.
   Sin embargo, la clase `PQCHandshakeTranscript` no expone helpers de serialización a diccionario/JSON.
   En escenarios de auditoría, logging de seguridad o persistencia de sesiones de experimentos, los consumidores deben desempaquetar y reempaquetar manualmente los dos mensajes en lugar de invocar una serialización unificada.

3. **Escenario donde falla**:
   Al exportar el transcript completo de un handshake a JSON para almacenamiento o análisis forense:
   ```python
   data = transcript.to_dict()
   # AttributeError: 'PQCHandshakeTranscript' object has no attribute 'to_dict'
   ```

4. **Corrección propuesta**:
   Implementar `to_dict()` y `from_dict(cls, payload: Mapping[str, object]) -> Self` en `PQCHandshakeTranscript`, delegando en los métodos `to_dict()` / `from_dict()` de los dos mensajes autenticados contenidos.

---

### [L-02] Restricción indebida de sal no vacía en el adaptador genérico HKDF

1. **Archivo y función afectada**:
   - Archivo: `pqc/kdf/hkdf.py`
   - Función: `derive_hkdf_sha384` y `_validated_bytes` (líneas 7–38).

2. **Por qué es un problema**:
   La función auxiliar `_validated_bytes` comprueba `if not value: raise ValueError(f"{name} must not be empty.")`, aplicándose tanto a `key_material` como a `salt` e `info`.
   Según la especificación estándar RFC 5869 (sección 2.2), la sal en HKDF es formalmente opcional; si no se proporciona o está vacía (`salt=b""`), HKDF utiliza una cadena de ceros de longitud igual al tamaño del bloque hash.
   Aunque en el handshake de QuantumSec la sal es invariablemente el `transcript_hash` (48 bytes), rechazar `salt=b""` en la función genérica `derive_hkdf_sha384` limita su conformidad estricta con el estándar RFC 5869.

3. **Escenario donde falla**:
   Al reutilizar `derive_hkdf_sha384` para derivaciones secundarias donde la sal sea nula o vacía.

4. **Corrección propuesta**:
   Permitir `salt: bytes | None = None` y convertir `None` o `b""` a la sal nula estándar si se desea un comportamiento RFC 5869 completo, o documentar explícitamente que la función requiere una sal no vacía para forzar el uso del transcript.

---

## 4. Evaluación de Invariantes y Principios de Diseño Criptográfico

1. **Diseño de KDF y Transcript Binding (RFC 5869 y FIPS 203/204)**:
   - **Cumplimiento**: **Sobresaliente**.
   - La derivación aplica el principio *Extract-then-Expand* mediante HKDF-SHA-384.
   - **Sal (*Salt*)**: Utiliza el hash SHA-384 del transcript completo y autenticado (`transcript.transcript_hash`), asegurando que cualquier cambio en un solo bit de ofertas, respuestas, firmas o noeces (`server_nonce` o `client_nonce`) derive una clave de sesión completamente pseudoaleatoria e independiente.
   - **Material Clave (*IKM*)**: `canonical_kem_secret_input` estructura la concatenación de los secretos compartidos de forma inequívoca mediante prefijos de longitud, evitando colisiones o ataques de extensión de longitud en perfiles multi-KEM (`HIGH`).
   - **Información de Contexto (*Info*)**: `_session_key_info` fija el separador de dominio de propósito (`QuantumSec/PQCHandshake/v1/SessionKey`), la versión del protocolo y el identificador del perfil (`low` / `high`), garantizando que claves para distintos propósitos o perfiles nunca colisionen.

2. **Entropía Bilateral con `client_nonce`**:
   - **Cumplimiento**: **Excelente**.
   - Se incorporó exitosamente `client_nonce` (32 bytes generados mediante CSPRNG) en `ClientKeyExchange`, asegurando que ambas partes contribuyen entropía fresca e independiente al transcript del handshake.

3. **Aislamiento y Reutilización de Estados**:
   - **Cumplimiento**: **Excelente**.
   - `_KEMSharedSecretStateBase` resolvió la duplicación de código entre Alice y Bob, añadiendo además soporte nativo para gestores de contexto `with`.
   - Los estados de KEM fuente (`InitiatorKEMState`, `ResponderSharedSecretState`) permanecen abiertos tras la Fase 5 para permitir derivar claves de confirmación en la Fase 6 (mensajes Finished), mientras que `DerivedSessionKeyState` ofrece un ciclo de vida independiente y cerrable.

4. **Hermeticidad y Prevención de Fugas de Información**:
   - **Cumplimiento**: **Sobresaliente**.
   - Ni la clave de sesión derivada (`_session_key`), ni los secretos KEM intermedios se exponen en representaciones de depuración (`repr`), cadenas de texto ni serializaciones de transporte.

---

## 5. Conclusiones y Recomendaciones de Priorización

La Fase 5 consolida un diseño criptográfico de vanguardia, altamente robusto y formalmente respaldado por pruebas deterministas y analíticas.

Se sugiere abordar las mejoras en el siguiente orden:
1. **Prioridad 1 (API de Consumo de la Clave de Sesión)**:
   - Añadir la propiedad pública `session_key` en `DerivedSessionKeyState` (**M-01**).
2. **Prioridad 2 (Comodidad de Transporte e Interoperabilidad)**:
   - Implementar `to_dict()` y `from_dict()` en `PQCHandshakeTranscript` (**L-01**).
   - Ajustar el manejo de sal opcional en `derive_hkdf_sha384` (**L-02**).
