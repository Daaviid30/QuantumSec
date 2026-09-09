# E4 security assumptions

| profile | authentication_executed | bootstrap_requirement | mechanism | guarantee_nature | per_session_secret_consumption | persistent_identity_or_key | evidence_type | forgery_or_security_assumption | main_limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QKD-ASSUMED | no | external authenticated-channel assumption | not executed | external assumption | N/A | external | none | authenticated classical channel assumed | does not implement authentication |
| QKD-CLASSICAL-AUTH | yes | pre-shared secret | Toeplitz-U2 + one-time mask (Wegman-Carter style) | information-theoretic under construction/PSK assumptions | recorded secret_bits_consumed | fresh sufficient PSK material | authentication tags | recorded forgery bound under one-time-key discipline | consumes pre-shared secret material |
| QKD-PQC-AUTH | yes | pre-provisioned ML-DSA public identities | ML-DSA-65 signatures | computational post-quantum signature authentication | none | persistent private identity and trusted public keys | digital signatures | ML-DSA-65 computational assumptions | computational guarantee and identity provisioning |
