from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import ApiState, build_router
from app.core.config import settings
from app.protocols.sctp_adapter import capability_summary
from app.protocols.tcp_server import TcpServer
from app.protocols.udp_server import UdpServer
from app.services.protocol_manager import ProtocolManager
from app.services.telemetry import TelemetryBuffer

telemetry = TelemetryBuffer(capacity=settings.event_buffer_size)
tcp_server = TcpServer(settings.tcp_host, settings.tcp_port, telemetry)
udp_server = UdpServer(settings.udp_host, settings.udp_port, telemetry)
manager = ProtocolManager(
    tcp=tcp_server,
    udp=udp_server,
    telemetry=telemetry,
    tcp_host=settings.tcp_host,
    tcp_port=settings.tcp_port,
    udp_host=settings.udp_host,
    udp_port=settings.udp_port,
)

app = FastAPI(title=settings.app_name)
app.include_router(build_router(ApiState(manager)))

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def home() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")


@app.on_event("startup")
def on_startup() -> None:
    telemetry.add("system", "INFO", capability_summary())
    manager.start_all()


@app.on_event("shutdown")
def on_shutdown() -> None:
    manager.stop_all()
