import type { ChannelCapability } from '../../types/api'

interface GuidedChannelControlsProps {
  channels: ChannelCapability[]
  selectedNoise: string
  noiseStrength: number
  eveFraction: number
  onNoiseChange: (value: string) => void
  onNoiseStrengthChange: (value: number) => void
  onEveFractionChange: (value: number) => void
}

export function GuidedChannelControls({
  channels,
  selectedNoise,
  noiseStrength,
  eveFraction,
  onNoiseChange,
  onNoiseStrengthChange,
  onEveFractionChange,
}: GuidedChannelControlsProps) {
  const choices = channels.filter(
    (channel) => channel.implemented && channel.id !== 'pauli',
  )
  const selected = choices.find((channel) => channel.id === selectedNoise)
  const parameter = selected?.parameters[0]

  return (
    <div className="control-section">
      <div className="control-section__title">
        <span className="step-index">02</span>
        <span>
          <strong>Channel and adversary</strong>
          <small>Guided mode keeps one noise model and one optional Eve stage</small>
        </span>
      </div>
      <div className="field-grid field-grid--two">
        <label className="field">
          <span>Channel model</span>
          <select value={selectedNoise} onChange={(event) => onNoiseChange(event.target.value)}>
            <option value="identity">Ideal / identity</option>
            {choices
              .filter((channel) => channel.id !== 'identity')
              .map((channel) => (
                <option key={channel.id} value={channel.id}>{channel.name}</option>
              ))}
          </select>
          <small>{selected?.description ?? 'No state transformation is applied.'}</small>
        </label>
        <label className="field">
          <span>{parameter?.label ?? 'Noise strength'}</span>
          <input
            type="number"
            min={parameter?.minimum ?? 0}
            max={parameter?.maximum ?? 1}
            step={parameter?.step ?? 0.01}
            value={noiseStrength}
            onChange={(event) => onNoiseStrengthChange(Number(event.target.value))}
            disabled={selectedNoise === 'identity'}
          />
          <small>{selectedNoise === 'identity' ? 'Disabled for the ideal path' : parameter?.description}</small>
        </label>
        <label className="field field--wide">
          <span>Eve interception fraction</span>
          <div className="range-field">
            <input
              type="range"
              min={0}
              max={1}
              step={0.01}
              value={eveFraction}
              onChange={(event) => onEveFractionChange(Number(event.target.value))}
            />
            <output>{(eveFraction * 100).toFixed(0)}%</output>
          </div>
          <small>Zero removes Eve from the real ordered pipeline; non-zero executes intercept-resend.</small>
        </label>
      </div>
    </div>
  )
}
