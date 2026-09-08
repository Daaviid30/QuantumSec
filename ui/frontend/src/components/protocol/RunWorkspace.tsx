import { CheckCircle2, Clipboard, KeyRound, RadioTower, XCircle } from 'lucide-react'
import { useState, type Ref } from 'react'

import type { SessionRunResponse } from '../../types/api'
import { SessionMetricsView } from '../metrics/SessionMetricsView'
import { DataPlaneDemo } from './DataPlaneDemo'
import { ProtocolTrace } from './ProtocolTrace'
import { SecurityEvidence } from './SecurityEvidence'

interface RunWorkspaceProps {
  run: SessionRunResponse
  /** Focus target for the outcome heading, so a completed run moves the reader to its result. */
  outcomeHeadingRef?: Ref<HTMLHeadingElement>
}

const OUTCOME_HEADINGS: Record<string, string> = {
  established: 'Session established',
  aborted: 'Session securely aborted',
}

export function RunWorkspace({ run, outcomeHeadingRef }: RunWorkspaceProps) {
  const { record } = run
  const { status } = record.result
  const established = status === 'established'
  const heading = OUTCOME_HEADINGS[status] ?? 'Session failed'
  const acceptedKey = record.result.established_key
  const [copied, setCopied] = useState(false)
  const copyRecord = async () => {
    await navigator.clipboard.writeText(JSON.stringify(record, null, 2))
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1400)
  }

  return (
    <div className="run-workspace">
      <section className={`run-outcome run-outcome--${status}`}>
        <div className="run-outcome__icon">
          {established ? <CheckCircle2 size={24} aria-hidden="true" /> : <XCircle size={24} aria-hidden="true" />}
        </div>
        <div>
          <p className="section-kicker">Terminal outcome</p>
          {/*
            A completed run moves focus here rather than announcing a live region around the whole
            workspace: the previous `aria-live` wrapper enclosed the full public record, so assistive
            technology was asked to read kilobytes of JSON to reach this one sentence.
          */}
          <h2 ref={outcomeHeadingRef} tabIndex={-1}>
            {record.profile} — {heading}
          </h2>
          {record.result.abort_reason ? (
            <p className="run-outcome__reason">
              <strong>Abort reason</strong>
              {record.result.abort_reason}
            </p>
          ) : (
            <p className="run-outcome__reason">
              Every required profile check completed and accepted the session material.
            </p>
          )}
        </div>
        <div className="run-outcome__meta">
          <span><small>Profile</small><strong>{record.profile}</strong></span>
          <span><small>Run ID</small><code>{record.run_id.slice(0, 12)}</code></span>
          <span>
            <small>Accepted material</small>
            {acceptedKey.type ? (
              <strong><KeyRound size={14} aria-hidden="true" /> {acceptedKey.bit_length} bit</strong>
            ) : (
              <strong>None accepted</strong>
            )}
          </span>
        </div>
      </section>

      {run.attack_diagnostics.length ? (
        <section className="surface eve-evidence">
          <div className="section-heading">
            <div>
              <p className="section-kicker">Executed adversarial stage</p>
              <h2>Eve intercept-resend diagnostics</h2>
              <p>Real aggregate counts from the intercept-resend stage as it was applied in the ordered channel pipeline. Alice&apos;s and Bob&apos;s private choices are not exposed.</p>
            </div>
            <RadioTower size={18} aria-hidden="true" />
          </div>
          {run.attack_diagnostics.map((diagnostic) => (
            <dl key={diagnostic.stage_index}>
              <div><dt>Interception fraction</dt><dd>{(diagnostic.intercept_fraction * 100).toFixed(0)}%</dd></div>
              <div><dt>Signals seen</dt><dd>{diagnostic.n_signals_seen.toLocaleString()}</dd></div>
              <div><dt>Signals intercepted</dt><dd>{diagnostic.n_intercepted.toLocaleString()}</dd></div>
              <div><dt>Eve Z-basis measurements</dt><dd>{diagnostic.eve_z_measurements.toLocaleString()}</dd></div>
              <div><dt>Eve X-basis measurements</dt><dd>{diagnostic.eve_x_measurements.toLocaleString()}</dd></div>
              <div><dt>Eve outcome 0 / 1</dt><dd>{diagnostic.eve_zero_outcomes.toLocaleString()} / {diagnostic.eve_one_outcomes.toLocaleString()}</dd></div>
            </dl>
          ))}
        </section>
      ) : null}

      <ProtocolTrace events={record.trace.events} />
      <SessionMetricsView
        metrics={record.metrics}
        phaseErrorAbortThreshold={record.config.session.qkd_postprocessing?.phase_error_abort_threshold ?? null}
      />
      <SecurityEvidence
        qkd={record.result.authentication.qkd_classical}
        pqc={record.result.authentication.pqc_exchange}
        provenance={record.result.provenance}
      />
      {run.data_plane_available ? <DataPlaneDemo runId={record.run_id} /> : null}

      <details className="surface record-details">
        <summary>Technical record <span>Versioned configuration, environment, trace, and metrics</span></summary>
        <div className="record-details__body">
          <button type="button" className="button button--tertiary" onClick={copyRecord}><Clipboard size={14} aria-hidden="true" /> {copied ? 'Copied' : 'Copy public JSON'}</button>
          <pre>{JSON.stringify(record, null, 2)}</pre>
        </div>
      </details>
    </div>
  )
}
