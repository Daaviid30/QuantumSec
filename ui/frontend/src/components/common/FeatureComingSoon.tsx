import { LockKeyhole } from 'lucide-react'

interface FeatureComingSoonProps {
  title: string
  compact?: boolean
}

export function FeatureComingSoon({ title, compact = false }: FeatureComingSoonProps) {
  return (
    <div className={compact ? 'coming-soon coming-soon--compact' : 'coming-soon'}>
      <LockKeyhole size={compact ? 12 : 15} aria-hidden="true" />
      <span>{title}</span>
      <span className="ml-auto text-[9px] font-semibold uppercase tracking-[0.17em] text-slate-600">
        Coming soon
      </span>
    </div>
  )
}
