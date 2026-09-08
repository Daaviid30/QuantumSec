import { Check, LockKeyhole, Send, ShieldAlert } from 'lucide-react'
import { useState } from 'react'

import { protectMessage } from '../../api/client'
import type { ProtectedMessageResponse } from '../../types/api'

interface DataPlaneDemoProps {
  runId: string
}

export function DataPlaneDemo({ runId }: DataPlaneDemoProps) {
  const [plaintext, setPlaintext] = useState('QuantumSec protected research payload')
  const [result, setResult] = useState<ProtectedMessageResponse | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const submit = async () => {
    setBusy(true)
    setError(null)
    try {
      setResult(await protectMessage(runId, plaintext, 'QuantumSec/WebLab/v1'))
    } catch (reason: unknown) {
      setError(reason instanceof Error ? reason.message : 'Payload protection failed.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="surface data-plane">
      <div className="data-plane__path">
        <span><small>Establishment plane</small><strong>256-bit K_SESSION retained by backend</strong></span>
        <span className="data-plane__arrow">→</span>
        <span><small>Data plane</small><strong>AES-256-GCM</strong></span>
      </div>
      <div className="data-plane__controls">
        <label className="field">
          <span><LockKeyhole size={13} aria-hidden="true" /> Test payload</span>
          <input maxLength={512} value={plaintext} onChange={(event) => setPlaintext(event.target.value)} />
        </label>
        <button className="button button--secondary" type="button" onClick={submit} disabled={busy || !plaintext.trim()}>
          <Send size={15} aria-hidden="true" /> {busy ? 'Protecting…' : 'Protect and verify'}
        </button>
      </div>
      {error ? <p className="inline-error" role="alert">{error}</p> : null}
      {result ? (
        <div className="data-plane__result">
          <span><Check size={14} aria-hidden="true" /> Round trip verified</span>
          <span><ShieldAlert size={14} aria-hidden="true" /> Tamper rejected</span>
          <code>{result.ciphertext_preview}</code>
          <small>{result.plaintext_bytes} B plaintext · {result.ciphertext_bytes} B ciphertext · {result.nonce_bytes} B nonce · {result.tag_bytes} B tag</small>
        </div>
      ) : null}
    </section>
  )
}
