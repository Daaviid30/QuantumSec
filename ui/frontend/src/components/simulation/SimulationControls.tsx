import { AlertTriangle, LoaderCircle, Play, RotateCcw, Terminal } from 'lucide-react'

import type { SimulationStatus } from '../../types/api'

interface SimulationControlsProps {
  status: SimulationStatus
  validationError: string | null
  error: string | null
  technicalDetails: string | null
  disabled: boolean
  onRun: () => void
}

const labels: Record<SimulationStatus, string> = {
  idle: 'Run simulation',
  validating: 'Validating configuration',
  running: 'Simulating BB84',
  completed: 'Run again with same seed',
  failed: 'Retry simulation',
}

export function SimulationControls({
  status,
  validationError,
  error,
  technicalDetails,
  disabled,
  onRun,
}: SimulationControlsProps) {
  const busy = status === 'validating' || status === 'running'

  return (
    <div className="run-console">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <div className={`run-console__state run-console__state--${status}`}>
          {busy ? (
            <LoaderCircle className="animate-spin" size={16} aria-hidden="true" />
          ) : status === 'failed' ? (
            <AlertTriangle size={16} aria-hidden="true" />
          ) : (
            <Terminal size={16} aria-hidden="true" />
          )}
        </div>
        <div className="min-w-0">
          <div className="text-xs font-semibold text-slate-200">
            {validationError ?? error ?? (busy ? 'Engine execution in progress' : 'Configuration ready')}
          </div>
          <div className="mt-1 truncate text-[10px] text-slate-600">
            {technicalDetails || 'POST /api/simulations/bb84 · deterministic seeded execution'}
          </div>
        </div>
      </div>

      <button
        type="button"
        className="run-button"
        onClick={onRun}
        disabled={disabled || busy || Boolean(validationError)}
      >
        {status === 'completed' || status === 'failed' ? (
          <RotateCcw size={16} aria-hidden="true" />
        ) : (
          <Play size={16} fill="currentColor" aria-hidden="true" />
        )}
        <span>{labels[status]}</span>
      </button>
    </div>
  )
}
