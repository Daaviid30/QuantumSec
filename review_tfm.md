# Revisión independiente del TFM — QuantumSec

> **Historical review snapshot.** This report motivated the definitive TFM contract but does not
> describe current implementation status after later changes. Use code/tests, `README.md`,
> `TFM_GOAL.md`, and `docs/structure.md` as sources of truth.

> **Rol:** reviewer independiente de Trabajo Fin de Máster en Ciberseguridad (PQC, QKD,
> establecimiento híbrido de claves, ingeniería de protocolos criptográficos, investigación
> experimental, arquitectura software, investigación reproducible).
>
> **Fecha de revisión:** 2026-09-05
> **Commit base:** `6a763e6` (documentation refactor + serena + graphify update)
> **Entorno verificado:** Python 3.14, liboqs 0.16.0, 547 tests en 7,55 s

## Nota de procedimiento

- **Búsqueda web:** utilizada solo con consultas genéricas sobre estándares públicos (NIST, ETSI,
  IETF). No se introdujo en ninguna consulta el nombre del proyecto, código, ni contenido del
  repositorio.
- **Verificación:** esta revisión no se apoya en la documentación. Se ejecutó la suite completa, se
  cronometró BB84 y los handshakes PQC reales sobre liboqs 0.16.0, y se midió el QBER resuelto por
  base. Todos los números citados son **medidos**, no estimados.

---

## Executive Assessment

El software está claramente por encima de la media de un TFM: ~7.800 líneas de Python de
producción, ~5.200 de tests, 547 tests verdes, y una ingeniería criptográfica cuidadosa (transcript
canónico, separación de dominios HKDF, `K_CONFIRM` distinto de `K_SESSION`, Finished encadenados,
comparaciones en tiempo constante, estados secretos con ciclo de vida explícito). La documentación
tras el refactor es **honesta**: se buscaron activamente exageraciones y se encontraron muy pocas.

El problema no es el software. **El problema es que la tesis, tal y como está formulada, no es una
investigación: es la memoria descriptiva de un producto.**

Tres hallazgos dominan esta revisión:

### 1. La pregunta de investigación no es empírica

«¿Cómo pueden integrarse QKD y PQC en un laboratorio común y reproducible para comparar...?» es una
pregunta de **diseño**. Su respuesta es el propio repositorio. No es falsable, no produce números, y
un tribunal puede responderla mirando el README. Es exactamente el fallo que se quería evitar
(«Yes, they can be integrated»), solo que camuflado un nivel más arriba.

### 2. No existe adversario en ninguna parte del código

`grep -ri "eve|intercept|eavesdrop"` sobre todo el repositorio: cero coincidencias en `qkd/`,
`pqc/` y `ui/`. QKD tiene *una* propuesta de valor —que espiar sube el QBER— y el laboratorio no
puede demostrarla. El experimento «BB84 channel behaviour» sin Eve mide únicamente ruido→QBER, que
en los canales implementados es una identidad analítica cerrada (`QBER = p/2` para despolarizante,
bit-flip y phase-flip). No es un descubrimiento: es una comprobación de que NumPy sabe multiplicar
matrices.

### 3. Existe un fallo real en el modelo de seguridad de QKD, no documentado

`asymptotic_bb84_secret_length()` usa el QBER muestreado agregado como estimador de la tasa de error
de fase. Eso solo es válido si el canal es simétrico entre bases. Dos de los canales implementados
no lo son. Demostración medida:

```text
PhaseFlipChannel(p=0.16), n=40.000:
  e_Z = 0.0000    e_X = 0.1602    QBER agrupado = 0.0794

Sesión: status=completed, sampledQBER=0.0814, n_candidate=15.972,
        leak_ec=7.783, n_final=1.672 bits extraídos

  tasa usada    (1 - h(Q_agrupado)) = 0.5930
  tasa correcta (1 - h(e_X))        = 0.3651
  cota Shor-Preskill correcta       = 0 bits
```

El simulador **extrae 1.672 bits de clave donde la cota asintótica correcta permite 0**. No es
conservador; es no-conservador, que es la dirección peligrosa. Con `AmplitudeDampingChannel(0.20)`
se midió `e_Z=10.5%` vs `e_X=5.2%` (asimetría 2×, en este caso hacia el lado seguro). Con
`PauliChannel(pz > px)` vuelve a ser inseguro.

Esto es, paradójicamente, **la mejor noticia del informe**: es un resultado de tesis. Un TFM que
*encuentra, cuantifica y corrige* una violación de supuesto en su propio estimador vale mucho más
que uno que solo integra piezas.

### Veredicto resumido

La dirección conceptual es defendible pero está mal enfocada. No hay que rehacer nada. Hay que
**girar el eje del «qué construí» al «qué medí»**, añadir un adversario (que cuesta ~30 líneas
gracias a que ya existe `KrausChannel`), y cortar sin piedad la web.

---

## What QuantumSec Really Is Today

Clasificación verificada contra el código y los tests, no contra la documentación:

| Componente | Estado real | Evidencia |
|---|---|---|
| `core` (RNG inyectable, `SeededRNG`) | **IMPLEMENTED** | 138 LOC, 21 tests |
| `quantum` (álgebra, medidas proyectivas, entropías) | **IMPLEMENTED** | 769 LOC, 49 tests |
| BB84 prepare-and-measure + sifting | **IMPLEMENTED** | ejecutado: 20k señales en 3,77 s |
| Canales CPTP (Identity, Depol, BitFlip, PhaseFlip, Pauli, AmpDamp) | **IMPLEMENTED** | Kraus validado en construcción |
| Estimación QBER muestreada + abortos | **IMPLEMENTED** | 6 rutas de aborto |
| Cascade + verificación por hash universal | **IMPLEMENTED** | leakage contabilizado |
| Amplificación de privacidad Toeplitz-FFT | **IMPLEMENTED** | sin materializar la matriz |
| Estimador de longitud secreta | **PARTIAL / con defecto** | supuesto de simetría violado (arriba) |
| ML-KEM-768 + HQC-3 vía liboqs | **IMPLEMENTED** | medido: 0,27/0,30/0,37 ms y 21/47/67 ms |
| ML-DSA-65 identidades + confianza pre-provisionada | **IMPLEMENTED** | sin PKI, sin certificados, sin revocación |
| Handshake PQC completo (6 fases, Finished mutuo) | **IMPLEMENTED** | LOW 16,5 ms · HIGH 149 ms |
| Combinador canónico de secretos KEM | **IMPLEMENTED** | dominio, orden fijo, longitudes prefijadas |
| **Eavesdropper / modelo de atacante** | **AUSENTE** | grep: 0 coincidencias |
| **Autenticación del canal clásico QKD** | **AUSENTE (es un supuesto)** | documentado, no implementado |
| **Híbrido QKD-PQC** | **PLANNED** | 0 líneas |
| **AES-256-GCM** | **PLANNED** | 0 líneas (`cryptography` ya es dependencia) |
| **Motor de experimentos** | **PLANNED** | 0 líneas; `benchmarks/` solo mide medida proyectiva |
| Web: BB84 builder + resultados | **IMPLEMENTED** | 1.926 LOC TS, 3 endpoints |
| Web: PQC / híbrido / comparación / demo | **PLANNED** | 0 endpoints |
| Quantum-Safe Explorer | **PLANNED (y prescindible)** | — |

**Traducción honesta:** hoy hay **dos laboratorios excelentes que no se hablan**, más una UI para
uno de ellos. La expresión «laboratorio unificado» describe una intención, no un artefacto.

### Métricas medidas de referencia

```text
BB84 (SeededRNG, DepolarizingChannel(0.04)):
  n=  1.000   0.231 s   sifted=  478   final=  232   frac=0.2320
  n=  5.000   0.929 s   sifted=2.446   final=1.278   frac=0.2556
  n= 20.000   3.774 s   sifted=10.020  final=5.703   frac=0.2852
  => ~190 us por señal; n=100.000 ~ 19 s

Primitivas PQC (liboqs 0.16.0, medianas):
  ML-KEM-768  keygen 0.269 ms  encap 0.304 ms  decap 0.367 ms  pk 1184 B  ct 1088 B  ss 32 B
  HQC-3       keygen 20.7  ms  encap 46.9  ms  decap 66.8  ms  pk 4514 B  ct 8978 B  ss 32 B
  ML-DSA-65   keygen 2.324 ms  sign  8.827 ms  verify 2.598 ms pk 1952 B  sig 3309 B

  HQC-3 dispersión: encap p10=40.4 / p90=94.6 ms ; decap p10=57.8 / p90=148.4 ms

Handshake completo (incluye 2 identidades ML-DSA):
  LOW  (PQC-BASE)     mediana  16.5 ms   JSON total 12.611 B
  HIGH (PQC-DIVERSE)  mediana 149.1 ms   JSON total 30.607 B
  => x9.0 en tiempo, x2.43 en bytes

QBER resuelto por base:
  Depolarizing p=0.08     e_Z=0.0363  e_X=0.0394  agregado=0.0378  (~ p/2, simétrico)
  AmplitudeDamping g=0.20 e_Z=0.1050  e_X=0.0517  agregado=0.0782  (asimétrico)
  AmplitudeDamping g=0.40 e_Z=0.1992  e_X=0.1130  agregado=0.1559  (asimétrico)
  PhaseFlip p=0.16        e_Z=0.0000  e_X=0.1602  agregado=0.0794  (asimétrico, INSEGURO)
```

---

## Strongest Thesis Contribution

Ranking de mayor a menor fuerza defensiva ante un tribunal:

