import { Atom, LockKeyhole } from 'lucide-react'

import type { ProtocolCapability } from '../../types/api'

interface ProtocolSelectorProps {
  protocols: ProtocolCapability[]
  selected: string
  onSelect: (protocol: string) => void
}

export function ProtocolSelector({ protocols, selected, onSelect }: ProtocolSelectorProps) {
  return (
    <div id="protocol-config">
      <label className="field-label">Protocol</label>
      <div className="mt-2 grid grid-cols-2 gap-2">
        {protocols.map((protocol) => (
          <button
            key={protocol.id}
            type="button"
            disabled={!protocol.implemented}
            onClick={() => onSelect(protocol.id)}
            className={`protocol-option ${selected === protocol.id ? 'protocol-option--selected' : ''}`}
            aria-pressed={selected === protocol.id}
          >
            <span className="flex items-center gap-2">
              {protocol.implemented ? (
                <Atom size={14} aria-hidden="true" />
              ) : (
                <LockKeyhole size={12} aria-hidden="true" />
              )}
              <span className="font-mono text-xs font-semibold">{protocol.name}</span>
            </span>
            <span className="text-[9px] uppercase tracking-[0.12em]">
              {protocol.implemented ? 'Available' : 'Coming soon'}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
