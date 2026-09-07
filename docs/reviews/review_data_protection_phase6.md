# Informe de Revisión de Código Independiente: Plano de Protección de Datos AES-256-GCM (Fase 6)

**Fecha**: 7 de Septiembre de 2026  
**Alcance**: Commit `44671a7` (*"phase 6 implemented - AES 256 for messages encription"*).  
**Módulos analizados**:
- **Plano de protección de datos (`data_protection/`)**:
  - Primitiva criptográfica: `data_protection/aes_gcm.py`.
  - Contexto y política de nonces: `data_protection/context.py`.
  - Registro protegido: `data_protection/record.py`.
  - Sesión protegida y ciclo de vida: `data_protection/session.py`.
  - Punto de entrada y exportaciones: `data_protection/__init__.py`.
- **Adaptador de orquestación (`orchestration/`)**:
  - Transferencia de propiedad de claves: `orchestration/data_plane.py`.
  - Exportaciones de orquestación: `orchestration/__init__.py`.
- **Documentación y modelo de seguridad**:
  - `docs/SECURITY_MODEL.md`, `docs/structure.md`, `docs/tasks.md`.
- **Suites de verificación**:
  - `tests/test_data_protection/test_aes_gcm.py`.
  - `tests/test_data_protection/test_nonce_policy.py`.
  - `tests/test_data_protection/test_protected_session.py`.
  - `tests/test_orchestration/test_data_plane.py`.
  - `tests/test_orchestration/test_architecture_boundaries.py`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han modificado archivos fuente durante la revisión, preservando las directrices de `review_prompt.md`.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría exhaustiva e independiente sobre la implementación de la **Fase 6** de la arquitectura de **QuantumSec**, correspondiente al plano de datos criptográfico basado en AES-256-GCM para la protección de cargas útiles de aplicación:

1. **Aislamiento de Dominio e Invariante de Capas**:
   - El nuevo paquete `data_protection/` opera con total independencia del plano de establecimiento: no importa `qkd`, `pqc` ni `orchestration`.
   - La transferencia de la clave de sesión se realiza mediante el adaptador desacoplado `orchestration.open_data_plane()`, que exige un resultado de sesión en estado `ESTABLISHED`, tipo de clave `SESSION_KEY` de exactamente 256 bits, y cierra inmediatamente la capacidad de clave del plano de establecimiento (`session.close()`) tras transferir la propiedad.
   - Las claves variables tipo `QKD_BITSTRING` (provenientes de perfiles QKD puros) son rechazadas explícitamente para evitar truncamientos, paddings arbitrarios o derivaciones no formalizadas en esta fase.

2. **Criptografía de Carga Útil y Política de Nonces**:
   - Empleo de AES-256-GCM respaldado por `cryptography.hazmat.primitives.ciphers.aead.AESGCM` con claves de 32 bytes y etiqueta de autenticación completa de 128 bits (16 bytes).
   - Espacio de nonces determinista de 96 bits (12 bytes) con separación estricta por dirección:
     - Prefijo de 4 bytes disjunto: `00000001` para Alice $\rightarrow$ Bob y `00000002` para Bob $\rightarrow$ Alice.
     - Contador monótono de 64 bits en big-endian (`pack(">Q", seq)`).
   - Reserva de nonces protegida por un cerrojo (`threading.Lock`), asegurando unicidad en accesos concurrentes e impidiendo el desbordamiento o reutilización del espacio de nonces (*fail-closed* ante agotamiento de contador).
   - Inyección de Datos Asociados Autenticados (AAD) canónicos bajo el dominio `QuantumSec/DataPlane/v1/AAD`, enlazando versión, contexto público completo de la sesión, dirección, número de secuencia y longitud declarada del AAD de la aplicación.

