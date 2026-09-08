import { AlertTriangle, LoaderCircle, RefreshCw } from 'lucide-react'
import { useEffect, useState } from 'react'

import { AppShell } from '../components/layout/AppShell'
import { useCapabilities } from '../hooks/useCapabilities'
import { requestFromRecord } from '../lib/profiles'
import { ComparePage } from '../pages/ComparePage'
import { LaboratoryPage } from '../pages/LaboratoryPage'
import { OverviewPage } from '../pages/OverviewPage'
import { RunsPage } from '../pages/RunsPage'
import type { SessionRunRequest, SessionRunResponse } from '../types/api'
import { type AppView, viewFromHash } from './routes'

export function App() {
  const { capabilities, health, status, error } = useCapabilities()
  const [view, setView] = useState<AppView>(() => viewFromHash(window.location.hash))
  const [currentRun, setCurrentRun] = useState<SessionRunResponse | null>(null)
  const [runRefreshKey, setRunRefreshKey] = useState(0)
  const [preset, setPreset] = useState<SessionRunRequest | null>(null)
  const [compareIds, setCompareIds] = useState<[string, string] | null>(null)

  useEffect(() => {
    const onHashChange = () => setView(viewFromHash(window.location.hash))
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const navigate = (next: AppView) => {
    setView(next)
    window.location.hash = `/${next}`
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const rerun = (request: SessionRunRequest) => {
    setPreset(request)
    navigate('laboratory')
  }

  const openComparison = (ids: [string, string]) => {
    setCompareIds(ids)
    navigate('compare')
  }

  let content
  if (status === 'checking') {
    content = (
      <section className="connection-state" role="status">
        <LoaderCircle className="spin" size={20} aria-hidden="true" />
        <h2>Connecting to the QuantumSec engine</h2>
        <p>Discovering executable profiles and public laboratory contracts.</p>
      </section>
    )
  } else if (status === 'offline' || !capabilities) {
    content = (
      <section className="connection-state connection-state--error" role="alert">
        <AlertTriangle size={20} aria-hidden="true" />
        <h2>QuantumSec backend unavailable</h2>
        <p>{error ?? 'Start the FastAPI service and reconnect.'}</p>
        <button type="button" className="button button--secondary" onClick={() => window.location.reload()}>
          <RefreshCw size={14} aria-hidden="true" /> Retry connection
        </button>
      </section>
    )
  } else if (view === 'laboratory') {
    content = (
      <LaboratoryPage
        capabilities={capabilities}
        preset={preset}
        currentRun={currentRun}
        onRunComplete={(run) => {
          setCurrentRun(run)
          setPreset(requestFromRecord(run.record))
          setRunRefreshKey((value) => value + 1)
        }}
      />
    )
  } else if (view === 'runs') {
    content = <RunsPage refreshKey={runRefreshKey} onRerun={rerun} onCompare={openComparison} />
  } else if (view === 'compare') {
    content = <ComparePage refreshKey={runRefreshKey} initialIds={compareIds} />
  } else {
    content = <OverviewPage capabilities={capabilities} onStart={() => navigate('laboratory')} />
  }

  return (
    <AppShell
      activeView={view}
      backendStatus={status}
      version={health?.version ?? capabilities?.version}
      onNavigate={navigate}
    >
      {content}
    </AppShell>
  )
}
