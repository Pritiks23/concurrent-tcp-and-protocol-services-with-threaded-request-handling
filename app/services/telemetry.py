from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from threading import Lock
from time import time


@dataclass
class TelemetryEvent:
    timestamp: float
    source: str
    level: str
    message: str


@dataclass
class TelemetryBuffer:
    capacity: int
    _events: deque[TelemetryEvent] = field(init=False)
    _lock: Lock = field(default_factory=Lock, init=False)

    def __post_init__(self) -> None:
        self._events = deque(maxlen=self.capacity)

    def add(self, source: str, level: str, message: str) -> None:
        with self._lock:
            self._events.append(
                TelemetryEvent(timestamp=time(), source=source, level=level, message=message)
            )

    def snapshot(self) -> list[dict]:
        with self._lock:
            return [
                {
                    "timestamp": e.timestamp,
                    "source": e.source,
                    "level": e.level,
                    "message": e.message,
                }
                for e in self._events
            ]