3. **Estado de Calidad y Pruebas**:
   - 721 tests ejecutados con éxito en la suite completa (`pytest`).
   - Linter (`ruff check .`) limpio sin advertencias.
   - Análisis estático de tipos (`pyright`) con 0 errores y 0 advertencias.

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se detectaron vulnerabilidades que permitan la reutilización de nonces en AES-GCM, la manipulación de cargas útiles sin detección de tag, o la fuga de claves no autorizadas. |
| **HIGH** | 0 | El diseño respeta escrupulosamente las cotas de seguridad de NIST SP 800-38D, aísla los dominios y rechaza claves no normalizadas de QKD. |
| **MEDIUM** | 3 | Sensibilidad al orden de inserción en la serialización canónica de `public_context` en `DataPlaneContext`; ausencia de formato binario de transporte (`canonical_bytes`/`from_bytes`) en `ProtectedRecord`; y ausencia de ventana o política anti-replay en `ProtectedSession.decrypt`. |
| **LOW** | 4 | Condición tautológica y potencialmente defectuosa en `ProtectedRecord.__post_init__` ante futuros incrementos de versión; validación tardía de `session.is_closed` en `open_data_plane`; rigidez al rechazar diccionarios en `public_context`; y cobertura de pruebas limitada a cargas útiles de tamaño trivial sin evaluación de bloques múltiples. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | `MEDIUM` | `data_protection/context.py:68-76, 112-135` | Criptografía / Determinismo | `DataPlaneContext` preserva el orden de inserción de `public_context` sin ordenar lexicográficamente las claves, provocando que representaciones equivalentes con distinto orden produzcan hashes de contexto dispares y fallen en descifrado. |
| **M-02** | `MEDIUM` | `data_protection/record.py:24-100` | Diseño de API / Transporte | `ProtectedRecord` carece de métodos de serialización y deserialización binaria (`canonical_bytes` / `from_bytes`), obligando a serializar vía `to_public_dict` en JSON con codificación hexadecimal que duplica la sobrecarga de red. |
| **M-03** | `MEDIUM` | `data_protection/session.py:88-119` (`decrypt`) | Seguridad / Anti-Replay | `ProtectedSession.decrypt` no implementa registro de números de secuencia recibidos ni ventana anti-replay, permitiendo la reaparición indefinida de paquetes duplicados en el canal de red. |
| **L-01** | `LOW` | `data_protection/record.py:38` | Mantenibilidad / Lógica | Condición `self.version != PROTECTED_RECORD_VERSION or self.version != DATA_PLANE_VERSION` que se volverá tautológica y bloqueará la inicialización si ambas constantes se desincronizan en futuras versiones. |
| **L-02** | `LOW` | `orchestration/data_plane.py:10-33` | Robustez / Rendimiento | `open_data_plane` no comprueba `session.is_closed` al inicio, instanciando y calculando innecesariamente el contexto canónico antes de fallar con `RuntimeError` en la exportación de clave. |
| **L-03** | `LOW` | `data_protection/context.py:116-122` | Usabilidad de API | `DataPlaneContext` rechaza objetos de tipo `dict` para `public_context` a pesar de que su método `to_public_dict` exporta dicho campo como un diccionario nativo. |
| **L-04** | `LOW` | `tests/test_data_protection/test_aes_gcm.py` | Cobertura de Tests | Ausencia de casos de prueba con cargas útiles grandes (> 1 KB, 64 KB) o evaluación de fronteras de bloque de 128 bits en AES-GCM. |

---

## 3. Análisis Detallado de Hallazgos

### [M-01] Sensibilidad al orden de inserción en la serialización canónica de `DataPlaneContext`

1. **Archivo y función afectada**:
   - Archivo: `data_protection/context.py`
   - Función: `_encode_public_context` (líneas 68–76) y `DataPlaneContext.__post_init__` (líneas 112–135).

