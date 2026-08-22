import { ArrowDown, ArrowUp, GripVertical, Trash2 } from 'lucide-react'

import type { ChannelCapability, ChannelDraft } from '../../types/api'

interface ChannelCardProps {
  draft: ChannelDraft
  capability: ChannelCapability
  index: number
  total: number
  onParameterChange: (key: string, value: number) => void
  onMove: (direction: -1 | 1) => void
  onRemove: () => void
}

export function ChannelCard({
  draft,
  capability,
  index,
  total,
  onParameterChange,
  onMove,
  onRemove,
}: ChannelCardProps) {
  return (
    <article className="channel-card">
      <div className="channel-card__index">{String(index + 1).padStart(2, '0')}</div>
      <div className="min-w-0 flex-1">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <GripVertical size={14} className="text-slate-700" aria-hidden="true" />
              <h3 className="text-sm font-semibold text-slate-100">{capability.name}</h3>
            </div>
            <p className="mt-1 pl-[22px] text-[10px] leading-4 text-slate-500">{capability.description}</p>
          </div>
          <div className="flex items-center gap-1">
            <button
              type="button"
              className="mini-icon-button"
              disabled={index === 0}
              onClick={() => onMove(-1)}
              aria-label={`Move ${capability.name} up`}
            >
              <ArrowUp size={13} />
            </button>
            <button
              type="button"
              className="mini-icon-button"
              disabled={index === total - 1}
              onClick={() => onMove(1)}
              aria-label={`Move ${capability.name} down`}
            >
              <ArrowDown size={13} />
            </button>
            <button
              type="button"
              className="mini-icon-button mini-icon-button--danger"
              onClick={onRemove}
              aria-label={`Remove ${capability.name}`}
            >
              <Trash2 size={13} />
            </button>
          </div>
        </div>

        {capability.parameters.length > 0 && (
          <div className={`mt-3 grid gap-2 ${capability.parameters.length > 1 ? 'sm:grid-cols-3' : ''}`}>
            {capability.parameters.map((parameter) => (
              <label key={parameter.key} className="channel-parameter">
                <span className="flex items-center justify-between gap-2 text-[10px] text-slate-500">
                  <span>{parameter.label}</span>
                  <span className="font-mono text-cyan-300/80">{parameter.symbol}</span>
                </span>
                <input
                  aria-label={`${capability.name} ${parameter.label}`}
                  type="number"
                  min={parameter.minimum}
                  max={parameter.maximum}
                  step={parameter.step}
                  value={draft.parameters[parameter.key]}
                  onChange={(event) => onParameterChange(parameter.key, Number(event.target.value))}
                />
              </label>
            ))}
          </div>
        )}
      </div>
    </article>
  )
}
