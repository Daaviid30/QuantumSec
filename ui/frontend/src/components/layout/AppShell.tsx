import type { ReactNode } from 'react'

import type { BackendStatus } from '../../hooks/useCapabilities'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

interface AppShellProps {
  children: ReactNode
  backendStatus: BackendStatus
  version?: string
}

export function AppShell({ children, backendStatus, version }: AppShellProps) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-shell__main">
        <Header status={backendStatus} version={version} />
        <main className="app-content">{children}</main>
      </div>
    </div>
  )
}
