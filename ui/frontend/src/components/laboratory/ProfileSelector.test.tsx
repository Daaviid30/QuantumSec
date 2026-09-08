import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { capabilitiesFixture } from '../../test/fixtures'
import { ProfileSelector } from './ProfileSelector'

test('selects supported public profiles without exposing internal LOW or HIGH names', async () => {
  const onSelect = vi.fn()
  const user = userEvent.setup()
  render(<ProfileSelector profiles={capabilitiesFixture.profiles} selected="QKD-ASSUMED" onSelect={onSelect} />)

  expect(screen.getByRole('button', { name: /QKD-ASSUMED/i })).toHaveAttribute('aria-pressed', 'true')
  expect(screen.queryByText(/^LOW$/)).not.toBeInTheDocument()
  expect(screen.queryByText(/^HIGH$/)).not.toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /PQC-BASE/i }))
  expect(onSelect).toHaveBeenCalledWith('PQC-BASE')
})
