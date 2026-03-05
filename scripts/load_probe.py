from __future__ import annotations

import argparse
import concurrent.futures
import socket
import time


def tcp_once(host: str, port: int, payload: bytes) -> bool:
    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            sock.sendall(payload)
            data = sock.recv(2048)
            return data.startswith(b"ACK:")
    except OSError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple TCP load probe")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9101)
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--workers", type=int, default=20)
    args = parser.parse_args()

    payload = b"benchmark"
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda _: tcp_once(args.host, args.port, payload), range(args.requests)))
    elapsed = time.perf_counter() - start

    ok = sum(results)
    print(f"successful={ok}/{args.requests} elapsed_s={elapsed:.3f} rps={args.requests/elapsed:.1f}")


if __name__ == "__main__":
    main()