| # | Contribución | Fuerza | Por qué |
|---|---|---|---|
| 1 | **Cierre de la brecha de autenticación QKD mediante PQC, con coste medido** | ★★★★★ | Problema real, reconocido en la literatura, resoluble con lo que ya existe, y produce números |
| 2 | **Modelo cuantitativo del coste de cada incremento de garantía quantum-safe** | ★★★★★ | Los datos ya existen: HQC cuesta ×9 en tiempo y ×2,4 en bytes |
| 3 | **Validación del simulador BB84 contra predicción analítica + detección del fallo de simetría** | ★★★★☆ | Falsable, corregible, autocrítico. Oro en un tribunal |
| 4 | Diversificación de secretos (ML-KEM + HQC) con encoding canónico y coste medido | ★★★★☆ | Construcción defendible + datos duros |
| 5 | Establecimiento de sesión híbrido QKD-PQC con procedencia explícita | ★★★☆☆ | Necesario, pero por sí solo responde «sí, se puede» |
| 6 | Arquitectura común / agilidad criptográfica / perfiles | ★★★☆☆ | Ingeniería sólida, no investigación |
| 7 | Reproducibilidad (semillas inyectadas, snapshots de configuración) | ★★★☆☆ | Metodología correcta, pero «usé semillas» es delgado como aportación |
| 8 | Framework de experimentos | ★★☆☆☆ | Medio, no fin |
| 9 | Sesión segura extremo a extremo (AES-GCM) | ★★☆☆☆ | Imprescindible como demo, nulo como aportación |
| 10 | Visualización de protocolo | ★★☆☆☆ | Valor pedagógico, no científico |
| 11 | Laboratorio educativo | ★☆☆☆☆ | No se defiende un máster con esto |
| 12 | Benchmarking genérico | ★☆☆☆☆ | Sin pregunta detrás, es una tabla de números |

**Contribución principal recomendada:**

> *QuantumSec identifica y cierra la brecha de autenticación entre QKD y PQC dentro de una
> arquitectura única, y cuantifica el precio de cada incremento de garantía quantum-safe
> (autenticación PQC, diversificación de KEM, composición híbrida) en latencia de handshake, bytes
> en el cable y rendimiento de clave.*

**Por qué esta y no «integración híbrida»:** porque «integré QKD y PQC» es una afirmación de
existencia. «El canal clásico de BB84 estaba asumido como autenticado y ahora lo autentico
realmente con ML-DSA-65, y eso cuesta X ms y Y bytes» es una afirmación **medible, no trivial y con
un antes y un después**.

Además es la contribución que mejor reutiliza lo existente: `pqc/signatures/ml_dsa.py` ya firma y
verifica, y `qkd/postprocessing/universal_hashing.py` ya implementa hashing Toeplitz universal —que
es exactamente la primitiva de un MAC Wegman–Carter incondicionalmente seguro. Las dos mitades ya
están en el repositorio; solo falta el cable entre ellas.

**Secundarias (en la memoria, en este orden):** #2, #3, #4, luego #6 y #7 como capítulo de
ingeniería/metodología, y #9-#10 como demostrador.

---

## Problems I Found

### Críticos

**P1 — El estimador de longitud secreta viola su propio supuesto.**
`qkd/metrics/security.py:39` usa `estimated_qber` (agregado sobre ambas bases) como tasa de error de
fase. `PhaseFlipChannel` y `PauliChannel` con `pz > px` producen `e_X >> e_Z`, y el resultado es
sobre-extracción de clave (medido: 1.672 bits donde la cota correcta da 0). El docstring dice
«assumes a symmetric phase-error rate» pero nada lo comprueba ni lo impide.

**P2 — No existe adversario.** Sin Eve, la mitad QKD del TFM no tiene ningún experimento de
seguridad. El aborto por QBER nunca se dispara por la razón por la que existe.

**P3 — La pregunta de investigación no genera datos.** Ver `TFM_GOAL.md §3`. Es una pregunta de
arquitectura.

**P4 — «QKD vs PQC vs híbrido» es una comparación inválida tal y como está planteada.** Comparar
3,77 s de bucle NumPy sobre 20.000 qubits con 0,30 ms de `encap_secret()` en C no es una
comparación: es una tabla que un tribunal atacará en la primera pregunta. Son unidades distintas,
planos distintos y supuestos distintos.

### Importantes

**P5 — El experimento BB84 propuesto es analíticamente trivial.** Confirmado numéricamente:
`DepolarizingChannel(0.08)` → QBER medido 3,78% ≈ p/2 = 4%. La curva es una recta conocida de
antemano.

**P6 — No hay intervalo de confianza sobre el QBER muestreado.** `estimate_qber_from_sample`
devuelve una estimación puntual sobre el 20% de los bits sifted, y la decisión de abortar y la
longitud de clave se toman con ella sin cota superior ni probabilidad de fallo.
`security_margin_bits` existe como gancho pero vale `0` por defecto.

**P7 — El tag de verificación por defecto son 16 bits**
(`BB84PostprocessingConfig.verification_tag_length = 16`), es decir una probabilidad de error
residual no detectado de ~2⁻¹⁶ ≈ 1,5·10⁻⁵. Insuficiente para presentarlo como confirmación de clave
en una tesis.

**P8 — Alice no tiene política de perfil.** `ServerKeyOfferProcessor.process()`
(`pqc/protocol/initiator.py:106`) acepta el perfil que Bob firme, sin parámetro de perfiles
aceptables ni mínimo exigible. No es explotable por red (la oferta va firmada) pero es una omisión
de ingeniería de protocolos que un tribunal técnico verá.

**P9 — El coste de provisión se está midiendo como coste de sesión.** `create_phase5_flow()` incluye
dos `PQCParty.create()` (2,3 ms cada uno de keygen ML-DSA) dentro de lo cronometrado. Sobre 16,5 ms
de handshake LOW eso es ~9% atribuido mal. La generación de identidad es coste único, no por sesión.

**P10 — HQC-3 tiene una varianza de tiempo enorme.** Medido sobre 50 repeticiones: encap p10=40,4 ms
/ p90=94,6 ms; decap p10=57,8 ms / p90=148,4 ms. Ratio p90/p10 ≈ 2,3–2,6. Cualquier experimento que
reporte **medias** sobre HQC producirá números sin sentido. Obligatorio: medianas, IQR y n≥30.

**P11 — Alcance irrealizable.** Quedan cinco paquetes de trabajo abiertos (híbrido, AES-GCM, motor
de experimentos, cuatro workspaces web, campaña experimental + memoria). Algo va a quedar a medias.
Mejor decidirlo ahora que descubrirlo en abril.

### Menores

**P12 —** 100.000 señales ≈ 19 s de petición HTTP síncrona sin streaming ni progreso. Riesgo real
durante la defensa.

**P13 —** `benchmarks/` (98 LOC, solo medida proyectiva) y `reports/01..24` son restos de la fase
anterior; no sirven al TFM y confunden al lector.

**P14 —** La documentación se ha vuelto tan defensiva que la **afirmación desaparece**. Ver sección
de documentación.

---

## Security Concerns / Overclaims

Se buscaron overclaims agresivamente. La mayoría ya están corregidos. Lo que queda:

### Combinador híbrido — el punto más delicado

Cualquier frase equivalente a *«si al menos un secreto de origen permanece seguro, la clave de
sesión combinada permanece segura»* **no puede afirmarse sin más**. Desglose:

**Qué combinador permitiría esa propiedad.** La familia analizada: el *concatenation combiner* de
Giacon–Heuer–Poettering (PKC 2018) y los *split-key PRF* de Bindel et al. (PQCrypto 2019). La
propiedad requiere:

1. codificación **inyectiva** de los componentes (para que no exista ambigüedad `s1||s2` vs
   `s1'||s2'`);
2. la KDF modelada como **oráculo aleatorio** o como PRF de clave dividida;
3. **binding de los ciphertexts** en la entrada de derivación.

**Qué cumple la implementación actual.**

- (1) ✅ — `canonical_kem_secret_input()` prefija dominio, número de componentes, orden fijo,
  identificadores y longitudes; la codificación es inyectiva.
- (3) ✅ **indirectamente** — los ciphertexts no van en el IKM, pero entran por el `salt` = hash del
  transcript firmado, que los contiene. Es la misma estructura que usa TLS 1.3 híbrido.
- (2) es un **supuesto**, no algo demostrado.

Ojo con SP 800-227 (final, sept. 2025): recomienda la forma `K = KDF(ss1 || ss2 || ct1 || ct2)` con
separación explícita entre entradas. QuantumSec cumple el espíritu (binding vía salt, separación vía
prefijos de longitud) pero **no la letra**. Eso hay que argumentarlo en la memoria, no ocultarlo —y
es un párrafo excelente.

**Lenguaje académico exacto que sí puede usarse:**

> «La entrada de derivación de QuantumSec sigue la familia de combinadores por concatenación
> analizada por Giacon, Heuer y Poettering (PKC 2018) y el marco de PRF de clave dividida de Bindel
> et al. (PQCrypto 2019). Nuestra codificación es inyectiva por construcción, y los ciphertexts
> quedan ligados mediante el hash del transcript autenticado empleado como *salt* de HKDF-SHA-384,
> siguiendo el patrón de TLS 1.3 híbrido. Bajo el supuesto de que HKDF-SHA-384 se comporta como PRF
> de clave dividida, la clave derivada es indistinguible mientras al menos una entrada componente
> sea impredecible. **Este trabajo implementa y ejerce esa construcción; no aporta una demostración
> formal nueva ni verifica mecánicamente el supuesto.**»

**Punto que casi nadie ve y que suma puntos:** combinar material QKD (seguro en sentido
**teórico-informacional**) con un secreto KEM mediante una KDF **computacional destruye la propiedad
ITS**. El resultado es, como mucho, computacionalmente seguro. Debe escribirse explícitamente. Y es
precisamente el argumento que justifica la Mejora 2: el papel valioso del material QKD no es ser un
IKM más, sino **autenticar** el canal con un MAC Wegman–Carter incondicional, donde la propiedad ITS
sí se conserva.

### QKD

- El umbral `0.11` es la cota asintótica de Shor–Preskill para post-procesado unidireccional. Nunca
  presentarlo como umbral operativo. Ya está bien documentado; mantener así.
- «Canal clásico autenticado» debe aparecer siempre marcado como **supuesto no ejecutado**, y la UI
  debe mostrarlo. Hoy la documentación lo dice; el código no lo representa.
- `AmplitudeDampingChannel` **no es pérdida óptica**. Ya se dice tres veces. Correcto. No decirlo una
  cuarta.
- Añadir: el simulador no modela pérdidas, dark counts, detecciones múltiples ni ataques PNS, por lo
  que **no puede pronunciarse sobre distancia, tasa de clave ni seguridad de implementación**.

