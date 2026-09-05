# Agent-Based Extensions — Scope Decision

This document supersedes the earlier proposal to add protocol-controller, adaptive-channel,
experiment-orchestrator, or QKDN-routing agents to the TFM.

## Decision

Autonomous and LLM-based agents are **out of scope for the QuantumSec TFM**. They are not required
by the research question, do not contribute to the definition of done, and would broaden the work
beyond the bounded sequence:

```text
QKD–PQC hybrid integration
    -> AES-256-GCM protected-message demo
    -> reproducible experiment engine
    -> web laboratory
    -> experimental campaign and thesis results
```

Deterministic protocol decisions already implemented in domain code—such as BB84 abort conditions,
privacy-amplification length calculation, and profile validation—remain ordinary explicit protocol
logic. They should not be renamed “agents.” Experiment sweeps should first be transparent,
configuration-driven, and reproducible.

## Future research only

After the TFM, adaptive schedulers or QKDN controllers could be studied if they answer a separate
research question and preserve reproducibility. Any such work would require its own threat model,
decision policy, evaluation methodology, and architecture review. QKDN routing is itself future
work, so an agent controlling it is not part of the present system.

The authoritative scope is [`../TFM_GOAL.md`](../TFM_GOAL.md); the implementation roadmap is
[`tasks.md`](tasks.md).
