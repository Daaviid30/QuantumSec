import type {
  PublicSessionProfile,
  QKDPostprocessingRequest,
  RunRecord,
  SessionRunRequest,
} from '../types/api'

export const DEFAULT_POSTPROCESSING: QKDPostprocessingRequest = {
  sample_fraction: 0.2,
  phase_error_abort_threshold: 0.11,
  cascade_passes: 4,
  cascade_initial_block_factor: 0.73,
  verification_tag_length: 32,
  security_margin_bits: 0,
}

export const PROFILE_SHORT_LABELS: Record<PublicSessionProfile, string> = {
  'QKD-ASSUMED': 'Assumed authentication',
  'QKD-CLASSICAL-AUTH': 'Classical / ITS auth',
  'QKD-PQC-AUTH': 'PQC-authenticated QKD',
  'PQC-BASE': 'PQC baseline',
  'PQC-DIVERSE': 'Diversified PQC',
  HYBRID: 'QKD + PQC',
  'HYBRID-DIVERSE': 'Diversified hybrid',
}

export function profileUsesQkd(profile: PublicSessionProfile): boolean {
  return profile.startsWith('QKD-') || profile.startsWith('HYBRID')
}

export function profileIsHybrid(profile: PublicSessionProfile): boolean {
  return profile.startsWith('HYBRID')
}

export function defaultRunRequest(profile: PublicSessionProfile): SessionRunRequest {
  const usesQkd = profileUsesQkd(profile)
  return {
    profile,
    ...(profileIsHybrid(profile) ? { qkd_authentication_profile: 'QKD-PQC-AUTH' as const } : {}),
    ...(usesQkd
      ? {
          n_signals: 2048,
          seed: 2026,
          channels: [],
          postprocessing: { ...DEFAULT_POSTPROCESSING },
        }
      : {}),
  }
}

export function requestFromRecord(record: RunRecord): SessionRunRequest {
  const session = record.config.session
  const usesQkd = profileUsesQkd(record.profile)
  const savedPostprocessing = session.qkd_postprocessing
  return {
    profile: record.profile,
    ...(session.qkd_authentication_profile
      ? { qkd_authentication_profile: session.qkd_authentication_profile }
      : {}),
    ...(usesQkd
      ? {
          n_signals: session.qkd_signal_count,
          seed: record.config.seed,
          channels: record.config.qkd_stages.map((stage) => ({ ...stage })),
          postprocessing: savedPostprocessing
            ? {
                sample_fraction: savedPostprocessing.sample_fraction,
                phase_error_abort_threshold: savedPostprocessing.phase_error_abort_threshold,
                cascade_passes: savedPostprocessing.cascade_passes,
                cascade_initial_block_factor: savedPostprocessing.cascade_initial_block_factor,
                verification_tag_length: savedPostprocessing.verification_tag_length,
                security_margin_bits: savedPostprocessing.security_margin_bits,
              }
            : { ...DEFAULT_POSTPROCESSING },
        }
      : {}),
  }
}

export function formatPercent(value: number | null | undefined, digits = 2): string {
  return value == null ? 'Not available' : `${(value * 100).toFixed(digits)}%`
}

export function formatDurationNs(value: number | null | undefined): string {
  if (value == null) return 'Not available'
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(2)} s`
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(2)} ms`
  if (value >= 1_000) return `${(value / 1_000).toFixed(2)} µs`
  return `${value.toLocaleString()} ns`
}

export function formatBytes(value: number | null | undefined): string {
  if (value == null) return 'Not available'
  if (value >= 1024) return `${(value / 1024).toFixed(1)} KiB`
  return `${value.toLocaleString()} B`
}
