import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { capabilitiesFixture } from '../test/fixtures'
import { defaultRunRequest } from '../lib/profiles'
import { LaboratoryPage } from './LaboratoryPage'

test('configuration controls follow the selected profile capability', async () => {
  const user = userEvent.setup()
  render(
    <LaboratoryPage
      capabilities={capabilitiesFixture}
      preset={defaultRunRequest('QKD-ASSUMED')}
      currentRun={null}
      onRunComplete={vi.fn()}
    />,
  )

  expect(screen.getByLabelText(/quantum signals/i)).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: /PQC-BASE/i }))
  expect(screen.queryByLabelText(/quantum signals/i)).not.toBeInTheDocument()
  expect(screen.getByText(/persistent pre-provisioned ML-DSA identities/i)).toBeInTheDocument()
})
