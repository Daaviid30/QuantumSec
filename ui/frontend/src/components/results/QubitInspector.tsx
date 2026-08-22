import { ChevronLeft, ChevronRight, Microscope } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import type { BB84SimulationResponse } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'
import { StatusPill } from '../common/StatusPill'

interface QubitInspectorProps {
  result: BB84SimulationResponse
}

const PAGE_SIZE = 12

export function QubitInspector({ result }: QubitInspectorProps) {
  const [page, setPage] = useState(0)
  const totalPages = Math.max(1, Math.ceil(result.transmissions.length / PAGE_SIZE))

  useEffect(() => setPage(0), [result.metadata.request_id])

  const visibleRecords = useMemo(
    () => result.transmissions.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE),
    [page, result.transmissions],
  )

  return (
    <Panel className="overflow-hidden">
      <div className="p-5 pb-4 lg:p-6 lg:pb-4">
        <SectionHeading
          eyebrow="Transmission inspector"
          title="Alice → Channel → Bob"
          description="A bounded view of raw positions; unmatched bases are excluded from the sifted material."
          action={<StatusPill tone="muted">First {result.transmissions.length}</StatusPill>}
        />
      </div>

      <div className="overflow-x-auto">
        <table className="inspector-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Alice bit</th>
              <th>Alice basis</th>
              <th>Bob basis</th>
              <th>Bob result</th>
              <th>Sifting</th>
              <th>Observed error</th>
            </tr>
          </thead>
          <tbody>
            {visibleRecords.map((record) => (
              <tr key={record.index}>
                <td className="font-mono text-slate-600">{String(record.index).padStart(3, '0')}</td>
                <td><span className="bit-token bit-token--alice">{record.alice_bit}</span></td>
                <td><span className="basis-token">{record.alice_basis}</span></td>
                <td><span className="basis-token basis-token--bob">{record.bob_basis}</span></td>
                <td><span className="bit-token bit-token--bob">{record.bob_result}</span></td>
                <td>
                  <span className={`table-state ${record.basis_match ? 'table-state--kept' : 'table-state--discarded'}`}>
                    {record.basis_match ? 'Retained' : 'Discarded'}
                  </span>
                </td>
                <td>
                  {record.sifted_error === null ? (
                    <span className="text-slate-700">—</span>
                  ) : record.sifted_error ? (
                    <span className="table-state table-state--error">Mismatch</span>
                  ) : (
                    <span className="table-state table-state--kept">Match</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between border-t border-white/6 px-5 py-3.5 text-[10px] text-slate-600">
        <div className="flex items-center gap-2">
          <Microscope size={12} aria-hidden="true" />
          {result.metadata.inspector_truncated
            ? `Inspector capped at ${result.metadata.inspector_limit} of ${result.metrics.n_raw} positions`
            : `${result.transmissions.length} positions inspected`}
        </div>
        <div className="flex items-center gap-2">
          <span>Page {page + 1} / {totalPages}</span>
          <button
            type="button"
            className="mini-icon-button"
            disabled={page === 0}
            onClick={() => setPage((current) => Math.max(0, current - 1))}
            aria-label="Previous inspector page"
          >
            <ChevronLeft size={13} />
          </button>
          <button
            type="button"
            className="mini-icon-button"
            disabled={page >= totalPages - 1}
            onClick={() => setPage((current) => Math.min(totalPages - 1, current + 1))}
            aria-label="Next inspector page"
          >
            <ChevronRight size={13} />
          </button>
        </div>
      </div>
    </Panel>
  )
}
