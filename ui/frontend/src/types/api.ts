export interface HealthResponse {
  status: 'ok'
  service: string
  version: string
}

export interface ParameterCapability {
  key: string
  label: string
  symbol: string
  minimum: number
  maximum: number
  step: number
  default: number
  description: string
}

export interface ProtocolCapability {
  id: string
  name: string
  implemented: boolean
  description: string
}

export interface ChannelCapability {
  id: string
  name: string
  implemented: boolean
  description: string
  parameters: ParameterCapability[]
}

export interface FeatureCapability {
  id: string
  name: string
  implemented: boolean
  description: string
}

export interface CapabilitiesResponse {
  version: string
  protocols: ProtocolCapability[]
  channels: ChannelCapability[]
  features: FeatureCapability[]
  limits: Record<string, number>
}

export interface ChannelDraft {
  id: number
  type: string
  parameters: Record<string, number>
}

export type ChannelConfiguration = {
  type: string
  [parameter: string]: string | number
}

export interface BB84SimulationRequest {
  protocol: 'bb84'
  n_signals: number
  seed: number
  channels: ChannelConfiguration[]
}

export interface ChannelSummary {
  type: string
  name: string
  parameters: Record<string, number>
}

export interface SimulationMetadata {
  request_id: string
  protocol: 'bb84'
  seed: number
  duration_ms: number
  inspector_limit: number
  inspector_truncated: boolean
}

export interface SimulationMetrics {
  n_raw: number
  n_sifted: number
  sifting_efficiency: number
  qber: number | null
}

export interface PostprocessingSummary {
  status: 'completed' | 'aborted'
  abort_reason: string | null
  n_disclosed: number
  estimated_qber: number | null
  n_candidate: number
  leak_ec: number
  corrected_errors: number
  verification_passed: boolean | null
  verification_leakage: number
  n_reconciled: number
  n_final: number
  compression_ratio: number | null
  final_secret_fraction: number
  final_key: string | null
}

export interface BasisCounts {
  Z: number
  X: number
}

export interface OutcomeCounts {
  zero: number
  one: number
}

export interface TransmissionRecord {
  index: number
  alice_bit: number
  alice_basis: 'Z' | 'X'
  bob_basis: 'Z' | 'X'
  bob_result: number
  basis_match: boolean
  sifted_error: boolean | null
}

export interface BB84SimulationResponse {
  metadata: SimulationMetadata
  channels: ChannelSummary[]
  metrics: SimulationMetrics
  postprocessing: PostprocessingSummary
  alice_basis_counts: BasisCounts
  bob_basis_counts: BasisCounts
  bob_outcome_counts: OutcomeCounts
  transmissions: TransmissionRecord[]
}

export type SimulationStatus = 'idle' | 'validating' | 'running' | 'completed' | 'failed'
