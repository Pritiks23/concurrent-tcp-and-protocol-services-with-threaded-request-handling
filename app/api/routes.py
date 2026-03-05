from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import AiEvalRequest, AiEvalResult, ProbeRequest, ServiceStatus
from app.services.ai_evaluator import evaluate_output
from app.services.probe_client import tcp_probe, udp_probe


class ApiState:
    def __init__(self, protocol_manager):
        self.protocol_manager = protocol_manager


def build_router(state: ApiState) -> APIRouter:
    router = APIRouter(prefix="/api", tags=["platform"])

    @router.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @router.get("/status", response_model=ServiceStatus)
    def status() -> ServiceStatus:
        return state.protocol_manager.status()

    @router.post("/services/start", response_model=ServiceStatus)
    def start_services() -> ServiceStatus:
        state.protocol_manager.start_all()
        return state.protocol_manager.status()

    @router.post("/services/stop", response_model=ServiceStatus)
    def stop_services() -> ServiceStatus:
        state.protocol_manager.stop_all()
        return state.protocol_manager.status()

    @router.post("/probe")
    def probe(req: ProbeRequest) -> dict:
        try:
            if req.protocol == "tcp":
                data = tcp_probe(state.protocol_manager.tcp_host, state.protocol_manager.tcp_port, req.payload)
            else:
                data = udp_probe(state.protocol_manager.udp_host, state.protocol_manager.udp_port, req.payload)
            return {"response": data}
        except OSError as exc:
            raise HTTPException(status_code=502, detail=f"Probe failed: {exc}") from exc

    @router.post("/ai/evaluate", response_model=AiEvalResult)
    def evaluate(req: AiEvalRequest) -> AiEvalResult:
        result = evaluate_output(
            prompt=req.prompt,
            model_output=req.model_output,
            expected_keywords=req.expected_keywords,
            latency_ms=req.latency_ms,
            contains_sensitive_data=req.contains_sensitive_data,
        )
        return AiEvalResult(**result.__dict__)

    @router.get("/telemetry")
    def telemetry() -> dict:
        return {"events": state.protocol_manager.telemetry.snapshot()}

    return router
