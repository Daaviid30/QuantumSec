# QuantumSec Web Laboratory redesign

Status: implemented product architecture, 2026-09-08.

## Current-state audit

- The existing web is a single BB84 simulator page. Its strongest reusable pieces are the typed
  FastAPI boundary, capability discovery, fetch/error handling, seeded request validation, ordered
  channel serialization, result fixtures, and test setup.
- The existing page composition, simulation-centric navigation, visual tokens, decorative hero,
  generic metric cards, and protocol selector do not represent the current session/profile model.
- `ui/README.md` is stale relative to source and tests. Per-basis QBER, intercept-resend, all three
  QKD authentication policies, both PQC profiles, both hybrid profiles, reproducible experiment
  records, and the AES-256-GCM data plane are implemented below the web layer.
- `orchestration` already owns the seven stable public profiles, normalized session configuration,
  runtime-only secret context, ordered public trace, categorized metrics, authentication outcome,
  provenance, and secret-safe `SessionResult` serialization.
- `experiments` already owns runtime provisioning, environment capture, immutable versioned records,
  and public-record secret validation. The web should adapt these contracts instead of duplicating
  scientific or cryptographic logic.
- The old `/api/simulations/bb84` response remains useful for bounded per-transmission inspection and
  aggregate Eve diagnostics. It is retained as a compatibility endpoint; new product execution goes
  through the common session/experiment path.
- QKD-only results intentionally expose variable-length `QKD_BITSTRING` material and cannot open the
  AES data plane. `PQC-BASE`, `PQC-DIVERSE`, `HYBRID`, and `HYBRID-DIVERSE` establish a 256-bit
  `SESSION_KEY` that the backend may consume into an opaque protected-session capability.

## Retained and replaced

Retain:

- React 19, TypeScript, Vite, Tailwind 4, Lucide, Recharts, Vitest, and Testing Library;
- FastAPI health/capability routes and the BB84 compatibility route;
- channel draft serialization/validation and capability-driven parameter ranges;
- backend-owned execution, trace, metrics, provenance, environment capture, and key lifecycle;
- current domain, orchestration, experiment, and data-protection implementations unchanged.

Replace:

- `SimulatorPage` as the product root;
- the simulation/research/quantum/security sidebar taxonomy;
- the neon/cyber-laboratory visual language and decorative motion;
- frontend-authored protocol phase claims and the exposed final BB84 bit string;
- isolated result cards with a profile-aware run workspace and real ordered trace.

## Information architecture

1. **Overview** — product definition, start action, seven profile summaries, capability groups, and
   restrained backend readiness.
2. **Laboratory** — profile selection, Guided/Research disclosure, valid profile-derived controls,
   ordered channel/Eve pipeline, execution, outcome, authentication, trace, categorized metrics,
   provenance, and protected-payload demonstration when available.
3. **Runs** — server-held in-process public records, reproducibility metadata, exact-configuration
   rerun action, and selection for comparison.
4. **Compare** — exactly two records, configuration/profile/authentication/provenance differences,
   compatible metric groups, byte layers, outcomes, and explicit measurement limitations.

Campaign analysis is not recreated in the browser. Settings is omitted because there are no real
user settings in scope.

## Event and data flow

```text
Capabilities -> profile-aware builder -> typed session request
  -> Web laboratory service
    -> ExperimentConfig + ExperimentRuntimeFactory
      -> orchestration.run_session
        -> public SessionResult + real ordered trace + categorized metrics
          -> immutable ExperimentRecord -> bounded in-process run store -> browser

Established 256-bit SESSION_KEY
  -> backend-only open_data_plane -> opaque run-bound ProtectedSession
    -> AES-256-GCM protect/verify endpoint -> public sizes/status/ciphertext preview only
```

The browser never receives private identities, shared KEM secrets, QKD final material, `K_SESSION`,
`K_CONFIRM`, or authentication secrets. Navigation and selected records are UI state; execution
facts remain backend state.

## Backend/API changes

- Extend capabilities with the seven public profile definitions and truthful current web features.
- Add `POST /api/sessions` for profile execution and record creation.
- Add `GET /api/runs` and `GET /api/runs/{run_id}` for public run records.
- Add `POST /api/runs/{run_id}/protect` for a bounded backend-owned AES-GCM round trip and tamper
  rejection check when an opaque data-plane capability exists.
- Keep `GET /api/health`, `GET /api/capabilities`, and `POST /api/simulations/bb84` compatible.
- Keep storage explicitly process-local in this phase; durable multi-user persistence and access
  control are production concerns, not silently implied by the research UI.

## Implementation phases

1. Contracts, truthful capabilities, web session service, run store, and API tests.
2. Neutral design tokens, responsive shell, Overview, and capability/profile navigation.
3. Laboratory builder plus profile-aware QKD/PQC/hybrid run visualization.
4. Runs, exact rerun, two-record Compare, compatibility policy, and protected payload strip.
5. Accessibility/error/empty-state polish, updated documentation, and all repository quality gates.

## Explicit non-goals

- No new cryptographic primitives, QKD protocol, security proof, or browser cryptography.
- No fabricated events, artificial run delay, live telemetry, campaign-scale dashboard, or
  cross-domain fastest-profile ranking.
- No durable database, authentication/authorization system, remote job queue, or production key
  custody in this redesign phase.
- No claim that NumPy BB84 runtime is physical QKD latency, throughput, distance, or secret-key rate.
- No claim that HQC-3 is already a published NIST standard.
