from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from threading import Event, Lock, Thread

from app.services.telemetry import TelemetryBuffer


@dataclass
class TcpServer:
    host: str
    port: int
    telemetry: TelemetryBuffer
    _stop: Event = field(default_factory=Event, init=False)
    _thread: Thread | None = field(default=None, init=False)
    _socket: socket.socket | None = field(default=None, init=False)
    _executor: ThreadPoolExecutor = field(default_factory=lambda: ThreadPoolExecutor(max_workers=16), init=False)
    _active_connections: int = 0
    _lock: Lock = field(default_factory=Lock, init=False)

    @property
    def active_connections(self) -> int:
        with self._lock:
            return self._active_connections

    def _inc(self, delta: int) -> None:
        with self._lock:
            self._active_connections += delta

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = Thread(target=self._serve, name="tcp-server", daemon=True)
        self._thread.start()
        self.telemetry.add("tcp", "INFO", f"TCP server started on {self.host}:{self.port}")

    def stop(self) -> None:
        self._stop.set()
        if self._socket:
            try:
                self._socket.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=1)
        self.telemetry.add("tcp", "INFO", "TCP server stopped")

    def _serve(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(128)
        sock.settimeout(0.5)
        self._socket = sock

        while not self._stop.is_set():
            try:
                conn, addr = sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            self._executor.submit(self._handle_client, conn, addr)

    def _handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        self._inc(1)
        self.telemetry.add("tcp", "INFO", f"Accepted TCP client {addr[0]}:{addr[1]}")
        conn.settimeout(2)
        try:
            while not self._stop.is_set():
                data = conn.recv(2048)
                if not data:
                    break
                response = b"ACK:" + data
                conn.sendall(response)
                self.telemetry.add("tcp", "DEBUG", f"Processed {len(data)} bytes for {addr[0]}:{addr[1]}")
        except (OSError, TimeoutError) as exc:
            self.telemetry.add("tcp", "WARN", f"Client session ended: {exc}")
        finally:
            self._inc(-1)
            try:
                conn.close()
            except OSError:
                pass
