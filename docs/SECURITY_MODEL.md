# BB84 security model

QuantumSec models seeded prepare-and-measure BB84 over logical single-qubit channels. It is a
research simulator, not a security claim for an optical or hardware QKD deployment.

## Key and parameter-estimation model

Alice and Bob choose Z or X independently. Sifting retains every matching-basis position, and both
Z and X positions contribute to the candidate key. Parameter estimation samples independently and
without replacement inside each basis, reveals those positions, and removes them from the
candidate material. A session fails closed unless both bases provide at least one disclosed and one
retained position.

When an explicit total sample size creates an exact proportional tie, the injected RNG decides
which basis receives the unavoidable extra position. This avoids a fixed Z/X label bias while
remaining reproducible.

The protocol transcript exposes:

- `estimated_qber_z` and `estimated_qber_x`: errors in the disclosed Z and X subsets;
- `estimated_qber_aggregated`: the count-weighted error rate over all disclosed positions;
- `diagnostic_qber_z`, `diagnostic_qber_x`, and `diagnostic_qber_aggregated`: simulator-only rates
  over the complete sifted material.

Only estimated values available from public disclosure affect protocol decisions. Full-sifted
diagnostics are never used to authorize secret extraction.

## Intercept-resend threat model

QuantumSec implements one explicit adversary model: seeded intercept-resend on logical BB84
qubits. It is an ordered `QuantumChannel` stage, not a branch inside `BB84Protocol`. For each
signal, Eve independently intercepts with configured probability `f`. If she intercepts, she
chooses Z or X uniformly, measures the received density matrix, prepares a fresh BB84 state from
her own basis and outcome, and resends that state. She receives neither Alice's bit/basis nor Bob's
future basis.

In an otherwise ideal BB84 run, a sifted bit is disturbed only when Eve intercepts, chooses the
opposite basis (probability `1/2`), and Bob obtains the opposite bit after measuring in Alice's
basis (probability `1/2`). Therefore

```text
expected induced QBER = f * 1/2 * 1/2 = f/4
```

The simulator never inserts this formula into a run. Errors emerge from preparation, Eve's sampled
measurement and resend, Bob's sampled measurement, and sifting. The same existing per-basis
parameter estimation and phase-error policy decides whether to abort. Eve diagnostics are
external observations and are not passed into any security decision.

The backend derives a domain-separated `SeededRNG` stream for each adversarial stage while the
protocol retains the stream identified directly by the run seed. Eve's stochastic choices
therefore cannot advance Bob's or post-processing's PRNG cursor, while equal configuration and seed
still reproduce the full run. At `f=0` Eve returns an independent copy without consuming her own
stream; at `f=1` she avoids an unnecessary interception-decision draw. The stage can be placed
before or after physical channel stages, and `ChannelPipeline` preserves that configured order.
Diagnostics accumulate per instance and can be cleared explicitly without rewinding Eve's RNG.

## Phase-error relation

The implemented asymptotic model follows the BB84/CSS separation of bit and phase errors described
by Shor and Preskill. Applying a Hadamard exchanges Z and X and exchanges bit and phase errors.
Consequently, in the asymptotic representative-sampling model:

```text
phase error of retained Z positions <= estimated_qber_x
phase error of retained X positions <= estimated_qber_z
```

QuantumSec currently mixes both retained subsets and applies one privacy-entropy penalty to the
whole candidate. Therefore it uses the common bound

```text
phase_error_bound = max(estimated_qber_z, estimated_qber_x)
```

This maximum is not an undocumented symmetry heuristic: it upper-bounds the phase-error rate of
each basis-conditioned candidate subset before they are mixed. It is conservative relative to a
tighter basis-weighted treatment, which is not implemented.

Aggregated QBER is the sampled bit-error estimate used to size Cascade blocks. It is not
automatically a phase-error bound. Actual Cascade parity leakage is measured and subtracted, so an
additional idealized `n*h2(bit_error_rate)` term is not subtracted a second time.

## Secret-length and abort policy

The estimator receives semantically explicit inputs and computes

```text
floor(
    n_candidate * (1 - h2(phase_error_bound))
    - reconciliation_leakage
    - verification_leakage
    - security_margin_bits
)
```

A non-positive result produces no final material and the session aborts. Missing per-basis data,
non-finite or out-of-range rates, invalid lengths, or a phase-error value outside the entropy
model's `[0, 0.5]` domain cannot silently produce a key.

The default `phase_error_abort_threshold = 0.11` is applied to the common per-basis phase-error
bound. The legacy constructor name `qber_abort_threshold` remains a normalized compatibility alias.
The default is the familiar ideal asymptotic one-way BB84 boundary associated with the symmetric
`1 - 2*h2(Q)` expression; it is not a universal operational threshold for real QKD systems.

Reconciled-key verification uses a 32-bit universal-hash tag by default. This raises the previous
16-bit default but still represents only a bounded simulator agreement check. It does not
authenticate the classical channel, and a 32-bit tag must not be presented as a general deployment
recommendation.

