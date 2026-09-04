# Informe de Revisión de Código Independiente: Módulo `pqc` (Firmas Digitales y Autenticación Post-Cuántica)

**Fecha**: 1 de Septiembre de 2026  
**Alcance**: Módulo `pqc/` (`backends/`, `signatures/`, `protocol/`), integración con `liboqs-python` y suite de pruebas `tests/test_pqc/`.  
**Rol**: Revisor de código independiente.  
**Estado de la implementación**: No se han realizado modificaciones directas en el código fuente conforme a las directrices de revisión.

---

## 1. Resumen Ejecutivo y Alcance

Se ha realizado una auditoría estricta e independiente de la implementación de **criptografía post-cuántica (PQC)** y firmas digitales en el repositorio **QuantumSec**:
- **Capa `pqc/backends/`**: Adaptador de aislamiento para la biblioteca nativa `liboqs-python` (`oqs_backend.py`), gestión de contexto y ciclo de vida de memoria en C.
- **Capa `pqc/signatures/`**: Contratos independientes de backend (`base.py`), metadatos de algoritmos y proveedor concreto de firmas **ML-DSA-65** (FIPS 204) (`ml_dsa.py`).
- **Capa `pqc/protocol/`**: Identidades públicas y privadas (`identity.py`), almacén de confianza pre-aprovisionado fuera de banda (`trust.py`) y modelo de actores/partes autenticadas (`party.py`).
- **Jerarquía de Excepciones**: Errores específicos de dominio (`errors.py`).
- **Suite de Pruebas**: Tests unitarios y de integración con backend real (`tests/test_pqc/`).

### Resumen de Hallazgos

| Severidad | Cantidad | Descripción General |
| :--- | :---: | :--- |
| **CRITICAL** | 0 | No se identificaron vulnerabilidades criptográficas críticas en el uso del backend nativo de liboqs ni fugas de claves privadas. |
| **HIGH** | 2 | Acoplamiento de capacidades: la verificación de firmas exige una instancia de identidad privada, y `TrustedIdentityStore` está rígidamente ligado a un único algoritmo. |
| **MEDIUM** | 3 | Validación tardía de longitud de clave pública, sobrescritura silenciosa en el almacén de confianza y mutabilidad interna en dataclass marcada como `frozen=True`. |
| **LOW** | 4 | Metadatos de algoritmo incompletos (sin longitud de firma), sobrecarga redundante de `is_sig_enabled` en FFI, falta de helpers de serialización y casos límite de test no cubiertos. |

---

## 2. Tabla Resumen de Hallazgos

| ID | Severidad | Archivo / Componente | Categoría | Resumen del Problema |
| :--- | :--- | :--- | :--- | :--- |
| **H-01** | `HIGH` | `pqc/protocol/identity.py`, `party.py` | Diseño / Criptografía | La verificación de firmas está acoplada a identidades privadas (`MLDSAIdentity`); `PublicIdentity` no puede verificar directamente. |
| **H-02** | `HIGH` | `pqc/protocol/trust.py:23` | Diseño / Extensibilidad | `TrustedIdentityStore` codifica en duro `"ML-DSA-65"`, bloqueando el uso de otros algoritmos PQC o esquemas híbridos. |
| **M-01** | `MEDIUM` | `pqc/protocol/identity.py:20`, `trust.py:18` | Validación / Robustez | `PublicIdentity` y `TrustedIdentityStore` no validan la longitud de la clave pública al crearse/registrarse. |
| **M-02** | `MEDIUM` | `pqc/protocol/trust.py:18` (`trust`) | Seguridad / TOFU | `TrustedIdentityStore.trust()` sobrescribe identidades preexistentes de forma silenciosa sin control de reemplazo. |
| **M-03** | `MEDIUM` | `pqc/protocol/party.py:10` (`PQCParty`) | Diseño / Invariantes | `PQCParty` es `@dataclass(frozen=True)` pero muta in-place su almacén interno `_trusted_peers` mediante `trust_peer()`. |
| **L-01** | `LOW` | `pqc/signatures/base.py`, `ml_dsa.py` | Metadatos | `SignatureMetadata` no expone tamaños de clave/firma, y la constante de longitud de firma ML-DSA-65 (3309 B) no existe. |
| **L-02** | `LOW` | `pqc/backends/oqs_backend.py:58` | Rendimiento / FFI | `_new_signature` consulta `is_sig_enabled` en la biblioteca C en cada firma/verificación sin caché. |
| **L-03** | `LOW` | `pqc/protocol/identity.py` | Mantenibilidad | Ausencia de métodos de serialización estándar (`to_dict`, `from_dict`, `to_bytes`) para transporte/persistencia. |
| **L-04** | `LOW` | `tests/test_pqc/` | Calidad de Tests | Faltan tests para mensajes vacíos, nombres Unicode, simulación de backend no disponible y métodos del almacén de confianza. |

