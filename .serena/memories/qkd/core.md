# Capa qkd/

- Dominio QKD sobre `quantum/` y `core/`; no importa `pqc` ni `experiments`.
- `primitives/`: estados/bases/operadores/mediciones con significado QKD.
- `channel/`: interfaz `QuantumChannel`, identidad, canales Kraus, ruido Pauli/despolarizante/amortiguación y composición secuencial.
- Canales actuales son transformaciones CPTP deterministas de matrices densidad. Pérdida fotónica/vacío/no-detección será una capa óptica separada; amortiguación de amplitud no es sinónimo de pérdida de fibra.
- `protocols/bb84.py`: `BB84Protocol` recibe canal y RNG; prepara, transmite, mide, filtra y devuelve `BB84Result`.
- `postprocessing/sifting.py` conserva posiciones con bases iguales; `metrics/qber.py` calcula la fracción de discrepancias sobre claves alineadas no vacías.
- Resultados y estados almacenados se copian/protegen; no exponer arrays internos mutables.
- `qkd/_validation.py` centraliza la validación defensiva de bits, índices y claves alineadas para protocolos, métricas y postprocesado.
- En canal ideal, BB84 debe dar QBER 0; longitud filtrada es aleatoria y no se prueba como exactamente la mitad.
- Tests relevantes viven bajo `tests/test_qkd/` y reflejan primitivas, canales, postprocesado, métricas y protocolos.
