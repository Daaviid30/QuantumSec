import { render, screen, within } from '@testing-library/react'

import type { SessionRunResponse } from '../../types/api'
import { RunWorkspace } from './RunWorkspace'

const run: SessionRunResponse = {
  data_plane_available: false,
  attack_diagnostics: [{ stage_index: 0, attack_type: 'intercept_resend', intercept_fraction: 0.5, n_signals_seen: 512, n_intercepted: 251, eve_z_measurements: 120, eve_x_measurements: 131, eve_zero_outcomes: 126, eve_one_outcomes: 125 }],
  record: {
    version: 1,
    run_id: '11111111-1111-4111-8111-111111111111',
    experiment_kind: 'E4',
    condition_id: 'web-QKD-ASSUMED',
    replicate_index: 0,
    batch: null,
    execution_order_index: null,
    timestamp_utc: '2026-09-08T12:00:00+00:00',
    seed: 2026,
    profile: 'QKD-ASSUMED',
    environment: { python_version: '3.14' },
    config: { version: 1, experiment_kind: 'E4', condition_id: 'web-QKD-ASSUMED', replicate_index: 0, seed: 2026, session: { version: 1, profile: 'QKD-ASSUMED', qkd_authentication_profile: 'QKD-ASSUMED', qkd_signal_count: 512, qkd_postprocessing: { sample_fraction: 0.2, phase_error_abort_threshold: 0.11, cascade_passes: 4, cascade_initial_block_factor: 0.73, verification_tag_length: 32, security_margin_bits: 0 }, internal_pqc_profile: null }, qkd_stages: [{ type: 'intercept_resend', intercept_fraction: 0.5 }], tags: ['web-ui'] },
    provisioning: {},
    result: { version: 1, session_id: '00112233445566778899aabbccddeeff', profile: 'QKD-ASSUMED', status: 'established', abort_reason: null, established_key: { type: 'qkd_bitstring', bit_length: 73 }, provenance: [{ position: 1, source: 'qkd', protocol: 'BB84', algorithm: 'BB84', encoding: 'packed_bits', bit_length: 73, byte_length: 10 }], authentication: { qkd_classical: { purpose: 'QKD classical transcript authentication', mechanism: 'assumed', algorithm: 'external authenticated channel', executed: false, verified: null, trust_assumption: 'Authenticated classical channel is externally assumed.' }, pqc_exchange: null }, public_context: {} },
    trace: { version: 1, events: [{ sequence: 0, source: 'session', stage: 'session', state: 'started', detail: 'QKD-ASSUMED' }, { sequence: 1, source: 'qkd', stage: 'classical_authentication', state: 'assumed', detail: 'Authentication is externally assumed.' }, { sequence: 2, source: 'session', stage: 'session', state: 'established', detail: 'Session material accepted.' }] },
    metrics: { qkd: { simulation_time_ns: 5000000, n_raw: 512, n_sifted: 254, n_disclosed: 52, n_candidate: 202, n_reconciled: 202, n_final: 73, sifting_efficiency: 0.496, final_secret_fraction: 0.143, estimated_qber_z: 0.1, estimated_qber_x: 0.09, estimated_qber_aggregated: 0.095, phase_error_bound: 0.1, diagnostic_full_sifted_qber: 0.1, diagnostic_qber_z: 0.1, diagnostic_qber_x: 0.09, diagnostic_qber_aggregated: 0.095, transcript_bytes: 3000 }, pqc: null, qkd_authentication: null, pqc_authentication: null, hybrid: null, orchestration_software_wall_time_ns: 6000000 },
    artifact: { experiment_record_json_bytes: 8000 },
  },
}

test('renders real Eve evidence, per-basis QBER, trace, and explicit assumed authentication', () => {
  render(<RunWorkspace run={run} />)

  expect(screen.getByText('ASSUMED — NOT EXECUTED')).toBeInTheDocument()
  expect(screen.getByText(/251/)).toBeInTheDocument()
  expect(screen.getByText('Estimated e_Z')).toBeInTheDocument()
  expect(screen.getAllByText('10.00%').length).toBeGreaterThan(0)
  expect(screen.getAllByText(/Authentication is externally assumed/i).length).toBeGreaterThan(0)
  expect(screen.getByRole('cell', { name: 'QKD' })).toBeInTheDocument()
  expect(screen.queryByText(/[01]{40,}/)).not.toBeInTheDocument()
})

test('trace stages and sources keep canonical protocol spelling', () => {
  render(<RunWorkspace run={run} />)

  // Previously these were lower-case identifiers styled with CSS `text-transform: capitalize`,
  // which rendered "Bb84" and "Qkd".
  expect(screen.getAllByText('BB84').length).toBeGreaterThan(0)
  expect(screen.queryByText(/\bBb84\b/)).not.toBeInTheDocument()
  expect(screen.queryByText(/\bQkd\b/)).not.toBeInTheDocument()
  expect(screen.getByText('Classical authentication')).toBeInTheDocument()
})

test('an aborted run leads with its reason and reports no accepted material', () => {
  const aborted: SessionRunResponse = {
    ...run,
    record: {
      ...run.record,
      result: {
        ...run.record.result,
        status: 'aborted',
        abort_reason:
          'BB84 security abort: Per-basis errors Z=0.231481, X=0.208333 give phase-error bound 0.231481, above the configured asymptotic threshold 0.110000.',
        established_key: { type: null, bit_length: 0 },
        provenance: [],
      },
    },
  }

  render(<RunWorkspace run={aborted} />)

  const outcome = screen.getByRole('heading', { name: /QKD-ASSUMED — Session securely aborted/i })
  expect(outcome).toBeInTheDocument()
  // Scoped to the banner: the reason also occurs inside the public JSON record.
  const banner = outcome.closest('.run-outcome') as HTMLElement
  expect(banner).toHaveClass('run-outcome--aborted')
  expect(within(banner).getByText('Abort reason')).toBeInTheDocument()
  expect(within(banner).getByText(/above the configured asymptotic threshold 0\.110000/)).toBeInTheDocument()
  expect(screen.getByText('None accepted')).toBeInTheDocument()
  expect(screen.queryByText('0 bit')).not.toBeInTheDocument()
  // The configured abort threshold is shown beside the bound it was tested against.
  expect(screen.getByText(/abort above 11\.00%/i)).toBeInTheDocument()
})