2. **Por qué es un problema**:
   `DataPlaneContext` almacena pares clave-valor en el atributo `public_context` y los serializa en `_encode_public_context` iterando en el orden estricto en que fueron suministrados en la tupla:
   ```python
   def _encode_public_context(entries: tuple[tuple[str, str | int], ...]) -> bytes:
       encoded = [pack(">H", len(entries))]
       for name, value in entries:
           encoded.append(_length_prefixed(name.encode("utf-8")))
           ...
   ```
   En la criptografía canónica (estándares como Canonical CBOR RFC 8949, DER en ASN.1 o Canonical JSON RFC 8785), toda estructura asociativa o mapa de atributos **debe ordenarse lexicográficamente por su clave**.
   En la implementación actual, si Alice y Bob instancian `DataPlaneContext` con los mismos metadatos pero con un orden de tupla distinto:
   - Alice: `(("qkd_transcript_hash_sha384", "aa..."), ("pqc_transcript_hash_sha384", "bb..."))`
   - Bob: `(("pqc_transcript_hash_sha384", "bb..."), ("qkd_transcript_hash_sha384", "aa..."))`
   El método `canonical_bytes()` emitirá secuencias de bytes diferentes y, por ende, `context.context_hash` generará digests SHA-384 distintos.
   Cuando Bob reciba el registro protegido emitido por Alice, la comprobación en `ProtectedSession.decrypt`:
   ```python
   if record.context_hash != self.context.context_hash:
       raise ValueError("Protected record does not belong to this data-plane context.")
   ```
   fallará con `ValueError`, rechazando indebidamente un registro legítimo y perfectamente autenticado.

3. **Escenario donde falla**:
   Si dos extremos intercambian o reconstruyen el contexto de sesión a partir de formatos deserializados (por ejemplo, leyendo el diccionario JSON emitido por `session.to_public_dict()["public_context"]`), el orden de las claves devuelto por los parsers de JSON de diferentes lenguajes o plataformas no está garantizado. Esto provoca que el descifrado aborte con error de contexto no coincidente.

4. **Corrección propuesta**:
   Ordenar `clean_entries` de forma determinista por clave UTF-8 en `DataPlaneContext.__post_init__`:
   ```python
   clean_entries.sort(key=lambda entry: entry[0].encode("utf-8"))
   object.__setattr__(self, "public_context", tuple(clean_entries))
   ```

---

### [M-02] Ausencia de serialización y deserialización binaria (`canonical_bytes` / `from_bytes`) en `ProtectedRecord`

1. **Archivo y función afectada**:
   - Archivo: `data_protection/record.py`
   - Clase: `ProtectedRecord` (líneas 24–100).

2. **Por qué es un problema**:
   `ProtectedRecord` es el artefacto final concebido para viajar por el canal de transporte (red, sockets o IPC) entre Alice y Bob. Sin embargo, a diferencia de los restantes artefactos criptográficos del sistema:
   - `SignedServerKeyOffer` cuenta con `canonical_bytes()` y `from_bytes()`.
   - `SignedClientKeyExchange` cuenta con `canonical_bytes()` y `from_bytes()`.
   - `AuthenticationFrame` cuenta con `canonical_bytes()` y `from_bytes()`.
   - `HybridFinishedMessage` cuenta con `canonical_bytes()`.
   `ProtectedRecord` no ofrece ningún método de codificación binaria ni función constructora desde bytes. Su único método de exportación es `to_public_dict()`.
   Esto obliga a los consumidores a:
   1. Serializar el diccionario a JSON, codificando en cadenas hexadecimales (`nonce.hex()`, `ciphertext.hex()`, `tag.hex()`), lo que duplica el ancho de banda requerido para el payload y la sobrecarga del canal.
   2. O bien diseñar ad-hoc un empaquetador binario propio fuera de la biblioteca, violando el principio de encapsulación y arriesgando discrepancias de framing en red.

3. **Escenario donde falla**:
   Al implementar una prueba de comunicación real de aplicación o un benchmark de rendimiento sobre sockets TCP en capas superiores, el desarrollador no dispone de una función estándar en la biblioteca para enviar y recibir un `ProtectedRecord` en binario compacto.

