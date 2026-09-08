import { Atom, Boxes, GitMerge } from 'lucide-react'

import { PROFILE_SHORT_LABELS } from '../../lib/profiles'
import type { ProfileCapability, ProfileFamily, PublicSessionProfile } from '../../types/api'

interface ProfileSelectorProps {
  profiles: ProfileCapability[]
  selected: PublicSessionProfile
  onSelect: (profile: PublicSessionProfile) => void
}

const familyMeta: Record<ProfileFamily, { label: string; icon: typeof Atom }> = {
  qkd: { label: 'QKD', icon: Atom },
  pqc: { label: 'Post-quantum', icon: Boxes },
  hybrid: { label: 'Hybrid', icon: GitMerge },
}

export function ProfileSelector({ profiles, selected, onSelect }: ProfileSelectorProps) {
  return (
    <section className="surface profile-selector" aria-labelledby="profile-heading">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Security profile</p>
          <h2 id="profile-heading">Choose an executable composition</h2>
          <p>The profile fixes establishment and authentication roles; algorithms are not mixed arbitrarily.</p>
        </div>
        <span className="quiet-badge">7 current profiles</span>
      </div>

      <div className="profile-groups">
        {(Object.keys(familyMeta) as ProfileFamily[]).map((family) => {
          const meta = familyMeta[family]
          const Icon = meta.icon
          return (
            <div key={family} className="profile-group">
              <div className="profile-group__label">
                <Icon size={14} aria-hidden="true" /> {meta.label}
              </div>
              <div className="profile-group__options">
                {profiles
                  .filter((profile) => profile.family === family)
                  .map((profile) => (
                    <button
                      key={profile.id}
                      type="button"
                      className={`profile-option ${selected === profile.id ? 'profile-option--selected' : ''}`}
                      onClick={() => onSelect(profile.id)}
                      disabled={!profile.implemented}
                      aria-pressed={selected === profile.id}
                    >
                      <span>
                        <strong>{profile.name}</strong>
                        <small>{PROFILE_SHORT_LABELS[profile.id]}</small>
                      </span>
                      {profile.implemented ? null : (
                        <span className="status-note status-note--attention">{profile.status}</span>
                      )}
                    </button>
                  ))}
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
