export interface HealthResponse {
  status: 'ok'
  service: string
  version: string
}

export type PublicSessionProfile =
  | 'QKD-ASSUMED'
  | 'QKD-CLASSICAL-AUTH'
  | 'QKD-PQC-AUTH'
  | 'PQC-BASE'
  | 'PQC-DIVERSE'
  | 'HYBRID'
  | 'HYBRID-DIVERSE'

export type ProfileFamily = 'qkd' | 'pqc' | 'hybrid'

export interface ProfileCapability {
  id: PublicSessionProfile
  name: string
  family: ProfileFamily
  implemented: boolean
  status: 'current' | 'partial' | 'planned' | 'future'
  description: string
  establishment: string[]
  authentication: string[]
  algorithms: string[]
  hybrid: boolean
  diversified: boolean
  supports_qkd: boolean
  supports_data_plane: boolean
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

export type AdversaryCapability = ChannelCapability

export interface FeatureCapability {
  id: string
  name: string
  implemented: boolean
  description: string
}

export interface CapabilitiesResponse {
  version: string
  profiles: ProfileCapability[]
  protocols: ProtocolCapability[]
  channels: ChannelCapability[]
  adversaries: AdversaryCapability[]
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

export interface QKDPostprocessingRequest {
  sample_fraction: number
  phase_error_abort_threshold: number
  cascade_passes: number
  cascade_initial_block_factor: number
  verification_tag_length: number
  security_margin_bits: number
}

export interface SessionRunRequest {
  profile: PublicSessionProfile
  qkd_authentication_profile?: Extract<PublicSessionProfile, `QKD-${string}`> | null
  n_signals?: number | null
  seed?: number | null
  channels?: ChannelConfiguration[]
  postprocessing?: QKDPostprocessingRequest
}

export interface AttackDiagnosticsSummary {
  stage_index: number
  attack_type: 'intercept_resend'
  intercept_fraction: number
  n_signals_seen: number
  n_intercepted: number
  eve_z_measurements: number
  eve_x_measurements: number
  eve_zero_outcomes: number
  eve_one_outcomes: number
}

export interface AuthenticationOutcome {
  purpose: string
  mechanism: string
  algorithm: string
  executed: boolean
  verified: boolean | null
  trust_assumption: string
}

export interface SecretProvenance {
  position: number
  source: string
  protocol: string
  algorithm: string
  encoding: string
  bit_length: number
  byte_length: number
}

export interface SessionTraceEvent {
  sequence: number
  source: 'session' | 'qkd' | 'pqc' | 'hybrid'
  stage: string
  state: string
  detail: string
}

export interface QKDSessionMetrics {
  simulation_time_ns: number
  n_raw: number
  n_sifted: number
  n_disclosed: number
  n_candidate: number
  n_reconciled: number
  n_final: number
  sifting_efficiency: number
  final_secret_fraction: number
  estimated_qber_z: number | null
  estimated_qber_x: number | null
  estimated_qber_aggregated: number | null
  phase_error_bound: number | null
  diagnostic_full_sifted_qber: number | null
  diagnostic_qber_z: number | null
  diagnostic_qber_x: number | null
  diagnostic_qber_aggregated: number | null
  transcript_bytes: number
  [key: string]: unknown
}

export interface PQCSessionMetrics {
  internal_profile: string
  algorithms: string[]
  crypto_software_time_ns: number
  /**
   * Per-phase software timings. Declared explicitly (rather than reaching them through the index
   * signature and casting with Number()) so that absent values cannot be coerced to a misleading 0.
   * `orchestration.metrics` types these as non-optional ints; the hybrid runner reports 0 for the
   * phases the hybrid layer owns instead of the PQC sibling.
   */
  server_offer_time_ns: number
  client_exchange_time_ns: number
  key_schedule_time_ns: number
  confirmation_time_ns: number
  kem_public_key_bytes: number
  kem_ciphertext_bytes: number
  canonical_protocol_bytes: number
  transcript_bytes: number
  signature_bytes: number
  finished_bytes: number
  serialized_transport_bytes: number | null
  [key: string]: unknown
}

export interface HybridSessionMetrics {
  component_count: number
  qkd_contribution_bits: number
  ml_kem_contribution_bytes: number
  hqc_contribution_bytes: number | null
  canonical_combiner_input_bytes: number
  encoding_overhead_bytes: number
  derived_session_key_bits: number
  [key: string]: unknown
}

export interface QKDAuthenticationMetrics {
  mechanism: string
  algorithm: string
  family: string
  authenticated_bytes: number
  evidence_bytes: number
  checkpoints: number
  total_time_ns: number
  trust_assumption: string
  secret_bits_consumed: number | null
  [key: string]: unknown
}

export interface SessionMetrics {
  qkd: QKDSessionMetrics | null
  pqc: PQCSessionMetrics | null
  qkd_authentication: QKDAuthenticationMetrics | null
  pqc_authentication: Record<string, unknown> | null
  hybrid: HybridSessionMetrics | null
  orchestration_software_wall_time_ns: number
}

export interface PublicSessionResult {
  version: number
  session_id: string
  profile: PublicSessionProfile
  status: 'established' | 'aborted' | 'failed'
  abort_reason: string | null
  established_key: { type: 'qkd_bitstring' | 'session_key' | null; bit_length: number }
  provenance: SecretProvenance[]
  authentication: {
    qkd_classical: AuthenticationOutcome | null
    pqc_exchange: AuthenticationOutcome | null
  }
  public_context: Record<string, string | number>
}

export interface ExperimentSessionConfiguration {
  version: number
  profile: PublicSessionProfile
  qkd_authentication_profile: Extract<PublicSessionProfile, `QKD-${string}`> | null
  qkd_signal_count: number | null
  qkd_postprocessing: QKDPostprocessingRequest | null
  internal_pqc_profile: string | null
}

export interface ExperimentConfiguration {
  version: number
  experiment_kind: string
  condition_id: string
  replicate_index: number
  seed: number | null
  session: ExperimentSessionConfiguration
  qkd_stages: ChannelConfiguration[]
  tags: string[]
}

export interface RunRecord {
  version: number
  run_id: string
  experiment_kind: string
  condition_id: string
  replicate_index: number
  batch: Record<string, unknown> | null
  execution_order_index: number | null
  timestamp_utc: string
  seed: number | null
  profile: PublicSessionProfile
  environment: Record<string, unknown>
  config: ExperimentConfiguration
  provisioning: Record<string, unknown>
  result: PublicSessionResult
  trace: { version: number; events: SessionTraceEvent[] }
  metrics: SessionMetrics
  artifact: { experiment_record_json_bytes?: number; [key: string]: unknown }
}

export interface SessionRunResponse {
  record: RunRecord
  attack_diagnostics: AttackDiagnosticsSummary[]
  data_plane_available: boolean
}

export interface RunListResponse {
  runs: SessionRunResponse[]
}

export interface ComparisonCompatibility {
  qkd_metrics: boolean
  pqc_timing: boolean
  same_environment: boolean
  notes: string[]
}

export interface CompareResponse {
  left: SessionRunResponse
  right: SessionRunResponse
  compatibility: ComparisonCompatibility
}

export interface ProtectedMessageResponse {
  algorithm: 'AES-256-GCM'
  plaintext_bytes: number
  ciphertext_bytes: number
  nonce_bytes: number
  tag_bytes: number
  application_aad_bytes: number
  round_trip_verified: boolean
  tamper_rejected: boolean
  ciphertext_preview: string
}

export type RequestStatus = 'idle' | 'running' | 'completed' | 'failed'

// Compatibility types for the retained legacy BB84 API.
export interface BB84SimulationRequest {
  protocol: 'bb84'
  n_signals: number
  seed: number
  channels: ChannelConfiguration[]
}

export interface BB84SimulationResponse {
  metadata: {
    request_id: string
    protocol: 'bb84'
    seed: number
    duration_ms: number
    inspector_limit: number
    inspector_truncated: boolean
  }
  channels: Array<{
    stage_kind: 'channel' | 'adversary'
    type: string
    name: string
    parameters: Record<string, number>
  }>
  attack_diagnostics: AttackDiagnosticsSummary[]
  metrics: {
    n_raw: number
    n_sifted: number
    sifting_efficiency: number
    qber: number | null
    qber_z: number | null
    qber_x: number | null
    qber_aggregated: number | null
  }
  postprocessing: {
    status: 'completed' | 'aborted'
    abort_reason: string | null
    n_disclosed: number
    estimated_qber: number | null
    estimated_qber_z: number | null
    estimated_qber_x: number | null
    estimated_qber_aggregated: number | null
    phase_error_bound: number | null
    n_candidate: number
    leak_ec: number
    corrected_errors: number
    verification_passed: boolean | null
    verification_leakage: number
    n_reconciled: number
    n_final: number
    compression_ratio: number | null
    final_secret_fraction: number
  }
  alice_basis_counts: { Z: number; X: number }
  bob_basis_counts: { Z: number; X: number }
  bob_outcome_counts: { zero: number; one: number }
  transmissions: Array<{
    index: number
    alice_bit: number
    alice_basis: 'Z' | 'X'
    bob_basis: 'Z' | 'X'
    bob_result: number
    basis_match: boolean
    sifted_error: boolean | null
  }>
}

export type SimulationStatus = 'idle' | 'validating' | 'running' | 'completed' | 'failed'
