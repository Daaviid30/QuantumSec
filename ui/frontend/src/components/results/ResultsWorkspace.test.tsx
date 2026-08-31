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

  expect(screen.getByText('64')).toBeInTheDocument()
  expect(screen.getByText('32')).toBeInTheDocument()
  expect(screen.getByText('25')).toBeInTheDocument()
  expect(screen.getByText('0.00%')).toBeInTheDocument()
  expect(screen.getByText('13')).toBeInTheDocument()
  expect(screen.getByText(/completed/i)).toBeInTheDocument()
  expect(screen.getByText(/show final simulated key/i)).toBeInTheDocument()
  expect(screen.getByText(resultFixture.postprocessing.final_key!)).toBeInTheDocument()
})

test('aborted session shows the exact reason instead of a final key', () => {
  const abortedResult = {
    ...resultFixture,
    postprocessing: {
      ...resultFixture.postprocessing,
      status: 'aborted' as const,
      abort_reason: 'Estimated QBER exceeds the configured threshold.',
      n_final: 0,
      final_key: null,
    },
  }

  render(<ResultsSummary result={abortedResult} />)

  expect(screen.getByRole('alert')).toHaveTextContent(/final key generation failed/i)
  expect(screen.getByRole('alert')).toHaveTextContent(/estimated qber exceeds/i)
  expect(screen.queryByText(/show final simulated key/i)).not.toBeInTheDocument()
})