### PQC

- Terminología: decir **«NIST security category 3»** para ML-KEM-768 y ML-DSA-65. Nunca «192 bits de
  seguridad».
- Nombres: ML-KEM (FIPS 203) y ML-DSA (FIPS 204), publicados 2024-08-13. Nunca Kyber/Dilithium salvo
  en contexto histórico. Verificado: en el repo no aparecen. Bien.
- Distinguir siempre: ML-KEM **establece** secreto, ML-DSA **autentica**, HKDF **deriva**, AES-GCM
  **protege**. Ninguno cifra por sí solo la carga útil. Ya se hace.

### HQC

Estado verificado: **seleccionado para estandarización el 11-03-2025** (documentado en NIST IR
8545). El borrador de FIPS **no consta publicado** en la página oficial de estandarización PQC de
NIST consultada; las fuentes secundarias sitúan el draft en 2026 y el final en 2027. Clasificación
correcta para la memoria: **SELECTED FOR STANDARDIZATION**, no STANDARDIZED, no DRAFT.

Advertencia adicional: **`HQC-3` es un nombre de algoritmo de liboqs, no un nombre de conjunto de
parámetros de NIST.** Cuando salga el FIPS el nombre cambiará. Escribir: *«el conjunto de parámetros
expuesto por liboqs 0.16.0 como `HQC-3`»*.

### Key confirmation

El análisis actual es correcto y no hace falta tocarlo. Los Finished demuestran que el par calculó el
mismo `K_CONFIRM` → autenticación explícita de clave y confirmación mutua. **No** demuestran a Alice
que Bob aceptó `Finished_A` (falta el tercer flight). Ya se documenta con precisión en
`docs/structure.md §5.4`. Mantener tal cual: es un ejemplo de honestidad que juega a favor.

### AES-GCM (aún no implementado — requisitos para cuando se haga)

- **Clave:** los 32 bytes de `K_SESSION` exportados de `EstablishedPQCSession`, nunca un valor
  público o no confirmado.
- **Nonce:** 96 bits. Con nonces aleatorios, límite de 2³² mensajes por clave; **preferible contador
  por rol** (`role_byte || counter`) que hace la repetición estructuralmente imposible. Un test debe
  demostrar que dos cifrados consecutivos producen nonces distintos.
- **Tag:** 128 bits completos. Nunca truncar.
- **AAD:** ligar `session_id || profile || transcript_hash`. Recordar y documentar que **el AAD se
  autentica pero no se cifra**.
- **Matriz de manipulación** (tres tests independientes, no uno): (a) flip de un byte del ciphertext,
  (b) flip de un byte del tag, (c) modificación del AAD. Los tres deben producir `InvalidTag` y
  **ningún plaintext parcial**.

---

## Recommended Research Question

### La actual (para contraste)

> «¿Cómo pueden integrarse rutas QKD y PQC implementadas, junto con composiciones híbridas
> explícitamente especificadas, en un laboratorio común y reproducible para comparar su
> comportamiento, supuestos de seguridad y sobrecarga operativa?»

Problema: pregunta de diseño, no falsable, se responde enseñando el repositorio.

### Recomendada

> **¿Cuál es el coste medible —en latencia de handshake, bytes intercambiados y rendimiento de
> clave— de cada incremento de garantía quantum-safe (autenticación post-cuántica, diversificación
> de KEM, composición híbrida con material QKD), y bajo qué condiciones de canal y de adversario
> deja de ser rentable cada incremento?**

Por qué es mejor: tiene **variables independientes** (nivel de garantía, parámetro de canal, fracción
de intercepción), **variables dependientes numéricas** (ms, bytes, bits/señal), admite un **«no»**
como respuesta, y produce conclusiones no triviales (p. ej. «la diversificación con HQC-3 multiplica
por 9 el tiempo de handshake para una diversidad matemática cuyo beneficio no es cuantificable con
estas métricas — es una decisión de política, no de rendimiento»).

### Subpreguntas

**SQ1 — Descomposición del coste PQC.** ¿Cómo se reparte el coste del handshake entre generación de
claves, firma, verificación, encapsulación, decapsulación, combinador, HKDF y Finished, y qué
operación domina en cada perfil?
*Respuesta ya medida: en HIGH, HQC-3 (keygen 21 ms + encap 47 ms + decap 67 ms ≈ 135 ms) representa
>90% del handshake de 149 ms. En LOW domina ML-DSA sign (8,8 ms de 16,5 ms).*

**SQ2 — Coste en el cable.** ¿Cuál es el coste real en bytes de cada perfil, distinguiendo tamaño
criptográfico canónico de tamaño de codificación de transporte?
*Medido: LOW 12.611 B de JSON, HIGH 30.607 B (×2,43). Base64 infla un 33%.*

**SQ3 — Validez del simulador.** ¿Reproduce el simulador BB84 las predicciones analíticas de QBER de
sus canales, y qué supuestos del estimador de longitud secreta se rompen cuando el canal no es
simétrico entre bases?
*Aquí vive el hallazgo del phase-flip. Es la subpregunta con más valor científico.*

**SQ4 — Detección de adversario.** ¿A partir de qué fracción de intercepción el aborto por QBER se
dispara de forma fiable, y cómo se compara la fracción detectada con la predicción teórica del 25%
de intercept-resend?

**SQ5 — Coste del supuesto de autenticación.** ¿Qué cuesta —en ms y bytes— sustituir el supuesto de
«canal clásico autenticado» de BB84 por autenticación real con ML-DSA-65, y qué cuesta continuar esa
autenticación con MACs Wegman–Carter alimentados por la propia clave QKD?

**SQ6 — Sobrecarga marginal del híbrido.** ¿Cuál es el coste adicional de la composición híbrida por
encima de la suma de sus partes (combinador + HKDF + confirmación)?
*Hipótesis falsable: < 1 ms, es decir, despreciable frente a HQC. Si se confirma, es una conclusión
útil: el híbrido no cuesta por combinar, cuesta por lo que combina.*

---

## Experimental Design Review

### Revisión transversal

**Confusores a controlar en todos los experimentos PQC:**

- generación de identidad ML-DSA **fuera** del cronómetro (P9);
- calentamiento de liboqs: descartar las 5 primeras repeticiones;
- gestión térmica/turbo de la CPU: aleatorizar el orden de las condiciones, no ejecutar «todo LOW y
  luego todo HIGH»;
- serialización JSON/Base64 medida por separado del coste criptográfico;
- versión de liboqs, del wrapper Python, CPU y SO registrados en cada récord (hoy: liboqs 0.16.0).

**Tratamiento estadístico obligatorio:** n≥30 por condición, reportar **mediana + IQR**, nunca
media±desviación (P10 lo hace inevitable). Para diferencias entre perfiles usar Mann–Whitney U, no
t-test — las distribuciones de tiempo criptográfico tienen cola derecha larga. Para QBER, intervalos
de Clopper–Pearson (binomial exacto), no aproximación normal.

**Comparación inválida a prohibirse explícitamente:** poner en la misma tabla, misma columna y mismas
unidades el tiempo de BB84 y el tiempo de ML-KEM. Si aparece esa tabla, la defensa se irá en
explicarla.

### Cómo comparar QKD vs PQC vs híbrido correctamente

No compararlos en **rendimiento**. Compararlos en **tres ejes ortogonales**, cada uno con su propia
tabla:

| Eje | QKD (simulado) | PQC | Híbrido |
|---|---|---|---|
| **Supuestos de seguridad** (cualitativo) | ITS bajo supuestos de dispositivo; requiere canal clásico autenticado | Computacional (lattice / código); autenticación por firma | Intersección: computacional tras la KDF |
| **Rendimiento de clave** | bits/señal cuántica — medible | bits/handshake (fijo: 256) | 256 bits, con procedencia registrada |
| **Coste en el cable** (bytes) | tráfico clásico de post-procesado | mensajes de handshake | suma + combinador |

El **tiempo** solo es comparable **dentro** del dominio PQC (todo es liboqs real). El tiempo QKD es
tiempo de NumPy y solo sirve para comparar configuraciones del simulador entre sí.

### E1 — Descomposición del coste PQC

**Operaciones que deben medirse por separado:**

| Operación | Medir | Notas |
|---|---|---|
| Generación de identidad ML-DSA-65 | Sí, **aparte** | Coste de provisión, no de sesión |
| Generación de clave efímera KEM | Sí | Por algoritmo (ML-KEM, HQC) |
| Firma ML-DSA (ServerKeyOffer) | Sí | 8,8 ms medidos |
| Verificación ML-DSA (×2) | Sí | 2,6 ms cada una |
| Encapsulación | Sí, por algoritmo | ML-KEM 0,30 ms · HQC 47 ms |
| Decapsulación | Sí, por algoritmo | ML-KEM 0,37 ms · HQC 67 ms |
| Construcción del transcript + SHA-384 | Sí | Debería ser <0,1 ms |
| Combinador canónico | Sí | Hipótesis: despreciable |
| HKDF-SHA-384 (×2: sesión + confirmación) | Sí | |
| Generación Finished (HMAC) | Sí | |
| Verificación Finished | Sí | |
| **Handshake total** | Sí | Debe ≈ suma de las partes; la diferencia es overhead de orquestación |

- *Variables independientes:* perfil (LOW/HIGH), rol (iniciador/respondedor).
- *Variables dependientes:* mediana e IQR de cada operación.
- *Control:* la suma de fases debe reconciliar con el total (±5%). Si no, hay coste oculto.
- *Repeticiones:* 50 por perfil, orden aleatorizado, 5 de calentamiento descartadas.
- *Figuras:* barras apiladas por perfil (una barra = un handshake, segmentos = fases). Es **la figura
  más citable de la tesis**.
- *Conclusión legítima:* «en el perfil diversificado, HQC-3 concentra >90% del tiempo de handshake;
  la diversificación es un coste de KEM, no de arquitectura».
- *Conclusión ilegítima:* cualquier cosa sobre «HQC es lento» como propiedad del algoritmo — es una
  propiedad de **esta implementación en esta versión de liboqs en esta CPU**.

### E2 — Coste en el cable

