import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { capabilitiesFixture } from '../../test/fixtures'
import { ProtocolSelector } from './ProtocolSelector'

test('BB84 is enabled while unavailable protocols are disabled', async () => {
  const onSelect = vi.fn()
  const user = userEvent.setup()
  render(
    <ProtocolSelector
      protocols={capabilitiesFixture.protocols}
      selected="bb84"
      onSelect={onSelect}
    />,
  )

  const bb84 = screen.getByRole('button', { name: /bb84/i })
  const e91 = screen.getByRole('button', { name: /e91/i })

  expect(bb84).toBeEnabled()
  expect(bb84).toHaveAttribute('aria-pressed', 'true')
  expect(e91).toBeDisabled()

  await user.click(bb84)
  expect(onSelect).toHaveBeenCalledWith('bb84')
})
