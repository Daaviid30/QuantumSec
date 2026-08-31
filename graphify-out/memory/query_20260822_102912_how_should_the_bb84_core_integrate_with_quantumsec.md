---
type: "query"
date: "2026-08-22T10:29:12.691508+00:00"
question: "How should the BB84 core integrate with QuantumSec architecture?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["Basis", "QuantumChannel", "BaseRNG", "sample_projective_outcome()"]
---

# Q: How should the BB84 core integrate with QuantumSec architecture?

## Answer

Expanded from the graph vocabulary via [architecture, dependency, qkd, quantum, channel, measurement, rng, basis, state, protocol, postprocessing]. The graph showed BB84 belongs in qkd/protocols and should compose BaseRNG, Basis, QuantumChannel, sample_projective_outcome, qkd/postprocessing, and qkd/metrics while preserving qkd to quantum/core dependency direction. The implementation follows that boundary and introduces no import cycle.

## Outcome

- Signal: useful

## Source Nodes

- Basis
- QuantumChannel
- BaseRNG
- sample_projective_outcome()