| Magnitud | Cómo | Valor medido |
|---|---|---|
| Claves públicas | `len()` de los bytes crudos | ML-KEM 1184 B · HQC 4514 B · ML-DSA 1952 B |
| Ciphertexts | bytes crudos | ML-KEM 1088 B · HQC 8978 B |
| Firmas | bytes crudos | ML-DSA-65 3309 B |
| **Mensaje de protocolo canónico** | `canonical_bytes()` | offer LOW 1313 B · offer HIGH 5841 B |
| **Mensaje serializado (transporte)** | `len(json.dumps(msg.to_dict()))` | — |
| **Total intercambiado** | suma de todos los mensajes, ambas direcciones | **LOW 12.611 B · HIGH 30.607 B** |

Regla metodológica: reportar **siempre las dos** cifras (canónica y serializada) y explicar el factor
4/3 de Base64. Un tribunal que vea solo la cifra JSON preguntará por qué ML-KEM-768 «ocupa 6 KB».

- *Repeticiones:* 10 (los tamaños son deterministas salvo el nonce; sirve para confirmarlo).
- *Figura:* barras apiladas por mensaje y por componente.
- *Conclusión legítima:* «la diversificación multiplica por 2,43 el tráfico de establecimiento».

### E3 — Validación del simulador BB84 (reemplaza «BB84 channel behaviour»)

Este es el experimento que salva la mitad QKD del TFM.

- *Variables independientes:* tipo de canal (6), parámetro del canal (10 niveles), `n_signals` (3
  niveles), semilla (30).
- *Variables dependientes:* QBER **resuelto por base** (`e_Z`, `e_X`) y agregado, eficiencia de
  sifting, `n_final`, fracción secreta.
- *Control clave:* **predicción analítica cerrada** para cada canal. Despolarizante:
  `e_Z = e_X = p/2`. Bit-flip: `e_Z = p, e_X = 0`. Phase-flip: `e_Z = 0, e_X = p`. Pauli:
  `e_Z = px+py, e_X = py+pz`. Sifting: 0,5.
- *Repeticiones:* 30 semillas × 10 parámetros × 6 canales.
- *Estadística:* Clopper–Pearson al 99% sobre el QBER; la predicción analítica debe caer dentro del
  intervalo. Un canal donde no caiga = bug.
- *Confusor:* el QBER muestreado usa solo el 20% de los bits; usar el QBER de diagnóstico completo
  para la validación y el muestreado para la decisión de protocolo. Son cosas distintas y hay que
  decirlo.
- *Figuras:* (a) QBER medido vs predicho con barras de error, seis paneles; (b) **`e_Z` vs `e_X` por
  canal** — el panel que revela la asimetría.
- *Conclusión legítima:* «el simulador reproduce las predicciones analíticas dentro del error
  binomial en los seis canales, **y la separación entre `e_Z` y `e_X` en phase-flip, Pauli asimétrico
  y amplitude damping viola el supuesto de simetría del estimador de longitud secreta, produciendo
  sobre-extracción de hasta N bits**».
- *Conclusión ilegítima:* nada sobre distancia, fibra o tasa de clave física.

### E4 — Detección de adversario *(nuevo — obligatorio)*

- *Variables independientes:* fracción de intercepción `f ∈ {0, 0.1, …, 1.0}`, ruido de fondo
  `p ∈ {0, 0.02, 0.05}`.
- *Variables dependientes:* QBER estimado, **tasa de aborto**, `n_final`.
- *Control:* predicción teórica — intercept-resend en base aleatoria induce `QBER = 0.25·f`; con
  `f=1` → 25%, muy por encima del umbral 11%.
- *Repeticiones:* 50 semillas por celda (la tasa de aborto es una proporción; se necesita n para su
  IC).
- *Figuras:* (a) QBER vs `f` con la recta teórica `0.25f` superpuesta; (b) **curva de probabilidad de
  aborto vs `f`**, con el punto de cruce del umbral marcado.
- *Conclusión legítima:* «el laboratorio detecta intercept-resend total con probabilidad ~1 y
  localiza el umbral de detección fiable en `f ≈ 0.44` (donde `0.25f = 0.11`), coincidiendo con la
  predicción analítica».
- *Por qué es obligatorio:* sin este experimento, el TFM contiene QKD pero no contiene **seguridad**
  de QKD.

### E5 — Establecimiento híbrido

- *Variables independientes:* perfil (PQC-BASE, PQC-DIVERSE, HYBRID, HYBRID-DIVERSE).
- *Variables dependientes:* acuerdo funcional (ambos lados derivan la misma `K_SESSION`), coste del
  combinador+HKDF+confirmación, bytes adicionales, procedencia registrada.
- *Control:* test negativo obligatorio — un componente alterado debe producir claves distintas y
  fallo de Finished.
- *Repeticiones:* 30.
- *Comparación válida:* **overhead marginal** del híbrido sobre la suma de sus partes. No «híbrido vs
  QKD».
- *Conclusión legítima:* «la composición añade menos de X ms sobre el coste de los componentes; el
  coste del híbrido es el coste de sus entradas».

### E6 — Sesión extremo a extremo con AES-256-GCM

- *Variables independientes:* perfil de origen de `K_SESSION`, tamaño de payload {64 B, 1 KB, 1 MB},
  tipo de manipulación {ninguna, ciphertext, tag, AAD}.
- *Variables dependientes:* éxito/fallo de descifrado, tiempo de cifrado/descifrado, expansión de
  tamaño (nonce 12 B + tag 16 B).
- *Control:* el mismo payload debe descifrarse correctamente bajo los cuatro perfiles.
- *Repeticiones:* 20 por celda; la matriz de manipulación es determinista (basta 1 por tipo, pero
  repetir para descartar flakiness).
- *Conclusión legítima:* «la clave establecida por cualquiera de los cuatro perfiles protege y
  autentica idénticamente el payload; el plano de datos es independiente del plano de
  establecimiento».
- *Esto es un demostrador, no un hallazgo.* Presentarlo como tal.

### Tabla resumen del plan experimental

| Experiment | Variables (indep. → dep.) | Metrics | Runs | Output | RQ answered |
|---|---|---|---|---|---|
| **E1** Descomposición coste PQC | perfil, rol → tiempo por operación | mediana/IQR de 12 operaciones + total | 50×2 perfiles | Barras apiladas + tabla | SQ1 |
| **E2** Coste en el cable | perfil → bytes | pk, ct, sig, canónico, JSON, total | 10×2 | Barras apiladas + tabla | SQ2 |
| **E3** Validación simulador BB84 | canal(6), parámetro(10), n(3) → QBER por base | e_Z, e_X, sifting, n_final, IC 99% | 30×10×6 ≈ 1.800 (~2 h a 20k señales) | 2 figuras + tabla medido-vs-analítico | SQ3 |
| **E4** Detección de adversario | fracción intercepción(11), ruido(3) → QBER, aborto | QBER, P(abort), n_final | 50×11×3 ≈ 1.650 | QBER vs f + curva de aborto | SQ4 |
| **E5** Coste de la autenticación | modo auth {asumido, ML-DSA, WC-MAC} → ms, bytes | latencia, bytes clásicos, bits QKD consumidos | 30×3 | Tabla comparativa | SQ5 |
| **E6** Establecimiento híbrido | perfil(4) → acuerdo, overhead | igualdad de clave, ms marginales, bytes | 30×4 | Tabla + test negativo | SQ6 |
| **E7** Sesión E2E + AES-GCM | perfil(4), payload(3), manipulación(4) → éxito/fallo | descifrado OK, InvalidTag, expansión | 20×48 | Matriz de manipulación | Demostrador DoD |

Coste de máquina estimado con los tiempos medidos: **≈ 4–5 horas de cómputo total**. Perfectamente
asumible.

---

## Recommended Security Profiles

### Problema con la taxonomía actual

`LOW` / `HIGH` es un error de nomenclatura, y la prueba es que la propia documentación necesita
**tres frases distintas en tres archivos** para aclarar que no significan lo que parecen. Cuando un
nombre necesita nota al pie, el nombre está mal.

Un tribunal leerá `LOW` como «menos seguro». No lo es: ML-KEM-768 solo y ML-KEM-768+HQC-3 son ambos
categoría 3 de NIST. La diferencia no es **nivel**, es **estrategia de diversificación**. Y hay un
riesgo real de que alguien concluya «usaron el perfil bajo, la tesis es floja».

### Taxonomía recomendada

Dos ejes ortogonales, nombres descriptivos, cero adjetivos de nivel:

| ID | Nombre | Fuente de secreto | Autenticación | Estado |
|---|---|---|---|---|
| `PQC-BASE` | PQC Base | ML-KEM-768 | ML-DSA-65 | CURRENT (hoy `LOW`) |
| `PQC-DIVERSE` | PQC Diversificado | ML-KEM-768 + HQC-3 | ML-DSA-65 | CURRENT (hoy `HIGH`) |
| `QKD-ASSUMED` | QKD, autenticación asumida | BB84 | **ninguna (supuesto)** | CURRENT — el nombre lo declara |
| `QKD-PQC-AUTH` | QKD autenticado con PQC | BB84 | ML-DSA-65 real | PLANNED ← la aportación |
| `HYBRID` | Híbrido | BB84 + ML-KEM-768 | ML-DSA-65 | PLANNED |
| `HYBRID-DIVERSE` | Híbrido diversificado | BB84 + ML-KEM-768 + HQC-3 | ML-DSA-65 | PLANNED |

**Coste de implementación: cero refactor de dominio.** Mantener `PQCProfile.LOW/HIGH` como
identificadores internos de `pqc/` (están en el transcript firmado y en el `info` de HKDF;
renombrarlos cambia claves derivadas y rompe tests). Introducir la taxonomía **solo en la capa de
orquestación/UI**, como un mapeo de presentación:

```python
DISPLAY_PROFILE = {
    PQCProfile.LOW:  "PQC-BASE",
    PQCProfile.HIGH: "PQC-DIVERSE",
}
```

Y documentar la equivalencia una vez, en una tabla, en `TFM_GOAL.md`. `QKD-ASSUMED` es el nombre más
valioso de la lista: convierte la limitación mejor documentada en algo que el usuario **ve en
pantalla** en lugar de leerlo en un README.

---

## Minimum Web Laboratory

