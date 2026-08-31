import { BarChart3 } from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { BB84SimulationResponse } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'

interface ResultsChartsProps {
  result: BB84SimulationResponse
}

const tooltipStyle = {
  background: '#0c1820',
  border: '1px solid rgba(103, 232, 249, 0.14)',
  borderRadius: '10px',
  color: '#d9edf2',
  fontSize: '11px',
}

export function ResultsCharts({ result }: ResultsChartsProps) {
  const basisData = [
    { basis: 'Z', Alice: result.alice_basis_counts.Z, Bob: result.bob_basis_counts.Z },
    { basis: 'X', Alice: result.alice_basis_counts.X, Bob: result.bob_basis_counts.X },
  ]
  const outcomeData = [
    { outcome: '|0⟩', count: result.bob_outcome_counts.zero },
    { outcome: '|1⟩', count: result.bob_outcome_counts.one },
  ]
  const keyPipelineData = [
    { stage: 'Raw', bits: result.metrics.n_raw },
    { stage: 'Sifted', bits: result.metrics.n_sifted },
    { stage: 'Candidate', bits: result.postprocessing.n_candidate },
    { stage: 'Reconciled', bits: result.postprocessing.n_reconciled },
    { stage: 'Final', bits: result.postprocessing.n_final },
  ]

  return (
    <Panel className="p-5 lg:p-6">
      <SectionHeading
        eyebrow="Observed distributions"
        title="Basis & measurement balance"
        description="Counts derived from the exact arrays returned by the completed run."
        action={<BarChart3 size={17} className="text-cyan-300/60" aria-hidden="true" />}
      />

      <div className="mt-5 grid gap-5 xl:grid-cols-2">
        <div className="chart-frame xl:col-span-2">
          <div className="chart-label">Secret-material shrinkage</div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={keyPipelineData} margin={{ top: 12, right: 4, left: -24, bottom: 0 }}>
                <CartesianGrid vertical={false} stroke="rgba(148, 163, 184, 0.07)" />
                <XAxis dataKey="stage" tickLine={false} axisLine={false} tick={{ fill: '#64748b', fontSize: 10 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 9 }} />
                <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(103, 232, 249, 0.025)' }} />
                <Bar dataKey="bits" fill="#39d9f2" radius={[4, 4, 0, 0]} maxBarSize={52} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="chart-frame">
          <div className="chart-label">Basis selections</div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={basisData} margin={{ top: 12, right: 4, left: -24, bottom: 0 }}>
                <CartesianGrid vertical={false} stroke="rgba(148, 163, 184, 0.07)" />
                <XAxis dataKey="basis" tickLine={false} axisLine={false} tick={{ fill: '#64748b', fontSize: 10 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 9 }} />
                <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(103, 232, 249, 0.025)' }} />
                <Bar dataKey="Alice" fill="#39d9f2" radius={[4, 4, 0, 0]} maxBarSize={28} />
                <Bar dataKey="Bob" fill="#8b7cf6" radius={[4, 4, 0, 0]} maxBarSize={28} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-legend">
            <span><i className="bg-cyan-300" /> Alice</span>
            <span><i className="bg-violet-400" /> Bob</span>
          </div>
        </div>

        <div className="chart-frame">
          <div className="chart-label">Bob measurement outcomes</div>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={outcomeData} margin={{ top: 12, right: 4, left: -24, bottom: 0 }}>
                <CartesianGrid vertical={false} stroke="rgba(148, 163, 184, 0.07)" />
                <XAxis dataKey="outcome" tickLine={false} axisLine={false} tick={{ fill: '#64748b', fontSize: 10 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 9 }} />
                <Tooltip contentStyle={tooltipStyle} cursor={{ fill: 'rgba(103, 232, 249, 0.025)' }} />
                <Bar dataKey="count" fill="#36c7a0" radius={[4, 4, 0, 0]} maxBarSize={42} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-legend">
            <span><i className="bg-emerald-400" /> Projective outcome count</span>
          </div>
        </div>
      </div>
    </Panel>
  )
}
