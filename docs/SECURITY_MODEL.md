# BB84 security model

QuantumSec models seeded prepare-and-measure BB84 over logical single-qubit channels. It is a
research simulator, not a security claim for an optical or hardware QKD deployment.

## Key and parameter-estimation model

Alice and Bob choose Z or X independently. Sifting retains every matching-basis position, and both
Z and X positions contribute to the candidate key. Parameter estimation samples independently and
without replacement inside each basis, reveals those positions, and removes them from the
candidate material. A session fails closed unless both bases provide at least one disclosed and one
retained position.

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

The stage shares the run's injected `BaseRNG`, so equal configuration and seed reproduce the full
run. At `f=0` it returns an independent copy without consuming randomness; at `f=1` it avoids an
unnecessary interception-decision draw. It can be placed before or after physical channel stages,
and `ChannelPipeline` preserves that configured order.

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

The default `qber_abort_threshold = 0.11` is applied to the common per-basis phase-error bound. It is
the familiar ideal asymptotic one-way BB84 boundary associated with the symmetric
`1 - 2*h2(Q)` expression; it is not a universal operational threshold for real QKD systems.

Reconciled-key verification uses a 32-bit universal-hash tag by default. This raises the previous
16-bit default but still represents only a bounded simulator agreement check. It does not
authenticate the classical channel, and a 32-bit tag must not be presented as a general deployment
recommendation.

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
- The classical BB84 transcript is assumed authenticated; authentication is not yet executed.
- There is no optical loss model, vacuum outcome, detector dark counts, decoy states, multi-photon
  source model, or photon-number-splitting analysis.
- Amplitude damping is logical-qubit relaxation, not fiber loss.
- Intercept-resend is one pedagogical individual attack, not a general QKD adversary. It does not
  model optimal individual, collective, coherent, entangling-probe, photon-number-splitting,
  detector-blinding, source, or other implementation attacks.
- Eve acts on one logical qubit at a time; there is no optical hardware, loss, multi-photon source,
  quantum memory, side channel, or classical man-in-the-middle model.
- The simulator makes no physical secret-key-rate, distance, throughput, or hardware-latency claim.

## Reference

P. W. Shor and J. Preskill, “Simple Proof of Security of the BB84 Quantum Key Distribution
Protocol,” *Physical Review Letters* 85, 441–444 (2000),
[doi:10.1103/PhysRevLett.85.441](https://doi.org/10.1103/PhysRevLett.85.441).
