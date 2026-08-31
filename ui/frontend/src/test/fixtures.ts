import type { BB84SimulationResponse, CapabilitiesResponse } from '../types/api'

export const capabilitiesFixture: CapabilitiesResponse = {
  version: '0.1.0',
  protocols: [
    { id: 'bb84', name: 'BB84', implemented: true, description: 'Available' },
    { id: 'e91', name: 'E91', implemented: false, description: 'Planned' },
  ],
  channels: [
    {
      id: 'depolarizing',
      name: 'Depolarizing',
      implemented: true,
      description: 'Noise',
      parameters: [
        {
          key: 'p',
          label: 'Noise probability',
          symbol: 'p',
          minimum: 0,
          maximum: 1,
          step: 0.01,
          default: 0.03,
          description: 'Strength',
        },
      ],
    },
  ],
  features: [],
  limits: { max_signals: 100_000, max_channels: 12, inspector_records: 64 },
}

export const resultFixture: BB84SimulationResponse = {
  metadata: {
    request_id: 'e62dd185-107b-4e9f-9f09-a2f28e02babc',
    protocol: 'bb84',
    seed: 2026,
    duration_ms: 18.42,
    inspector_limit: 64,
    inspector_truncated: false,
  },
  channels: [],
  metrics: { n_raw: 64, n_sifted: 32, sifting_efficiency: 0.5, qber: 0 },
  postprocessing: {
    status: 'completed',
    abort_reason: null,
    n_disclosed: 7,
    estimated_qber: 0,
    n_candidate: 25,
    leak_ec: 4,
    corrected_errors: 0,
    verification_passed: true,
    verification_leakage: 8,
    n_reconciled: 25,
    n_final: 13,
    compression_ratio: 0.52,
    final_secret_fraction: 0.203125,
    final_key: '1011010010110',
  },
  alice_basis_counts: { Z: 2, X: 2 },
  bob_basis_counts: { Z: 2, X: 2 },
  bob_outcome_counts: { zero: 3, one: 1 },
  transmissions: [
    {
      index: 0,
      alice_bit: 0,
      alice_basis: 'Z',
      bob_basis: 'Z',
      bob_result: 0,
      basis_match: true,
      sifted_error: false,
    },
  ],
}
