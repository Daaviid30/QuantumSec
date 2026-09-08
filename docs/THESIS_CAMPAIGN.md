# Thesis Campaign `thesis-v1.0.1`

## Status

SMOKE and THESIS passed. The definitive local dataset is `results/thesis_v1/`; generated results
remain Git-ignored by repository policy. Its sealed manifest reports `status: complete`, raw
JSON/CSV SHA-256 values, 13 PDF and 13 PNG figures, and `secret_audit: PASS`.

| Experiment | Records | Fixed design |
|---|---:|---|
| E1 | 100 | 50 each for PQC-BASE/PQC-DIVERSE; five discarded warm-ups per profile |
| E2 | 250 | 25 channel conditions; 10 seeded replicates; 20,000 signals |
| E3 | 550 | 11 intercept fractions; 50 seeded replicates; 10,000 signals |
| E4 | 90 | three profiles; 30 paired-seed replicates; 8,192 signals |
| E5 | 120 | four profiles; 30 runs each; three discarded warm-ups per condition |
| D1 | 1 | HYBRID-DIVERSE + QKD-PQC-AUTH to AES-256-GCM tamper matrix |

## Reproduction

Run the quality gate first, then execute:

```bash
uv run python -m experiments.campaigns.thesis_v1 \
  --preset smoke --output results/thesis_v1_smoke

uv run python -m experiments.campaigns.thesis_v1 \
  --preset thesis --output results/thesis_v1
```

Regenerate analysis without executing sessions:

```bash
uv run python -m experiments.analysis.thesis_v1 results/thesis_v1
```

Analysis verifies completeness and raw hashes before producing summaries and figures. It preserves
non-applicable values as null, pools exact binomial counts before Wilson 95% intervals, and keeps
QKD numerical simulation time separate from liboqs cryptographic and hybrid-composition timings.

## Interpretation boundary

The generated `campaign_report.md` is the source for numerical results and H1-H5 status. Its claims
are bounded to the recorded software/hardware environment and logical-qubit model. The campaign
does not measure physical QKD latency/SKR/distance, does not model a general Eve, and does not claim
a formal robust-combiner proof.
