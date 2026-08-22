import { useCallback, useState } from 'react'

import { runBB84Simulation } from '../api/client'
import type {
  BB84SimulationRequest,
  BB84SimulationResponse,
  SimulationStatus,
} from '../types/api'

export function useSimulation() {
  const [status, setStatus] = useState<SimulationStatus>('idle')
  const [result, setResult] = useState<BB84SimulationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [technicalDetails, setTechnicalDetails] = useState<string | null>(null)

  const run = useCallback(async (request: BB84SimulationRequest) => {
    setStatus('validating')
    setError(null)
    setTechnicalDetails(null)

    await Promise.resolve()
    setStatus('running')

    try {
      const response = await runBB84Simulation(request)
      setResult(response)
      setStatus('completed')
    } catch (reason: unknown) {
      setStatus('failed')
      setError(reason instanceof Error ? reason.message : 'Simulation failed.')
      setTechnicalDetails(
        reason && typeof reason === 'object' && 'details' in reason
          ? String(reason.details ?? '')
          : null,
      )
    }
  }, [])

  return { status, result, error, technicalDetails, run }
}
