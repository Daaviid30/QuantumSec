import { render, screen } from '@testing-library/react'

import { capabilitiesFixture } from '../../test/fixtures'
import { CompositionSummary } from './CompositionSummary'

test('presents embedded backend identifiers with canonical cryptographic spelling', () => {
  const base = capabilitiesFixture.profiles[0]
  const profile = {
    ...base,
    id: 'QKD-PQC-AUTH' as const,
    name: 'QKD-PQC-AUTH',
    authentication: ['QKD classical authentication: ml_dsa_65'],
    algorithms: ['BB84', 'ML-DSA-65'],
  }

  render(
    <CompositionSummary
      profile={profile}
      qkdStages={[{ type: 'intercept_resend', intercept_fraction: 0.5 }]}
    />,
  )

  expect(screen.getByText('QKD classical authentication: ML-DSA-65')).toBeInTheDocument()
  expect(screen.getByText('Intercept-resend')).toBeInTheDocument()
  expect(screen.queryByText(/ml_dsa_65/i)).not.toBeInTheDocument()
})