Hay 3 endpoints y 1.926 líneas de TypeScript. Los cuatro workspaces propuestos son, siendo realista,
dos o tres semanas de trabajo que no hay. Recorte:

### Clasificación

#### Session Builder

| Feature | Clase |
|---|---|
| Selector de perfil (6 perfiles, deshabilitados si no implementados) | **ESSENTIAL** |
| Parámetros BB84 (n_signals, seed, pipeline de canales) — *ya existe* | **ESSENTIAL** |
| Control de fracción de intercepción de Eve | **ESSENTIAL** |
| Exponer `sample_fraction`, umbral QBER, `verification_tag_length` | **USEFUL** |
| Selector de algoritmos PQC arbitrarios | **ORNAMENTAL** — el backend solo soporta un conjunto fijo |
| Presets guardados / plantillas de configuración | **FUTURE** |

#### Protocol Visualizer

| Feature | Clase |
|---|---|
| Timeline vertical de eventos reales con timestamps por fase | **ESSENTIAL** |
| Distinción visual establecimiento vs plano de datos | **ESSENTIAL** |
| Marca «SUPUESTO, no ejecutado» sobre el canal clásico en perfiles QKD | **ESSENTIAL** — honestidad hecha interfaz |
| Diagrama animado de mensajes Alice↔Bob | **USEFUL** |
| `QuantumFlow` educativo — *ya existe* | **USEFUL**, no tocar |
| Animación de fotones viajando | **ORNAMENTAL** |
| Vista de red multi-nodo | **FUTURE** |

#### Results / Metrics

| Feature | Clase |
|---|---|
| Métricas del run + estado/razón de aborto — *ya existe* | **ESSENTIAL** |
| Persistencia de runs (lista, seleccionar, releer) | **ESSENTIAL** |
| **Comparación lado a lado de exactamente 2 runs** | **ESSENTIAL** |
| Export JSON/CSV del récord de run | **ESSENTIAL** (para la memoria) |
| Gráficas actuales — *ya existen* | **USEFUL** |
| `QubitInspector` — *ya existe* | **USEFUL** |
| Dashboard de comparación N-runs con filtros/agregaciones | **ORNAMENTAL** → matplotlib para la memoria |
| Estadística en el navegador (IC, tests) | **FUTURE** — va en Python |

#### Quantum-Safe Explorer

| Feature | Clase |
|---|---|
| Todo | **FUTURE — CORTAR** |

Razón: es un catálogo estático de datos de estándares que caducan. Mantenerlo correcto es trabajo
continuo, aporta cero valor experimental, y su contenido vive mejor en el capítulo de estado del arte
de la memoria, donde además se puede citar. **Si se construye, habrá que defender su exactitud.**

#### Protected Message Demo

| Feature | Clase |
|---|---|
| Cifrar/descifrar un payload con `K_SESSION` | **ESSENTIAL** |
| Botón «manipular ciphertext» → mostrar fallo de autenticación | **ESSENTIAL** — el momento más visual de la defensa |
| Mostrar nonce/tag/AAD | **USEFUL** |
| Chat interactivo, ficheros, streaming | **FUTURE** |

**Decisión de arquitectura:** *no* es un workspace. Es una **franja al pie de la pantalla de
resultado**, que aparece cuando el run terminó con sesión establecida. Así el usuario ve físicamente
que el plano de datos cuelga del plano de establecimiento.

### Web V1 mínima: tres pantallas

1. **Builder** — perfil + parámetros + Eve. (Extender lo existente; no reescribir.)
2. **Run** — timeline de eventos + métricas + gráficas + franja de mensaje protegido.
3. **Compare** — dos runs lado a lado, tabla de diferencias, botón de export.

Endpoints nuevos necesarios: `POST /api/sessions` (unificado, con perfil), `GET /api/runs`,
`GET /api/runs/{id}`, `POST /api/sessions/{id}/protect`. Cuatro rutas. Extender `/api/capabilities`
con el estado de los seis perfiles.

### Pantallas para una defensa de 10-15 min

Cuatro, en este orden, sin salir de ellas:

1. **Builder con perfil `QKD-ASSUMED`, Eve al 100%** → ejecutar → **aborto por QBER en pantalla**.
   (~2 min. El mejor momento: la seguridad cuántica funcionando delante del tribunal.)
2. **Mismo builder, Eve al 0%** → completa → mostrar el rendimiento de clave. (~1 min)
3. **Perfil `HYBRID-DIVERSE`** → timeline PQC completo → `K_SESSION` de 256 bits establecida con
   procedencia de tres componentes. (~3 min)
4. **Compare: `PQC-BASE` vs `PQC-DIVERSE`** → 16,5 ms vs 149 ms, 12,6 KB vs 30,6 KB → y en la franja
   inferior, el mensaje protegido y su fallo al manipularlo. (~3 min)

Cortar el resto. Con 4 pantallas y 9 minutos hay margen para preguntas.

---

## Documentation Problems

Contradicciones directas entre README / STRUCTURE / TFM_GOAL / código / tests: **se buscaron y se
encontraron muy pocas**. El refactor documental funcionó. Lo que queda:

**D1 — Sobre-cobertura (el problema dominante).** El README dice cinco veces que el tiempo de NumPy
no es latencia física; `docs/structure.md` lo repite; `ui/README.md` también; `TFM_GOAL.md §9` lo
repite. Es correcto pero **la afirmación positiva ha desaparecido bajo las negaciones**. Un tribunal
que lee tres páginas de «esto no es» y ninguna de «esto sí es» concluye que no hay tesis. Regla: cada
no-claim se escribe **una vez**, en la sección de limitaciones. Y por cada limitación debe haber una
afirmación positiva medible.

**D2 — «CURRENT, partial» para la web** (README, tabla de estado) mezcla dos ejes. Separar:
`Web laboratory (BB84): CURRENT` / `Web laboratory (PQC, hybrid, data plane): PLANNED`.

**D3 — Estado de HQC.** Correcto pero incompleto. Falta decir que `HQC-3` es un nombre de liboqs y
que el nombre normativo cambiará. Y falta la fecha de consulta junto a la afirmación (dice «as of
2026-09-05» — mantener y **verificar antes de entregar**, porque el draft FIPS puede publicarse entre
hoy y el depósito).

**D4 — El estimador asintótico se documenta como limitación, no como riesgo.** Tras el hallazgo del
phase-flip, el docstring de `asymptotic_bb84_secret_length` debe decir explícitamente: *«bajo canales
asimétricos entre bases este estimador **no es conservador**»*. Hoy dice «assumes a symmetric
phase-error rate», que suena a matiz y es un fallo.

**D5 — Ruido histórico.** `reports/01..24` (24 informes de la fase quantum) y `docs/reviews/*` son
snapshots de desarrollo. Ya llevan cabecera «Historical review snapshot», bien. Moverlos a
`docs/history/` para que no compitan visualmente con la documentación viva.

**D6 — `benchmarks/`** mide medida proyectiva y nada más. O se convierte en el punto de entrada del
motor de experimentos, o se mueve a `docs/history/`. Dejarlo donde está sugiere que existe un
framework de benchmarking que no existe.

**D7 — Tabla de dimensiones en `docs/structure.md §5.4`.** Los valores coinciden con lo medido
(ML-KEM 1184/1088/32, ML-DSA 1952/3309, HQC 4514/8978/32). Bien. Añadir la versión de liboqs (0.16.0)
**en la tabla**, no solo en el texto: esos números son específicos de una versión.

**D8 — Nada dice qué NO tiene el modelo QKD.** Falta un párrafo explícito: sin pérdidas ópticas, sin
dark counts, sin decoy states, sin ataques PNS, sin desalineamiento, sin efectos finitos de tamaño de
clave. Hoy hay que inferirlo por ausencia.

---

## Recommended Changes to TFM_GOAL.md

Como tutor: **aprobaría** §2 (problema), §8/§9 (qué es y qué no es — ejemplares), §10 (modelo de
seguridad, con una corrección), §14 (entregables), §16/§17 (fuera de alcance / trabajo futuro).
**Reescribiría** §3, §4, §7, §11, §12, §15. **Eliminaría** nada. **Añadiría** dos secciones.

### §3 — Research Question — REESCRIBIR

> ## 3. Research Question
>
> **¿Cuál es el coste medible —en latencia de establecimiento, bytes intercambiados y rendimiento de
> clave— de cada incremento de garantía quantum-safe (autenticación post-cuántica del canal clásico,
> diversificación de KEM y composición híbrida con material QKD), y bajo qué condiciones de canal y
> de adversario deja de compensar cada incremento?**
>
> La pregunta es empírica y falsable: cada incremento de garantía se implementa dentro de una única
> arquitectura, se ejecuta bajo condiciones controladas y se mide con métricas comparables dentro de
> su propio dominio. Una respuesta válida puede concluir que un incremento concreto **no** está
> justificado por su coste.

### §4 — Subquestions — REESCRIBIR

> ## 4. Research Subquestions
>
> 1. **Descomposición del coste PQC.** ¿Cómo se reparte el coste de un handshake autenticado entre
>    generación de identidad, generación de clave efímera, firma, verificación, encapsulación,
>    decapsulación, combinador, derivación HKDF y confirmación, y qué operación domina en cada
>    perfil?
> 2. **Coste en el cable.** ¿Cuál es el coste en bytes de cada perfil, distinguiendo el tamaño
>    criptográfico canónico del tamaño de la codificación de transporte?
> 3. **Validez del simulador y de su modelo de seguridad.** ¿Reproduce el simulador BB84 las
>    predicciones analíticas de QBER de cada canal implementado, y qué supuestos del estimador de
>    longitud secreta se violan cuando el canal no es simétrico entre bases?
> 4. **Detección de adversario.** ¿A partir de qué fracción de intercepción el mecanismo de aborto
>    por QBER detecta de forma fiable un ataque intercept-resend, y cómo se compara con la predicción
>    teórica?
> 5. **Coste del supuesto de autenticación.** ¿Qué cuesta sustituir el supuesto de canal clásico
>    autenticado de BB84 por autenticación real basada en ML-DSA-65, y qué cuesta continuarla con
>    MACs de hash universal alimentados por la propia clave QKD?
> 6. **Sobrecarga marginal del híbrido.** ¿Cuál es el coste adicional de la composición híbrida por
>    encima de la suma del coste de sus componentes?

