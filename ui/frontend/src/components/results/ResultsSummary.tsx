import { Activity, Binary, Clock3, Gauge, KeyRound, RadioTower } from 'lucide-react'

import type { BB84SimulationResponse } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'
import { StatusPill } from '../common/StatusPill'

interface ResultsSummaryProps {
  result: BB84SimulationResponse
}

function formatPercent(value: number | null): string {
  return value === null ? 'Undefined' : `${(value * 100).toFixed(2)}%`
}

export function ResultsSummary({ result }: ResultsSummaryProps) {
  const metrics = [
    { label: 'Raw signals', value: result.metrics.n_raw.toLocaleString(), icon: RadioTower, tone: 'cyan' },
    { label: 'Sifted positions', value: result.metrics.n_sifted.toLocaleString(), icon: Binary, tone: 'violet' },
    { label: 'Candidate bits', value: result.postprocessing.n_candidate.toLocaleString(), icon: Binary, tone: 'blue' },
    { label: 'Estimated QBER', value: formatPercent(result.postprocessing.estimated_qber), icon: Gauge, tone: 'green' },
    { label: 'Final secret bits', value: result.postprocessing.n_final.toLocaleString(), icon: KeyRound, tone: 'green' },
    { label: 'Engine time', value: `${result.metadata.duration_ms.toFixed(1)} ms`, icon: Clock3, tone: 'amber' },
  ]

  return (
    <Panel className="p-5 lg:p-6">
      <SectionHeading
        eyebrow="03 · Analyze"
        title="Run summary"
        description="Sampled estimation, Cascade leakage, confirmation, and final extraction."
        action={
          <StatusPill tone={result.postprocessing.status === 'completed' ? 'green' : 'red'}>
            {result.postprocessing.status === 'completed' ? 'Completed' : 'Secure abort'}
          </StatusPill>
        }
      />

      <div className="mt-5 grid grid-cols-2 gap-3 lg:grid-cols-5">
        {metrics.map((metric) => {
          const Icon = metric.icon
          return (
            <div key={metric.label} className={`metric-card metric-card--${metric.tone}`}>
              <div className="metric-card__icon">
                <Icon size={15} strokeWidth={1.7} aria-hidden="true" />
              </div>
              <div className="mt-5 font-mono text-xl font-semibold tracking-[-0.04em] text-white">
                {metric.value}
              </div>
              <div className="mt-1 text-[10px] uppercase tracking-[0.12em] text-slate-500">{metric.label}</div>
            </div>
          )
        })}
      </div>

      {result.postprocessing.status === 'completed' && result.postprocessing.final_key ? (
        <details className="group mt-4 rounded-xl border border-emerald-400/15 bg-emerald-400/[0.035] px-4 py-3">
          <summary className="cursor-pointer select-none text-xs font-medium text-emerald-200/90">
            Show final simulated key ({result.postprocessing.n_final.toLocaleString()} bits)
          </summary>
          <div className="mt-3 border-t border-emerald-400/10 pt-3">
            <code className="block max-h-48 overflow-auto break-all rounded-lg bg-black/20 p-3 font-mono text-xs leading-5 text-emerald-100 selection:bg-emerald-300 selection:text-slate-950">
              {result.postprocessing.final_key}
            </code>
            <p className="mt-2 text-[10px] leading-4 text-slate-500">
              Simulation output for inspection. Do not use this displayed value as a real cryptographic key.
            </p>
          </div>
        </details>
      ) : result.postprocessing.status === 'aborted' ? (
        <div
          role="alert"
          className="mt-4 rounded-xl border border-red-400/20 bg-red-400/[0.045] px-4 py-3"
        >
          <div className="text-xs font-semibold text-red-200">Final key generation failed</div>
          <div className="mt-1 text-xs leading-5 text-red-200/75">
            {result.postprocessing.abort_reason ?? 'The BB84 session aborted without a final key.'}
          </div>
        </div>
      ) : null}

      <div className="mt-4 flex flex-wrap items-center gap-x-5 gap-y-2 rounded-xl border border-emerald-400/10 bg-emerald-400/[0.025] px-4 py-3 text-[10px] text-slate-500">
        <span className="flex items-center gap-2 text-emerald-300/80">
          <Activity size={12} aria-hidden="true" /> Run {result.metadata.request_id.slice(0, 8)}
        </span>
        <span>
          Seed <strong className="font-mono font-medium text-slate-300">{result.metadata.seed}</strong>
        </span>
        <span>
          Pipeline{' '}
          <strong className="font-medium text-slate-300">
            {result.channels.length ? result.channels.map((channel) => channel.name).join(' → ') : 'Ideal'}
          </strong>
        </span>
      </div>
    </Panel>
  )
}
