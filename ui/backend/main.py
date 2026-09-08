"""FastAPI entry point for the QuantumSec Web UI."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ui.backend.adapters import run_bb84
from ui.backend.capabilities import get_capabilities, project_version
from ui.backend.laboratory import WebLaboratoryService
from ui.backend.schemas import (
    BB84SimulationRequest,
    BB84SimulationResponse,
    CapabilitiesResponse,
    CompareRequest,
    CompareResponse,
    HealthResponse,
    ProtectedMessageRequest,
    ProtectedMessageResponse,
    RunListResponse,
    SessionRunRequest,
    SessionRunResponse,
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

laboratory = WebLaboratoryService()


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


@app.post("/api/sessions", tags=["laboratory"])
def run_session(request: SessionRunRequest) -> SessionRunResponse:
    try:
        return laboratory.run(request)
    except (TypeError, ValueError) as error:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_session_configuration",
                "message": "The session configuration is not valid.",
                "details": str(error),
            },
        ) from error
    except (OSError, RuntimeError) as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "session_execution_unavailable",
                "message": "The selected profile could not be executed in this environment.",
                "details": str(error),
            },
        ) from error


@app.get("/api/runs", tags=["laboratory"])
def list_runs() -> RunListResponse:
    return laboratory.list_runs()


@app.get("/api/runs/{run_id}", tags=["laboratory"])
def get_run(run_id: str) -> SessionRunResponse:
    try:
        return laboratory.get_run(run_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.post("/api/compare", tags=["laboratory"])
def compare_runs(request: CompareRequest) -> CompareResponse:
    try:
        return laboratory.compare(request.run_ids[0], request.run_ids[1])
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.post("/api/runs/{run_id}/protect", tags=["data-plane"])
def protect_message(
    run_id: str,
    request: ProtectedMessageRequest,
) -> ProtectedMessageResponse:
    try:
        return laboratory.protect(run_id, request)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "data_plane_unavailable",
                "message": "Protected messaging is unavailable for this run.",
                "details": str(error),
            },
        ) from error
