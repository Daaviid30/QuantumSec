import { AlertTriangle, LoaderCircle, RefreshCw } from 'lucide-react'

import { AppShell } from '../components/layout/AppShell'
import { useCapabilities } from '../hooks/useCapabilities'
import { SimulatorPage } from '../pages/SimulatorPage'

export function App() {
  const { capabilities, health, status, error } = useCapabilities()

  return (
    <AppShell backendStatus={status} version={health?.version ?? capabilities?.version}>
      {status === 'checking' && (
        <div className="connection-state">
          <LoaderCircle className="animate-spin text-cyan-300" size={22} aria-hidden="true" />
          <h2>Connecting to the simulation engine</h2>
          <p>Discovering available protocols, channels and result features.</p>
        </div>
      )}

      {status === 'offline' && (
        <div className="connection-state connection-state--error">
          <AlertTriangle className="text-amber-300" size={22} aria-hidden="true" />
          <h2>QuantumSec backend unavailable</h2>
          <p>{error ?? 'Start the FastAPI service and reconnect.'}</p>
          <button type="button" className="secondary-button mt-4" onClick={() => window.location.reload()}>
            <RefreshCw size={14} aria-hidden="true" /> Retry connection
          </button>
        </div>
      )}

      {status === 'online' && capabilities && <SimulatorPage capabilities={capabilities} />}
    </AppShell>
  )
}
