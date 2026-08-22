import { Activity, Binary, Clock3, Gauge, GitCompareArrows, RadioTower } from 'lucide-react'

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
    {
      label: 'Sifting efficiency',
      value: formatPercent(result.metrics.sifting_efficiency),
      icon: GitCompareArrows,
      tone: 'blue',
    },
    { label: 'QBER', value: formatPercent(result.metrics.qber), icon: Gauge, tone: 'green' },
    { label: 'Engine time', value: `${result.metadata.duration_ms.toFixed(1)} ms`, icon: Clock3, tone: 'amber' },
  ]

  return (
    <Panel className="p-5 lg:p-6">
      <SectionHeading
        eyebrow="03 · Analyze"
        title="Run summary"
        description="Metrics adapted directly from BB84Result and its SiftingResult."
        action={<StatusPill tone="green">Completed</StatusPill>}
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