---

## 3. Análisis Detallado de Hallazgos

### [H-01] Acoplamiento de la verificación de firmas a identidades privadas con material secreto

1. **Archivo y función afectada**:
   - Archivos: `pqc/protocol/identity.py` (líneas 83–93, `MLDSAIdentity.verify`), `pqc/protocol/party.py` (líneas 58–63, `PQCParty.verify`) y `pqc/signatures/base.py` (líneas 30–65, `SignatureProvider`).

2. **Por qué es un problema**:
   En criptografía asimétrica, la verificación de una firma digital es una operación de solo lectura puramente pública: únicamente requiere la clave pública del firmante, el mensaje y la firma.
   En la arquitectura actual, `PublicIdentity` es un objeto puramente pasivo de datos (propietario, algoritmo, clave pública) sin capacidad de verificación. Para verificar una firma, la API exige disponer de una instancia de `MLDSAIdentity` (que encapsula una clave secreta propia) o de `PQCParty` (que delega en su identidad privada interna).
   Un actor que actúe exclusivamente como verificador, auditor, pasarela o monitor de tráfico pasivo (sin clave privada ni capacidad de firma) no puede verificar firmas sin generar innecesariamente un par de claves privadas completo o depender de la capa de bajo nivel `OQSSignatureBackend`.

3. **Escenario donde falla**:
   Un servicio de auditoría o nodo receptor pasivo que recibe la clave pública de Alice y un paquete firmado por ella:
   ```python
   # El auditor no tiene clave privada propia.
   alice_pub = PublicIdentity(owner="Alice", algorithm="ML-DSA-65", public_key=alice_pk_bytes)
   # alice_pub.verify(message, signature) -> AttributeError: 'PublicIdentity' object has no attribute 'verify'
   
   # Para verificar, se ve forzado a instanciar un firmante ficticio:
   auditor = MLDSAIdentity.generate("DummyAuditor")
   is_valid = auditor.verify(message, signature, alice_pub)
   ```

4. **Corrección propuesta**:
   - Desacoplar la verificación a nivel de interfaz:
     - Proporcionar un método `verify(message, signature) -> bool` directamente en `PublicIdentity` o a través de un `SignatureVerifier` independiente.
     - Implementar una función pública de nivel de módulo (ej. `verify_signature(identity: PublicIdentity, message: bytes, signature: bytes) -> bool`).

---

### [H-02] Acoplamiento rígido de algoritmo en `TrustedIdentityStore`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/trust.py`
   - Función: `TrustedIdentityStore.trust(self, identity: PublicIdentity)` (líneas 23–26).

2. **Por qué es un problema**:
   El método `trust()` comprueba explícitamente:
   ```python
   if identity.algorithm != ML_DSA_65_METADATA.name:
       raise UnsupportedAlgorithmError(
           f"Trusted identity {identity.owner!r} uses unsupported algorithm {identity.algorithm!r}."
       )
   ```
   Esta comprobación acopla una clase general de protocolo (`TrustedIdentityStore`) exclusivamente a un algoritmo concreto (`"ML-DSA-65"`). En un entorno heterogéneo o en fases posteriores donde se evalúen otros esquemas PQC (ML-DSA-44, ML-DSA-87, Falcon-512, SPHINCS+ o esquemas clásicos para pruebas comparativas), el almacén de confianza rechazará incondicionalmente cualquier identidad válida que no use exactamente ML-DSA-65.

