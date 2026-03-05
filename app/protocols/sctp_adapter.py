from __future__ import annotations

import socket


def sctp_supported() -> bool:
    return hasattr(socket, "IPPROTO_SCTP")


def capability_summary() -> str:
    if sctp_supported():
        return "SCTP capability detected in OS socket stack."
    return "SCTP not available in this runtime; project uses TCP/UDP services with SCTP readiness abstraction."