### §7 — Contribution — REESCRIBIR

> ## 7. Thesis Contribution
>
> **Principal.** QuantumSec identifica y cierra la brecha de autenticación entre la ruta QKD y la
> ruta PQC —el canal clásico de BB84, habitualmente *asumido* autenticado, se autentica realmente con
> ML-DSA-65— y cuantifica el precio de cada incremento de garantía quantum-safe dentro de una única
> arquitectura y metodología de medición.
>
> **Secundarias.**
>
> - *Experimental:* un modelo de coste medido de la diversificación de KEM y de la composición
>   híbrida, con descomposición por operación y por bytes.
> - *Metodológica:* validación del simulador BB84 contra predicciones analíticas cerradas por canal,
>   incluyendo la identificación de un supuesto de simetría entre bases que el estimador de longitud
>   secreta no verifica y bajo el cual no es conservador.
> - *De ingeniería:* una frontera de composición acíclica que permite integrar QKD y PQC preservando
>   la procedencia de cada componente, con perfiles de seguridad explícitos y contratos de
>   configuración, traza, métrica y resultado versionados.
> - *Educativa:* un laboratorio web que hace visible la separación entre el plano de establecimiento
>   y el plano de protección de datos, y que muestra los supuestos no ejecutados como tales.
>
> QuantumSec **no** aporta un protocolo QKD nuevo, un algoritmo PQC nuevo, ni una demostración formal
> nueva de combinador robusto.

### §11 — Security Profiles — REESCRIBIR (tabla)

Sustituir la tabla por la de la sección *Recommended Security Profiles* de este informe, añadiendo
debajo:

> `PQC-BASE` y `PQC-DIVERSE` corresponden a los identificadores internos `PQCProfile.LOW` y
> `PQCProfile.HIGH` del paquete `pqc`. Esos identificadores se mantienen sin cambios porque forman
> parte del transcript firmado y del contexto `info` de HKDF; renombrarlos alteraría las claves
> derivadas. La taxonomía de esta tabla es la nomenclatura de presentación y documentación. Los
> términos «base» y «diversificado» describen **estrategias de composición**, no niveles de
> seguridad: ambos perfiles emplean ML-KEM-768 y ML-DSA-65, ambos en la categoría 3 de seguridad de
> NIST.

### §12 — Methodology — REESCRIBIR (añadir el bloque estadístico)

> ## 12. Experimental Methodology
>
> [conservar los dos primeros párrafos actuales]
>
> **Tratamiento estadístico.** Cada condición se ejecuta un mínimo de 30 veces. Las mediciones de
> tiempo criptográfico se reportan como mediana y rango intercuartílico, nunca como media y
> desviación típica: las distribuciones observadas presentan cola derecha larga (en HQC-3 el cociente
> p90/p10 supera 2,3 en el entorno de referencia). Las diferencias entre perfiles se contrastan con
> la prueba U de Mann–Whitney. Las proporciones —QBER, tasa de aborto, eficiencia de sifting— se
> acompañan de intervalos de confianza binomiales exactos de Clopper–Pearson. El orden de ejecución
> de las condiciones se aleatoriza para evitar sesgo por efectos térmicos de la CPU, y se descartan
> las cinco primeras repeticiones de cada bloque como calentamiento.
>
> **Separación de planos de medida.** Los tiempos del dominio PQC proceden de operaciones
> criptográficas reales sobre liboqs y son comparables entre sí. Los tiempos del dominio QKD son
> tiempos de simulación numérica y **solo** son comparables entre configuraciones del propio
> simulador. En ninguna tabla, figura o conclusión se comparan magnitudes temporales entre ambos
> dominios. La comparación entre QKD, PQC e híbrido se realiza sobre tres ejes separados: supuestos
> de seguridad (cualitativo), rendimiento de clave y coste en bytes.
>
> **Registro de entorno.** Cada récord de ejecución incluye versión de liboqs y del wrapper, versión
> de Python y NumPy, identificación de CPU y sistema operativo, semilla de la aleatoriedad modelada,
> instantánea inmutable de la configuración e identificador de run.

### §15 — Definition of Done — REESCRIBIR

> ## 15. Definition of Done
>
> El TFM está completo únicamente cuando:
>
> 1. la ruta BB84 es demostrable desde la preparación hasta el material final o un aborto
>    justificado;
> 2. **el laboratorio contiene un modelo de adversario ejecutable y demuestra el aborto por QBER
>    inducido por intercepción**;
> 3. **el estimador de longitud secreta comprueba, o documenta y acota explícitamente, su supuesto de
>    simetría entre bases**;
> 4. las rutas `PQC-BASE` y `PQC-DIVERSE` son demostrables hasta la confirmación mutua por Finished;
> 5. **el canal clásico de al menos un perfil QKD está realmente autenticado con ML-DSA-65, y no
>    meramente asumido**;
> 6. la integración híbrida QKD-PQC es demostrable sin acoplamiento directo entre paquetes hermanos,
>    y ambos lados derivan la misma `K_SESSION` de 256 bits;
> 7. la demostración AES-256-GCM descifra datos válidos y rechaza manipulación de ciphertext, de tag
>    y de AAD por separado;
> 8. el laboratorio web ejecuta y visualiza las tres pantallas de la V1 mínima (Builder, Run,
>    Compare);
> 9. los experimentos emiten configuraciones, trazas, métricas y resultados versionados y
>    exportables;
> 10. **cada subpregunta de §4 tiene una respuesta respaldada por datos, con su tratamiento
>     estadístico, o una justificación explícita de por qué no pudo responderse.**

### AÑADIR §19 — Threats to Validity

> ## 19. Threats to Validity
>
> **Validez interna.** Las mediciones de tiempo dependen del entorno de ejecución (CPU, gestión
> térmica, versión de liboqs). Se mitiga con aleatorización del orden, descarte de calentamiento y
> reporte de distribuciones.
>
> **Validez de constructo.** El tiempo de simulación QKD no mide ninguna propiedad de un sistema QKD
> físico. No se emplea como métrica comparable fuera del propio simulador.
>
> **Validez externa.** El modelo de canal es de qubit lógico: no incluye pérdidas ópticas, dark
> counts, decoy states, ataques PNS ni desalineamiento. Las conclusiones sobre comportamiento QKD son
> conclusiones sobre este modelo, no sobre enlaces desplegados. Los resultados PQC se obtienen en una
> única plataforma y una única versión de liboqs.
>
> **Validez de conclusión.** El modelo de longitud de clave es asintótico. No es una demostración de
> seguridad componible de clave finita, y los tamaños de muestra empleados no permiten afirmaciones
> de seguridad ε-composable.

### AÑADIR §20 — Related Work Positioning

> ## 20. Positioning
>
> QuantumSec no reclama novedad en la idea de combinar QKD y PQC: la integración híbrida, los
> combinadores de KEM y la autenticación post-cuántica de canales QKD son líneas activas de
> investigación y de estandarización. La aportación de este trabajo es de **integración, medición y
> honestidad metodológica**: reunir estas rutas bajo una arquitectura acíclica única, ejecutarlas con
> un modelo de adversario explícito, y publicar el coste de cada incremento de garantía con su
> tratamiento estadístico y sus amenazas a la validez.

---

## Scope Matrix

### MUST HAVE — sin esto no hay tesis defendible

| # | Trabajo | Coste estimado |
|---|---|---|
| M1 | **Canal `InterceptResendChannel`** (4 operadores de Kraus sobre la clase existente) + parámetro de fracción de intercepción | 0,5 día |
| M2 | **QBER resuelto por base** (`e_Z`, `e_X`) expuesto en `BB84SessionResult` | 0,5 día |
| M3 | **Corregir o acotar el estimador asintótico** ante asimetría de bases (usar `max(e_Z, e_X)` como cota conservadora, o abortar si la asimetría supera un umbral) | 1 día |
| M4 | **Capa de orquestación** con contratos config/trace/metrics/result y perfiles unificados | 3 días |
| M5 | **Combinador híbrido** con dominio propio, etiquetas, longitudes, orden y procedencia + tests de frontera | 2 días |
| M6 | **AES-256-GCM** con nonce por contador, AAD ligado a la sesión y matriz de manipulación de 3 casos | 1 día |
| M7 | **Motor de experimentos** mínimo: `CONFIG → RUN → RECORD → export JSON/CSV` | 2 días |
| M8 | **Ejecución de E1–E4 + E6–E7** y análisis estadístico | 3 días |
| M9 | **Web V1: tres pantallas** (Builder extendido, Run con timeline, Compare de 2) | 4 días |
| M10 | Reescritura de `TFM_GOAL.md` según este informe | 0,5 día |

**≈ 17,5 días de desarrollo.**

### SHOULD HAVE — muy recomendable si el coste es pequeño

| # | Trabajo | Coste |
|---|---|---|
| S1 | **Autenticación real del canal clásico QKD con ML-DSA-65** (perfil `QKD-PQC-AUTH`) + E5 | 2 días |
| S2 | Cota superior de Clopper–Pearson sobre el QBER usada en la fórmula de longitud (`security_margin_bits` ya existe como gancho) | 0,5 día |
| S3 | Subir `verification_tag_length` por defecto a 32-64 bits y documentar la probabilidad de error residual | 0,25 día |
| S4 | Política de perfil aceptable en `ServerKeyOfferProcessor.process()` | 0,25 día |
| S5 | Exponer en la UI la etiqueta «SUPUESTO, no ejecutado» sobre el canal clásico | 0,25 día |
| S6 | Separar generación de identidad del cronometraje del handshake en los benchmarks | 0,25 día |
| S7 | Mover `reports/` y `docs/reviews/` a `docs/history/` | 0,1 día |

**≈ 3,6 días.** S1 es el que convierte el TFM de notable a sobresaliente. Los demás son casi gratis.

### NICE TO HAVE — solo si sobra tiempo

- MAC Wegman–Carter incondicional sobre el hashing Toeplitz existente, para continuar la
  autenticación con clave QKD (1,5 días).
