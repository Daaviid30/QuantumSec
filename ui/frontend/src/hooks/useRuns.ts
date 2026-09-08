import { useEffect, useState } from 'react'

import { getRuns } from '../api/client'
import type { SessionRunResponse } from '../types/api'

export function useRuns(refreshKey = 0) {
  const [runs, setRuns] = useState<SessionRunResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    setLoading(true)
    getRuns()
      .then((response) => {
        if (!active) return
        setRuns(response.runs)
        setError(null)
      })
      .catch((reason: unknown) => {
        if (!active) return
        setError(reason instanceof Error ? reason.message : 'Run records could not be loaded.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [refreshKey])

  return { runs, loading, error }
}
