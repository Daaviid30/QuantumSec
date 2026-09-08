import { useCallback, useState } from 'react'

import { runSession } from '../api/client'
import type { RequestStatus, SessionRunRequest, SessionRunResponse } from '../types/api'

export function useSessionRun() {
  const [status, setStatus] = useState<RequestStatus>('idle')
  const [result, setResult] = useState<SessionRunResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [technicalDetails, setTechnicalDetails] = useState<string | null>(null)

  const run = useCallback(async (request: SessionRunRequest) => {
    setStatus('running')
    setError(null)
    setTechnicalDetails(null)
    try {
      const response = await runSession(request)
      setResult(response)
      setStatus('completed')
      return response
    } catch (reason: unknown) {
      setStatus('failed')
      setError(reason instanceof Error ? reason.message : 'Session execution failed.')
      setTechnicalDetails(
        reason && typeof reason === 'object' && 'details' in reason
          ? String(reason.details ?? '')
          : null,
      )
      return null
    }
  }, [])

  return { status, result, error, technicalDetails, run }
}
