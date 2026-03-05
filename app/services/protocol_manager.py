from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import ServiceStatus
from app.protocols.tcp_server import TcpServer
from app.protocols.udp_server import UdpServer
from app.services.telemetry import TelemetryBuffer


@dataclass
class ProtocolManager:
    tcp: TcpServer
    udp: UdpServer
    telemetry: TelemetryBuffer
    tcp_host: str
    tcp_port: int
    udp_host: str
    udp_port: int

    def start_all(self) -> None:
        self.tcp.start()
        self.udp.start()

    def stop_all(self) -> None:
        self.tcp.stop()
        self.udp.stop()

    def status(self) -> ServiceStatus:
        tcp_running = bool(self.tcp._thread and self.tcp._thread.is_alive())
        udp_running = bool(self.udp._thread and self.udp._thread.is_alive())
        return ServiceStatus(
            tcp_running=tcp_running,
            udp_running=udp_running,
            tcp_connections=self.tcp.active_connections,
            udp_packets=self.udp.packets,
        )
