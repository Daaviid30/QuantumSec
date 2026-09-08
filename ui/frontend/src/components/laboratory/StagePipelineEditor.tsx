import { ArrowDown, ArrowUp, Plus, Trash2 } from 'lucide-react'

import type { ChannelCapability, ChannelDraft } from '../../types/api'

interface StagePipelineEditorProps {
  capabilities: ChannelCapability[]
  stages: ChannelDraft[]
  selectedType: string
  maxStages: number
  onSelectedTypeChange: (value: string) => void
  onAdd: () => void
  onRemove: (id: number) => void
  onMove: (id: number, direction: -1 | 1) => void
  onParameterChange: (id: number, key: string, value: number) => void
}

export function StagePipelineEditor({
  capabilities,
  stages,
  selectedType,
  maxStages,
  onSelectedTypeChange,
  onAdd,
  onRemove,
  onMove,
  onParameterChange,
}: StagePipelineEditorProps) {
  return (
    <div className="control-section">
      <div className="control-section__title">
        <span className="step-index">02</span>
        <span>
          <strong>Ordered channel pipeline</strong>
          <small>Research mode applies every physical/adversary stage from top to bottom</small>
        </span>
      </div>

      <ol className="stage-list">
        {stages.length === 0 ? (
          <li className="stage-empty"><strong>Ideal quantum path</strong><span>No channel stage configured.</span></li>
        ) : stages.map((stage, index) => {
          const capability = capabilities.find((candidate) => candidate.id === stage.type)
          if (!capability) return null
          return (
            <li key={stage.id} className={`stage-row ${stage.type === 'intercept_resend' ? 'stage-row--eve' : ''}`}>
              <span className="stage-row__number">{String(index + 1).padStart(2, '0')}</span>
              <div className="stage-row__body">
                <div className="stage-row__heading">
                  <span><strong>{capability.name}</strong><small>{capability.description}</small></span>
                  <span className="row-actions">
                    <button type="button" onClick={() => onMove(stage.id, -1)} disabled={index === 0} aria-label={`Move ${capability.name} up`}><ArrowUp size={14} /></button>
                    <button type="button" onClick={() => onMove(stage.id, 1)} disabled={index === stages.length - 1} aria-label={`Move ${capability.name} down`}><ArrowDown size={14} /></button>
                    <button type="button" onClick={() => onRemove(stage.id)} aria-label={`Remove ${capability.name}`}><Trash2 size={14} /></button>
                  </span>
                </div>
                {capability.parameters.length ? (
                  <div className="stage-parameters">
                    {capability.parameters.map((parameter) => (
                      <label className="field" key={parameter.key}>
                        <span>{parameter.label} <code>{parameter.symbol}</code></span>
                        <input
                          type="number"
                          min={parameter.minimum}
                          max={parameter.maximum}
                          step={parameter.step}
                          value={stage.parameters[parameter.key]}
                          onChange={(event) => onParameterChange(stage.id, parameter.key, Number(event.target.value))}
                        />
                      </label>
                    ))}
                  </div>
                ) : null}
              </div>
            </li>
          )
        })}
      </ol>

      <div className="stage-adder">
        <label className="sr-only" htmlFor="stage-type">Stage type</label>
        <select id="stage-type" value={selectedType} onChange={(event) => onSelectedTypeChange(event.target.value)}>
          {capabilities.filter((item) => item.implemented).map((item) => (
            <option key={item.id} value={item.id}>{item.name}</option>
          ))}
        </select>
        <button type="button" className="button button--secondary" onClick={onAdd} disabled={stages.length >= maxStages}>
          <Plus size={15} aria-hidden="true" /> Add stage
        </button>
      </div>
    </div>
  )
}
