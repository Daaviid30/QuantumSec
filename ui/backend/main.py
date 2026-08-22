"""FastAPI entry point for the QuantumSec Web UI."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ui.backend.adapters import run_bb84
from ui.backend.capabilities import get_capabilities, project_version
from ui.backend.schemas import (
    BB84SimulationRequest,
    BB84SimulationResponse,
    CapabilitiesResponse,
    HealthResponse,
)

app = FastAPI(
    title="QuantumSec UI API",
    description="Typed orchestration layer over the QuantumSec simulation engine.",
    version=project_version(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="quantumsec-ui", version=project_version())


@app.get("/api/capabilities", tags=["system"])
def capabilities() -> CapabilitiesResponse:
    return get_capabilities()


@app.post("/api/simulations/bb84", tags=["simulation"])
def simulate_bb84(request: BB84SimulationRequest) -> BB84SimulationResponse:
    try:
        return run_bb84(request)
    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_simulation_configuration",
                "message": "The simulation configuration is not valid.",
                "details": str(error),
            },
        ) from error
