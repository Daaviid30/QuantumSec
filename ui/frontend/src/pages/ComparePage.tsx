import { AlertTriangle, ArrowRight, BarChart3, Check, Info, Minus, Scale } from 'lucide-react'
import { useEffect, useState } from 'react'

import { compareRuns } from '../api/client'
import { useRuns } from '../hooks/useRuns'
import { formatBytes, formatDurationNs, formatPercent } from '../lib/profiles'
import type { CompareResponse, SessionRunResponse } from '../types/api'

interface ComparePageProps {
  refreshKey: number
  initialIds: [string, string] | null
}

function ComparisonRow({ label, left, right }: { label: string; left: string; right: string }) {
  const differs = left !== right
  return <div className={`comparison-row ${differs ? 'comparison-row--different' : ''}`}><span>{label}</span><strong>{left}</strong><i>{differs ? 'differs' : 'same'}</i><strong>{right}</strong></div>
}

/**
 * A metric category is in one of three states, which the UI must not conflate:
 *
 * - `comparable`     — the backend compatibility policy allows the comparison;
 * - `inapplicable`   — neither record produced the category at all (e.g. QKD metrics for two
 *                      PQC-only runs), which is not a warning about anything;
 * - `incomparable`   — at least one record has the category but the policy declines to rank them.
 *
 * The backend flag remains the sole authority over whether a metrics section renders. Only the
 * explanation is derived here.
 */
type CompatibilityState = 'comparable' | 'inapplicable' | 'incomparable'

function compatibilityState(allowed: boolean, presentOnEither: boolean): CompatibilityState {
  if (allowed) return 'comparable'
  return presentOnEither ? 'incomparable' : 'inapplicable'
}

const STATE_COPY: Record<CompatibilityState, string> = {
  comparable: 'Comparable',
  inapplicable: 'Not applicable to this pair',
  incomparable: 'Present, but not comparable',
}

function CompatibilityFlag({ label, state }: { label: string; state: CompatibilityState }) {
  const modifier = state === 'comparable' ? 'yes' : state === 'inapplicable' ? 'neutral' : 'no'
  return (
    <div className={`compatibility-flag compatibility-flag--${modifier}`}>
      {state === 'comparable' ? (
        <Check size={15} aria-hidden="true" />
      ) : state === 'inapplicable' ? (
        <Minus size={15} aria-hidden="true" />
      ) : (
        <AlertTriangle size={15} aria-hidden="true" />
      )}
      <span>
        <strong>{label}</strong>
        <small>{STATE_COPY[state]}</small>
      </span>
    </div>
  )
}

function authLabel(run: SessionRunResponse): string {
  const qkd = run.record.result.authentication.qkd_classical
  const pqc = run.record.result.authentication.pqc_exchange
  return [qkd ? `${qkd.algorithm} (${qkd.executed ? qkd.verified ? 'verified' : 'failed' : 'assumed'})` : null, pqc ? `${pqc.algorithm} (${pqc.verified ? 'verified' : 'failed'})` : null].filter(Boolean).join(' + ') || 'None recorded'
}