- Frontera de entrega de clave con forma ETSI GS QKD 014 entre el simulador QKD y la orquestación
  (1,5 días).
- Exportación de figuras matplotlib listas para la memoria desde los récords de experimento (1 día).
- Streaming/progreso en el endpoint BB84 para n grandes (0,5 días).

### FUTURE WORK — NO tocar antes de entregar

Todo lo siguiente debe quedar escrito en §17 y **no ejecutarse**:

- **Quantum-Safe Explorer** — cortar del TFM, no solo posponer.
- **Dashboard de comparación N-runs** — usar matplotlib.
- B92, E91, BBM92.
- QKDN, topología, enrutamiento, repetidores.
- Modelos de hardware, pérdida óptica, decoy states, dark counts.
- KEMs o firmas adicionales (SLH-DSA, Falcon/FIPS 206...).
- Agentes / LLM.
- Post-procesado avanzado (LDPC, reconciliación multinivel, clave finita componible).
- Verificación formal del combinador.
- Optimización de producción, endurecimiento, certificación.

---

## Up to Three Improvements Worth Adding

### Mejora 1 — Modelo de adversario intercept-resend

**Qué.** Una clase `InterceptResendChannel(KrausChannel)` con los cuatro operadores
`{|k_b><k_b|/sqrt(2)}` para `b ∈ {Z,X}`, `k ∈ {0,1}` (verifican `sum K†K = I` exactamente), envuelta
en un `PartialInterceptChannel(f)` que mezcla con identidad según la fracción `f`. Se enchufa en el
`ChannelPipeline` existente sin tocar BB84.

- **Benefit.** Convierte el aborto por QBER de código muerto en el resultado central del TFM.
  Habilita E4, que es el único experimento que demuestra *seguridad* de QKD y no solo aritmética de
  ruido. Predicción teórica verificable: `QBER = 0.25·f`.
- **Implementation cost.** **Muy bajo.** ~30 líneas de dominio + ~40 de test + 1 campo en el schema
  de la UI. Medio día. `KrausChannel` ya valida completitud en construcción, así que la corrección es
  automática.
- **Thesis value.** **Máximo.** Aporta una figura (curva de aborto vs `f`), una predicción teórica
  confirmada, y **el momento más contundente de la defensa**: pulsar «ejecutar» y ver el aborto en
  pantalla.
- **Recomendación.** **Sí, sin reservas. Es la mejora con mejor ratio valor/coste de todo el
  proyecto.**

### Mejora 2 — Autenticación real del canal clásico QKD con ML-DSA-65

**Qué.** Un perfil `QKD-PQC-AUTH` en la capa de orquestación donde el transcript clásico de BB84
(bases reveladas, posiciones muestreadas, paridades Cascade, semilla y tag Toeplitz) se firma con
ML-DSA-65 usando las identidades pre-provisionadas que ya existen en `pqc/protocol/identity.py`. La
ruta QKD deja de asumir autenticación y pasa a tenerla.

Extensión natural (NICE TO HAVE): una vez existe clave QKD, continuar la autenticación con un MAC
Wegman–Carter incondicional construido sobre el `toeplitz_hash` que **ya está implementado** —
`tag = T_s(m) XOR k` con `k` de la clave QKD. Eso convierte la autenticación de computacional a
teórico-informacional a partir de la segunda ronda, que es exactamente el argumento del bootstrap
PQC→QKD de la literatura reciente.

- **Benefit.** Cierra la única brecha conceptual real del proyecto y transforma la contribución de
  «integré dos cosas» a «resolví un problema conocido». Además da un resultado cuantitativo limpio:
  *el precio de la autenticación real* en ms y bytes clásicos (SQ5/E5). Y neutraliza la pregunta más
  peligrosa del tribunal: *«¿pero su BB84 no asume autenticado el canal clásico?»* — la respuesta
  pasa de «sí, es una limitación» a «lo era; aquí está resuelto y medido».
- **Implementation cost.** **Bajo-medio.** Firma del transcript clásico: ~2 días, todo reutilizando
  `MLDSASigner` y `TrustedIdentityStore`. El MAC Wegman–Carter: +1,5 días, reutilizando
  `universal_hashing.py`. Cero dependencias nuevas.
- **Thesis value.** **Muy alto.** Es la aportación principal recomendada, y está alineada con líneas
  de trabajo activas (p. ej. *Hybrid AKE for QKD(N) without signatures*, IACR ePrint 2026/1231; ETSI
  ISG QKD).
- **Recomendación.** **Sí** para la parte de firma (SHOULD HAVE). El MAC Wegman–Carter solo si se
  terminan M1–M10 con holgura.

### Mejora 3 — Frontera de entrega de clave con forma ETSI GS QKD 014

**Qué.** Que la capa de orquestación no lea el `BB84SessionResult` directamente, sino que consuma el
material QKD a través de un adaptador con la forma de la API de entrega de claves de ETSI GS QKD 014
(`get_status`, `get_key`, `get_key_with_key_ids`), implementado sobre el simulador. Ya hay FastAPI y
contratos JSON tipados, así que la infraestructura está.

- **Benefit.** Tres cosas a la vez: (a) fuerza una frontera de integración limpia que hace imposible
  el acoplamiento `qkd`↔`pqc`; (b) alinea el trabajo con la estandarización industrial real, lo que
  da peso al estado del arte; (c) habilita una frase muy fuerte en la memoria y en la defensa: *«el
  simulador es sustituible por un KME físico sin cambiar la capa de orquestación»* — que responde de
  golpe a la objeción «esto es solo una simulación».
- **Implementation cost.** **Bajo.** Es un shim de interfaz, no un sistema: ~1,5 días para las tres
  operaciones sobre un almacén de claves en memoria.
- **Thesis value.** **Medio-alto.** No genera datos experimentales nuevos, pero eleva mucho la
  percepción de madurez arquitectónica y da un párrafo sólido de trabajo futuro con credibilidad.
- **Recomendación.** **Sí, pero como NICE TO HAVE.** No sacrificar ningún MUST HAVE por esto. Si el
  tiempo aprieta, **describirlo en la memoria como diseño de la frontera de integración sin
  implementarlo** — casi todo el valor argumental se conserva.

**Descartadas deliberadamente** (interesantes técnicamente, no rentables para el TFM): decoy states,
LDPC, seguridad de clave finita componible, protocolos QKD adicionales, algoritmos PQC adicionales,
verificación formal.

---

## Proposed Thesis Title

**Español:**
*QuantumSec: cierre de la brecha de autenticación entre QKD y PQC y evaluación cuantitativa del coste
de las estrategias de establecimiento de sesión quantum-safe*

**English:**
*QuantumSec: Closing the QKD–PQC Authentication Gap and Quantifying the Cost of Quantum-Safe
Session-Establishment Strategies*

Alternativa más conservadora, si el tutor prefiere no comprometerse con la Mejora 2:

- **Español:** *QuantumSec: laboratorio reproducible para la evaluación experimental del coste de las
  estrategias de establecimiento de sesión quantum-safe basadas en QKD, PQC e híbridos*
- **English:** *QuantumSec: A Reproducible Laboratory for the Experimental Cost Evaluation of QKD-,
  PQC- and Hybrid-Based Quantum-Safe Session Establishment*

En ambos casos: la palabra que cambia todo es **coste/evaluación** en lugar de **integración**.
«Integración» promete existencia; «evaluación del coste» promete números.

---

## Thesis Defense Story

Guion de 5-7 minutos. Un hilo, sin desvíos.

**Problema (60 s).**
«Un adversario con ordenador cuántico rompe el establecimiento de claves que usamos hoy. Hay dos
respuestas: la criptografía post-cuántica, que ya está estandarizada —FIPS 203 y 204, agosto de
2024— y la distribución cuántica de claves, que ofrece garantías de otra naturaleza. Se presentan a
menudo como alternativas, pero tienen un problema complementario: **la PQC necesita confianza en
supuestos matemáticos, y la QKD necesita un canal clásico autenticado que ella misma no puede
proporcionar.** Nadie discute que se puedan combinar. Lo que casi nadie publica es **cuánto cuesta
hacerlo**.»

**Enfoque (45 s).**
«Mi pregunta no es si se pueden integrar, sino cuál es el precio medible de cada incremento de
garantía: autenticar de verdad el canal clásico, diversificar el KEM, y componer material QKD con
material PQC. Para responderla necesitaba las tres rutas ejecutándose bajo una misma arquitectura,
con una misma metodología de medición y con un adversario dentro.»

**QuantumSec (75 s).**
«QuantumSec es esa arquitectura. Cinco capas acíclicas. `qkd` y `pqc` nunca se importan entre sí; se
componen por encima, lo que preserva la procedencia de cada componente de secreto. La ruta QKD es
BB84 sobre canales CPTP con post-procesado completo: sifting, estimación muestreada de QBER, Cascade,
verificación por hash universal y amplificación de privacidad Toeplitz. La ruta PQC es un handshake
mutuamente autenticado real sobre liboqs: ML-KEM-768, ML-DSA-65, opcionalmente HQC-3, transcript
canónico autenticado, HKDF-SHA-384 y confirmación de clave bilateral. Y sobre ambas, una capa de
composición y un plano de datos AES-256-GCM. Unas 8.000 líneas de dominio con 5.200 de tests.»

**Experimento (90 s).**
«Cuatro bloques experimentales. Primero, descomposición del coste PQC operación por operación.
Segundo, coste en bytes distinguiendo tamaño criptográfico de tamaño de transporte. Tercero,
**validación**: comparo el QBER que produce el simulador con la predicción analítica cerrada de cada
canal. Cuarto, **detección de adversario**: introduzco un ataque intercept-resend con fracción de
intercepción variable y mido a partir de qué punto el protocolo aborta.»

**Resultado (90 s).**
«Tres resultados. Uno: la diversificación no es gratis. Añadir HQC-3 multiplica por nueve el tiempo
de handshake y por dos y medio los bytes en el cable, y más del noventa por ciento de ese tiempo es
el propio HQC, no la arquitectura. Es una decisión de política de riesgo, no de rendimiento, y ahora
tiene precio.

Dos: el laboratorio detecta al adversario. Con intercepción total, el QBER sube al veinticinco por
ciento —exactamente la predicción teórica— y el protocolo aborta con probabilidad prácticamente uno.