## Classical-channel authentication profiles

The low-level `BB84SessionResult` continues to model post-processing under an authenticated-channel
assumption. The upper `orchestration/` layer makes the policy and acceptance barrier explicit:

- `QKD-ASSUMED` reports `ASSUMED_NOT_EXECUTED`, produces no authentication evidence, and retains
  the exact trust statement that authentication is external.
- `QKD-CLASSICAL-AUTH` executes bilateral 128-bit one-time universal-hash tags from explicitly
  provisioned PSK material.
- `QKD-PQC-AUTH` executes bilateral ML-DSA-65 signatures verified with pre-provisioned trusted
  public identities.

The canonical public transcript contains Alice's and Bob's basis announcements, retained sifting
indices, per-basis estimation indices/bases/disclosed bits, every Cascade permutation and both
parties' root/binary parities (including look-back), the reconciled-key comparison seed and tags,
and the privacy-amplification seed. Raw, candidate, reconciled, and final keys are excluded. Every
event is length-delimited and binds a domain, version, 128-bit session identifier, direction,
sequence number, and message type. Two directional checkpoint frames then bind that complete
ordered encoding. Persistent authentication contexts reserve session identifiers and reject their
reuse; callers that rebuild a context must preserve this public replay state or provision a fresh,
unique identifier through their surrounding session system.

This is explicitly an end-of-transcript checkpoint model, not a distributed message-by-message
network simulation. Tampering may therefore cause computation to be wasted before the checkpoint
fails (a denial-of-service limitation), but unverified data can never produce accepted key
material at the orchestration boundary.

### One-time Toeplitz/Wegman-Carter-style construction

For a canonical `n`-bit frame and a `t`-bit tag, the classical profile computes

```text
tag = Toeplitz_selector(frame) XOR fresh_secret_mask
```

where the secret Toeplitz selector consumes `n + t - 1` fresh bits and the independent mask
consumes `t` fresh bits. Thus each direction/checkpoint consumes exactly `n + 2t - 1` PSK bits.
The current `t = 128` policy yields a forgery/substitution bound no larger than `2^-128` per
fresh-key checkpoint under the XOR-universal Toeplitz-family and uniform independent-secret
assumptions. Both selector and mask are single-use; this implementation claims no hash-key or
authentication-key recycling. Reuse of the same session/direction/sequence/type context and
material exhaustion fail explicitly. Tags use `hmac.compare_digest`, without claiming general
side-channel resistance for the Python process.

The construction follows the universal-hashing authentication framework of Wegman and Carter and
uses the conservative fresh-key policy because no key-recycling theorem is relied upon here. The
PSK must exist before the first authenticated QKD session and is separate from every QKD key,
verification seed, privacy-amplification seed, and PQC-derived key.

### ML-DSA-65 checkpoint authentication

Each signature covers the exact canonical authentication frame, including the full public
transcript plus frame domain/version/session/direction/sequence/type/length. Alice's private
identity signs Alice-to-Bob and Bob's signs Bob-to-Alice; the receiver resolves the expected owner
in its pre-provisioned `TrustedIdentityStore`. Public identities are provisioning cost, not
per-session transport bytes. Measurements record sign/verify operations and time, signature and
authenticated bytes, Python/platform/processor, and the `liboqs`/`liboqs-python` versions; timings
are observations of that recorded environment, not universal performance claims.

Classical-channel authentication protects transcript authenticity and integrity. It does not
protect quantum states: with valid ML-DSA or PSK evidence, full intercept-resend still produces a
normal BB84 phase-error abort.

## Hybrid session composition

`HYBRID` combines only an accepted BB84 final bitstring and authenticated ML-KEM-768 shared secret.
`HYBRID-DIVERSE` additionally includes the authenticated HQC-3 shared secret. The QKD contribution
is released through `AuthenticatedQKDSessionResult`; KEM contributions are released by a
single-use, transcript/session/profile-bound PQC capability only after both ML-DSA-65 signatures
verify. The hybrid path does not consume the pure-PQC derived session key.

`QuantumSec/HybridSession/v1/SecretInput` encodes the fixed component order with explicit labels,
sources, algorithms, encodings, exact bit and byte lengths. The public context under
`QuantumSec/HybridSession/v1/Transcript` binds the shared session ID, selected QKD authentication
policy and transcript hash, authenticated PQC transcript and internal profile, algorithm order,
and versions. Its SHA-384 digest salts independent HKDF-SHA-384 derivations under the SessionKey
and ConfirmationKey domains. A versioned `QuantumSec/HybridSession/v1/Finished` HMAC-SHA-384
exchange verifies Bob first and then Alice, whose MAC binds Bob's verify data. Key equality is not
the protocol decision.