export function ComparePage({ refreshKey, initialIds }: ComparePageProps) {
  const { runs, loading, error: runsError } = useRuns(refreshKey)
  const [leftId, setLeftId] = useState(initialIds?.[0] ?? '')
  const [rightId, setRightId] = useState(initialIds?.[1] ?? '')
  const [comparison, setComparison] = useState<CompareResponse | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (initialIds) {
      setLeftId(initialIds[0])
      setRightId(initialIds[1])
    }
  }, [initialIds])

  useEffect(() => {
    if (!initialIds) return
    setBusy(true)
    compareRuns(initialIds).then(setComparison).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : 'Comparison failed.')).finally(() => setBusy(false))
  }, [initialIds, refreshKey])

  const compare = async () => {
    if (!leftId || !rightId || leftId === rightId) return
    setBusy(true)
    setError(null)
    try {
      setComparison(await compareRuns([leftId, rightId]))
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : 'Comparison failed.')
    } finally {
      setBusy(false)
    }
  }

  const left = comparison?.left.record
  const right = comparison?.right.record
  return (
    <div className="page-stack">
      <section className="page-intro"><div><p className="section-kicker">Exactly two records</p><h2>Compare compatible evidence</h2><p>Configuration, composition, authentication, outcome, and byte layers remain comparable. Timing is enabled only for compatible PQC-only records from the same reported environment.</p></div></section>

      <section className="surface compare-picker">
        <label className="field"><span>Run A</span><select value={leftId} onChange={(event) => setLeftId(event.target.value)} disabled={loading}><option value="">Select a run</option>{runs.map((run) => <option key={run.record.run_id} value={run.record.run_id}>{run.record.profile} · {run.record.run_id.slice(0, 8)}</option>)}</select></label>
        <ArrowRight size={16} className="compare-picker__arrow" aria-hidden="true" />
        <label className="field"><span>Run B</span><select value={rightId} onChange={(event) => setRightId(event.target.value)} disabled={loading}><option value="">Select a run</option>{runs.map((run) => <option key={run.record.run_id} value={run.record.run_id}>{run.record.profile} · {run.record.run_id.slice(0, 8)}</option>)}</select></label>
        <button className="button button--primary" type="button" onClick={compare} disabled={busy || !leftId || !rightId || leftId === rightId}><Scale size={15} /> {busy ? 'Comparing…' : 'Compare runs'}</button>
      </section>
      {runsError || error ? <div className="error-box" role="alert">{runsError ?? error}</div> : null}

      {left && right && comparison ? (
        <div className="comparison-workspace">
          <section className="surface comparison-summary">
            <div className="comparison-head"><span>Field</span><strong>{left.profile}<small>{left.run_id.slice(0, 8)}</small></strong><i /><strong>{right.profile}<small>{right.run_id.slice(0, 8)}</small></strong></div>
            <ComparisonRow label="Terminal outcome" left={left.result.status} right={right.result.status} />
            <ComparisonRow label="Establishment" left={left.result.provenance.map((item) => item.algorithm).join(' + ') || 'No accepted material'} right={right.result.provenance.map((item) => item.algorithm).join(' + ') || 'No accepted material'} />
            <ComparisonRow label="Authentication" left={authLabel(comparison.left)} right={authLabel(comparison.right)} />
            <ComparisonRow label="QKD signals" left={left.config.session.qkd_signal_count?.toLocaleString() ?? 'Not applicable'} right={right.config.session.qkd_signal_count?.toLocaleString() ?? 'Not applicable'} />
            <ComparisonRow label="Seed" left={left.seed?.toString() ?? 'OS / liboqs randomness'} right={right.seed?.toString() ?? 'OS / liboqs randomness'} />
            <ComparisonRow label="Ordered QKD stages" left={left.config.qkd_stages.map((stage) => stage.type).join(' → ') || 'Ideal / not applicable'} right={right.config.qkd_stages.map((stage) => stage.type).join(' → ') || 'Ideal / not applicable'} />
            <ComparisonRow label="Accepted key type" left={left.result.established_key.type ?? 'None'} right={right.result.established_key.type ?? 'None'} />
          </section>

          <section className="surface compatibility-panel">
            <div className="section-heading"><div><p className="section-kicker">Compatibility decision</p><h2>Allowed measurement comparisons</h2></div><BarChart3 size={18} aria-hidden="true" /></div>
            <div className="compatibility-flags">
              <CompatibilityFlag
                label="BB84 result metrics"
                state={compatibilityState(
                  comparison.compatibility.qkd_metrics,
                  Boolean(left.metrics.qkd || right.metrics.qkd),
                )}
              />
              <CompatibilityFlag
                label="PQC software timing"
                state={compatibilityState(
                  comparison.compatibility.pqc_timing,
                  Boolean(left.metrics.pqc || right.metrics.pqc),
                )}
              />
              <CompatibilityFlag
                label="Same reported environment"
                state={comparison.compatibility.same_environment ? 'comparable' : 'incomparable'}
              />
            </div>
            {!comparison.compatibility.qkd_metrics && !comparison.compatibility.pqc_timing ? (
              <div className="compatibility-empty">
                <Info size={16} aria-hidden="true" />
                <p>
                  <strong>No metric category can be compared for this pair.</strong>
                  Configuration, composition, authentication, provenance, and terminal outcome remain
                  comparable above. Measurements are not: BB84 simulator runtime and real liboqs
                  operation timing are separate categories and are never placed on a common
                  performance axis.
                </p>
              </div>
            ) : null}
            <ul>{comparison.compatibility.notes.map((note) => <li key={note}>{note}</li>)}</ul>
          </section>

          {comparison.compatibility.qkd_metrics && left.metrics.qkd && right.metrics.qkd ? (
            <section className="surface comparison-metrics"><div className="section-heading"><div><p className="section-kicker">Compatible category</p><h2>BB84 result metrics</h2></div></div>
              <div className="comparison-head"><span>Metric</span><strong>Run A</strong><i /><strong>Run B</strong></div>
              <ComparisonRow label="Estimated e_Z" left={formatPercent(left.metrics.qkd.estimated_qber_z)} right={formatPercent(right.metrics.qkd.estimated_qber_z)} />
              <ComparisonRow label="Estimated e_X" left={formatPercent(left.metrics.qkd.estimated_qber_x)} right={formatPercent(right.metrics.qkd.estimated_qber_x)} />
              <ComparisonRow label="Phase-error bound" left={formatPercent(left.metrics.qkd.phase_error_bound)} right={formatPercent(right.metrics.qkd.phase_error_bound)} />
              <ComparisonRow label="Sifted material" left={`${left.metrics.qkd.n_sifted} bit`} right={`${right.metrics.qkd.n_sifted} bit`} />
              <ComparisonRow label="Final material" left={`${left.metrics.qkd.n_final} bit`} right={`${right.metrics.qkd.n_final} bit`} />
            </section>
          ) : null}

          {comparison.compatibility.pqc_timing && left.metrics.pqc && right.metrics.pqc ? (
            <section className="surface comparison-metrics"><div className="section-heading"><div><p className="section-kicker">Compatible category</p><h2>PQC software operation timing</h2></div></div>
              <div className="comparison-head"><span>Metric</span><strong>Run A</strong><i /><strong>Run B</strong></div>
              <ComparisonRow label="Crypto software time" left={formatDurationNs(left.metrics.pqc.crypto_software_time_ns)} right={formatDurationNs(right.metrics.pqc.crypto_software_time_ns)} />
              <ComparisonRow label="KEM public material" left={formatBytes(left.metrics.pqc.kem_public_key_bytes)} right={formatBytes(right.metrics.pqc.kem_public_key_bytes)} />
              <ComparisonRow label="KEM ciphertexts" left={formatBytes(left.metrics.pqc.kem_ciphertext_bytes)} right={formatBytes(right.metrics.pqc.kem_ciphertext_bytes)} />
              <ComparisonRow label="Canonical protocol" left={formatBytes(left.metrics.pqc.canonical_protocol_bytes)} right={formatBytes(right.metrics.pqc.canonical_protocol_bytes)} />
            </section>
          ) : null}
        </div>
      ) : (
        <section className="empty-workspace"><Scale size={24} /><p className="section-kicker">No active comparison</p><h2>Select two saved records</h2><p>The laboratory will determine which metric categories can be compared without collapsing incompatible provenance.</p></section>
      )}
    </div>
  )
}
