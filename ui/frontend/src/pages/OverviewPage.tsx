import { ArrowRight, Check, Cpu, FlaskConical, Layers3, ShieldCheck } from 'lucide-react'

import type { CapabilitiesResponse, ProfileFamily } from '../types/api'

interface OverviewPageProps {
  capabilities: CapabilitiesResponse
  onStart: () => void
}

const familyLabels: Record<ProfileFamily, string> = {
  qkd: 'Quantum key distribution',
  pqc: 'Post-quantum cryptography',
  hybrid: 'Upper-layer hybrid composition',
}

export function OverviewPage({ capabilities, onStart }: OverviewPageProps) {
  return (
    <div className="page-stack">
      <section className="overview-intro">
        <div>
          <p className="section-kicker">Interactive quantum-safe security laboratory</p>
          <h2>Inspect how quantum-safe sessions are established, authenticated, and accepted.</h2>
          <p>Configure supported QKD, PQC, and hybrid profiles; observe real execution traces; retain reproducible records; and compare only scientifically compatible evidence.</p>
          <button type="button" className="button button--primary" onClick={onStart}>
            <FlaskConical size={16} aria-hidden="true" /> Start experiment <ArrowRight size={15} aria-hidden="true" />
          </button>
        </div>
        <aside className="overview-principle">
          <span className="principle-index">01</span>
          <p>Configure</p><i />
          <span className="principle-index">02</span>
          <p>Run</p><i />
          <span className="principle-index">03</span>
          <p>Observe</p><i />
          <span className="principle-index">04</span>
          <p>Analyze</p><i />
          <span className="principle-index">05</span>
          <p>Compare</p>
        </aside>
      </section>

      <section className="surface">
        <div className="section-heading">
          <div>
            <p className="section-kicker">Supported security profiles</p>
            <h2>Seven bounded compositions, one laboratory model</h2>
            <p>Public profile names preserve the thesis contract. Components and authentication are derived from each profile.</p>
          </div>
          <span className="quiet-badge"><Check size={12} /> Source-backed</span>
        </div>
        <div className="overview-profiles">
          {(Object.keys(familyLabels) as ProfileFamily[]).map((family) => (
            <div key={family} className="overview-profile-group">
              <h3>{familyLabels[family]}</h3>
              {capabilities.profiles.filter((profile) => profile.family === family).map((profile) => (
                <article key={profile.id}>
                  <div><strong>{profile.name}</strong><span>{profile.status}</span></div>
                  <p>{profile.description}</p>
                  <small>{profile.algorithms.join(' · ')}</small>
                </article>
              ))}
            </div>
          ))}
        </div>
      </section>

      <div className="overview-bottom-grid">
        <section className="surface capability-summary">
          <div className="section-heading">
            <div><p className="section-kicker">Executable scope</p><h2>Backend capabilities</h2></div>
            <Layers3 size={18} aria-hidden="true" />
          </div>
          <ul>
            {capabilities.features.filter((feature) => feature.implemented).map((feature) => (
              <li key={feature.id}><Check size={13} aria-hidden="true" /><span><strong>{feature.name}</strong><small>{feature.description}</small></span></li>
            ))}
          </ul>
        </section>
        <aside className="surface readiness-panel">
          <div className="section-heading">
            <div><p className="section-kicker">System readiness</p><h2>Laboratory backend</h2></div>
            <span className="status-dot status-dot--ok" />
          </div>
          <dl>
            <div><dt>API</dt><dd>Ready</dd></div>
            <div><dt>Version</dt><dd><code>{capabilities.version}</code></dd></div>
            <div><dt>Profiles</dt><dd>{capabilities.profiles.filter((profile) => profile.implemented).length} current</dd></div>
            <div><dt>QKD stages</dt><dd>{capabilities.channels.length + capabilities.adversaries.length}</dd></div>
          </dl>
          <div className="readiness-boundary"><Cpu size={15} /><p><strong>Measurement boundary</strong> BB84 simulation and real PQC operations remain separate categories.</p></div>
          <div className="readiness-boundary"><ShieldCheck size={15} /><p><strong>Secret boundary</strong> Session keys and private material never enter browser records.</p></div>
        </aside>
      </div>
    </div>
  )
}
