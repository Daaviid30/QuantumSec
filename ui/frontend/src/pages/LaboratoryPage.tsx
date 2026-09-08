import { AlertTriangle, Beaker, LoaderCircle, Play, RotateCcw } from 'lucide-react'
import { useMemo, useRef, useState } from 'react'

import { CompositionSummary } from '../components/laboratory/CompositionSummary'
import { GuidedChannelControls } from '../components/laboratory/GuidedChannelControls'
import { ProfileSelector } from '../components/laboratory/ProfileSelector'
import { QKDControls, type LaboratoryMode } from '../components/laboratory/QKDControls'
import { StagePipelineEditor } from '../components/laboratory/StagePipelineEditor'
import { RunWorkspace } from '../components/protocol/RunWorkspace'
import { useSessionRun } from '../hooks/useSessionRun'
import { createChannelDraft, serializeChannels, validateChannels } from '../lib/channels'
import {
  DEFAULT_POSTPROCESSING,
  defaultRunRequest,
  profileIsHybrid,
  profileUsesQkd,
} from '../lib/profiles'
import type {
  CapabilitiesResponse,
  ChannelConfiguration,
  ChannelDraft,
  PublicSessionProfile,
  QKDPostprocessingRequest,
  SessionRunRequest,
  SessionRunResponse,
} from '../types/api'

interface LaboratoryPageProps {
  capabilities: CapabilitiesResponse
  preset: SessionRunRequest | null
  currentRun: SessionRunResponse | null
  onRunComplete: (run: SessionRunResponse) => void
}

function capabilityToDraft(configuration: ChannelConfiguration, capabilities: CapabilitiesResponse, id: number): ChannelDraft | null {
  const capability = [...capabilities.channels, ...capabilities.adversaries].find((item) => item.id === configuration.type)
  if (!capability) return null
  const draft = createChannelDraft(capability, id)
  for (const parameter of capability.parameters) {
    const value = configuration[parameter.key]
    if (typeof value === 'number') draft.parameters[parameter.key] = value
  }
  return draft
}