3. **Escenario donde falla**:
   En un experimento de interoperabilidad o comparación de algoritmos PQC:
   ```python
   bob_party = PQCParty.create("Bob")
   charlie_falcon = PublicIdentity(owner="Charlie", algorithm="Falcon-512", public_key=falcon_pk)
   bob_party.trust_peer(charlie_falcon)  # Lanza UnsupportedAlgorithmError incondicionalmente
   ```

4. **Corrección propuesta**:
   Permitir que `TrustedIdentityStore` admita un conjunto de algoritmos soportados inyectable o configurable (ej. `supported_algorithms: frozenset[str] = field(...)`), o validar la compatibilidad contra un registro dinámico de proveedores de firma registrados.

---

### [M-01] Validación ausente de longitud de clave pública en `PublicIdentity` y `TrustedIdentityStore`

1. **Archivo y función afectada**:
   - Archivos: `pqc/protocol/identity.py` (líneas 27–41, `PublicIdentity.__post_init__`) y `pqc/protocol/trust.py` (líneas 18–28, `TrustedIdentityStore.trust`).

2. **Por qué es un problema**:
   `PublicIdentity` valida que `public_key` sea de tipo `bytes` y no esté vacío (`if not self.public_key: raise ValueError`), pero no valida su longitud en función del algoritmo indicado (por ejemplo, exactamente 1952 bytes para ML-DSA-65).
   Asimismo, `TrustedIdentityStore.trust` almacena la identidad sin comprobar su estructura.
   Como consecuencia, una clave pública corrupta o truncada puede crearse, transmitirse y registrarse como de confianza sin error, y el fallo solo se manifiesta tardíamente durante una verificación criptográfica en tiempo de ejecución (`MLDSA65.verify` lanzará un `ValueError`).

3. **Escenario donde falla**:
   ```python
   # Clave pública corrupta de 10 bytes:
   bad_identity = PublicIdentity(owner="Alice", algorithm="ML-DSA-65", public_key=b"1234567890")
   store = TrustedIdentityStore()
   store.trust(bad_identity)  # Se registra como de confianza sin error
   
   # En tiempo de ejecución al verificar:
   party.verify("Alice", b"hello", signature)  # Lanza ValueError: ML-DSA-65 public_key must contain 1952 bytes. Got 10.
   ```

4. **Corrección propuesta**:
   Validar la longitud de la clave pública en `PublicIdentity.__post_init__` o en `TrustedIdentityStore.trust` contra los metadatos del algoritmo especificado.

---

### [M-02] Sobrescritura silenciosa de identidades en `TrustedIdentityStore` sin flag de reemplazo

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/trust.py`
   - Función: `TrustedIdentityStore.trust` (líneas 18–28).

2. **Por qué es un problema**:
   La asignación `self._identities[identity.owner] = identity` reemplaza cualquier entrada previa para ese `owner` sin ninguna comprobación de colisión. En protocolos de seguridad con confianza pre-establecida fuera de banda, la sustitución no advertida de una clave pública de confianza (*key substitution*) es un vector de riesgo frente a errores de configuración o inyecciones indebidas de claves.

3. **Escenario donde falla**:
   Un script de inicialización o aprovisionamiento concurrente registra por error una segunda clave bajo el nombre `"Alice"`, sobrescribiendo la clave legítima anterior sin que se genere ningún aviso, error ni log de auditoría.

4. **Corrección propuesta**:
   Añadir un parámetro booleano `overwrite: bool = False` a `trust()`:
   ```python
   def trust(self, identity: PublicIdentity, *, overwrite: bool = False) -> None:
       if not overwrite and identity.owner in self._identities:
           raise ValueError(
               f"Identity for {identity.owner!r} is already trusted. Use overwrite=True to replace."
           )
       self._identities[identity.owner] = identity
   ```

---

### [M-03] Modelo de mutabilidad inconsistente en `PQCParty`

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/party.py`
   - Clase: `PQCParty` (líneas 10–28).

2. **Por qué es un problema**:
   `PQCParty` está decorada con `@dataclass(frozen=True, slots=True)`. La inmutabilidad (`frozen=True`) transmite al usuario y a otras capas que las instancias de `PQCParty` son objetos de valor inmutables y seguros frente a efectos colaterales.
   Sin embargo, el atributo `_trusted_peers` es un `TrustedIdentityStore` completamente mutable. El método `party.trust_peer(identity)` muta internamente el almacén en el mismo objeto.
   Esto genera un modelo híbrido confuso: el objeto bloquea la asignación de atributos pero permite mutaciones de estado interno que afectan a todas las referencias compartidas.

