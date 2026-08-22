import { render, screen } from '@testing-library/react'

import { resultFixture } from '../../test/fixtures'
import { ResultsSummary } from './ResultsSummary'
import { ResultsWorkspace } from './ResultsWorkspace'

test('idle result state does not imply synthetic simulation data', () => {
  render(<ResultsWorkspace status="idle" request={null} result={null} />)

  expect(screen.getByText(/awaiting a simulation run/i)).toBeInTheDocument()
  expect(screen.getByText(/no synthetic dashboard data/i)).toBeInTheDocument()
})

test('completed result summary renders real BB84 metrics', () => {
  render(<ResultsSummary result={resultFixture} />)

  expect(screen.getByText('4')).toBeInTheDocument()
  expect(screen.getByText('2')).toBeInTheDocument()
  expect(screen.getByText('50.00%')).toBeInTheDocument()
  expect(screen.getByText('0.00%')).toBeInTheDocument()
  expect(screen.getByText(/completed/i)).toBeInTheDocument()
})
