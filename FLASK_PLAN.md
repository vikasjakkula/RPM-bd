# Flask Backend Plan – Remote Patient Monitoring (RPM) IoT Agent

## Tech Stack
- **Python 3.10+**
- **Flask** – API and real-time endpoints
- **Mock IoT data stream** – in-process generator simulating device vitals
- **Flask-CORS** – allow frontend on port 3000

## Architecture

```
┌─────────────────┐     HTTP/SSE      ┌──────────────────────────────────┐
│  Frontend       │ ◄────────────────►│  Flask Backend (Port 4000)       │
│  (Vite/React)   │                   │  ├── Mock stream (background)    │
└─────────────────┘                   │  ├── Alert engine (thresholds)   │
                                      │  ├── Emergency workflow          │
                                      │  └── REST + optional SSE         │
                                      └──────────────────────────────────┘
```

## Deliverables Mapping

| # | Deliverable | Implementation |
|---|-------------|----------------|
| 1 | Remote monitoring agent | Flask app + background thread producing mock vitals; alert engine evaluates every reading |
| 2 | Real-time vitals dashboard | `GET /api/vitals/latest`, `GET /api/vitals/history`; frontend polls or uses SSE |
| 3 | Emergency alert demo | `GET /api/alerts`, `POST /api/emergency/trigger`; workflow logs and returns demo response |
| 4 | Threshold configuration | `GET /api/thresholds`, `PUT /api/thresholds`; in-memory store (or file) |

## API Design

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness check |
| GET | `/api/hello` | Compatibility with existing frontend |
| GET | `/api/vitals/latest` | Single latest vital reading |
| GET | `/api/vitals/history?limit=50` | Recent readings for charts |
| GET | `/api/alerts` | Active/recent alerts (e.g. last 30s) |
| GET | `/api/thresholds` | Current threshold config |
| PUT | `/api/thresholds` | Update thresholds (JSON body) |
| POST | `/api/emergency/trigger` | Trigger emergency workflow (demo) |

## Modules

- **`app.py`** – Create Flask app, register blueprints, start mock stream thread.
- **`config.py`** – Port, debug, CORS origins.
- **`routes/main.py`** – Health, hello.
- **`routes/vitals.py`** – Latest, history (and optional SSE).
- **`routes/alerts.py`** – List alerts.
- **`routes/thresholds.py`** – Get/put thresholds.
- **`routes/emergency.py`** – Trigger workflow.
- **`services/mock_stream.py`** – Generate vitals in a loop; push to a thread-safe buffer; optional alert evaluation per reading.
- **`services/alert_engine.py`** – Compare reading vs thresholds; return list of alerts.
- **`services/emergency_workflow.py`** – On trigger: log, optionally call webhook/side-effect, return demo payload.

## Flow

1. On startup, Flask starts a **background thread** that runs the mock stream (e.g. one reading every 2s).
2. Each new reading is appended to a **bounded buffer** (e.g. last 100 readings) and passed to the **alert engine**.
3. If any threshold is crossed, alerts are appended to an **alerts buffer** (e.g. last 20 alerts).
4. **Emergency workflow** is triggered by `POST /api/emergency/trigger` (and optionally auto-triggered when critical alert is added).
5. Frontend polls `GET /api/vitals/latest`, `GET /api/vitals/history`, `GET /api/alerts`, and uses `GET/PUT /api/thresholds` for the dashboard and threshold config.

## File Layout

```
backend/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── FLASK_PLAN.md
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── vitals.py
│   ├── alerts.py
│   ├── thresholds.py
│   └── emergency.py
└── services/
    ├── __init__.py
    ├── mock_stream.py
    ├── alert_engine.py
    └── emergency_workflow.py
```

## Running

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
# or: flask run --port 4000
```

Server: `http://localhost:4000`. Frontend proxy to `/api` and `/health` remains unchanged.