3. **Escenario donde falla**:
   Al realizar copias superficiales (`copy.copy(party)`) o compartir instancias de `PQCParty` entre diferentes hilos o contextos de simulación, la modificación de pares de confianza en un hilo altera inadvertidamente el almacén de los demás.

4. **Corrección propuesta**:
   - O bien documentar explícitamente y declarar `PQCParty` como clase mutable (`frozen=False`),
   - O bien hacer que `TrustedIdentityStore` y `PQCParty` sean verdaderamente inmutables, donde añadir un par devuelva una nueva instancia (`def with_trusted_peer(self, identity: PublicIdentity) -> Self:`).

---

### [L-01] Metadatos de algoritmo incompletos y ausencia de constante de longitud de firma

1. **Archivo y función afectada**:
   - Archivos: `pqc/signatures/base.py` (líneas 8–28, `SignatureMetadata`) y `pqc/signatures/ml_dsa.py` (líneas 9–18).

2. **Por qué es un problema**:
   `SignatureMetadata` define nombre, tipo, familia, categoría NIST y estandarización, pero no incluye los tamaños en bytes (`public_key_length`, `secret_key_length`, `signature_length`).
   En `ml_dsa.py` se definen de forma privada `_ML_DSA_65_PUBLIC_KEY_LENGTH` (1952) y `_ML_DSA_65_SECRET_KEY_LENGTH` (4032), pero la longitud estándar de una firma ML-DSA-65 (3309 bytes según FIPS 204) no está definida en ningún lugar del módulo.

3. **Escenario donde falla**:
   Cálculos de sobrecarga de comunicación, reserva de búferes de red o empaquetado de tramas autenticadas en capas superiores (ej. análisis de overhead en `experiments/`).

4. **Corrección propuesta**:
   Añadir `public_key_length: int`, `secret_key_length: int` y `signature_length: int` como campos de `SignatureMetadata`, y declarar `_ML_DSA_65_SIGNATURE_LENGTH: Final = 3309` en `ml_dsa.py`.

---

### [L-02] Sobrecarga redundante de comprobación FFI `is_sig_enabled` en cada operación

1. **Archivo y función afectada**:
   - Archivo: `pqc/backends/oqs_backend.py`
   - Función: `_new_signature` (líneas 58–72).

2. **Por qué es un problema**:
   Cada llamada a `sign()` o `verify()` ejecuta `_new_signature()`, la cual importa `oqs` y realiza una llamada FFI en C a `module.is_sig_enabled(algorithm)`.
   Dado que los algoritmos habilitados en la biblioteca C estática/dinámica son invariantes durante la ejecución del proceso de Python, invocar repetidamente esta función FFI en simulaciones que firman miles de mensajes genera una sobrecarga prescindible.

3. **Escenario donde falla**:
   Simulaciones de alto rendimiento con miles de mensajes autenticados por segundo.

4. **Corrección propuesta**:
   Cachear los algoritmos habilitados comprobados mediante un conjunto en memoria o `functools.lru_cache`.

---

### [L-03] Ausencia de métodos estándar de serialización / deserialización

1. **Archivo y función afectada**:
   - Archivo: `pqc/protocol/identity.py` (`PublicIdentity`, `MLDSAIdentity`).

2. **Por qué es un problema**:
   No se proporcionan métodos para exportar o importar identidades públicas a formatos estándar (representación hexadecimal, base64, JSON DTOs o bytes codificados). Esto complicará la integración con la API REST (`ui/backend`) y la persistencia en disco de identidades pre-aprovisionadas.

3. **Escenario donde falla**:
   Exportar el almacén de confianza a un archivo de configuración YAML/JSON o serializar `PublicIdentity` en respuestas HTTP de FastAPI.

4. **Corrección propuesta**:
   Añadir métodos `to_dict()`, `from_dict()`, `to_hex()` o `from_hex()` en `PublicIdentity`.

