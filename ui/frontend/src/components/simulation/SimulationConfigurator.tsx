import { Braces, Dices, Fingerprint, Info } from 'lucide-react'

import type { ProtocolCapability } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'
import { StatusPill } from '../common/StatusPill'
import { ProtocolSelector } from './ProtocolSelector'

interface SimulationConfiguratorProps {
  protocols: ProtocolCapability[]
  protocol: string
  nSignals: number
  seed: number
  maxSignals: number
  onProtocolChange: (protocol: string) => void
  onSignalsChange: (value: number) => void
  onSeedChange: (value: number) => void
}

export function SimulationConfigurator({
  protocols,
  protocol,
  nSignals,
  seed,
  maxSignals,
  onProtocolChange,
  onSignalsChange,
  onSeedChange,
}: SimulationConfiguratorProps) {
  return (
    <Panel className="p-5 lg:p-6">
      <SectionHeading
        eyebrow="01 · Configure"
        title="Simulation parameters"
        description="Define the real engine inputs for this reproducible run."
        action={<StatusPill tone="cyan">BB84</StatusPill>}
      />

      <div className="mt-6 space-y-6">
        <ProtocolSelector protocols={protocols} selected={protocol} onSelect={onProtocolChange} />

        <div>
          <div className="flex items-center justify-between">
            <label className="field-label" htmlFor="n-signals">
              Quantum signals
            </label>
            <span className="font-mono text-[10px] text-slate-600">MAX {maxSignals.toLocaleString()}</span>
          </div>
          <div className="relative mt-2">
            <Braces className="field-icon" size={15} aria-hidden="true" />
            <input
              id="n-signals"
              className="lab-input pl-10 font-mono"
              type="number"
              min={1}
              max={maxSignals}
              step={1}
              value={nSignals}
              onChange={(event) => onSignalsChange(Number(event.target.value))}
            />
          </div>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {[128, 512, 2048].map((preset) => (
              <button
                key={preset}
                type="button"
                onClick={() => onSignalsChange(preset)}
                className={`preset-button ${nSignals === preset ? 'preset-button--active' : ''}`}
              >
                {preset.toLocaleString()}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between">
            <label className="field-label" htmlFor="simulation-seed">
              Experiment seed
            </label>
            <span className="flex items-center gap-1 text-[9px] font-semibold uppercase tracking-[0.12em] text-emerald-400/70">
              <Fingerprint size={11} aria-hidden="true" /> Reproducible
            </span>
          </div>
          <div className="relative mt-2">
            <Dices className="field-icon" size={15} aria-hidden="true" />
            <input
              id="simulation-seed"
              className="lab-input pl-10 font-mono"
              type="number"
              min={0}
              max={4_294_967_295}
              step={1}
              value={seed}
              onChange={(event) => onSeedChange(Number(event.target.value))}
            />
          </div>
          <p className="mt-2 flex gap-2 text-[11px] leading-5 text-slate-500">
            <Info className="mt-0.5 shrink-0" size={12} aria-hidden="true" />
            The seed is passed to QuantumSec’s injected SeededRNG. Identical configurations reproduce the
            same quantum run.
          </p>
        </div>
      </div>
    </Panel>
  )
}
