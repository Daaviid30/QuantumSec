import type { ReactNode } from 'react'

import type { AppView } from '../../app/routes'
import type { BackendStatus } from '../../hooks/useCapabilities'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

interface AppShellProps {
  children: ReactNode
  activeView: AppView
  backendStatus: BackendStatus
  version?: string
  onNavigate: (view: AppView) => void
}

export function AppShell({
  children,
  activeView,
  backendStatus,
  version,
  onNavigate,
}: AppShellProps) {
  return (
    <div className="app-shell">
      <Sidebar activeView={activeView} onNavigate={onNavigate} />
      <div className="app-shell__main">
        <Header view={activeView} status={backendStatus} version={version} />
        <main className="app-content">{children}</main>
      </div>
    </div>
  )
}