---

### [L-04] Casos límite ausentes en la suite de pruebas de PQC

1. **Archivo y función afectada**:
   - Archivos: `tests/test_pqc/test_identity.py`, `test_ml_dsa.py`, `test_party.py`.

2. **Por qué es un problema**:
   Los 14 tests existentes cubren los flujos nominales principales de manera limpia, pero presentan lagunas en casos límite:
   - Firma y verificación de un mensaje vacío `b""`.
   - Nombres de identidad con caracteres no ASCII / Unicode (`"Álvaro"`, `"Bób"`).
   - Simulación del fallo de carga del backend (`BackendUnavailableError`) cuando `oqs` no está instalado o falla su inicialización.
   - Verificación de los métodos de colección de `TrustedIdentityStore` (`__len__`, `__iter__`, `owners`).

3. **Escenario donde falla**:
   Regresiones no detectadas al procesar payloads vacíos, nombres internacionalizados o despliegues en entornos donde liboqs no esté disponible en el sistema operativo.

4. **Corrección propuesta**:
   Añadir tests unitarios específicos para mensajes vacíos, nombres Unicode y mocking de fallo de carga de `oqs`.

---

## 4. Evaluación de Invariantes y Principios de Diseño

1. **Aislamiento de Criptografía Post-Cuántica (PQC Layer Boundary)**:
   - **Cumplimiento**: **Excelente**.
   - `pqc/` no importa nada de `qkd`, `quantum`, `experiments` ni `ui`.
   - Se respetan estrictamente las dependencias de capa unidireccionales.

2. **Gestión Segura de Memoria y Ciclo de Vida en C (liboqs)**:
   - **Cumplimiento**: **Muy Bueno**.
   - `OQSSignatureBackend` utiliza gestores de contexto (`with signer:`) asegurando que los punteros C (`OQS_SIG`) se liberen mediante `OQS_SIG_free`.
   - Las claves y firmas se copian defensivamente a buffers de Python `bytes` antes de salir del bloque de contexto.

3. **Protección de Claves Privadas**:
   - **Cumplimiento**: **Excelente**.
   - `PublicIdentity` no contiene referencias a material secreto ni métodos de firma.
   - `MLDSA65` y `MLDSAIdentity` excluyen explícitamente `_secret_key` de su representación textual (`__repr__`), evitando fugas accidentales en logs.
   - El generador de números aleatorios utilizado para las claves criptográficas proviene exclusivamente de `liboqs` / CSPRNG del SO (no de PRNGs reproducibles de simulación como `SeededRNG`).

4. **Modelo de Confianza Explícita**:
   - **Cumplimiento**: **Excelente**.
   - Ninguna clave pública recibida se asume confiable de forma automática; `PQCParty` exige aprovisionamiento previo en `TrustedIdentityStore`.

---

## 5. Conclusiones y Recomendaciones de Priorización

La implementación de firmas post-cuánticas ML-DSA-65 en `pqc/` proporciona una base sólida, segura y bien aislada para la autenticación de entidades.

Se recomienda priorizar las mejoras en el siguiente orden:
1. **Prioridad 1 (Diseño e Interfaz Criptográfica)**:
   - Desacoplar la capacidad de verificación para que `PublicIdentity` pueda verificar firmas sin requerir una clave privada (**H-01**).
   - Flexibilizar `TrustedIdentityStore` para soportar múltiples algoritmos PQC (**H-02**).
2. **Prioridad 2 (Validación y Robustez)**:
   - Validar la longitud de la clave pública en la construcción de `PublicIdentity` (**M-01**).
   - Añadir salvaguarda contra sobrescrituras silenciosas en el almacén de confianza (**M-02**).
   - Clarificar el modelo de mutabilidad de `PQCParty` (**M-03**).
3. **Prioridad 3 (Metadatos, Rendimiento y Pruebas)**:
   - Añadir tamaños de clave y firma a `SignatureMetadata` (**L-01**).
   - Cachear la verificación de algoritmos habilitados en `oqs_backend` (**L-02**).
   - Añadir métodos de serialización en `PublicIdentity` (**L-03**).
   - Ampliar la suite de pruebas con casos límite y mensajes vacíos (**L-04**).
