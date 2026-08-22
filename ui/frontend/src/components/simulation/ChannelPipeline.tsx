import { ChevronDown, Plus, RadioTower, Waves } from 'lucide-react'

import type { ChannelCapability, ChannelDraft } from '../../types/api'
import { Panel, SectionHeading } from '../common/Panel'
import { StatusPill } from '../common/StatusPill'
import { ChannelCard } from './ChannelCard'

interface ChannelPipelineProps {
  capabilities: ChannelCapability[]
  channels: ChannelDraft[]
  selectedType: string
  maxChannels: number
  onSelectedTypeChange: (type: string) => void
  onAdd: () => void
  onRemove: (id: number) => void
  onMove: (id: number, direction: -1 | 1) => void
  onParameterChange: (id: number, key: string, value: number) => void
}

export function ChannelPipeline({
  capabilities,
  channels,
  selectedType,
  maxChannels,
  onSelectedTypeChange,
  onAdd,
  onRemove,
  onMove,
  onParameterChange,
}: ChannelPipelineProps) {
  return (
    <Panel id="channel-pipeline" className="p-5 lg:p-6">
      <SectionHeading
        eyebrow="Channel stack"
        title="Quantum channel pipeline"
        description="Each CPTP channel is applied sequentially from top to bottom. Order changes the physical transformation."
        action={<StatusPill tone={channels.length ? 'cyan' : 'muted'}>{channels.length || 'Ideal'} stage</StatusPill>}
      />

      <div className="mt-5">
        <div className="flex items-center gap-3 rounded-xl border border-cyan-300/10 bg-cyan-300/[0.025] px-4 py-3">
          <div className="source-node source-node--alice">A</div>
          <div>
            <div className="text-[10px] font-semibold uppercase tracking-[0.15em] text-cyan-300/70">Alice</div>
            <div className="mt-0.5 text-xs text-slate-400">Prepared BB84 density matrices</div>
          </div>
          <Waves className="ml-auto text-cyan-300/30" size={19} aria-hidden="true" />
        </div>

        <div className="pipeline-rail">
          {channels.length === 0 ? (
            <div className="ideal-channel-state">
              <RadioTower size={18} aria-hidden="true" />
              <div>
                <div className="text-xs font-semibold text-slate-300">Ideal quantum path</div>
                <div className="mt-0.5 text-[10px] text-slate-600">Empty ChannelPipeline acts as identity.</div>
              </div>
            </div>
          ) : (
            channels.map((draft, index) => {
              const capability = capabilities.find((candidate) => candidate.id === draft.type)
              if (!capability) return null
              return (
                <div key={draft.id} className="relative">
                  <ChannelCard
                    draft={draft}
                    capability={capability}
                    index={index}
                    total={channels.length}
                    onParameterChange={(key, value) => onParameterChange(draft.id, key, value)}
                    onMove={(direction) => onMove(draft.id, direction)}
                    onRemove={() => onRemove(draft.id)}
                  />
                  {index < channels.length - 1 && (
                    <ChevronDown className="pipeline-arrow" size={15} aria-hidden="true" />
                  )}
                </div>
              )
            })
          )}
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-violet-300/10 bg-violet-300/[0.025] px-4 py-3">
          <div className="source-node source-node--bob">B</div>
          <div>
            <div className="text-[10px] font-semibold uppercase tracking-[0.15em] text-violet-300/70">Bob</div>
            <div className="mt-0.5 text-xs text-slate-400">Projective measurement in Z / X</div>
          </div>
          <RadioTower className="ml-auto text-violet-300/30" size={19} aria-hidden="true" />
        </div>
      </div>

      <div className="mt-5 flex flex-col gap-2 sm:flex-row">
        <div className="relative flex-1">
          <select
            aria-label="Channel type"
            className="lab-select"
            value={selectedType}
            onChange={(event) => onSelectedTypeChange(event.target.value)}
          >
            {capabilities
              .filter((channel) => channel.implemented)
              .map((channel) => (
                <option key={channel.id} value={channel.id}>
                  {channel.name}
                </option>
              ))}
          </select>
          <ChevronDown className="select-chevron" size={14} aria-hidden="true" />
        </div>
        <button
          type="button"
          className="secondary-button"
          disabled={channels.length >= maxChannels}
          onClick={onAdd}
        >
          <Plus size={15} aria-hidden="true" /> Add channel
        </button>
      </div>
    </Panel>
  )
}
