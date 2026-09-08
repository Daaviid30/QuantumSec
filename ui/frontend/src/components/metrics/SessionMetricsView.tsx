import { BarChart3, Boxes, GitMerge, RadioTower } from 'lucide-react'

import { formatBytes, formatDurationNs, formatPercent } from '../../lib/profiles'
import type { SessionMetrics } from '../../types/api'

interface SessionMetricsViewProps {
  metrics: SessionMetrics
  /**
   * Configured asymptotic abort threshold from the run's own record, shown beside the phase-error
   * bound it was tested against. Read from the record; never computed or inferred here.
   */
  phaseErrorAbortThreshold?: number | null
}

function MetricRow({ label, value, note }: { label: string; value: string; note?: string }) {
  return (
    <div className="metric-row">
      <span>{label}{note ? <small>{note}</small> : null}</span>
      <strong>{value}</strong>
    </div>
  )
}

export function SessionMetricsView({ metrics, phaseErrorAbortThreshold }: SessionMetricsViewProps) {
  const qkd = metrics.qkd
  const pqc = metrics.pqc
  const hybrid = metrics.hybrid
  const phaseErrorNote =
    phaseErrorAbortThreshold == null
      ? 'Security decision'
      : `Security decision · abort above ${formatPercent(phaseErrorAbortThreshold)}`

  return (
    <section className="surface metrics-panel">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Profile-compatible measurements</p>
          <h2>Results and measurement provenance</h2>
          <p>Only categories produced by this profile are shown; unlike clocks are kept separate.</p>
        </div>
        <BarChart3 size={18} aria-hidden="true" />
      </div>

      <div className="metric-groups">
        {qkd ? (
          <article className="metric-group">
            <h3><RadioTower size={15} aria-hidden="true" /> BB84 numerical simulation</h3>
            <div className="shrinkage" aria-label="BB84 secret material shrinkage">
              {[
                ['Raw', qkd.n_raw],
                ['Sifted', qkd.n_sifted],
                ['Disclosed', qkd.n_disclosed],
                ['Candidate', qkd.n_candidate],
                ['Reconciled', qkd.n_reconciled],
                ['Final', qkd.n_final],
              ].map(([label, value]) => {
                const numeric = Number(value)
                return (
                  <div key={String(label)} className="shrinkage__stage">
                    <span><strong>{numeric.toLocaleString()}</strong><small>{label}</small></span>
                    <i style={{ width: `${Math.max(2, (numeric / Math.max(qkd.n_raw, 1)) * 100)}%` }} />
                  </div>
                )
              })}
            </div>
            <div className="metric-table">
              <MetricRow label="Estimated e_Z" value={formatPercent(qkd.estimated_qber_z)} />
              <MetricRow label="Estimated e_X" value={formatPercent(qkd.estimated_qber_x)} />
              <MetricRow label="Aggregate bit QBER" value={formatPercent(qkd.estimated_qber_aggregated)} note="Cascade input" />
              <MetricRow label="Phase-error bound" value={formatPercent(qkd.phase_error_bound)} note={phaseErrorNote} />
              <MetricRow label="Final secret fraction" value={formatPercent(qkd.final_secret_fraction)} />
              <MetricRow label="Simulator software runtime" value={formatDurationNs(qkd.simulation_time_ns)} />
            </div>
            <p className="measurement-note">NumPy runtime characterizes this software simulation. It is not physical QKD latency, key rate, fiber throughput, or device performance.</p>
          </article>
        ) : null}

        {pqc ? (
          <article className="metric-group">
            <h3><Boxes size={15} aria-hidden="true" /> Executed PQC operations</h3>
            <div className="metric-table">
              <MetricRow label="Cryptographic software time" value={formatDurationNs(pqc.crypto_software_time_ns)} />
              {/*
                Not wrapped in Number(): these fields are `number | null`, and Number(null) is 0,
                which would render an absent measurement as a confident "0 ns". formatDurationNs
                already reports null as "Not available".
              */}
              <MetricRow label="Server offer" value={formatDurationNs(pqc.server_offer_time_ns)} />
              <MetricRow label="Client exchange" value={formatDurationNs(pqc.client_exchange_time_ns)} />
              <MetricRow label="Key schedule" value={formatDurationNs(pqc.key_schedule_time_ns)} />
              <MetricRow label="Finished confirmation" value={formatDurationNs(pqc.confirmation_time_ns)} />
            </div>
            <h4>Communication layers</h4>
            <div className="metric-table">
              <MetricRow label="KEM public material" value={formatBytes(pqc.kem_public_key_bytes)} />
              <MetricRow label="KEM ciphertexts" value={formatBytes(pqc.kem_ciphertext_bytes)} />
              <MetricRow label="Signatures" value={formatBytes(pqc.signature_bytes)} />
              <MetricRow label="Canonical protocol" value={formatBytes(pqc.canonical_protocol_bytes)} />
              <MetricRow label="Serialized transport" value={formatBytes(pqc.serialized_transport_bytes)} />
            </div>
            <p className="measurement-note">These are real liboqs software operations on the environment recorded with this run. One run is evidence, not a benchmark distribution.</p>
          </article>
        ) : null}

        {hybrid ? (
          <article className="metric-group">
            <h3><GitMerge size={15} aria-hidden="true" /> Upper-layer hybrid composition</h3>
            <div className="metric-table">
              <MetricRow label="Ordered contributions" value={hybrid.component_count.toLocaleString()} />
              <MetricRow label="QKD contribution" value={`${hybrid.qkd_contribution_bits.toLocaleString()} bits`} />
              <MetricRow label="ML-KEM contribution" value={formatBytes(hybrid.ml_kem_contribution_bytes)} />
              <MetricRow label="HQC contribution" value={formatBytes(hybrid.hqc_contribution_bytes)} />
              <MetricRow label="Canonical combiner input" value={formatBytes(hybrid.canonical_combiner_input_bytes)} />
              <MetricRow label="Encoding overhead" value={formatBytes(hybrid.encoding_overhead_bytes)} />
              <MetricRow label="Derived application key" value={`${hybrid.derived_session_key_bits} bits`} />
            </div>
            <p className="measurement-note">Composition records provenance and domain separation. It does not imply a new formal hybrid security proof.</p>
          </article>
        ) : null}
      </div>
    </section>
  )
}
