# Capa quantum/

- Matemática cuántica reutilizable, sin Alice/Bob, BB84, QBER, autenticación ni decisiones de protocolo.
- `linalg.py`: kets, productos, normalización y probabilidades.
- `validation.py`: distribuciones, estados, operadores unitarios, matrices densidad, proyectores y mediciones proyectivas.
- `states.py`: matrices densidad puras y ensambles.
- `measures.py`: objetos/resultados de medición y muestreo/colapso proyectivo.
- `information.py`: pureza, distancia de traza, fidelidad y entropía.
- `types.py` define aliases NumPy; las validaciones públicas usan `ValueError` y `errors.py` queda reservado para una futura jerarquía de dominio con consumidores concretos.
- Validaciones físicas usan tolerancia explícita/centralizada, matrices `complex128` y mensajes con forma, traza, autovalores o desviación.
- No generalizar prematuramente a POVM. Añadir efectos/operadores POVM como frontera separada cuando exista un caso de uso concreto.