4. **Corrección propuesta**:
   Añadir métodos de serialización y parseo canónico con prefijos de longitud en `ProtectedRecord`:
   ```python
   def canonical_bytes(self) -> bytes:
       return b"".join(
           (
               _length_prefixed(b"QuantumSec/ProtectedRecord/v1"),
               pack(">H", self.version),
               _length_prefixed(self.session_id),
               _length_prefixed(self.profile.encode("utf-8")),
               _length_prefixed(self.context_hash),
               _length_prefixed(self.direction.value.encode("ascii")),
               pack(">Q", self.sequence_number),
               _length_prefixed(self.nonce),
               _length_prefixed(self.ciphertext),
               _length_prefixed(self.tag),
               pack(">Q", self.application_aad_bytes),
           )
       )

   @classmethod
   def from_bytes(cls, data: bytes) -> Self:
       ...
   ```

---

### [M-03] Ausencia de ventana o política anti-replay a nivel de recepción en `ProtectedSession.decrypt`

1. **Archivo y función afectada**:
   - Archivo: `data_protection/session.py`
   - Función: `ProtectedSession.decrypt` (líneas 88–119).

2. **Por qué es un problema**:
   La clase `ProtectedSession` gestiona con rigor la unicidad del nonce en la emisión mediante un cerrojo (`threading.Lock`) y el avance monótono del contador `_next_sequences[direction]`.
   No obstante, el receptor en `decrypt()` es completamente apátrida (*stateless*): se limita a validar que el nonce coincida estructuralmente con `nonce_for(record.direction, record.sequence_number)` y que el tag AEAD sea válido.
   Aunque `docs/SECURITY_MODEL.md` advierte explícitamente que la unicidad en el cifrado no equivale a protección anti-replay en red, desde una perspectiva de seguridad de transporte, la falta de una política receptora (como un contador de secuencia monótona esperada o una ventana deslizante de recepción tipo IPsec/TLS) permite que un atacante pasivo capture un `ProtectedRecord` válido y lo retransmita $N$ veces al destinatario. El método `decrypt()` validará y entregará el texto claro tantas veces como se reciba, posibilitando ataques de repetición en capa de aplicación.

3. **Escenario donde falla**:
   En una sesión interactiva protegida donde se transmiten órdenes de control o transacciones bancarias autenticadas, un atacante captura el registro con `sequence_number=1`. El atacante inyecta el mismo paquete repetidamente en el enlace. El receptor descifra y procesa la misma instrucción múltiples veces sin error.

4. **Corrección propuesta**:
   Permitir configurar un modo de recepción con verificación de orden y anti-replay en `ProtectedSession`:
   - Mantener un registro del mayor número de secuencia recibido por dirección (`_highest_received_sequence`).
   - Rechazar registros duplicados o con secuencia decreciente si se activa la política estricta de transporte en orden, o mantener una máscara de bits para ventanas deslizantes.
   - Alternativamente, documentar con una advertencia en el docstring de `decrypt()` que el llamador es responsable de verificar la monotonicidad del `record.sequence_number` recibido.

---

### [L-01] Condición potencialmente defectuosa en `ProtectedRecord.__post_init__`

1. **Archivo y función afectada**:
   - Archivo: `data_protection/record.py`
   - Clase: `ProtectedRecord` (línea 38).

2. **Por qué es un problema**:
   En la línea 38 se comprueba:
   ```python
   if self.version != PROTECTED_RECORD_VERSION or self.version != DATA_PLANE_VERSION:
       raise ValueError(f"version must be {PROTECTED_RECORD_VERSION}.")
   ```
   Actualmente ambas constantes valen `1`. Sin embargo, la disyunción lógica `x != A or x != B` es una trampa de mantenimiento clásica: si en el futuro `PROTECTED_RECORD_VERSION` se incrementa a `2` mientras que `DATA_PLANE_VERSION` permanece en `1`, la expresión se convertirá en una tautología que será verdadera para **cualquier** valor entero (pues ningún número puede ser simultáneamente 1 y 2). En tal caso, la clase `ProtectedRecord` levantará `ValueError` incondicionalmente para cualquier instancia.

3. **Escenario donde falla**:
   Durante una futura actualización del esquema del registro de datos donde se cambie la versión de `ProtectedRecord` de 1 a 2 sin cambiar `DATA_PLANE_VERSION`, todos los tests y ejecuciones fallarán de forma catastrófica.

