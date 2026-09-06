# Capa qkd/

- Dominio QKD sobre `quantum/` y `core/`; no importa `pqc` ni `experiments`.
- `primitives/`: estados, bases, operadores y mediciones con significado QKD.
- `channel/`: `QuantumChannel`, identidad, canales Kraus, ruido Pauli/despolarizante/amortiguación
  y composición secuencial.
- Los canales actuales son transformaciones CPTP de qubits lógicos. Pérdida fotónica,
  vacío/no-detección y fibra no están modelados; amortiguación de amplitud no es pérdida de fibra.
- `protocols/bb84.py`: `BB84Protocol` recibe canal y RNG; prepara, transmite, mide, filtra y
  ejecuta postprocesado/abortos.
- `postprocessing/sifting.py` conserva bases iguales; `metrics/qber.py` calcula discrepancias
  agregadas sobre claves alineadas no vacías.
- Parameter estimation muestrea de forma estratificada por Z/X, conserva bases reveladas y
  candidatas, y expone QBER estimado y diagnóstico por base y agregado.
- El candidato mezcla bits Z/X. La reducción BB84/CSS usa `e_X` para acotar fase en Z y `e_Z` para
  acotar fase en X; `max(e_Z, e_X)` es la cota común conservadora que consume el estimador.
  El agregado solo dimensiona Cascade y no sustituye la cota de fase.
- La verificación universal tras Cascade usa por defecto un tag de 32 bits, comprueba igualdad de
  claves y no autentica el canal clásico. Actualmente `QKD-ASSUMED` asume esa autenticación.
- El estimador sigue siendo asintótico y no componible de clave finita; si falta una base, la cota
  no es válida o la longitud no es positiva, la sesión aborta sin material final.
- Eve intercept-resend y `QKD-CLASSICAL-AUTH`/`QKD-PQC-AUTH` están PLANNED.
- Resultados y estados almacenados se copian/protegen; no exponer arrays internos mutables.
- En canal ideal, BB84 debe dar QBER 0; la longitud filtrada es aleatoria y no se prueba como
  exactamente la mitad.
- Tests relevantes viven bajo `tests/test_qkd/`.
