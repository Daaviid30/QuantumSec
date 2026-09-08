import { FlaskConical, Gauge, History, Scale } from 'lucide-react'

import type { AppView } from '../../app/routes'
import { QuantumMark } from './QuantumMark'

interface SidebarProps {
  activeView: AppView
  onNavigate: (view: AppView) => void
}

const navigation = [
  { id: 'overview' as const, label: 'Overview', description: 'System scope', icon: Gauge },
  { id: 'laboratory' as const, label: 'Laboratory', description: 'Build and run', icon: FlaskConical },
  { id: 'runs' as const, label: 'Runs', description: 'Reproducible records', icon: History },
  { id: 'compare' as const, label: 'Compare', description: 'Two-run analysis', icon: Scale },
]

export function Sidebar({ activeView, onNavigate }: SidebarProps) {
  return (
    <aside className="sidebar">
      <button className="brand" type="button" onClick={() => onNavigate('overview')}>
        <QuantumMark />
        <span>
          <strong>QuantumSec</strong>
          <small>Security laboratory</small>
        </span>
      </button>

      <nav className="sidebar__nav" aria-label="Primary navigation">
        <p className="sidebar__label">Workspace</p>
        {navigation.map((item) => {
          const Icon = item.icon
          const active = activeView === item.id
          return (
            <button
              key={item.id}
              type="button"
              className={`nav-item ${active ? 'nav-item--active' : ''}`}
              onClick={() => onNavigate(item.id)}
              aria-current={active ? 'page' : undefined}
            >
              <Icon size={17} strokeWidth={1.8} aria-hidden="true" />
              <span>
                <strong>{item.label}</strong>
                <small>{item.description}</small>
              </span>
            </button>
          )
        })}
      </nav>

      <div className="sidebar__scope">
        <span className="scope-dot" />
        <div>
          <strong>Research boundary</strong>
          <p>Numerical BB84 and real liboqs operations keep separate measurement provenance.</p>
        </div>
      </div>
    </aside>
  )
}
