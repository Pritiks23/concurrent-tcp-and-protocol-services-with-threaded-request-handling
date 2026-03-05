# Leidos Real-Time Eval Suite
<img width="2810" height="1786" alt="image" src="https://github.com/user-attachments/assets/668f6b40-5047-42af-9ad7-436304495274" />



Production-style SWE interview project focused on:
- real-time, multi-threaded systems
- low-level communications protocols (TCP/IP + UDP, with SCTP capability abstraction)
- debugging and automated test creation
- automated testing frameworks
- evaluation of AI-generated outputs for correctness, performance, safety, and bias

## Architecture
- `app/protocols/tcp_server.py`: thread-pooled TCP ACK server
- `app/protocols/udp_server.py`: threaded UDP ACK server
- `app/services/ai_evaluator.py`: scoring engine for model outputs
- `app/api/routes.py`: operational and evaluation APIs
- `frontend/index.html`: monitoring dashboard and operator controls
- `tests/`: unit + API tests

## Quick Start (Local)
```bash
cd /Users/pritikavipin/Documents/Leidos-project
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make run
```

Open [http://localhost:8000](http://localhost:8000)

## Docker Deploy
```bash
cd /Users/pritikavipin/Documents/Leidos-project
docker compose up --build
```

## Key API Endpoints
- `GET /api/health`
- `GET /api/status`
- `POST /api/services/start`
- `POST /api/services/stop`
- `POST /api/probe`
- `POST /api/ai/evaluate`
- `GET /api/telemetry`

##  Demo Script (8-10 min)
1. Start app, show dashboard status and telemetry.
2. Send TCP and UDP probes; point out ACK and packet counters.
3. Show multi-thread load probe: `python scripts/load_probe.py --requests 500 --workers 50`.
4. Run AI evaluation with safe and unsafe samples; explain scoring deltas.
5. Run tests: `pytest` and `ruff check app tests`.
6. Explain how CI enforces quality (`.github/workflows/ci.yml`).

## Notes
- SCTP is environment-dependent in userland Python. This project includes explicit runtime capability detection and clean abstraction for extension.
- Designed for readability + production-style operational controls suitable for interview walkthroughs.


-------
Leidos Real-Time Eval Suite: Beginner-Friendly Engineering Report
This project is a small but production-style platform that demonstrates how to build and operate a real-time system. It combines low-level network services (TCP and UDP), a web API, a live frontend dashboard, and an AI-output evaluator in one codebase. The main idea is: run protocol services in the background, monitor them live, test them automatically, and evaluate AI responses with clear quality rules. Even though the system is compact, it reflects real software engineering practices used in defense and enterprise teams.

The system starts in main.py. This file creates the FastAPI application, mounts the frontend, and starts/stops runtime services on app startup/shutdown. It wires together TcpServer, UdpServer, a shared telemetry buffer, and the API router. This is a strong design choice because it keeps startup behavior centralized and predictable. In simple terms: one entry point controls how everything boots and shuts down safely.

Real-time and multi-threaded behavior is implemented mainly in tcp_server.py and udp_server.py. The TcpServer class listens for many clients and uses a ThreadPoolExecutor so each connection can be handled concurrently without blocking new clients. The UdpServer class runs in its own thread and processes datagrams continuously. Both services are controlled with start/stop events and use locks for thread-safe counters. This is important because it shows safe concurrency patterns: shared state is protected, shutdown is graceful, and services remain responsive.

For low-level communications protocols, the project supports TCP/IP and UDP directly and includes SCTP capability awareness through sctp_adapter.py. SCTP is platform-dependent in many Python environments, so the project checks whether SCTP support exists rather than pretending it always does. This is a practical engineering decision: detect environment constraints, expose capability clearly, and keep the system reliable instead of fragile.

Operational visibility and debugging are handled through telemetry in telemetry.py. The TelemetryBuffer stores recent events (source, level, message, timestamp) in a thread-safe way. This data is exposed via API and shown in the frontend. For beginners, this means you can “see the system think”: when clients connect, probes run, or errors happen, you get live evidence. That makes debugging much faster than guessing from code alone.

API design is in routes.py. Endpoints cover health checks, service status, start/stop controls, protocol probing, AI evaluation, and telemetry retrieval. ProtocolManager in protocol_manager.py abstracts runtime control so route handlers stay clean. This separation of concerns is a core software engineering practice: API code handles requests, manager code handles operations, and protocol classes handle networking.

The AI evaluation capability is implemented in ai_evaluator.py, especially the evaluate_output(...) function. It scores model responses on correctness (keyword and prompt relevance), performance (latency), safety (harmful language and sensitive data), and bias markers. The output includes scores plus an issue list and a final summary (PASS or REVIEW_REQUIRED). This demonstrates a key modern SWE skill: not just generating AI output, but systematically checking if it is acceptable for real-world use.

Testing and quality automation are built in. Unit and API tests live in test_ai_evaluator.py and test_api.py. Linting and test commands are standardized in Makefile, and CI is defined in ci.yml. Deployment readiness is provided by Dockerfile and docker-compose.yml. Together, these show production-minded habits: repeatable setup, automated verification, and consistent runtime behavior across machines.
