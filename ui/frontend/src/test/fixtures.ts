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
  metrics: { n_raw: 4, n_sifted: 2, sifting_efficiency: 0.5, qber: 0 },
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
