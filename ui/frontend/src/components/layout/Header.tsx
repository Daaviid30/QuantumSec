import { BookOpen } from 'lucide-react'

import { viewTitles, type AppView } from '../../app/routes'
import type { BackendStatus } from '../../hooks/useCapabilities'

interface HeaderProps {
  view: AppView
  status: BackendStatus
  version?: string
}

export function Header({ view, status, version }: HeaderProps) {
  const heading = viewTitles[view]
  const label = status === 'online' ? 'Backend ready' : status === 'offline' ? 'Backend offline' : 'Checking backend'

  return (
    <header className="app-header">
      <div>
        <p className="page-eyebrow">{heading.eyebrow}</p>
        <h1>{heading.title}</h1>
      </div>
      <div className="header-actions">
        <a href="/docs" target="_blank" rel="noreferrer" className="icon-link" aria-label="Open API documentation">
          <BookOpen size={16} aria-hidden="true" />
        </a>
        <div className={`backend-status backend-status--${status}`} role="status">
          <span className="backend-status__dot" />
          <span>{label}</span>
          {version ? <code>v{version}</code> : null}
        </div>
      </div>
    </header>
  )
}
