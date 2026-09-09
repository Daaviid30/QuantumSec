# QuantumSec UI — Final Visual / UX / Frontend Review

Status: review completed 2026-09-08, against commit `0bdf3a2` ("UI redesign").
Reviewer role: senior product designer + senior frontend engineer.
Scope: refinement of the completed product. No redesign, no architecture change, no
protocol/semantic change.

---

## 1. Executive assessment

The redesign succeeded at the hard part. The information architecture
(Overview / Laboratory / Runs / Compare) is correct, the `Configure → Run → Observe → Analyze →
Compare` model is legible in the layout, and the scientific contract is respected with unusual
discipline: public profile names are preserved, assumed vs. executed authentication is explicit,
QKD and PQC measurement categories are never merged, and no protocol event is fabricated in the
frontend. The visual language is restrained and correctly avoids the cyberpunk/SaaS traps. The
component decomposition is clean and proportionate — 3.1k lines of frontend for this much
functionality is a good result, and no component needs to be broken up.

The product's remaining weakness is not structure or taste. It is **legibility**. The interface was
tuned as a dense, small-scale console at close reading distance, and the type scale collapsed to
the point where the scientific content is the least readable part of a scientific tool. Measured on
the actual stylesheet: of 89 explicit font declarations, **79 are ≤ 11px**, including 12 at 7px and
24 at 8px. Sampling 66 real text styles against their actual backgrounds, **30 fail WCAG AA
(4.5:1)**, five of them below 3:1. The most important line in an aborted QKD run — the phase-error
abort reason — renders at 10px, and its trace-row equivalent is clipped by `white-space: nowrap` to
roughly half of its 178 characters at 1280px and under a quarter at 1024px.

Separately, a blanket `text-transform: capitalize` in the protocol trace corrupts protocol
identifiers: every QKD run currently displays the stage **"Bb84"**, and the event inspector
displays sources **"Qkd"** and **"Pqc"**. This is visible on the primary surface in the most likely
demo path.

None of this is a structural failure. It is a final calibration pass on typography, contrast,
status semantics, and three interaction gaps. Once corrected, the product is defensible.

---

## 2. What is already strong (do not redesign)

These are working. They were left alone.

- **Information architecture and navigation.** Four views, hash routing, a sticky sidebar with a
  persistent research-boundary statement. Correct and restrained.
- **The scientific measurement boundary.** `SessionMetricsView` separates BB84 simulation, executed
  PQC operations, and hybrid composition into distinct panels with per-panel provenance notes. The
  backend compatibility policy is respected rather than reinterpreted in the browser. This is the
  single best decision in the UI and must not be softened.
- **Assumed vs. executed authentication.** `SecurityEvidence` states `ASSUMED — NOT EXECUTED` /
  `EXECUTED — VERIFIED` / `EXECUTED — FAILED` as text, with a supporting colour, plus mechanism,
  algorithm and trust boundary. Text-first, colour-second — exactly right.
- **Profile selector composition.** Grouping the seven public profiles by family (QKD /
  Post-quantum / Hybrid) makes seven options scannable without a card catalogue.
- **The `CompositionSummary` sidebar.** Alice → (Eve) → channel → Bob, then establishment,
  authentication policy and executed components. It answers "what changed when I switched profile"
  better than most research tooling manages, and the HQC-3 standardization caveat is correctly
  placed.
- **Guided / Research progressive disclosure.** Research controls are genuinely subordinate; the
  ordered stage pipeline editor is a good, honest representation of the real channel list.
- **Secret discipline.** No key material reaches the browser; the record `<pre>` is public-only and
  the event inspector says so. `RunWorkspace.test.tsx` asserts no long bitstring is rendered.
