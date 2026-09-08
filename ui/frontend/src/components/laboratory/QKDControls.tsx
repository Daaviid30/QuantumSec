import { Dices, RadioTower } from 'lucide-react'

import type { QKDPostprocessingRequest } from '../../types/api'

export type LaboratoryMode = 'guided' | 'research'

interface QKDControlsProps {
  mode: LaboratoryMode
  nSignals: number
  seed: number
  maxSignals: number
  postprocessing: QKDPostprocessingRequest
  onSignalsChange: (value: number) => void
  onSeedChange: (value: number) => void
  onPostprocessingChange: (value: QKDPostprocessingRequest) => void
}

export function QKDControls({
  mode,
  nSignals,
  seed,
  maxSignals,
  postprocessing,
  onSignalsChange,
  onSeedChange,
  onPostprocessingChange,
}: QKDControlsProps) {
  const setPost = (key: keyof QKDPostprocessingRequest, value: number) => {
    onPostprocessingChange({ ...postprocessing, [key]: value })
  }

  return (
    <div className="control-section">
      <div className="control-section__title">
        <RadioTower size={15} aria-hidden="true" />
        <span>
          <strong>BB84 execution</strong>
          <small>Seeded numerical logical-qubit simulation</small>
        </span>
      </div>
      <div className="field-grid field-grid--two">
        <label className="field">
          <span>Quantum signals</span>
          <input
            type="number"
            min={1}
            max={maxSignals}
            step={1}
            value={nSignals}
            onChange={(event) => onSignalsChange(Number(event.target.value))}
          />
          <small>1–{maxSignals.toLocaleString()} prepared signals</small>
        </label>
        <label className="field">
          <span className="field__with-icon"><Dices size={13} aria-hidden="true" /> Seed</span>
          <input
            type="number"
            min={0}
            max={4_294_967_295}
            step={1}
            value={seed}
            onChange={(event) => onSeedChange(Number(event.target.value))}
          />
          <small>Exact reruns preserve this injected RNG seed</small>
        </label>
      </div>

      {mode === 'research' ? (
        <div className="advanced-grid">
          <label className="field">
            <span>Per-basis sample fraction</span>
            <input
              type="number"
              min={0.01}
              max={0.99}
              step={0.01}
              value={postprocessing.sample_fraction}
              onChange={(event) => setPost('sample_fraction', Number(event.target.value))}
            />
          </label>
          <label className="field">
            <span>Phase-error abort threshold</span>
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={postprocessing.phase_error_abort_threshold}
              onChange={(event) => setPost('phase_error_abort_threshold', Number(event.target.value))}
            />
          </label>
          <label className="field">
            <span>Cascade passes</span>
            <input
              type="number"
              min={1}
              max={16}
              step={1}
              value={postprocessing.cascade_passes}
              onChange={(event) => setPost('cascade_passes', Number(event.target.value))}
            />
          </label>
          <label className="field">
            <span>Security margin (bits)</span>
            <input
              type="number"
              min={0}
              max={100000}
              step={1}
              value={postprocessing.security_margin_bits}
              onChange={(event) => setPost('security_margin_bits', Number(event.target.value))}
            />
          </label>
        </div>
      ) : null}
    </div>
  )
}
