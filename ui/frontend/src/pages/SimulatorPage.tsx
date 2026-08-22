import { Cpu, DatabaseZap, FlaskConical, RadioTower, ShieldCheck, Sparkles } from 'lucide-react'
import { useMemo, useRef, useState } from 'react'

import { createChannelDraft, serializeChannels, validateChannels } from '../lib/channels'
import type {
  BB84SimulationRequest,
  CapabilitiesResponse,
  ChannelDraft,
} from '../types/api'
import { ResultsWorkspace } from '../components/results/ResultsWorkspace'
import { ChannelPipeline } from '../components/simulation/ChannelPipeline'
import { QuantumFlow } from '../components/simulation/QuantumFlow'
import { SimulationConfigurator } from '../components/simulation/SimulationConfigurator'
import { SimulationControls } from '../components/simulation/SimulationControls'
import { useSimulation } from '../hooks/useSimulation'

interface SimulatorPageProps {
  capabilities: CapabilitiesResponse
}

export function SimulatorPage({ capabilities }: SimulatorPageProps) {
  const [protocol, setProtocol] = useState('bb84')
  const [nSignals, setNSignals] = useState(512)
  const [seed, setSeed] = useState(2026)
  const [channels, setChannels] = useState<ChannelDraft[]>([])
  const [selectedChannelType, setSelectedChannelType] = useState(
    capabilities.channels.find((channel) => channel.id === 'depolarizing')?.id ??
      capabilities.channels[0]?.id ??
      '',
  )
  const [lastRequest, setLastRequest] = useState<BB84SimulationRequest | null>(null)
  const nextChannelId = useRef(1)
  const simulation = useSimulation()

  const maxSignals = capabilities.limits.max_signals ?? 100_000
  const maxChannels = capabilities.limits.max_channels ?? 12

  const validationError = useMemo(() => {
    if (!Number.isInteger(nSignals) || nSignals < 1 || nSignals > maxSignals) {
      return `Signals must be an integer between 1 and ${maxSignals.toLocaleString()}.`
    }
    if (!Number.isInteger(seed) || seed < 0 || seed > 4_294_967_295) {
      return 'Seed must be an integer between 0 and 4,294,967,295.'
    }
    return validateChannels(channels, capabilities.channels)
  }, [capabilities.channels, channels, maxSignals, nSignals, seed])

  const channelNames = channels
    .map((draft) => capabilities.channels.find((channel) => channel.id === draft.type)?.name)
    .filter((name): name is string => Boolean(name))

  const addChannel = () => {
    const capability = capabilities.channels.find((channel) => channel.id === selectedChannelType)
    if (!capability || channels.length >= maxChannels) return
    setChannels((current) => [...current, createChannelDraft(capability, nextChannelId.current++)])
  }

  const removeChannel = (id: number) => {
    setChannels((current) => current.filter((channel) => channel.id !== id))
  }

  const moveChannel = (id: number, direction: -1 | 1) => {
    setChannels((current) => {
      const index = current.findIndex((channel) => channel.id === id)
      const target = index + direction
      if (index < 0 || target < 0 || target >= current.length) return current
      const reordered = [...current]
      ;[reordered[index], reordered[target]] = [reordered[target], reordered[index]]
      return reordered
    })
  }

  const changeParameter = (id: number, key: string, value: number) => {
    setChannels((current) =>
      current.map((channel) =>
        channel.id === id
          ? { ...channel, parameters: { ...channel.parameters, [key]: value } }
          : channel,
      ),
    )
  }

  const runSimulation = () => {
    if (validationError || protocol !== 'bb84') return
    const request: BB84SimulationRequest = {
      protocol: 'bb84',
      n_signals: nSignals,
      seed,
      channels: serializeChannels(channels),
    }
    setLastRequest(request)
    void simulation.run(request)
  }

  return (
    <div id="simulator" className="space-y-5">
      <section className="hero-strip">
        <div className="relative z-10">
          <div className="flex items-center gap-2 text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-300/75">
            <Sparkles size={13} aria-hidden="true" /> Simulation workspace / BB84
          </div>
          <h2 className="mt-2 max-w-3xl text-2xl font-semibold tracking-[-0.04em] text-white md:text-3xl">
            Reproducible quantum-channel laboratory
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Configure the protocol, compose physical noise models, and inspect the exact state of the
            sifted BB84 material.
          </p>
        </div>
        <div className="hero-strip__telemetry">
          <div><Cpu size={14} /><span>Density matrix</span></div>
          <div><RadioTower size={14} /><span>CPTP pipeline</span></div>
          <div><DatabaseZap size={14} /><span>Seeded RNG</span></div>
          <div><ShieldCheck size={14} /><span>QBER</span></div>
        </div>
        <FlaskConical className="hero-strip__watermark" aria-hidden="true" />
      </section>

      <div className="grid items-start gap-4 xl:grid-cols-[360px_minmax(0,1fr)]">
        <SimulationConfigurator
          protocols={capabilities.protocols}
          protocol={protocol}
          nSignals={nSignals}
          seed={seed}
          maxSignals={maxSignals}
          onProtocolChange={setProtocol}
          onSignalsChange={setNSignals}
          onSeedChange={setSeed}
        />
        <div className="space-y-4">
          <ChannelPipeline
            capabilities={capabilities.channels}
            channels={channels}
            selectedType={selectedChannelType}
            maxChannels={maxChannels}
            onSelectedTypeChange={setSelectedChannelType}
            onAdd={addChannel}
            onRemove={removeChannel}
            onMove={moveChannel}
            onParameterChange={changeParameter}
          />
          <QuantumFlow
            features={capabilities.features}
            status={simulation.status}
            channelNames={channelNames}
          />
        </div>
      </div>

      <SimulationControls
        status={simulation.status}
        validationError={validationError}
        error={simulation.error}
        technicalDetails={simulation.technicalDetails}
        disabled={false}
        onRun={runSimulation}
      />

      <ResultsWorkspace status={simulation.status} request={lastRequest} result={simulation.result} />
    </div>
  )
}
