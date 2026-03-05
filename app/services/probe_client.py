from __future__ import annotations

import socket


def tcp_probe(host: str, port: int, payload: str) -> str:
    with socket.create_connection((host, port), timeout=2) as sock:
        sock.sendall(payload.encode())
        return sock.recv(2048).decode(errors="ignore")


def udp_probe(host: str, port: int, payload: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(payload.encode(), (host, port))
        data, _ = sock.recvfrom(2048)
        return data.decode(errors="ignore")
