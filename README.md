# RPM Backend – Remote Patient Monitoring (IoT) Agent

Flask API: mock IoT vitals stream, threshold-based alerts, emergency workflow.  
See **[FLASK_PLAN.md](./FLASK_PLAN.md)** for architecture and API details.

## Quick start

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Runs at **http://localhost:4000**. Frontend (Vite) proxies `/api` and `/health` to this port.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness |
| GET | `/api/hello` | Hello (frontend compatibility) |
| GET | `/api/vitals/latest` | Latest vital reading |
| GET | `/api/vitals/history?limit=50` | Recent vitals for charts |
| GET | `/api/alerts` | Recent alerts |
| GET | `/api/thresholds` | Current thresholds |
| PUT | `/api/thresholds` | Update thresholds (JSON body) |
| POST | `/api/emergency/trigger` | Trigger emergency workflow (demo) |

## Tech stack

- Python 3.10+
- Flask, Flask-CORS, python-dotenv
- Mock data stream (background thread), in-memory thresholds and alerts