- **Empty and error states exist everywhere** — connection, run workspace, runs table, comparison.
  They are honest ("No protocol events are fabricated before the backend returns a real terminal
  result").
- **The single-accent colour system.** One teal accent, semantic success/warning/danger, no
  per-profile rainbow coding. The palette is correct; only its *contrast levels* need work.

---

## 3. Findings

Severity: **P0** blocking for defense · **P1** important · **P2** polish · **P3** optional.
"Implemented" marks what was carried into Phase 2.

### P0 — Blocking

#### P0-1 · Global type scale is below the readable floor · **Implemented**
- **Screen/component:** every screen; `src/styles/index.css`.
- **Issue:** 79 of 89 font declarations are ≤ 11px. Body copy is 11px, metadata 9px, table headers,
  `dt` labels, comparison `same/differs`, metric notes and `run-outcome__meta` labels are 7–8px.
  There is no scale — 7, 8, 9, 10, 11 are used interchangeably for the same semantic role
  (e.g. metadata labels appear at 7px, 8px and 9px in different panels).
- **Why it matters:** this is a research tool that will be projected in a thesis defense. At 7–9px
  the scientifically load-bearing content — QBER values, phase-error bound, provenance rows,
  authentication detail — is unreadable from the third row of a room, and uncomfortable even at a
  desk. It also reads as *decoration of technicality* rather than density: the tiny text signals
  "technical" without conveying information. The prompt's own instruction applies directly: do not
  preserve tiny text because it looks technical.
- **Proposed fix:** define a disciplined 6-step token scale and map every role onto it, raising the
  floor to 12px and body to 14px. Not "make everything bigger" — collapse five ad-hoc sizes into a
  system, keeping the density hierarchy intact.
- **Risk of change:** medium-high. It is confined to one stylesheet, but many fixed track widths and
  min-heights were sized against the old text (e.g. `.shrinkage__stage` 83px label column,
  `.auth-card dl` 90px column, `.run-outcome__meta` 115px, `.trace-event` 29px/25px tracks,
  `.range-field` 48px output). These must be re-sized in the same pass or rows will clip.

#### P0-2 · 30 of 66 sampled text styles fail WCAG AA contrast · **Implemented**
- **Screen/component:** global; worst in sidebar, protocol trace, metrics rows, compare rows.
- **Issue:** measured against actual backgrounds — `nav-item small` 3.00:1, `metric-row small`
  2.97:1, `trace-event__sequence` 2.83:1, `comparison-row i` ("same"/"differs") 2.97:1,
  `event-inspector__note` 3.07:1, `data-table th` 3.55:1, `field small` (input help text) 3.56:1,
  `--faint` used for body-adjacent copy 3.66:1. The muted ramp is compressed into a narrow band of
  near-identical greys (`#586268`, `#596269`, `#5f696f`, `#606a70`, `#627077`, `#657077`, `#667076`,
  `#687278`, `#697278`…) that carry no hierarchy and all fail.
- **Why it matters:** accessibility floor, and it compounds P0-1 — small *and* low-contrast. Under
  projector gamma these greys disappear entirely. The near-identical greys also mean the intended
  three-level text hierarchy (text / muted / faint) does not actually read as three levels.
- **Proposed fix:** re-derive a three-step muted ramp that clears 4.5:1 on the surfaces it is used
  on, consolidate the ~20 hardcoded greys onto those tokens, and keep genuine de-emphasis by weight
  and size rather than by fading toward the background.
- **Risk of change:** low-medium. Colour-only; no layout impact. Must be verified per surface
  because the same token sits on `--surface`, `--surface-soft` and the sidebar.

#### P0-3 · Protocol identifiers are corrupted to "Bb84", "Qkd", "Pqc" · **Implemented**
- **Screen/component:** `ProtocolTrace.tsx` (trace rows + event inspector); `index.css`
  `.trace-event__copy strong`, `.trace-event__state`, `.event-inspector h3`, `.event-inspector dd`.
- **Issue:** stage/state/source strings are lower-cased backend identifiers rendered through
  `text-transform: capitalize`. CSS capitalization uppercases only the first letter, so the real
  backend stage `bb84` renders as **"Bb84"** in the trace row *and* as the inspector's `<h3>`
  heading, and sources `qkd` / `pqc` render as **"Qkd"** / **"Pqc"**.
- **Why it matters:** this is on the Laboratory surface, in the first screen of every QKD run, in
  the demo path most likely to be shown to a supervisor. Misspelling BB84, QKD and PQC in a
  quantum-cryptography thesis tool undermines the credibility that the rest of the UI earns. It is
  also not a styling preference — it is factually wrong output.
- **Proposed fix:** replace blanket CSS capitalization with a small shared label formatter holding
  an acronym map (BB84, QKD, PQC, HQC, ML-KEM, ML-DSA, HKDF, AES, GCM, QBER…). Backend facts are
  unchanged; only presentation of the identifier is corrected.
- **Risk of change:** low. Pure presentation, no semantic change, easily unit-tested.

### P1 — Important

#### P1-4 · The abort reason — the answer to "why?" — is clipped in the trace and 10px in the banner · **Implemented**
- **Screen/component:** `ProtocolTrace.tsx` `.trace-event__copy small`; `RunWorkspace.tsx`
  `.run-outcome > div > p`.
- **Issue:** real backend abort details are long and load-bearing, e.g. 178 characters:
  *"Per-basis errors Z=0.231481, X=0.208333 give phase-error bound 0.231481, above the configured
  asymptotic threshold 0.110000; aggregate QBER 0.220588 is not the phase-error bound."* The trace
  row renders it with `white-space: nowrap; text-overflow: ellipsis` at 8px. Computing the real
  `.trace-layout` tracks, the detail cell is ≈430px at 1280px and ≈190px at 1024px — about 90 and 40
  of those 178 characters respectively, and proportionally fewer once the type scale is corrected
  (≈55 characters at 1280px/13px). In the outcome banner the same reason is 10px, low-contrast, and
  visually subordinate to the "Session securely aborted" headline.
- **Why it matters:** for an aborted QKD run this sentence *is* the scientific result. Section 6 of
  the review brief requires the first seconds after a run to answer "Established / aborted /
  failed? Why?" — currently "why" is available only by clicking the row and reading a 9px
  paragraph.
- **Proposed fix:** let trace details wrap to a two-line clamp instead of a single truncated line;
  promote the outcome banner's reason to readable body size with an explicit "Abort reason" label
  on non-established outcomes. Backend text is reproduced verbatim.
- **Risk of change:** low. Row height becomes variable, which the flex/grid rows already tolerate.

#### P1-5 · Aborted and failed runs still render green-tinted metadata · **Implemented**
- **Screen/component:** `RunWorkspace.tsx` outcome banner; `.run-outcome__meta` in `index.css`.
- **Issue:** `.run-outcome--aborted` / `--failed` restyle the card border, background and icon, but
  `.run-outcome__meta` keeps its success palette (`#2a3930` border, `#111713` cell background,
  `#c7cfca` text). An aborted run therefore shows a green-tinted metadata strip inside a red card.
  The strip also labels `established_key.bit_length` as "Accepted material" and prints `0 bit` for
  aborts, where the record's key `type` is `null`.
- **Why it matters:** mixed status colour inside a single status card is exactly the kind of
  incoherence that reads as unfinished, and "Accepted material: 0 bit" is a weaker statement than
  the truth, which is that no material was accepted.
- **Proposed fix:** make the meta strip inherit the outcome status; state "No key material accepted"
  when `established_key.type` is `null` rather than "0 bit".
- **Risk of change:** low. Presentation of an already-present record field.

#### P1-6 · No transition from configuration to result after a run · **Implemented**
- **Screen/component:** `LaboratoryPage.tsx`.
- **Issue:** the run workspace renders below the builder grid. After pressing "Run session" nothing
  moves the viewport or focus; on a 1080p projector the outcome banner is below the fold, so the
  visible feedback is only the button changing to "Run again".
- **Why it matters:** it breaks the core `Configure → Run → Observe` loop at its most important
  moment and makes live demonstration awkward — the presenter must scroll to reveal their own
  result. It is also a keyboard/screen-reader gap: focus stays on the button.
- **Proposed fix:** on completion, scroll the run workspace into view and move focus to the outcome
  heading, honouring `prefers-reduced-motion`.
- **Risk of change:** low. No fabricated state; triggered only by a real backend result.

#### P1-7 · `aria-live` wraps the entire run workspace including the full JSON record · **Implemented**
- **Screen/component:** `RunWorkspace.tsx` (`<div className="run-workspace" aria-live="polite">`).
- **Issue:** the live region encloses every section plus the `<pre>` holding the complete
  pretty-printed record (multiple kilobytes). On completion a screen reader is asked to announce
  the whole subtree.
- **Why it matters:** it makes the result unusable with assistive technology — the one announcement
  that matters (outcome + profile + reason) is buried in a JSON dump.
- **Proposed fix:** scope the live region to a concise status sentence; leave the rest as ordinary
  static content reachable by navigation.
- **Risk of change:** low.

#### P1-8 · Compare conflates "not applicable" with "not comparable", and says nothing when nothing is comparable · **Implemented**
- **Screen/component:** `ComparePage.tsx` compatibility panel.
- **Issue:** each compatibility flag has two states — green check or amber warning triangle.
  Verified against the real endpoint: comparing PQC-BASE with PQC-DIVERSE returns
  `qkd_metrics: false`, so "QKD metrics" shows a **warning triangle** although QKD metrics are
  simply *not applicable* to two PQC-only runs. Worse, the cross-domain case (QKD vs PQC) returns
  both metric flags false and the page then renders the summary table, the compatibility panel, and
  then **nothing** — "not comparable" is communicated only by absence.
- **Why it matters:** the brief asks specifically for the distinction between comparable / not
  comparable / not applicable, and this is the page where the thesis' measurement-boundary argument
  is made. A warning icon on an inapplicable category implies something went wrong; silence in the
  cross-domain case loses the argument entirely at the moment it should be made.
- **Proposed fix:** derive three states from data already present — *comparable* (backend flag
  true), *not applicable* (neither record carries the category), *not comparable* (both carry it but
  the backend policy declines) — with distinct icon + wording, and render an explicit statement when
  no metric category is comparable. The backend flag remains the sole authority over whether a
  metrics section renders; only the explanation is added.
- **Risk of change:** low. No change to the compatibility policy.

#### P1-9 · `Number()` casts defeat null handling in PQC timing rows · **Implemented**
- **Screen/component:** `SessionMetricsView.tsx`.
- **Issue:** four rows wrap the value in `Number(...)` before `formatDurationNs`, e.g.
  `formatDurationNs(Number(pqc.server_offer_time_ns))`. `formatDurationNs` returns
  `'Not available'` for `null`, but `Number(null)` is `0`, so a missing measurement would render as
  a confident **"0 ns"**. The type is `number | null` and sibling fields in the same real payload
  (`serialized_transport_bytes`, `hqc_keygen_time_ns`) are in fact `null`.
- **Why it matters:** presenting an absent measurement as a measured zero is a factual defect in a
  measurement panel, and it silently bypasses a formatter that exists precisely to prevent it.
- **Proposed fix:** remove the casts and let the formatter handle `null`.
- **Risk of change:** very low.
- **Related observation, deliberately not "fixed":** in a HYBRID run the backend legitimately
  reports `key_schedule_time_ns: 0` and `confirmation_time_ns: 0` in the PQC panel, because the key
  schedule and Finished exchange happen in the hybrid layer above. Those zeros are backend facts and
  are left exactly as reported; re-labelling them would be the UI inventing an interpretation.

### P2 — Polish

#### P2-10 · Overview hero is at landing-page scale · **Implemented**
- **Issue:** `.overview-intro h2` is `clamp(28px, 3.4vw, 46px)`, more than twice the app's own `<h1>`
  ("Overview", 20px) and disconnected from every other heading. `min-height: 305px` reserves a
  further screen of space.
- **Why it matters:** inverts the semantic hierarchy visually and is the one place the product reads
  as a marketing page instead of a research console.
- **Proposed fix:** bring the hero into the new type scale (~32px ceiling) and reduce reserved
  height. Content and CTA unchanged — this is scale only, not a restructure.
- **Risk:** low.

#### P2-11 · Seven green "current" badges · **Implemented**
- **Issue:** every profile is `status: 'current'`, so Overview renders seven green uppercase status
  words and `ProfileSelector` renders seven green "Current" labels — redundant with each other and
  with the fact that all seven are executable.
- **Why it matters:** the brief warns explicitly against excessive green badges; green should mean
  "this run succeeded", not "this profile exists". It also spends the success colour before any
  result is shown.
- **Proposed fix:** render these in the neutral muted style and reserve success colour for
  non-current statuses only. No wording or data change.
- **Risk:** low.

#### P2-12 · Runs: selecting a record for comparison gives no row feedback, and the control is not a checkbox · **Implemented**
- **Issue:** selection is a `<button>` swapping a `Square`/`CheckSquare` icon; the row itself has no
  selected state (only `:hover`). With several records the selected pair is hard to see, and the
  control is semantically a button rather than a checkbox.
- **Why it matters:** the compare workflow starts here; "which two did I pick?" should be answerable
  at a glance. Section 5 of the brief calls out selected states and comparison-selection affordance.
- **Proposed fix:** add a selected-row treatment and `aria-pressed`→checkbox-appropriate semantics
  while keeping the existing two-item cap and labels.
- **Risk:** low.

#### P2-13 · Compare's "same/differs" signal is effectively invisible · **Implemented**
- **Issue:** the difference indicator is a 7px word at 2.97:1 contrast, and
  `.comparison-row--different` tints the row with `rgba(118,189,200,0.025)` — a 2.5%-opacity wash
  that is imperceptible.
- **Why it matters:** difference highlighting is the entire purpose of the page. As built, the user
  compares the two value columns manually and the indicator adds noise without signal. (The brief
  asks whether these labels add value or noise — they add value, but only if they are visible.)
- **Proposed fix:** make "differs" legible and give the differing row a perceptible marker; keep
  "same" quiet so difference is what stands out.
- **Risk:** low.

#### P2-14 · The protected data plane has no section heading · **Implemented**
- **Issue:** `DataPlaneDemo` is the only `.surface` in the run workspace without the
  `section-heading` (kicker + `h2` + description) pattern used by every sibling section. It opens
  directly with two path chips, so the section is unlabelled.
- **Why it matters:** AES-256-GCM is a named deliverable; an unlabelled panel is both a coherence
  break and a missed explanation of the establishment-plane → data-plane boundary.
- **Proposed fix:** add the standard section heading. No behaviour change.
- **Risk:** very low.

#### P2-15 · Eve diagnostics panel is stylistically detached · **Implemented**
- **Issue:** the Eve panel is the only run-workspace section that is not a `.surface` and does not
  use `section-heading`; its `dt`/`dd` are 7px/9px amber, and labels are abbreviated to "Eve Z / X"
  and "Outcomes 0 / 1".
- **Why it matters:** the brief requires Eve to read as part of the executed channel model rather
  than a decorative coloured card — which is what the current detached amber strip resembles. The
  content is factually good (real aggregate diagnostics); the framing undersells it.
- **Proposed fix:** align it to the shared surface/heading pattern, keep the amber adversarial
  accent as a border/marker, and label the measurements in full. Facts unchanged.
- **Risk:** low.

#### P2-16 · The API documentation link 404s in development · **Implemented**
- **Issue:** `Header.tsx` links to `/docs`, but `vite.config.ts` proxies only `/api`. In dev the link
  resolves against the Vite server on :5173 and fails; FastAPI serves `/docs` on :8000.
- **Why it matters:** a visibly broken affordance in the app chrome, on the path a reviewer would
  plausibly click.
- **Proposed fix:** proxy `/docs` and `/openapi.json` alongside `/api`.
- **Risk:** very low, dev-only configuration.

#### P2-17 · "Assumed" authentication is neutral in the trace but amber in the evidence panel · **Implemented**
- **Issue:** `eventTone()` maps only abort/fail/withheld → danger and verified/established/released/
  completed → success. The real state `assumed_not_executed` therefore falls through to neutral,
  rendering with the same `CircleDot` as `started`, `created` and `encoded` — while
  `SecurityEvidence` renders the same fact in amber as `ASSUMED — NOT EXECUTED`.
- **Why it matters:** assumed-but-not-executed authentication is a first-class distinction in this
  thesis, and the two surfaces currently disagree about its weight. Cross-page terminology and
  status coherence is a stated review objective.
- **Proposed fix:** add a `warning` tone for assumed states, matching the evidence panel, with a
  distinct icon (not colour alone).
- **Risk:** low; derived from the backend state string, no new facts.

#### P2-18 · Phase-error abort threshold is not shown next to the bound it is compared against · **Implemented**
- **Issue:** the metrics panel shows "Phase-error bound — 23.15%" with the note "Security decision",
  but the configured threshold it was tested against (`0.11`) appears only inside the abort reason
  prose.
- **Why it matters:** the abort decision is a comparison of two numbers; showing one of them next to
  the label "Security decision" asks the reader to hold the other in their head.
- **Proposed fix:** surface the configured threshold from `record.config.session.qkd_postprocessing`
  as context on that row. The value already exists in the record — nothing is computed or inferred.
- **Risk:** low. Adds one optional prop.

#### P2-19 · Mode switch has no group semantics · **Implemented**
- **Issue:** `aria-label="Configuration mode"` sits on a plain `<div>` with no role, so it is
  discarded by accessibility APIs; the two `aria-pressed` buttons are announced without their shared
  context.
- **Proposed fix:** give the wrapper a `group` role so the label applies.
- **Risk:** very low.

#### P2-20 · Document title contradicts the measurement boundary · **Implemented**
- **Screen/component:** `ui/frontend/index.html`.
- **Issue:** the browser tab reads `QuantumSec · Simulation Laboratory` and the meta description says
  "a reproducible quantum-security simulation laboratory". The PQC handshakes and the AES-256-GCM
  data plane are *real* liboqs/cryptographic executions, not simulation — that distinction is the
  interface's central scientific claim, and the sidebar itself says "Security laboratory".
  Separately, `theme-color` is `#071016`, a stale value from the pre-redesign palette that does not
  match the app background `#0c0e10`.
- **Why it matters:** the tab title is on screen for the whole defense, and it is the one place the
  product describes itself as something the rest of the UI carefully says it is not.
- **Proposed fix:** retitle to "Security Laboratory", widen the description to name QKD/PQC/hybrid,
  and correct `theme-color`.
- **Risk of change:** none.

#### P2-21 · Dead CSS · **Implemented**
- **Issue:** `.run-workspace .run-record-actions` has no counterpart in any component, and
  `.run-workspace details summary button { margin-left: auto }` targets a button that lives in
  `.record-details__body`, not in `<summary>`.
- **Proposed fix:** delete both.
- **Risk:** none.

### P3 — Optional (reported, not implemented)

- **P3-22 · `recharts` is an unused dependency.** Nothing in `src/` imports it, and
  `dist/assets/ResultsCharts-*.js` is a stale artifact from the pre-redesign build. However
  `docs/UI_REDESIGN.md` explicitly lists Recharts under "Retain", so removing it would contradict
  documented intent and churn the lockfile for no user-visible gain. Left in place deliberately.
- **P3-23 · `LaboratoryPage` recomputes `initial`/`initialStages` on every render** although both are
  only consumed by `useState` initializers. Harmless (the work is trivial) and any fix — `useRef`,
  lazy initializers — adds indirection to otherwise readable code. Not worth touching.
- **P3-24 · Heading levels are flat.** Every section uses `<h2>` under the single `<h1>`, with the
  `section-kicker` as a `<p>`. Defensible as-is; converting kickers to real heading structure would
  be a larger semantic refactor than this pass warrants.
- **P3-25 · `formatPercent`/`formatDurationNs`/`formatBytes` all return the bare string
  `'Not available'`.** Consistent and readable; a typed "absent value" abstraction would be
  over-engineering at this size.
- **P3-26 · Overview capability list renders 15 implemented features** in two columns. Dense, but the
  content is genuinely a list of 15 true things and the brief warns against turning Overview into a
  marketing page. Density reduced only via the global type scale; no content curation applied.

---

## 4. Cross-page design-system recommendations

1. **One type scale, six steps, 12px floor.** Replace the ad-hoc 7/8/9/10/11 band with tokens
   (`--fs-2xs` 12 · `--fs-xs` 13 · `--fs-sm` 14 · `--fs-md` 15 · `--fs-lg` 17 · `--fs-xl` 20+) and
   assign each *semantic role* one step: page title, section title, body, metadata label, mono value,
   micro-label. Hierarchy then comes from weight, colour and spacing — not from shrinking text past
   the readable floor.
2. **A three-step text ramp that actually has three steps.** `--text` / `--muted` / `--faint` should
   be visibly distinct *and* all clear 4.5:1 on the surfaces they occupy. Consolidate the ~20
   hardcoded greys onto them; a grey that is not a token is a bug waiting to drift.
3. **Status is text + shape + colour, never colour alone** — already true in `SecurityEvidence` and
   the compatibility flags; extend the same rule to the trace (assumed vs. neutral) and to the
   outcome banner's metadata strip, and stop spending success-green on non-status facts such as
   "profile is current".
4. **One surface pattern per section.** Every run-workspace and page section should be a `.surface`
   opened by `section-heading` (kicker + `h2` + optional description + optional right-hand badge).
   The Eve panel and the data plane were the two exceptions; both are now aligned. This is the
   cheapest possible coherence win and needs no new components.
5. **Never truncate backend-emitted scientific prose to one line.** Detail strings run to ~200
   characters and carry the result. Clamp to two lines with the full text one interaction away;
   reserve `nowrap` for identifiers and mono values.
6. **Format identifiers in code, not in CSS.** `text-transform: capitalize` cannot know that `bb84`
   is BB84. Domain vocabulary belongs in a shared formatter with an acronym map.

---

## 5. Screens and states manually reviewed

Browser automation was **not available** in this environment, so no screenshots were captured. To
avoid reviewing from source alone, the FastAPI backend was run locally and every representative
state was executed against the real engine (`/api/capabilities`, `/api/sessions`, `/api/runs`,
`/api/compare`), and the resulting payloads were read against the components and stylesheet that
render them. Layout behaviour at each breakpoint was derived by computing the actual grid tracks
from `index.css` (e.g. the 614px trace-list column and 430px detail cell at 1280px cited in P1-4).
Contrast and the type census are measured from the stylesheet, not estimated.

**Verified against real backend payloads:**

| State | Result observed |
| --- | --- |
| Capabilities / backend online | 7 profiles all `current`, 6 channels, 1 adversary, 15 implemented features + 1 future (`qkdn`) |
| `QKD-ASSUMED`, clean BB84 | established, 775-bit `qkd_bitstring`, 5 trace events, assumed auth, no data plane |
| `QKD-ASSUMED` + depolarizing + Eve 15% | established, 753 bit, 1 attack diagnostic |
| `QKD-CLASSICAL-AUTH`, depolarizing p=0.03 | **aborted** — universal-hash confirmation failed; Wegman-Carter auth executed+verified; 156-char trust detail |
| `QKD-PQC-AUTH`, clean | established, ML-DSA-65 executed+verified |
| `QKD-PQC-AUTH` + Eve 100% | **aborted** — phase-error bound 0.2315 > 0.11; 178/199-char abort details |
| `PQC-BASE` | established, 256-bit session key, 8 events, data plane available |
| `PQC-DIVERSE` | established, ML-KEM-768 + HQC-3 provenance |
| `HYBRID` (QKD-PQC-AUTH) | established, 2 provenance entries, qkd+pqc+hybrid metric categories |
| `HYBRID-DIVERSE` (QKD-ASSUMED, bit_flip) | established, 3 provenance entries, assumed QKD auth inside a hybrid run |
| Runs — empty / 9 records | list ordering newest-first confirmed; rerun payload round-trips |
| Compare — QKD vs QKD | `qkd_metrics: true`, BB84 metrics section renders |
| Compare — PQC vs PQC | `pqc_timing: true`, timing section renders |
| Compare — QKD vs PQC (cross-domain) | both metric flags false → **no metrics section and no explanation** (P1-8) |
| Compare — HYBRID vs PQC | both flags false; same silent outcome |
| Compare — established vs aborted QKD | `qkd_metrics: true`; comparison across terminal outcomes works |
| AES-256-GCM data plane | available for `PQC-*` and `HYBRID*` only, correctly hidden for QKD-only runs |

**Breakpoints analysed:** 1920 · 1440 · 1280 · 1024 · 900 · 640 · 320px, focusing on the sticky
sidebar collapse, profile groups, builder grid, trace + inspector split, compare rows, runs table
overflow and long cryptographic names.

**Not verified visually:** rendered antialiasing, real projector gamma, and actual focus-ring
appearance. These are called out as residual risk rather than claimed as reviewed.

---

## 6. Changes selected for implementation

Implemented: **P0-1, P0-2, P0-3** (all three justified as blocking); **P1-4 … P1-9** (all six judged
strong); **P2-10 … P2-21** (twelve low-risk, high-value polish items).

Deliberately **not** implemented: **P3-22 … P3-26**, plus every finding that would have required
redesigning a working part of the product. In particular, no change was made to the information
architecture, the four-view navigation, the profile taxonomy, the Guided/Research model, the
`CompositionSummary` flow, the measurement-boundary panel structure, the backend compatibility
policy, any API contract, any public profile name, or any secret boundary. The metrics panels'
section structure, the security-evidence wording, and the empty-state copy were left as written.

---

## 7. Phase 2 — implementation record

### Design system (`ui/frontend/src/styles/index.css`, rewritten in place)

- **Type scale.** Introduced eight role-assigned tokens (`--fs-micro` 12 · `--fs-xs` 13 ·
  `--fs-sm` 14 · `--fs-md` 15 · `--fs-lg` 17 · `--fs-xl` 21 · `--fs-2xl` 25 · `--fs-3xl` 32) and
  mapped every text style onto one. **No literal `px` font size remains in the stylesheet** — the
  12px floor is now structural, not a convention. Fixed tracks sized against the old text were
  widened in the same pass: `.shrinkage__stage` 83→116px, `.auth-card dl` 90→118px,
  `.run-outcome__meta` 115→136px, `.comparison-row` difference column 55→78px, `.range-field`
  output 48→56px, `.trace-event` markers 29/25→31/26px, `.stage-row__number` 35→40px, inputs and
  buttons 37/38→40px.
- **Text ramp.** Replaced ~20 near-identical hardcoded greys with four tokens whose **minimum**
  contrast across every surface they occupy is `--text` 14.34:1 · `--text-value` 10.32:1 ·
  `--muted` 7.11:1 · `--faint` 6.01:1. All 34 re-sampled styles, including every semantic and
  tinted variant, now clear WCAG AA. The ramp also finally reads as four distinct levels.
- **Density preserved.** Section padding, grid gaps, and panel structure are unchanged; several
  fixed-column grids became `auto-fit`/`minmax` so larger labels reflow instead of clipping
  (`.advanced-grid`, `.stage-parameters`, `.algorithm-list`, `.eve-evidence dl`).
- **Breakpoints.** Builder/overview collapse moved 1180→1240px to match the wider text; the
  `.event-inspector` is now sticky beside the trace; the 640px `overview-intro` font override was
  removed as redundant against the new clamp.
- **Dead CSS removed**: `.run-workspace .run-record-actions`, `.run-workspace details summary
  button`, `.profile-option__state`, `.compatibility-flags span`/`.is-compatible`.

### Components

| File | Change |
| --- | --- |
| `lib/labels.ts` *(new)* | `formatIdentifier` / `formatSource` with a canonical-acronym map, replacing CSS `capitalize`. |
| `lib/labels.test.ts` *(new)* | Pins `bb84→BB84`, `qkd→QKD`, `pqc→PQC`, `finished_b→Finished B`. |
| `components/protocol/ProtocolTrace.tsx` | Formatter applied to stage/state/source; added a `warning` tone with its own icon for `assumed_*` states; details wrap to a two-line clamp instead of a truncated single line. |
| `components/protocol/RunWorkspace.tsx` | Outcome heading now names the profile and outcome and is the focus target; abort reason promoted to labelled body text; `established_key.type === null` reports "None accepted" instead of "0 bit"; metadata strip follows the outcome status; the `aria-live` wrapper around the whole workspace (including the JSON record) removed; Eve panel rebuilt on the shared `surface`/`section-heading` pattern with full measurement labels. |
| `components/metrics/SessionMetricsView.tsx` | Removed four `Number()` casts that would coerce a null measurement to "0 ns"; phase-error row now carries the configured abort threshold from the record. |
| `components/protocol/DataPlaneDemo.tsx` | Added the standard section heading naming the AES-256-GCM data plane and its boundary. |
| `components/laboratory/ProfileSelector.tsx` | Redundant green "Current" label dropped; only non-current statuses are shown, in the attention style. |
| `pages/OverviewPage.tsx` | Same treatment for the seven green `status` badges. |
| `pages/LaboratoryPage.tsx` | Completed runs scroll the outcome into view and move focus to it, honouring `prefers-reduced-motion`; mode switch given `role="group"` so its label applies. |
| `pages/ComparePage.tsx` | Three-state compatibility (comparable / not applicable / not comparable) with distinct icon and wording, plus an explicit panel when no metric category is comparable. |
| `pages/RunsPage.tsx` | Selected rows get a visible state; selection control given checkbox semantics and a fuller accessible name. |
| `components/protocol/RunWorkspace.test.tsx` | Two regression tests: canonical trace spelling, and the aborted-run presentation. |
| `types/api.ts` | Declared the four PQC per-phase timing fields that previously fell through the index signature and required the casts. |
| `vite.config.ts` | Proxy `/docs` and `/openapi.json` so the header's API-documentation link resolves. |
| `index.html` | Title/description no longer call the whole product a "simulation"; `theme-color` corrected to the real background. |

### Phase 3 — validation

| Gate | Result |
| --- | --- |
| `uv run pytest` | **806 passed** (unchanged; no backend code touched) |
| `uv run ruff check .` | **All checks passed** |
| `uv run pyright` | **0 errors, 0 warnings** |
| `npm test` | **11 passed** (6 pre-existing + 5 new) |
| `npm run typecheck` | **clean** |
| `npm run build` | **clean** — 41.3 kB CSS / 261.5 kB JS |

Browser automation was unavailable, so re-verification was done by (a) re-running the contrast and
type-census scripts against the new stylesheet, (b) re-computing the responsive grid tracks, (c)
confirming every `className` in the markup resolves to a rule and no rule is orphaned, and (d)
running the dev server and confirming `/`, `/api/health` and `/docs` all resolve — `/docs` now
returns Swagger UI rather than the app shell.

### Residual risks before the defense

1. **No visual confirmation.** Every change was verified by computation, tests and type-checking, not
   by eye. The type scale in particular touched most of the stylesheet; a human should page through
   Overview, Laboratory (guided + research), a QKD abort, a hybrid run, Runs and Compare at the
   projector resolution before the defense. This is the main outstanding risk.
2. **Vertical length grew.** Larger text makes every page taller — most visibly the run workspace
   and the Overview capability list. The post-run scroll/focus change offsets this for the result,
   but a reviewer scrolls more than before. This was the deliberate trade for readability.
3. **The 15-item Overview capability list** is still dense (P3-26); it was left as content, not
   curated, because the items are all true and trimming them would weaken the Overview's claim.
4. **`recharts` remains an unused dependency** (P3-22), retained to match `docs/UI_REDESIGN.md`.
5. **Hybrid PQC panel still shows `0 ns`** for key schedule and Finished confirmation, because
   `orchestration/hybrid/runner.py` genuinely reports zero for the phases the hybrid layer owns.
   Left as the backend fact; re-labelling it would be the UI inventing an interpretation. Worth a
   sentence in the defense if a reviewer asks.

---

## 8. Follow-up verification

Status: completed 2026-09-08 against the current worktree after the final-review implementation.

The four product surfaces were rechecked with the Vite development server connected to the real
FastAPI backend. Headless Chrome captures covered Overview, Laboratory and Runs at 1440, 1024 and
640 px, including a real `QKD-PQC-AUTH` execution and the automatic transition to its terminal
outcome. This closes the main visual-verification risk recorded above for those representative
states; projector-specific gamma and physical-room viewing distance still require a human check on
the target display.

All P0, P1 and P2 findings remain present in the implementation. The browser pass exposed two small
presentation gaps beyond the original checklist:

- Capability, evidence and comparison panels could still print backend identifiers such as
  `ml_dsa_65`, `intercept_resend`, `qkd`, `pqc` and `qkd_bitstring` outside the protocol trace. The
  shared formatter now covers composition, authentication mechanisms, provenance sources and
  comparison values, including canonical
  `ML-DSA-65`, `Wegman–Carter`, `Intercept-resend`, `QKD` and `PQC` spellings.
- Programmatic focus after a completed run used the browser's rectangular heading outline. It now
  retains a visible focus cue as a restrained accent underline, with the danger colour used for
  aborted and failed outcomes.

The optional P3 observations remain deliberately unchanged: none produces a user-visible defect or
justifies the additional dependency, semantic or abstraction churn in this final calibration pass.

Follow-up quality gates: `806 passed` in Python, `13 passed` in the frontend, Ruff clean, Pyright
clean, TypeScript clean, and the Vite production build completed successfully.
