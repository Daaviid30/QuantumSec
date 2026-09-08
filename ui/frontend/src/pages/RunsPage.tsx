import { CheckSquare, FlaskConical, RefreshCw, Scale, Square } from 'lucide-react'
import { useEffect, useState } from 'react'

import { useRuns } from '../hooks/useRuns'
import { requestFromRecord } from '../lib/profiles'
import type { SessionRunRequest } from '../types/api'

interface RunsPageProps {
  refreshKey: number
  onRerun: (request: SessionRunRequest) => void
  onCompare: (ids: [string, string]) => void
}

export function RunsPage({ refreshKey, onRerun, onCompare }: RunsPageProps) {
  const { runs, loading, error } = useRuns(refreshKey)
  const [selected, setSelected] = useState<string[]>([])
  useEffect(() => setSelected((current) => current.filter((id) => runs.some((run) => run.record.run_id === id))), [runs])

  const toggle = (runId: string) => {
    setSelected((current) => current.includes(runId) ? current.filter((id) => id !== runId) : current.length < 2 ? [...current, runId] : current)
  }

  return (
    <div className="page-stack">
      <section className="page-intro">
        <div><p className="section-kicker">Process-local record store</p><h2>Reproducible session evidence</h2><p>Every run retains normalized configuration, seed where applicable, environment, provisioning, ordered trace, metrics, and terminal outcome—never secret key material.</p></div>
        <button className="button button--secondary" type="button" disabled={selected.length !== 2} onClick={() => onCompare(selected as [string, string])}><Scale size={15} /> Compare selected <span>{selected.length}/2</span></button>
      </section>

      <section className="surface runs-panel">
        <div className="section-heading">
          <div><p className="section-kicker">Saved runs</p><h2>Execution history</h2><p>Newest records appear first. Storage is intentionally bounded to this backend process.</p></div>
          <span className="quiet-badge">{runs.length} records</span>
        </div>
        {loading ? <div className="loading-row"><RefreshCw className="spin" size={16} /> Loading run records…</div> : null}
        {error ? <p className="error-box" role="alert">{error}</p> : null}
        {!loading && !error && runs.length === 0 ? (
          <div className="table-empty"><FlaskConical size={20} /><strong>No runs recorded yet</strong><span>Execute a profile in the Laboratory to create reproducible evidence.</span></div>
        ) : null}
        {runs.length ? (
          <div className="table-scroll">
            <table className="data-table runs-table">
              <thead><tr><th aria-label="Select for comparison" /><th>Run</th><th>Profile</th><th>Outcome</th><th>Configuration</th><th>Recorded</th><th>Actions</th></tr></thead>
              <tbody>
                {runs.map((run) => {
                  const record = run.record
                  const checked = selected.includes(record.run_id)
                  const disabled = selected.length === 2 && !checked
                  return (
                    <tr key={record.run_id} className={checked ? 'is-selected' : undefined}>
                      <td>
                        <button
                          className="select-run"
                          type="button"
                          role="checkbox"
                          aria-checked={checked}
                          onClick={() => toggle(record.run_id)}
                          disabled={disabled}
                          aria-label={`${checked ? 'Remove' : 'Add'} run ${record.run_id.slice(0, 8)} (${record.profile}) ${checked ? 'from' : 'to'} comparison`}
                        >
                          {checked ? <CheckSquare size={16} aria-hidden="true" /> : <Square size={16} aria-hidden="true" />}
                        </button>
                      </td>
                      <td><code>{record.run_id.slice(0, 8)}</code><small>{record.result.session_id.slice(0, 12)}</small></td>
                      <td><strong>{record.profile}</strong><small>{record.experiment_kind}</small></td>
                      <td><span className={`outcome-label outcome-label--${record.result.status}`}>{record.result.status}</span>{run.data_plane_available ? <small>Data plane ready</small> : null}</td>
                      <td><span>{record.config.session.qkd_signal_count ? `${record.config.session.qkd_signal_count.toLocaleString()} signals` : 'Profile-derived PQC'}</span><small>{record.config.qkd_stages.length ? `${record.config.qkd_stages.length} QKD stages` : 'No channel stages'}</small></td>
                      <td><span>{new Date(record.timestamp_utc).toLocaleDateString()}</span><small>{new Date(record.timestamp_utc).toLocaleTimeString()}</small></td>
                      <td><button className="text-button" type="button" onClick={() => onRerun(requestFromRecord(record))}><RefreshCw size={13} /> Re-run exact config</button></td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : null}
      </section>
    </div>
  )
}
