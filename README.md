# Leidos Real-Time Eval Suite

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

## Interview Demo Script (8-10 min)
1. Start app, show dashboard status and telemetry.
2. Send TCP and UDP probes; point out ACK and packet counters.
3. Show multi-thread load probe: `python scripts/load_probe.py --requests 500 --workers 50`.
4. Run AI evaluation with safe and unsafe samples; explain scoring deltas.
5. Run tests: `pytest` and `ruff check app tests`.
6. Explain how CI enforces quality (`.github/workflows/ci.yml`).

## Notes
- SCTP is environment-dependent in userland Python. This project includes explicit runtime capability detection and clean abstraction for extension.
- Designed for readability + production-style operational controls suitable for interview walkthroughs.
