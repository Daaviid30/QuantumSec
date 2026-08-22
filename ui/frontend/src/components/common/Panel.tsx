import type { ReactNode } from 'react'

interface PanelProps {
  children: ReactNode
  className?: string
  id?: string
}

export function Panel({ children, className = '', id }: PanelProps) {
  return (
    <section id={id} className={`lab-panel ${className}`}>
      {children}
    </section>
  )
}

interface SectionHeadingProps {
  eyebrow?: string
  title: string
  description?: string
  action?: ReactNode
}

export function SectionHeading({ eyebrow, title, description, action }: SectionHeadingProps) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div>
        {eyebrow && <div className="section-eyebrow">{eyebrow}</div>}
        <h2 className="mt-1 text-lg font-semibold tracking-[-0.02em] text-white">{title}</h2>
        {description && <p className="mt-1.5 max-w-2xl text-sm leading-6 text-slate-400">{description}</p>}
      </div>
      {action}
    </div>
  )
}
