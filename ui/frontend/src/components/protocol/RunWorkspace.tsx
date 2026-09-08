import { CheckCircle2, Clipboard, KeyRound, XCircle } from 'lucide-react'
import { useState } from 'react'

import type { SessionRunResponse } from '../../types/api'
import { SessionMetricsView } from '../metrics/SessionMetricsView'
import { DataPlaneDemo } from './DataPlaneDemo'
import { ProtocolTrace } from './ProtocolTrace'
import { SecurityEvidence } from './SecurityEvidence'

interface RunWorkspaceProps {
  run: SessionRunResponse
}

export function RunWorkspace({ run }: RunWorkspaceProps) {
  const { record } = run
  const established = record.result.status === 'established'
  const [copied, setCopied] = useState(false)
  const copyRecord = async () => {
    await navigator.clipboard.writeText(JSON.stringify(record, null, 2))
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1400)
  }

  return (
    <div className="run-workspace" aria-live="polite">
      <section className={`run-outcome run-outcome--${record.result.status}`}>
        <div className="run-outcome__icon">
          {established ? <CheckCircle2 size={23} aria-hidden="true" /> : <XCircle size={23} aria-hidden="true" />}
        </div>
        <div>
          <p className="section-kicker">Terminal outcome</p>
          <h2>{established ? 'Session established' : record.result.status === 'aborted' ? 'Session securely aborted' : 'Session failed'}</h2>
          <p>{record.result.abort_reason ?? 'Every required profile check completed and accepted the session material.'}</p>
        </div>
        <div className="run-outcome__meta">
          <span><small>Profile</small><strong>{record.profile}</strong></span>
          <span><small>Run ID</small><code>{record.run_id.slice(0, 12)}</code></span>
          <span><small>Accepted material</small><strong><KeyRound size={13} /> {record.result.established_key.bit_length} bit</strong></span>
        </div>
      </section>

      {run.attack_diagnostics.length ? (
        <section className="eve-evidence">
          <div><strong>Eve / intercept-resend</strong><span>Real aggregate diagnostics from the executed channel stage.</span></div>
          {run.attack_diagnostics.map((diagnostic) => (
            <dl key={diagnostic.stage_index}>
              <div><dt>Interception</dt><dd>{(diagnostic.intercept_fraction * 100).toFixed(0)}%</dd></div>
              <div><dt>Signals seen</dt><dd>{diagnostic.n_signals_seen.toLocaleString()}</dd></div>
              <div><dt>Intercepted</dt><dd>{diagnostic.n_intercepted.toLocaleString()}</dd></div>
              <div><dt>Eve Z / X</dt><dd>{diagnostic.eve_z_measurements} / {diagnostic.eve_x_measurements}</dd></div>
              <div><dt>Outcomes 0 / 1</dt><dd>{diagnostic.eve_zero_outcomes} / {diagnostic.eve_one_outcomes}</dd></div>
            </dl>
          ))}
        </section>
      ) : null}

      <ProtocolTrace events={record.trace.events} />
      <SessionMetricsView metrics={record.metrics} />
      <SecurityEvidence
        qkd={record.result.authentication.qkd_classical}
        pqc={record.result.authentication.pqc_exchange}
        provenance={record.result.provenance}
      />
      {run.data_plane_available ? <DataPlaneDemo runId={record.run_id} /> : null}

      <details className="surface record-details">
        <summary>Technical record <span>Versioned configuration, environment, trace, and metrics</span></summary>
        <div className="record-details__body">
          <button type="button" className="button button--tertiary" onClick={copyRecord}><Clipboard size={14} /> {copied ? 'Copied' : 'Copy public JSON'}</button>
          <pre>{JSON.stringify(record, null, 2)}</pre>
        </div>
      </details>
    </div>
  )
}
