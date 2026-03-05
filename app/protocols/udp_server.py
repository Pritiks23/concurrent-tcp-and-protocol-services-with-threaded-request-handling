from __future__ import annotations

import socket
from dataclasses import dataclass, field
from threading import Event, Lock, Thread

from app.services.telemetry import TelemetryBuffer


@dataclass
class UdpServer:
    host: str
    port: int
    telemetry: TelemetryBuffer
    _stop: Event = field(default_factory=Event, init=False)
    _thread: Thread | None = field(default=None, init=False)
    _socket: socket.socket | None = field(default=None, init=False)
    _packets: int = 0
    _lock: Lock = field(default_factory=Lock, init=False)

    @property
    def packets(self) -> int:
        with self._lock:
            return self._packets

    def _increment_packets(self) -> None:
        with self._lock:
            self._packets += 1

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = Thread(target=self._serve, name="udp-server", daemon=True)
        self._thread.start()
        self.telemetry.add("udp", "INFO", f"UDP server started on {self.host}:{self.port}")

    def stop(self) -> None:
        self._stop.set()
        if self._socket:
            try:
                self._socket.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=1)
        self.telemetry.add("udp", "INFO", "UDP server stopped")

    def _serve(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        sock.settimeout(0.5)
        self._socket = sock

        while not self._stop.is_set():
            try:
                data, addr = sock.recvfrom(2048)
            except socket.timeout:
                continue
            except OSError:
                break
            self._increment_packets()
            message = data.decode(errors="ignore")
            sock.sendto(f"ACK:{message}".encode(), addr)
            self.telemetry.add("udp", "DEBUG", f"Packet from {addr[0]}:{addr[1]} size={len(data)}")
