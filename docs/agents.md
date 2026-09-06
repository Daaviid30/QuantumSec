# Agent-Based Extensions — Scope Decision

Autonomous and LLM-based agents are **FUTURE** and explicitly outside the QuantumSec TFM. They do
not answer the definitive research question, contribute to E1–E5, or satisfy the definition of
done.

Deterministic protocol decisions—BB84 aborts, authentication failures, profile validation,
secret-length policy, hybrid ordering, and experiment scheduling—remain explicit, testable logic.
They must not be relabeled as agents.

The bounded TFM sequence is:

```text
intercept-resend Eve
    -> per-basis QBER and model validation
    -> corrected security-decision model
    -> orchestration contracts
    -> executed QKD authentication
    -> hybrid profiles
    -> AES-256-GCM
    -> E1-E5 experiment campaign
    -> Builder / Run / Compare
```

Adaptive schedulers, autonomous experiment selection, and QKDN-routing agents may be studied only
as separate future research with their own question, threat model, policy, and evaluation.

The authoritative scope is [`../TFM_GOAL.md`](../TFM_GOAL.md); the exact implementation order is
[`tasks.md`](tasks.md).
