import type {
  BB84SimulationRequest,
  BB84SimulationResponse,
  CapabilitiesResponse,
  HealthResponse,
} from '../types/api'

export class QuantumSecApiError extends Error {
  readonly status: number
  readonly details?: string

  constructor(message: string, status: number, details?: string) {
    super(message)
    this.name = 'QuantumSecApiError'
    this.status = status
    this.details = details
  }
}

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(url, init)
  } catch {
    throw new QuantumSecApiError('The QuantumSec backend is unavailable.', 0)
  }

  const body = (await response.json().catch(() => null)) as
    | { detail?: string | { message?: string; details?: string } }
    | T
    | null

  if (!response.ok) {
    const detail = body && typeof body === 'object' && 'detail' in body ? body.detail : undefined
    if (detail && typeof detail === 'object') {
      throw new QuantumSecApiError(
        detail.message ?? 'The request could not be completed.',
        response.status,
        detail.details,
      )
    }
    throw new QuantumSecApiError(
      typeof detail === 'string' ? detail : 'The request could not be completed.',
      response.status,
    )
  }

  return body as T
}

export function getHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>('/api/health')
}

export function getCapabilities(): Promise<CapabilitiesResponse> {
  return requestJson<CapabilitiesResponse>('/api/capabilities')
}

export function runBB84Simulation(request: BB84SimulationRequest): Promise<BB84SimulationResponse> {
  return requestJson<BB84SimulationResponse>('/api/simulations/bb84', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })
}