4. **Corrección propuesta**:
   Separar o unificar la validación:
   ```python
   if self.version != PROTECTED_RECORD_VERSION:
       raise ValueError(f"version must be {PROTECTED_RECORD_VERSION}.")
   ```
   Si se requiere sincronización entre ambas constantes, verificarlo con una aserción estática a nivel de módulo:
   ```python
   assert PROTECTED_RECORD_VERSION == DATA_PLANE_VERSION, "Version constant mismatch"
   ```

---

### [L-02] Validación tardía de `session.is_closed` en `open_data_plane`

1. **Archivo y función afectada**:
   - Archivo: `orchestration/data_plane.py`
   - Función: `open_data_plane` (líneas 10–33).

2. **Por qué es un problema**:
   La función comienza con las siguientes precondiciones:
   ```python
   if not isinstance(session, SessionResult):
       raise TypeError("session must be a SessionResult.")
   if session.status is not SessionStatus.ESTABLISHED:
       raise RuntimeError("Data plane requires an established session.")
   if session.established_key_type is not EstablishedKeyType.SESSION_KEY:
       raise ValueError(...)
   if session.established_key_bits != DATA_PLANE_KEY_BITS:
       raise ValueError(...)
   ```
   Sin embargo, no comprueba si `session.is_closed` es `True`.
   A continuación, procede a instanciar `DataPlaneContext`, serializar su representación canónica y calcular su digest SHA-384. Solo en la línea 30, al llamar a `session.export_session_key()`, se lanza la excepción `RuntimeError("Established key capability is closed.")`.
   Esto contraviene el principio de fallo rápido (*fail-fast*), ejecutando trabajo criptográfico inútil sobre una sesión cuya clave ya fue retirada o consumida.

3. **Escenario donde falla**:
   Si se invoca accidentalmente `open_data_plane(session)` dos veces consecutivas sobre la misma instancia de sesión, la segunda llamada ejecuta todo el parsing y hashing del contexto antes de abortar.

4. **Corrección propuesta**:
   Comprobar `session.is_closed` junto a las guardas iniciales:
   ```python
   if session.is_closed:
       raise RuntimeError("Session key capability is already closed.")
   ```

---

### [L-03] Rigidez en `DataPlaneContext.__post_init__` al rechazar diccionarios para `public_context`

1. **Archivo y función afectada**:
   - Archivo: `data_protection/context.py`
   - Clase: `DataPlaneContext` (líneas 112–122).

2. **Por qué es un problema**:
   `DataPlaneContext` impone que `self.public_context` sea una secuencia de tuplas de 2 elementos:
   ```python
   for entry in entries:
       if not isinstance(entry, tuple) or len(entry) != 2:
           raise ValueError("public_context entries must be key/value tuples.")
   ```
   Por el contrario, el método exportador `DataPlaneContext.to_public_dict()` genera:
   `"public_context": dict(self.public_context)`.
   Si un consumidor intenta recrear un `DataPlaneContext` a partir de este diccionario (`public_context={"session_id": ...}`), la llamada falla con `ValueError` porque los diccionarios iteran sobre sus claves y no sobre pares. Aceptar tanto `Mapping[str, str | int]` como secuencias de pares mejoraría sensiblemente la usabilidad de la API.

3. **Escenario donde falla**:
   Un desarrollador pasa un diccionario deserializado de configuración a `DataPlaneContext(..., public_context=data["public_context"])` y recibe un `ValueError` inesperado.

4. **Corrección propuesta**:
   Normalizar la entrada permitiendo tanto tuplas como mapeos:
   ```python
   if isinstance(self.public_context, dict):
       entries = tuple(self.public_context.items())
   else:
       entries = tuple(self.public_context)
   ```

---

### [L-04] Cobertura de tests limitada a tamaños de carga útil triviales

1. **Archivo y función afectada**:
   - Archivos: `tests/test_data_protection/test_aes_gcm.py` y `test_protected_session.py`.

