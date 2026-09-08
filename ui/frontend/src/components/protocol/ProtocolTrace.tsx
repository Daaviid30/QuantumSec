import { Check, CircleDot, TriangleAlert, X } from 'lucide-react'
import { useEffect, useState } from 'react'

import { formatIdentifier, formatSource } from '../../lib/labels'
import type { SessionTraceEvent } from '../../types/api'

interface ProtocolTraceProps {
  events: SessionTraceEvent[]
}

type EventTone = 'success' | 'warning' | 'danger' | 'neutral'

function eventTone(state: string): EventTone {
  const normalized = state.toLowerCase()
  if (normalized.includes('abort') || normalized.includes('fail') || normalized.includes('withheld')) return 'danger'
  // `assumed_not_executed` is a first-class distinction in this thesis and is rendered with the same
  // weight the security-evidence panel gives it, rather than as a neutral procedural step.
  if (normalized.includes('assumed')) return 'warning'
  if (normalized.includes('verified') || normalized.includes('established') || normalized.includes('released') || normalized.includes('completed')) return 'success'
  return 'neutral'
}

function ToneIcon({ tone }: { tone: EventTone }) {
  if (tone === 'success') return <Check size={14} aria-hidden="true" />
  if (tone === 'danger') return <X size={14} aria-hidden="true" />
  if (tone === 'warning') return <TriangleAlert size={13} aria-hidden="true" />
  return <CircleDot size={12} aria-hidden="true" />
}

export function ProtocolTrace({ events }: ProtocolTraceProps) {
  const [selectedSequence, setSelectedSequence] = useState(events[0]?.sequence ?? 0)
  useEffect(() => setSelectedSequence(events[0]?.sequence ?? 0), [events])
  const selected = events.find((event) => event.sequence === selectedSequence) ?? events[0]

  return (
    <section className="surface trace-panel">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Ordered execution trace</p>
          <h2>What the engine executed</h2>
          <p>Every row is emitted by orchestration; selecting one opens its public evidence.</p>
        </div>
        <span className="quiet-badge">{events.length} events</span>
      </div>

      <div className="trace-layout">
        <ol className="trace-list">
          {events.map((event) => {
            const tone = eventTone(event.state)
            return (
              <li key={event.sequence}>
                <button
                  type="button"
                  className={`trace-event trace-event--${tone} ${selectedSequence === event.sequence ? 'trace-event--selected' : ''}`}
                  onClick={() => setSelectedSequence(event.sequence)}
                  aria-pressed={selectedSequence === event.sequence}
                >
                  <span className="trace-event__marker">
                    <ToneIcon tone={tone} />
                  </span>
                  <span className="trace-event__sequence">{String(event.sequence + 1).padStart(2, '0')}</span>
                  <span className="trace-event__copy">
                    <strong>{formatIdentifier(event.stage)}</strong>
                    <small>{event.detail}</small>
                  </span>
                  <span className="trace-event__state">{formatIdentifier(event.state)}</span>
                </button>
              </li>
            )
          })}
        </ol>

        {selected ? (
          <aside className="event-inspector">
            <p className="section-kicker">Event inspector</p>
            <h3>{formatIdentifier(selected.stage)}</h3>
            <dl>
              <div><dt>Sequence</dt><dd>{selected.sequence + 1}</dd></div>
              <div><dt>Source</dt><dd>{formatSource(selected.source)}</dd></div>
              <div><dt>State</dt><dd>{formatIdentifier(selected.state)}</dd></div>
            </dl>
            <div className="event-inspector__detail">
              <strong>Recorded detail</strong>
              <p>{selected.detail}</p>
            </div>
            <p className="event-inspector__note">This inspector presents public trace fields only. Secret inputs and derived keys are intentionally absent.</p>
          </aside>
        ) : null}
      </div>
    </section>
  )
}
