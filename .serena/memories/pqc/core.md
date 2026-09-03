# Capa pqc/ (Criptografía y Autenticación Post-Cuántica)

- Módulo hermano de `qkd/`; no importa de `qkd/` ni de `experiments/`.
- La aleatoriedad criptográfica proviene exclusivamente de `liboqs` y el CSPRNG del sistema operativo; no usa el RNG inyectado/sembrado (`BaseRNG`), que queda reservado para simulaciones científicas de QKD.
- `backends/`: adaptadores aislados `OQSSignatureBackend` y `OQSKEMBackend` para `liboqs-python`. Gestionan el ciclo de vida de memoria en C (`with`) y cachean la disponibilidad de mecanismos.
- `signatures/`: contrato `SignatureProvider`, metadatos `SignatureMetadata` e implementación de firmas `MLDSA65` (FIPS 204). Registro e invocación pública estática mediante `verify_signature`.
- `kem/`: contrato `KEMProvider`, metadatos `KEMMetadata`, e implementaciones efímeras `MLKEM768` (FIPS 203) y `HQC3`. `encapsulate` es un `@classmethod` público sin clave privada; `decapsulate` es método de instancia con clave privada.
- `profiles.py`: define los perfiles QuantumSec `LOW` (`ML-KEM-768` + `ML-DSA-65`) y `HIGH` (dual `ML-KEM-768` + `HQC-3` + `ML-DSA-65`). Son perfiles de despliegue, no categorías NIST ni el futuro perfil híbrido QKD+PQC.
- `protocol/`:
  - `identity.py`: `PublicIdentity` (inmutable, no secreta, serializable `to_dict`/`from_dict`) y `MLDSAIdentity` (con capacidad privada de firma).
  - `trust.py`: `TrustedIdentityStore` para pre-aprovisionamiento explícito fuera de banda con protección contra reemplazo silencioso (`overwrite=False`).
  - `party.py`: `PQCParty` combina identidad propia y almacén de confianza de pares.
  - `messages.py`: DTOs inmutables con serialización canónica determinista por prefijos de longitud y separación de dominio (`ServerKeyOffer`, `SignedServerKeyOffer`, `EncapsulationResponse`, `ClientKeyExchange`, `SignedClientKeyExchange`) y mapeos de transporte Base64 (`to_dict` / `from_dict`).
  - `server_offer.py`: `ServerKeyOfferFactory` crea `ResponderKEMState` (claves efímeras con `decapsulate_ml_kem`, `decapsulate_hqc` y `close()`) y `SignedServerKeyOffer`.
  - `initiator.py`: `ServerKeyOfferProcessor` autentica la oferta de Bob antes de encapsular, produciendo `InitiatorKEMState` (secretos cerrables con `close()`) y `ProcessedServerOffer`.
  - `client_exchange.py`: `ClientKeyExchangeFactory` vincula la respuesta al hash canónico de la oferta (`server_offer_hash` SHA-384) y firma como Alice; `ClientKeyExchangeProcessor` ejecuta 11 comprobaciones de seguridad antes de desencapsular en Bob, generando `ResponderSharedSecretState` y cerrando `ResponderKEMState`.
- Estado de los secretos: Alice y Bob recuperan secretos compartidos KEM idénticos tras autenticación mutua. Los secretos no se exportan en crudo hasta que la Fase 5 (KDF) defina el key schedule y la derivación de clave de sesión.