2. **Por qué es un problema**:
   Las pruebas actuales validan payloads de 0 bytes o frases cortas de 30 a 40 bytes (ej. `b"QuantumSec application payload"`).
   No existen tests que evalúen el comportamiento ante:
   - Bloques exactamente múltiplos del tamaño de bloque AES (16, 32, 64 bytes).
   - Bloques con longitud fraccionaria (ej. 17, 31 bytes).
   - Mensajes medianos o grandes (1 MB, 10 MB) para comprobar la sobrecarga y ausencia de fugas de memoria o saturación del heap.
   - Vectores de prueba oficiales KAT (*Known Answer Tests*) de NIST para AES-GCM.

3. **Escenario donde falla**:
   Un error de alineación o rendimiento al manejar paquetes de datos reales de aplicación en transmisiones de flujo continuo no sería detectado por la suite actual.

4. **Corrección propuesta**:
   Incorporar tests parametrizados con tamaños de carga útil variados (15, 16, 17, 1024, 65536 bytes) y verificar que `ciphertext` mantiene exactamente la misma longitud y que el tag se valida correctamente.

---

## 4. Aspectos Positivos y Fortalezas del Diseño

1. **Garantía Inviolable contra Reutilización de Nonces**:
   - El peor fallo de seguridad posible en AES-GCM es la reutilización del nonce bajo la misma clave. El diseño de `data_protection` hace imposible esta vulnerabilidad al **no permitir** que el llamador elija el nonce en `encrypt()`.
   - La partición del nonce en un prefijo de dirección de 4 bytes (`00000001` vs `00000002`) garantiza matemáticamente que los nonces de Alice y Bob jamás colisionarán, aun si ambos transmiten concurrentemente con la misma secuencia.
   - La asignación de secuencias es atómica y thread-safe mediante un cerrojo, y ante el agotamiento del contador uint64 se lanza `RuntimeError` impidiendo cualquier desbordamiento (*wrap-around*).

2. **Autenticación Fuerte de Contexto de Sesión en AAD**:
   - Los Datos Asociados Autenticados (AAD) no son opcionales ni vacíos: se inyecta siempre una estructura canónica determinista (`canonical_data_plane_aad`) que ata criptográficamente el texto cifrado al `session_id`, `profile`, `context_hash`, `direction` y `sequence_number`.
   - Esto impide de forma absoluta ataques de cruce de sesión (*cross-session reflection*), ataques de inversión de dirección (hacer pasar un mensaje de Alice como si fuera de Bob) o permutación de paquetes sin invalidar la autenticación GCM.

3. **Cumplimiento Estricto de la Arquitectura Acíclica**:
   - El paquete `data_protection/` no conoce ni importa nada sobre mecánica cuántica, BB84, KEMs o post-procesamiento.
   - La capa `orchestration` actúa limpiamente como adaptador puente, transfiriendo la clave y cerrando inmediatamente el resultado de sesión previo para evitar múltiples dueños del secreto en memoria.

4. **Rechazo Riguroso de Claves QKD no Adaptadas**:
   - Rechazar `QKD_BITSTRING` en lugar de inventar un padding silencioso o truncar bits demuestra una gran madurez arquitectónica, respetando que una secuencia de bits cruda de QKD requiere un plan de claves formal antes de ser consumida como clave simétrica AES.

---

## 5. Recomendaciones de Calidad

1. **Añadir ordenación canónica por clave a `DataPlaneContext`** para garantizar la interoperabilidad y evitar fallos de descifrado por permutación de metadatos en `public_context` (ver hallazgo [M-01]).
2. **Implementar serialización binaria en `ProtectedRecord`** (`canonical_bytes` y `from_bytes`) para facilitar su transporte compacto en red sin sobrecoste de JSON/Hexadecimal (ver hallazgo [M-02]).
3. **Adicionar verificación de monotonicidad o ventana anti-replay en `decrypt()`**, o documentar explícitamente en la firma de la función el requisito de gestión externa de duplicados (ver hallazgo [M-03]).
4. **Corregir la guarda de versión en `ProtectedRecord.__post_init__`** eliminando la disyunción redundante (ver hallazgo [L-01]).