export function LaboratoryPage({ capabilities, preset, currentRun, onRunComplete }: LaboratoryPageProps) {
  const initial = preset ?? defaultRunRequest('QKD-PQC-AUTH')
  const initialStages = (initial.channels ?? [])
    .map((stage, index) => capabilityToDraft(stage, capabilities, index + 1))
    .filter((stage): stage is ChannelDraft => stage !== null)
  const [profile, setProfile] = useState<PublicSessionProfile>(initial.profile)
  const [mode, setMode] = useState<LaboratoryMode>(preset ? 'research' : 'guided')
  const [nSignals, setNSignals] = useState(initial.n_signals ?? 2048)
  const [seed, setSeed] = useState(initial.seed ?? 2026)
  const [postprocessing, setPostprocessing] = useState<QKDPostprocessingRequest>(initial.postprocessing ?? { ...DEFAULT_POSTPROCESSING })
  const [hybridAuth, setHybridAuth] = useState<Extract<PublicSessionProfile, `QKD-${string}`>>(initial.qkd_authentication_profile ?? 'QKD-PQC-AUTH')
  const [guidedNoise, setGuidedNoise] = useState('identity')
  const [noiseStrength, setNoiseStrength] = useState(0.03)
  const [eveFraction, setEveFraction] = useState(0)
  const [stages, setStages] = useState<ChannelDraft[]>(initialStages)
  const allStages = useMemo(() => [...capabilities.channels, ...capabilities.adversaries], [capabilities])
  const [selectedStage, setSelectedStage] = useState(allStages.find((item) => item.id === 'depolarizing')?.id ?? allStages[0]?.id ?? '')
  const nextStageId = useRef(initialStages.length + 1)
  const outcomeHeading = useRef<HTMLHeadingElement>(null)
  const session = useSessionRun()
  const selectedProfile = capabilities.profiles.find((item) => item.id === profile) ?? capabilities.profiles[0]
  const usesQkd = profileUsesQkd(profile)
  const maxSignals = capabilities.limits.max_signals ?? 100_000
  const maxStages = capabilities.limits.max_channels ?? 12

  const guidedChannels = useMemo<ChannelConfiguration[]>(() => {
    const configured: ChannelConfiguration[] = []
    if (guidedNoise !== 'identity') {
      const capability = capabilities.channels.find((item) => item.id === guidedNoise)
      const parameter = capability?.parameters[0]
      if (parameter) configured.push({ type: guidedNoise, [parameter.key]: noiseStrength })
    }
    if (eveFraction > 0) configured.push({ type: 'intercept_resend', intercept_fraction: eveFraction })
    return configured
  }, [capabilities.channels, eveFraction, guidedNoise, noiseStrength])

  const validationError = useMemo(() => {
    if (!selectedProfile?.implemented) return 'The selected profile is not executable.'
    if (!usesQkd) return null
    if (!Number.isInteger(nSignals) || nSignals < 1 || nSignals > maxSignals) return `Signals must be an integer between 1 and ${maxSignals.toLocaleString()}.`
    if (!Number.isInteger(seed) || seed < 0 || seed > 4_294_967_295) return 'Seed must be an integer between 0 and 4,294,967,295.'
    if (mode === 'guided' && guidedNoise !== 'identity') {
      const parameter = capabilities.channels.find((item) => item.id === guidedNoise)?.parameters[0]
      if (!parameter || !Number.isFinite(noiseStrength) || noiseStrength < parameter.minimum || noiseStrength > parameter.maximum) return 'Channel strength is outside the backend-reported range.'
    }
    if (mode === 'guided' && (!Number.isFinite(eveFraction) || eveFraction < 0 || eveFraction > 1)) return 'Eve interception fraction must lie between 0 and 1.'
    return mode === 'research' ? validateChannels(stages, allStages) : null
  }, [allStages, capabilities.channels, eveFraction, guidedNoise, maxSignals, mode, nSignals, noiseStrength, seed, selectedProfile, stages, usesQkd])

  const addStage = () => {
    const capability = allStages.find((item) => item.id === selectedStage)
    if (!capability || stages.length >= maxStages) return
    setStages((current) => [...current, createChannelDraft(capability, nextStageId.current++)])
  }
  const moveStage = (id: number, direction: -1 | 1) => setStages((current) => {
    const index = current.findIndex((stage) => stage.id === id)
    const target = index + direction
    if (index < 0 || target < 0 || target >= current.length) return current
    const reordered = [...current]
    ;[reordered[index], reordered[target]] = [reordered[target], reordered[index]]
    return reordered
  })
  const changeStageParameter = (id: number, key: string, value: number) => setStages((current) => current.map((stage) => stage.id === id ? { ...stage, parameters: { ...stage.parameters, [key]: value } } : stage))

  const execute = async () => {
    if (validationError) return
    const request: SessionRunRequest = {
      profile,
      ...(profileIsHybrid(profile) ? { qkd_authentication_profile: hybridAuth } : {}),
      ...(usesQkd ? {
        n_signals: nSignals,
        seed,
        channels: mode === 'research' ? serializeChannels(stages) : guidedChannels,
        postprocessing,
      } : {}),
    }
    const response = await session.run(request)
    if (!response) return
    onRunComplete(response)
    // Configure -> Run -> Observe: bring the real terminal outcome into view and move the reader to
    // it. Without this the result renders below the fold and the only feedback is the button label.
    requestAnimationFrame(() => {
      const heading = outcomeHeading.current
      if (!heading) return
      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
      heading.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' })
      heading.focus({ preventScroll: true })
    })
  }

  const displayedRun = session.result ?? currentRun
  const busy = session.status === 'running'

  return (
    <div className="page-stack">
      <div className="laboratory-header">
        <div><p className="section-kicker">Primary product surface</p><h2>Build a quantum-safe session</h2><p>Select a supported profile, configure only valid inputs, and inspect the public evidence emitted by the engine.</p></div>
        <div className="mode-switch" role="group" aria-label="Configuration mode">
          <button type="button" onClick={() => setMode('guided')} aria-pressed={mode === 'guided'}>Guided</button>
          <button type="button" onClick={() => setMode('research')} aria-pressed={mode === 'research'}>Research</button>
        </div>
      </div>

      <ProfileSelector profiles={capabilities.profiles} selected={profile} onSelect={setProfile} />

      <div className="builder-grid">
        <section className="surface builder-controls">
          <div className="section-heading">
            <div><p className="section-kicker">Configuration · {mode}</p><h2>Executable parameters</h2><p>{usesQkd ? 'QKD controls are mapped to the seeded simulator and ordered channel pipeline.' : 'This profile derives its cryptographic composition without arbitrary algorithm controls.'}</p></div>
            <Beaker size={18} aria-hidden="true" />
          </div>
          {profileIsHybrid(profile) ? (
            <label className="field field--standalone">
              <span>QKD classical-channel authentication</span>
              <select value={hybridAuth} onChange={(event) => setHybridAuth(event.target.value as typeof hybridAuth)}>
                <option value="QKD-ASSUMED">Assumed — not executed</option>
                <option value="QKD-CLASSICAL-AUTH">Classical / ITS — executed</option>
                <option value="QKD-PQC-AUTH">ML-DSA-65 — executed</option>
              </select>
              <small>Hybrid profiles require this policy to be chosen explicitly.</small>
            </label>
          ) : null}
          {usesQkd ? (
            <>
              <QKDControls mode={mode} nSignals={nSignals} seed={seed} maxSignals={maxSignals} postprocessing={postprocessing} onSignalsChange={setNSignals} onSeedChange={setSeed} onPostprocessingChange={setPostprocessing} />
              {mode === 'guided' ? (
                <GuidedChannelControls channels={capabilities.channels} selectedNoise={guidedNoise} noiseStrength={noiseStrength} eveFraction={eveFraction} onNoiseChange={setGuidedNoise} onNoiseStrengthChange={setNoiseStrength} onEveFractionChange={setEveFraction} />
              ) : (
                <StagePipelineEditor capabilities={allStages} stages={stages} selectedType={selectedStage} maxStages={maxStages} onSelectedTypeChange={setSelectedStage} onAdd={addStage} onRemove={(id) => setStages((current) => current.filter((stage) => stage.id !== id))} onMove={moveStage} onParameterChange={changeStageParameter} />
              )}
            </>
          ) : (
            <div className="derived-config"><strong>Profile-derived execution</strong><p>Persistent pre-provisioned ML-DSA identities and peer trust are created outside session timing. The selected profile fixes its KEM components, HKDF, and Finished exchange.</p></div>
          )}
          <div className="run-bar">
            <div>{validationError ? <><AlertTriangle size={14} /><span>{validationError}</span></> : <><span className="status-dot status-dot--ok" /><span>Configuration is valid and ready</span></>}</div>
            <button className="button button--primary" type="button" onClick={execute} disabled={busy || Boolean(validationError)}>
              {busy ? <LoaderCircle className="spin" size={16} /> : session.status === 'completed' ? <RotateCcw size={16} /> : <Play size={16} />}
              {busy ? 'Executing real profile…' : session.status === 'completed' ? 'Run again' : 'Run session'}
            </button>
          </div>
          {session.error ? <div className="error-box" role="alert"><strong>{session.error}</strong>{session.technicalDetails ? <span>{session.technicalDetails}</span> : null}</div> : null}
        </section>
        {selectedProfile ? <CompositionSummary profile={selectedProfile} qkdStages={mode === 'research' ? serializeChannels(stages) : guidedChannels} /> : null}
      </div>

      {displayedRun ? <RunWorkspace run={displayedRun} outcomeHeadingRef={outcomeHeading} /> : (
        <section className="empty-workspace"><span className="empty-workspace__mark">QS</span><p className="section-kicker">Awaiting execution</p><h2>The session trace will appear here</h2><p>No protocol events are fabricated before the backend returns a real terminal result.</p></section>
      )}
    </div>
  )
}