Y tres, el resultado que no esperaba: **la validación encontró un fallo en mi propio estimador de
seguridad.** Estimaba la tasa de error de fase con el QBER promediado sobre ambas bases. Bajo un
canal de phase-flip medí cero por ciento de error en la base Z y dieciséis en la base X. El estimador
extraía mil seiscientos setenta y dos bits de clave donde la cota de Shor-Preskill correcta permite
cero. Lo detecté porque validé contra teoría en lugar de contra mi intuición.»

**Conclusión (60 s).**
«Tres conclusiones. Primera: comparar QKD y PQC en rendimiento es un error de categoría; solo son
comparables en supuestos, en rendimiento de clave y en bytes, y mi metodología separa esos ejes
explícitamente. Segunda: el valor de la composición híbrida no está en el combinador —su coste es
despreciable— sino en lo que se combina y en lo que se asume. Tercera, y la que me llevo: **un
laboratorio reproducible no vale por lo que demuestra que funciona, sino por lo que le permite a uno
descubrir que estaba roto.** QuantumSec encontró un fallo en mi propio modelo de seguridad. Ese es el
argumento más fuerte que puedo dar a favor de construirlo.»

**Nota táctica:** ese cierre es el mejor activo. Un tribunal recuerda al estudiante que encontró y
corrigió su propio error mucho más que al que presentó un sistema sin fisuras.

---

## VERDICT AS TFM REVIEWER

**1. Is this a solid Master's Thesis?**

El **software** sí, con holgura: está por encima de lo que se exige. La **tesis, tal y como está
formulada hoy, no**. Es una memoria de producto con una pregunta de investigación que se responde
enseñando el repositorio. Con los cambios de este informe —principalmente girar de «integración» a
«coste medido», añadir un adversario y cerrar la brecha de autenticación— pasa a ser sólida y con
margen para nota alta. La distancia entre lo que hay y lo que hace falta es de unas 3-4 semanas, no
de un rediseño.

**2. What is its strongest contribution?**

Hoy, latente: el material medido del coste de la diversificación PQC (×9 en tiempo, ×2,4 en bytes) y
la calidad de la ingeniería del handshake. Como debería declararse: **el cierre de la brecha de
autenticación QKD-PQC con su coste cuantificado**, sostenido por la validación del simulador contra
teoría.

**3. What is currently its weakest point?**

**La ausencia total de un modelo de adversario.** Un laboratorio de seguridad cuántica sin Eve no
puede demostrar la única propiedad que hace interesante a la QKD. En segundo lugar, y muy cerca: la
pregunta de investigación no puede responderse con datos.

**4. What must be implemented next?**

En este orden exacto: (1) `InterceptResendChannel`, medio día — desbloquea el experimento más
importante; (2) QBER resuelto por base, medio día — desbloquea la validación y confirma el fallo del
estimador; (3) corrección/acotación del estimador asintótico, un día; (4) capa de orquestación con
contratos de resultado; (5) combinador híbrido; (6) AES-256-GCM; (7) las tres pantallas de la web V1.
Nada de lo anterior debe empezar antes que (1) y (2): son baratos y cambian qué tesis se está
escribiendo.

**5. What should explicitly NOT be implemented?**

El **Quantum-Safe Explorer** (cortarlo, no solo posponerlo: su contenido caduca y habría que defender
su exactitud), el **dashboard de comparación N-runs** (usar matplotlib para la memoria), protocolos
QKD adicionales, QKDN, repetidores, modelos de hardware o pérdida óptica, KEMs/firmas adicionales,
agentes o LLM, post-procesado avanzado, y cualquier intento de demostración formal del combinador.

**6. What experiments are mandatory?**

Cuatro, sin excepción: **E1** (descomposición del coste PQC), **E2** (coste en bytes), **E3**
(validación del simulador contra predicción analítica, con QBER por base), **E4** (detección de
adversario y curva de aborto). Más **E7** (AES-GCM con matriz de manipulación) como demostrador del
*definition of done*. E5 (coste de la autenticación) es el que sube la nota. E6 (overhead híbrido) es
necesario pero de bajo valor por sí solo.

**7. What claim can be defended safely before a committee?**

> «QuantumSec ejecuta rutas QKD simuladas y rutas PQC criptográficamente reales bajo una arquitectura
> acíclica común, con un modelo de adversario explícito, y cuantifica el coste de cada incremento de
> garantía quantum-safe en latencia, bytes y rendimiento de clave, con procedencia de componentes
> explícita, separación de dominios en la derivación de claves y confirmación bilateral de clave. La
> validación contra predicciones analíticas identificó y corrigió una violación de supuesto en su
> propio estimador de longitud secreta.»

Todo en esa frase está respaldado por código ejecutable y por números medibles.

**8. What claim should never be made?**

Cinco frases prohibidas:

- (a) *«el combinador híbrido es seguro si al menos un componente lo es»* sin el marco de supuestos y
  las citas de la sección de seguridad;
- (b) cualquier equiparación del tiempo de simulación con latencia física, tasa de clave o distancia;
- (c) *«QKD proporciona seguridad incondicional extremo a extremo»* — el canal clásico rompe esa
  cadena, y la KDF computacional destruye la propiedad ITS al combinar;
- (d) *«HQC es un estándar NIST»* — está seleccionado, no publicado, y `HQC-3` es un nombre de
  liboqs;
- (e) cualquier comparación directa de rendimiento entre QKD y PQC en la misma unidad.

**9. What single change would improve the thesis the most?**

**Añadir el canal intercept-resend.** Medio día de trabajo. Convierte el experimento QKD de una
identidad aritmética en una demostración de seguridad, activa la única ruta de código que justifica
la existencia del umbral de aborto, produce la figura más citable de la memoria y da el momento más
contundente de la defensa. Ninguna otra intervención tiene este ratio.

Segunda opción: **reformular la pregunta de investigación de «cómo integrar» a «cuánto cuesta»**.
Cuesta una tarde de escritura y cambia la naturaleza del trabajo.

**10. Final score of the current proposal from 0 to 10.**

### 6,5 / 10

Desglose:

| Dimensión | Nota | Justificación |
|---|---:|---|
| Calidad del software | **9,0** | Arquitectura acíclica, 547 tests, ingeniería criptográfica de nivel profesional, ciclos de vida de secretos explícitos |
| Honestidad documental | **9,0** | Se buscaron overclaims agresivamente y se encontraron muy pocos. Excepcional para un TFM |
| Corrección técnica | **7,0** | Penalizado por el supuesto de simetría no verificado en el estimador (con sobre-extracción demostrada) y por la falta de política de perfil |
| Calidad de la pregunta de investigación | **4,0** | Pregunta de diseño, no falsable, sin datos |
| Diseño experimental | **4,5** | Cuatro experimentos propuestos, uno analíticamente trivial, uno basado en una comparación inválida, cero adversarios |
| Realismo del alcance | **5,0** | Cinco paquetes abiertos y una web de cuatro workspaces con tiempo limitado |
| Claridad para un tribunal | **6,0** | La sobre-cobertura ha sepultado la afirmación positiva |

**Proyección con los cambios recomendados: 8,5-9,0.** El techo es alto porque la base de ingeniería
ya está construida; lo que falta es barato en horas y caro en decisión. Y esa es la buena noticia de
esta revisión: **no hay un problema de código, hay un problema de encuadre, y el encuadre se arregla
en una semana.**

---

## Fuentes

Consultadas y verificadas el 2026-09-05 con consultas genéricas sobre estándares públicos:

- [NIST Post-Quantum Cryptography Standardization (CSRC)](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization)
  — FIPS 203/204/205 publicados 2024-08-13; HQC seleccionado 2025-03-11 (NIST IR 8545); FIPS 206 en
  desarrollo
- [NIST publishes SP 800-227, Recommendations for Key-Encapsulation Mechanisms (sept. 2025)](https://www.nist.gov/news-events/news/2025/09/recommendations-key-encapsulation-mechanisms-nist-publishes-sp-800-227)
- [NIST SP 800-227 (PDF)](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-227.pdf)
- [draft-ietf-tls-hybrid-design-16 — Hybrid key exchange in TLS 1.3](https://datatracker.ietf.org/doc/html/draft-ietf-tls-hybrid-design)
  — sigue siendo Internet-Draft
- [draft-connolly-cfrg-xwing-kem-10 — X-Wing hybrid KEM](https://datatracker.ietf.org/doc/html/draft-connolly-cfrg-xwing-kem-10)
  — Internet-Draft CFRG
- [ETSI GS QKD 014 V1.1.1 (2019-02) — Protocol and data format of REST-based key delivery API](https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_qkd014v010101p.pdf)
- [ETSI GS QKD 004 V2.1.1 (2020-08) — Application interface](https://www.etsi.org/deliver/etsi_gs/QKD/001_099/004/02.01.01_60/gs_qkd004v020101p.pdf)
- [The Best of Both Worlds: Hybrid Authenticated Key Exchange for QKD(N) without Signatures (IACR ePrint 2026/1231)](https://eprint.iacr.org/2026/1231)
- [Assessment of provably secure hybrid authenticated key exchange for dual-use applications — EPJ Quantum Technology](https://link.springer.com/article/10.1140/epjqt/s40507-026-00532-9)
- [PQC-Enhanced QKD Networks: A Layered Approach (arXiv)](https://arxiv.org/html/2604.05599v1)

Referencias académicas citadas en el análisis del combinador (no verificadas por búsqueda web en
esta sesión; comprobar cita exacta antes de incluirlas en la memoria):

- F. Giacon, F. Heuer, B. Poettering, *KEM Combiners*, PKC 2018.
- N. Bindel, J. Brendel, M. Fischlin, B. Goncalves, D. Stebila, *Hybrid Key Encapsulation Mechanisms
  and Authenticated Key Exchange*, PQCrypto 2019.
- H. Krawczyk, *Cryptographic Extraction and Key Derivation: The HKDF Scheme*, CRYPTO 2010.
- P. W. Shor, J. Preskill, *Simple Proof of Security of the BB84 Quantum Key Distribution Protocol*,
  PRL 85, 441 (2000).