This is a domain-separated canonical hybrid composition and cryptographic diversification design,
not a new formal robust combiner. It does not establish that one secure component makes the result
secure under every adversary. Passing QKD material through HKDF-SHA-384 places the derived key in
the computational model of that construction; it is not automatically an information-theoretic
output. Numerical BB84 runtime and real PQC software runtime are separate categories, not a
physical hybrid-latency claim.

## AES-256-GCM data plane

The data plane accepts only an established 256-bit `SESSION_KEY` from `PQC-BASE`, `PQC-DIVERSE`,
`HYBRID`, or `HYBRID-DIVERSE`. QKD-only results expose a variable-length `QKD_BITSTRING` and are
rejected: this phase does not silently truncate, hash, pad, or introduce a new application HKDF.

Payload protection uses `cryptography`'s high-level AES-GCM AEAD with a 32-byte key, a 96-bit nonce,
and the full 128-bit authentication tag. Under a correct secret key and a nonce never reused with
that key, it provides confidentiality plus integrity/authenticity for ciphertext and AAD. It does
not authenticate Alice's or Bob's identity; peer authentication belongs to the establishment
plane.

Nonce policy is deterministic and direction separated. The first four bytes are `00000001` for
Alice-to-Bob or `00000002` for Bob-to-Alice, followed by a monotonic unsigned 64-bit big-endian
sequence. Each direction has an independent lock-protected counter, their nonce sets cannot
overlap, and exhaustion fails without wrapping.

Internal AAD under `QuantumSec/DataPlane/v1/AAD` binds the data-plane version, established session
ID and public profile, `SessionResult` version, key type and size, normalized public session
context, record direction and sequence, declared application-AAD length, and application AAD.
Changing ciphertext, tag, or application AAD causes `cryptography.exceptions.InvalidTag`; AEAD
decryption returns plaintext only after successful tag verification.

Nonce uniqueness on encryption is not network replay protection. This phase implements no replay
window or receive sequence policy. Closing session capabilities releases Python references and
prevents accidental reuse, but does not claim memory zeroization.

## Analytical channel expectations

For uniformly random BB84 input bits and the channel parameterizations implemented in `qkd/`:

| Channel | Expected `e_Z` | Expected `e_X` |
|---|---:|---:|
| Identity | `0` | `0` |
| Depolarizing, `E(rho)=(1-p)rho+pI/2` | `p/2` | `p/2` |
| Bit flip | `p` | `0` |
| Phase flip | `0` | `p` |
| Pauli `(px, py, pz)` | `px + py` | `pz + py` |
| Amplitude damping `gamma` | `gamma/2` | `(1-sqrt(1-gamma))/2` |

These identities validate the logical-qubit simulator. They do not predict physical secret-key
rates.

## Security boundary and remaining limitations

- The secret-length model is asymptotic and uses sampled point estimates as asymptotic rates.
- There is no composable finite-key proof or finite-sample confidence correction.
- Authentication is batched at terminal bilateral transcript checkpoints rather than simulated
  on a distributed network message by message; this leaves a denial-of-service/wasted-work window.
- There is no optical loss model, vacuum outcome, detector dark counts, decoy states, multi-photon
  source model, or photon-number-splitting analysis.
- Amplitude damping is logical-qubit relaxation, not fiber loss.
- Intercept-resend is one pedagogical individual attack, not a general QKD adversary. It does not
  model optimal individual, collective, coherent, entangling-probe, photon-number-splitting,
  detector-blinding, source, or other implementation attacks.
- Eve acts on one logical qubit at a time; there is no optical hardware, loss, multi-photon source,
  quantum memory, side channel, or classical man-in-the-middle model.
- The simulator makes no physical secret-key-rate, distance, throughput, or hardware-latency claim.
- The hybrid construction has no formal robust-combiner proof and no automatic
  information-theoretic output claim.
- The AES-GCM data plane does not provide identity authentication, network anti-replay, or memory
  zeroization.

## Reference

P. W. Shor and J. Preskill, “Simple Proof of Security of the BB84 Quantum Key Distribution
Protocol,” *Physical Review Letters* 85, 441–444 (2000),
[doi:10.1103/PhysRevLett.85.441](https://doi.org/10.1103/PhysRevLett.85.441).

M. N. Wegman and J. L. Carter, “New hash functions and their use in authentication and set
equality,” *Journal of Computer and System Sciences* 22(3), 265–279 (1981),
[doi:10.1016/0022-0000(81)90033-7](https://doi.org/10.1016/0022-0000(81)90033-7).

H. Krawczyk, “LFSR-based hashing and authentication,” *CRYPTO '94*, LNCS 839, 129–139 (1994),
[doi:10.1007/3-540-48658-5_11](https://doi.org/10.1007/3-540-48658-5_11).

C. Portmann, “Key recycling in authentication,” *IEEE Transactions on Information Theory* 60(7),
4383–4396 (2014), [IACR ePrint 2012/058](https://eprint.iacr.org/2012/058). QuantumSec does not
implement or claim the recycling result in this phase.
