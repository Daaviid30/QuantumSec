import {
  Atom,
  Beaker,
  Boxes,
  ChartNoAxesCombined,
  FlaskConical,
  KeyRound,
  Network,
  RadioTower,
  ShieldCheck,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

import { QuantumMark } from './QuantumMark'

interface NavigationItem {
  label: string
  icon: LucideIcon
  href?: string
  active?: boolean
  disabled?: boolean
}

interface NavigationSection {
  label: string
  items: NavigationItem[]
}

const sections: NavigationSection[] = [
  {
    label: 'Simulation',
    items: [{ label: 'Simulator', icon: FlaskConical, href: '#simulator', active: true }],
  },
  {
    label: 'Research',
    items: [
      { label: 'Experiments', icon: Beaker, disabled: true },
      { label: 'Results', icon: ChartNoAxesCombined, disabled: true },
    ],
  },
  {
    label: 'Quantum',
    items: [
      { label: 'Protocols', icon: Atom, href: '#protocol-config' },
      { label: 'Channels', icon: RadioTower, href: '#channel-pipeline' },
    ],
  },
  {
    label: 'Security',
    items: [
      { label: 'Post-processing', icon: ShieldCheck, disabled: true },
      { label: 'PQC', icon: KeyRound, disabled: true },
    ],
  },
  {
    label: 'Network',
    items: [{ label: 'QKDN', icon: Network, disabled: true }],
  },
]

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="flex items-center gap-3 px-5 pt-6 pb-8">
        <QuantumMark />
        <div>
          <div className="text-[15px] font-bold tracking-[0.18em] text-white">QUANTUMSEC</div>
          <div className="mt-0.5 text-[9px] font-medium uppercase tracking-[0.2em] text-cyan-400/70">
            Research platform
          </div>
        </div>
      </div>

      <nav className="sidebar__nav" aria-label="Primary navigation">
        {sections.map((section) => (
          <div key={section.label} className="mb-5">
            <div className="sidebar__section-label">{section.label}</div>
            <div className="mt-1.5 space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon
                if (item.disabled) {
                  return (
                    <div key={item.label} className="sidebar__item sidebar__item--disabled">
                      <Icon size={15} strokeWidth={1.7} aria-hidden="true" />
                      <span>{item.label}</span>
                      <span className="ml-auto text-[8px] font-semibold uppercase tracking-wider text-slate-700">
                        Soon
                      </span>
                    </div>
                  )
                }
                return (
                  <a
                    key={item.label}
                    href={item.href ?? '#simulator'}
                    className={`sidebar__item ${item.active ? 'sidebar__item--active' : ''}`}
                  >
                    <Icon size={15} strokeWidth={1.7} aria-hidden="true" />
                    <span>{item.label}</span>
                  </a>
                )
              })}
            </div>
          </div>
        ))}
      </nav>

      <div className="mt-auto p-4">
        <div className="rounded-xl border border-white/6 bg-white/[0.025] p-3.5">
          <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-500">
            <Boxes size={13} aria-hidden="true" /> Engine scope
          </div>
          <p className="mt-2 text-[11px] leading-5 text-slate-500">
            Logical-qubit simulation. Optical loss and final key generation are not implemented.
          </p>
        </div>
      </div>
    </aside>
  )
}
