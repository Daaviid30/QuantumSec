import { ChevronDown, ClipboardCheck, Code2, Fingerprint } from 'lucide-react'
import { useState } from 'react'

import type { BB84SimulationRequest, BB84SimulationResponse } from '../../types/api'
import { Panel } from '../common/Panel'

interface ScientificDetailsProps {
  request: BB84SimulationRequest
  result: BB84SimulationResponse
}

export function ScientificDetails({ request, result }: ScientificDetailsProps) {
  const [copied, setCopied] = useState(false)
  const scientificRecord = { request, response: result }
  const json = JSON.stringify(scientificRecord, null, 2)

  const copy = async () => {
    await navigator.clipboard.writeText(json)
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1600)
  }

  return (
    <Panel>
      <details className="group">
        <summary className="flex cursor-pointer list-none items-center gap-3 px-5 py-4 lg:px-6">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-white/7 bg-white/[0.025] text-slate-500">
            <Code2 size={15} aria-hidden="true" />
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-300">Simulation details</div>
            <div className="mt-0.5 text-[10px] text-slate-600">Exact configuration and structured API output</div>
          </div>
          <ChevronDown
            size={15}
            className="ml-auto text-slate-600 transition-transform group-open:rotate-180"
            aria-hidden="true"
          />
        </summary>
        <div className="border-t border-white/6 px-5 py-5 lg:px-6">
          <div className="mb-4 grid gap-3 sm:grid-cols-3">
            <div className="detail-chip">
              <Fingerprint size={13} aria-hidden="true" />
              <span>Seed</span>
              <strong>{result.metadata.seed}</strong>
            </div>
            <div className="detail-chip">
              <ClipboardCheck size={13} aria-hidden="true" />
              <span>Request</span>
              <strong>{result.metadata.request_id.slice(0, 12)}</strong>
            </div>
            <div className="detail-chip">
              <Code2 size={13} aria-hidden="true" />
              <span>Protocol</span>
              <strong>BB84</strong>
            </div>
          </div>
          <div className="relative">
            <button type="button" className="code-copy-button" onClick={copy}>
              {copied ? 'Copied' : 'Copy JSON'}
            </button>
            <pre className="scientific-json">{json}</pre>
          </div>
        </div>
      </details>
    </Panel>
  )
}
