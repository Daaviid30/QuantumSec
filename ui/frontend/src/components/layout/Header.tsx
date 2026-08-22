import { Activity, CircleHelp } from 'lucide-react'

import type { BackendStatus } from '../../hooks/useCapabilities'

interface HeaderProps {
  status: BackendStatus
  version?: string
}

export function Header({ status, version }: HeaderProps) {
  const statusLabel = status === 'online' ? 'Engine online' : status === 'offline' ? 'Offline' : 'Connecting'

  return (
    <header className="app-header">
      <div>
        <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-400/80">
          <Activity size={13} aria-hidden="true" /> Quantum security laboratory
        </div>
        <h1 className="mt-1 text-xl font-semibold tracking-[-0.03em] text-white">QuantumSec</h1>
      </div>

      <div className="flex items-center gap-2.5">
        <a className="header-icon-button" href="/docs" target="_blank" rel="noreferrer" aria-label="API docs">
          <CircleHelp size={16} />
        </a>
        <div className={`backend-status backend-status--${status}`}>
          <span className="backend-status__dot" />
          <span>{statusLabel}</span>
          {version && <span className="text-slate-600">v{version}</span>}
        </div>
      </div>
    </header>
  )
}
