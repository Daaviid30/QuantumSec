import {
  Atom,
  Binary,
  Check,
  KeyRound,
  RadioTower,
  ScanLine,
  ShieldCheck,
  SlidersHorizontal,
  UserRound,
} from 'lucide-react'

import type { FeatureCapability, SimulationStatus } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'

interface QuantumFlowProps {
  features: FeatureCapability[]
  status: SimulationStatus
  channelNames: string[]
}

const mainSteps = [
  { label: 'Alice', detail: 'Random bit + basis', icon: UserRound },
  { label: 'State prep', detail: 'BB84 encoding', icon: Atom },
  { label: 'Quantum channel', detail: 'Sequential CPTP map', icon: RadioTower },
  { label: 'Bob', detail: 'Random basis', icon: UserRound },
  { label: 'Measurement', detail: 'Projective sample', icon: ScanLine },
]

const futureSteps = [
  { feature: 'sifting', label: 'Sifting', icon: Binary },
  { feature: 'qber', label: 'QBER', icon: ShieldCheck },
  { feature: 'parameter_estimation', label: 'Parameter estimation', icon: SlidersHorizontal },
  { feature: 'reconciliation', label: 'Error correction', icon: Check },
  { feature: 'privacy_amplification', label: 'Privacy amplification', icon: KeyRound },
]

export function QuantumFlow({ features, status, channelNames }: QuantumFlowProps) {
  const active = status === 'running' || status === 'completed'

  return (
    <Panel className={`quantum-flow p-5 lg:p-6 ${active ? 'quantum-flow--active' : ''}`}>
      <SectionHeading
        eyebrow="02 · Simulate"
        title="Protocol signal path"
        description="The illuminated path mirrors the currently implemented engine execution."
      />

      <div className="signal-path mt-7">
        <div className="signal-path__line" />
        {active && <div className="signal-path__pulse" />}
        {mainSteps.map((step, index) => {
          const Icon = step.icon
          return (
            <div key={step.label} className="signal-step">
              <div className="signal-step__node">
                <Icon size={17} strokeWidth={1.6} aria-hidden="true" />
              </div>
              <div className="mt-2 text-[10px] font-semibold uppercase tracking-[0.1em] text-slate-300">
                {step.label}
              </div>
              <div className="mt-1 text-center text-[9px] leading-4 text-slate-600">
                {index === 2 && channelNames.length > 0 ? channelNames.join(' → ') : step.detail}
              </div>
            </div>
          )
        })}
      </div>

      <div className="mt-8 border-t border-white/6 pt-5">
        <div className="mb-3 flex items-center justify-between">
          <span className="text-[9px] font-semibold uppercase tracking-[0.18em] text-slate-600">
            Classical post-processing path
          </span>
          <span className="text-[9px] text-slate-700">Capability controlled</span>
        </div>
        <div className="grid grid-cols-2 gap-2 md:grid-cols-5">
          {futureSteps.map((step) => {
            const feature = features.find((candidate) => candidate.id === step.feature)
            const implemented = feature?.implemented ?? false
            const Icon = step.icon
            return (
              <div key={step.feature} className={`phase-step ${implemented ? 'phase-step--available' : ''}`}>
                <Icon size={13} aria-hidden="true" />
                <span>{step.label}</span>
                <span className="mt-auto pt-2 text-[8px] font-semibold uppercase tracking-[0.12em]">
                  {implemented ? 'Implemented' : 'Not implemented'}
                </span>
              </div>
            )
          })}
        </div>
        <div className="mt-2 rounded-lg border border-dashed border-white/6 px-3 py-2 text-center text-[10px] text-slate-600">
          Final secret-key generation is unavailable until reconciliation and privacy amplification exist.
        </div>
      </div>
    </Panel>
  )
}
