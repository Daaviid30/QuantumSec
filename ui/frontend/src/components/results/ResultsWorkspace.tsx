import { Activity, ArrowDown, FlaskConical } from 'lucide-react'
import { lazy, Suspense } from 'react'

import type { BB84SimulationRequest, BB84SimulationResponse, SimulationStatus } from '../../types/api'
import { QubitInspector } from './QubitInspector'
import { ResultsSummary } from './ResultsSummary'
import { ScientificDetails } from './ScientificDetails'

const ResultsCharts = lazy(() =>
  import('./ResultsCharts').then((module) => ({ default: module.ResultsCharts })),
)

interface ResultsWorkspaceProps {
  status: SimulationStatus
  request: BB84SimulationRequest | null
  result: BB84SimulationResponse | null
}

export function ResultsWorkspace({ status, request, result }: ResultsWorkspaceProps) {
  if (!result || !request) {
    return (
      <section className="results-empty" aria-live="polite">
        <div className="results-empty__radar">
          <span />
          <Activity size={20} aria-hidden="true" />
        </div>
        <div className="mt-5 text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-300/60">
          Analysis workspace
        </div>
        <h2 className="mt-2 text-lg font-semibold text-slate-200">
          {status === 'running' ? 'Quantum signals in flight' : 'Awaiting a simulation run'}
        </h2>
        <p className="mt-2 max-w-lg text-center text-sm leading-6 text-slate-500">
          {status === 'running'
            ? 'The backend is preparing, transmitting and measuring the configured BB84 signals.'
            : 'Configure BB84 and its channel pipeline above. Genuine engine output will appear here—no synthetic dashboard data.'}
        </p>
        {status !== 'running' && (
          <div className="mt-5 flex items-center gap-2 text-[10px] uppercase tracking-[0.14em] text-slate-700">
            <FlaskConical size={13} aria-hidden="true" /> Configure <ArrowDown size={11} /> Simulate{' '}
            <ArrowDown size={11} /> Analyze
          </div>
        )}
      </section>
    )
  }

  return (
    <section className="space-y-4" aria-live="polite">
      <ResultsSummary result={result} />
      <div className="grid gap-4 2xl:grid-cols-[0.9fr_1.1fr]">
        <Suspense fallback={<div className="lab-panel min-h-[360px] animate-pulse" aria-label="Loading charts" />}>
          <ResultsCharts result={result} />
        </Suspense>
        <QubitInspector result={result} />
      </div>
      <ScientificDetails request={request} result={result} />
    </section>
  )
}
