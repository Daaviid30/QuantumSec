import { ArrowDown, Atom, Boxes, GitMerge, KeyRound, ShieldCheck, UserRound } from 'lucide-react'

import type { ChannelConfiguration, ProfileCapability } from '../../types/api'

interface CompositionSummaryProps {
  profile: ProfileCapability
  qkdStages: ChannelConfiguration[]
}

export function CompositionSummary({ profile, qkdStages }: CompositionSummaryProps) {
  const hasEve = qkdStages.some((stage) => stage.type === 'intercept_resend')
  return (
    <aside className="surface composition-summary">
      <div className="section-heading">
        <div><p className="section-kicker">Profile definition</p><h2>{profile.name}</h2><p>{profile.description}</p></div>
        {profile.family === 'qkd' ? <Atom size={18} /> : profile.family === 'pqc' ? <Boxes size={18} /> : <GitMerge size={18} />}
      </div>

      {profile.supports_qkd ? (
        <div className="composition-flow">
          <div className="composition-node"><UserRound size={15} /><span><strong>Alice</strong><small>BB84 preparation</small></span></div>
          <ArrowDown size={14} className="composition-arrow" />
          {hasEve ? <><div className="composition-node composition-node--eve"><ShieldCheck size={15} /><span><strong>Eve</strong><small>Executed intercept-resend stage</small></span></div><ArrowDown size={14} className="composition-arrow" /></> : null}
          <div className="composition-node"><Atom size={15} /><span><strong>Quantum channel</strong><small>{qkdStages.length ? qkdStages.map((stage) => stage.type.replaceAll('_', ' ')).join(' → ') : 'Ideal pipeline'}</small></span></div>
          <ArrowDown size={14} className="composition-arrow" />
          <div className="composition-node"><UserRound size={15} /><span><strong>Bob</strong><small>Measurement and post-processing</small></span></div>
        </div>
      ) : null}

      <div className="composition-block">
        <h3>Established from</h3>
        <div className="composition-chips">{profile.establishment.map((item) => <span key={item}>{item}</span>)}</div>
      </div>
      <div className="composition-block">
        <h3>Authentication policy</h3>
        {profile.authentication.map((item) => <p key={item}><ShieldCheck size={13} /> {item}</p>)}
      </div>
      <div className="composition-block">
        <h3>Executed components</h3>
        <div className="algorithm-list">
          {profile.algorithms.map((algorithm) => (
            <div key={algorithm}><KeyRound size={13} /><span>{algorithm}</span></div>
          ))}
        </div>
      </div>
      {profile.algorithms.includes('HQC-3') ? <p className="standards-note">HQC-3 is selected for NIST standardization; it is not presented as a published standard.</p> : null}
    </aside>
  )
}
