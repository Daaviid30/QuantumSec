# D1 protected-session evidence

Algorithm: `AES-256-GCM`; key bits: `256`. Plaintext/ciphertext bytes: `42`/`42`; nonce/tag bytes: `12`/`16`.

Round trip verified: `True`.

| scenario | rejected | exception |
| --- | --- | --- |
| ciphertext_bit_flip | True | InvalidTag |
| tag_bit_flip | True | InvalidTag |
| aad_change | True | InvalidTag |
