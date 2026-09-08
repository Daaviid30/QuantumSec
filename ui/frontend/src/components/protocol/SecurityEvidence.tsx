import { Fingerprint, ShieldCheck } from 'lucide-react'

import type { AuthenticationOutcome, SecretProvenance } from '../../types/api'

interface SecurityEvidenceProps {
  qkd: AuthenticationOutcome | null
  pqc: AuthenticationOutcome | null
  provenance: SecretProvenance[]
}

function AuthenticationCard({ outcome }: { outcome: AuthenticationOutcome }) {
  const state = !outcome.executed ? 'assumed' : outcome.verified ? 'verified' : 'failed'
  return (
    <article className={`auth-card auth-card--${state}`}>
      <div className="auth-card__heading">
        <span><ShieldCheck size={15} aria-hidden="true" /> {outcome.purpose}</span>
        <strong>{!outcome.executed ? 'ASSUMED — NOT EXECUTED' : outcome.verified ? 'EXECUTED — VERIFIED' : 'EXECUTED — FAILED'}</strong>
      </div>
      <dl>
        <div><dt>Mechanism</dt><dd>{outcome.mechanism}</dd></div>
        <div><dt>Algorithm</dt><dd>{outcome.algorithm}</dd></div>
        <div><dt>Trust boundary</dt><dd>{outcome.trust_assumption}</dd></div>
      </dl>
    </article>
  )
}

export function SecurityEvidence({ qkd, pqc, provenance }: SecurityEvidenceProps) {
  return (
    <section className="surface security-evidence">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Authentication and provenance</p>
          <h2>Why this session material is accepted</h2>
        </div>
        <Fingerprint size={18} aria-hidden="true" />
      </div>
      <div className="auth-grid">
        {qkd ? <AuthenticationCard outcome={qkd} /> : null}
        {pqc ? <AuthenticationCard outcome={pqc} /> : null}
      </div>
      <div className="provenance-table-wrap">
        <table className="data-table">
          <thead><tr><th>#</th><th>Source</th><th>Protocol</th><th>Algorithm</th><th>Encoding</th><th>Length</th></tr></thead>
          <tbody>
            {provenance.map((item) => (
              <tr key={`${item.position}-${item.source}`}>
                <td><code>{String(item.position).padStart(2, '0')}</code></td>
                <td>{item.source}</td>
                <td>{item.protocol}</td>
                <td>{item.algorithm}</td>
                <td>{item.encoding}</td>
                <td><code>{item.bit_length} bit</code></td>
              </tr>
            ))}
          </tbody>
        </table>
        {provenance.length === 0 ? <p className="table-empty">No secret contribution was accepted for this terminal result.</p> : null}
      </div>
    </section>
  )
}
