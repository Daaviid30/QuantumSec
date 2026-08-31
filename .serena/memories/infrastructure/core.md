# Capa core/

- Infraestructura independiente del dominio; no importa `quantum`, `qkd`, `pqc` ni `experiments`.
- `core/rng.py`: contrato `BaseRNG`; implementaciones `SeededRNG`, `GlobalRNG`, `QRNGSimulator`; helpers `random_bit`, `random_basis`, `random_unitary`.
- Los consumidores reciben un RNG por inyección. `SeededRNG` es la opción para reproducibilidad; `GlobalRNG` solo cuando el no determinismo sea deliberado.
- `core/constants.py` centraliza `DEFAULT_ATOL = 1e-10`.
- Configuración, logging y benchmarking general son responsabilidades futuras válidas; matemáticas cuánticas y protocolos no lo son.
- Helpers RNG devuelven escalares/arrays NumPy, validan tamaños y no asignan semántica QKD a las elecciones binarias.