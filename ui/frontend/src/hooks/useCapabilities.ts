import { useEffect, useState } from 'react'

import { getCapabilities, getHealth } from '../api/client'
import type { CapabilitiesResponse, HealthResponse } from '../types/api'

export type BackendStatus = 'checking' | 'online' | 'offline'

export function useCapabilities() {
  const [capabilities, setCapabilities] = useState<CapabilitiesResponse | null>(null)
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [status, setStatus] = useState<BackendStatus>('checking')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    Promise.all([getCapabilities(), getHealth()])
      .then(([capabilityData, healthData]) => {
        if (controller.signal.aborted) return
        setCapabilities(capabilityData)
        setHealth(healthData)
        setStatus('online')
      })
      .catch((reason: unknown) => {
        if (controller.signal.aborted) return
        setError(reason instanceof Error ? reason.message : 'Backend unavailable')
        setStatus('offline')
      })

    return () => controller.abort()
  }, [])

  return { capabilities, health, status, error }
}
