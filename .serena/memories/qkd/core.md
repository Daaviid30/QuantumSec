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
- Estado de seguridad PARTIAL: resultado y muestra exponen QBER agregado, no `e_Z`/`e_X`; la
  decisión y longitud asintótica asumen simetría que PhaseFlip, Pauli o AmplitudeDamping pueden
  violar.
- La verificación universal tras Cascade comprueba igualdad de claves; no autentica el canal
  clásico. Actualmente `QKD-ASSUMED` asume esa autenticación.
- Eve intercept-resend y `QKD-CLASSICAL-AUTH`/`QKD-PQC-AUTH` están PLANNED.
- La corrección debe usar una cota de error de fase teóricamente justificada o abortar fuera del
  dominio válido; no adoptar `max(e_Z, e_X)` sin justificación.
- Resultados y estados almacenados se copian/protegen; no exponer arrays internos mutables.
- En canal ideal, BB84 debe dar QBER 0; la longitud filtrada es aleatoria y no se prueba como
  exactamente la mitad.
- Tests relevantes viven bajo `tests/test_qkd/`.
