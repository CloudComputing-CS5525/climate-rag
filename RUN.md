# Runbook — Climate Research Intelligence System

Setup, configuration, and operational guide for running locally or on AWS.

---

## Prerequisites

| Item | Notes |
|------|--------|
| Python | 3.12 |
| PostgreSQL | Running locally (pgAdmin4 or any Postgres install) with pgvector extension |
| Google Gemini API | API key → https://aistudio.google.com/app/apikey |

---

## 1. Clone and environment

```bash
git clone <repository-url>
cd climate-rag
python3.12 -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate   # Windows
```

---

## 2. Dependencies

```bash
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

---

## 3. Configuration

```bash
cp .env.example .env
```

Edit `.env`. Required variables:

| Variable | Purpose |
|----------|---------|
| `DB_HOST` | Postgres host (e.g. `localhost` for local, RDS endpoint for AWS) |
| `DB_PORT` | Postgres port (default `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `GEMINI_API_KEY` | LLM for RAG query answering |
| `BACKEND_URL` | FastAPI base URL used by Streamlit (no trailing slash) |

---

## 4. Database schema

Open pgAdmin4, connect to your database, and run `sql/01_create_schema.sql`.

Or run via Python:

```bash
python3 -c "
from scripts.db_connect import get_conn
conn = get_conn()
cur = conn.cursor()
with open('sql/01_create_schema.sql') as f:
    cur.execute(f.read())
conn.close()
print('Schema ready.')
"
```

---

## 5. Data ingestion

> **Note:** Takes ~2 hours for 2,000 papers. Run once. Use `--resume` if interrupted.

```bash
# Full run — 2,000 climate papers
python3 data/ingestion.py --n 2000

# Resume if interrupted
python3 data/ingestion.py --n 2000 --resume

# Quick test run — 20 papers
python3 data/ingestion.py --n 20
```

Ingestion is **not** run by `reproduce.sh` — run it manually once before using the app.

---

## 6. Backend (FastAPI)

```bash
uvicorn backend.app:app --reload --port 3001
```

| Endpoint | Use |
|----------|-----|
| `GET /health` | Liveness check |
| `GET /health/db` | Postgres connectivity + table row counts |
| `POST /query` | Run RAG query |
| `GET /history` | Query history |
| `GET /metrics` | Aggregated performance stats |
| `GET /metrics/history` | Per-query metrics for dashboard |
| `GET /papers` | List all papers in corpus |

---

## 7. Frontend (Streamlit)

```bash
streamlit run frontend/app.py --server.port 3000
```

Open http://localhost:3000. Make sure `BACKEND_URL` in `.env` points at the running API.

---

## 8. Smoke tests

Requires the backend running first.

```bash
pytest tests/smoke_test.py -v
```

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| Missing env var errors | Confirm `.env` exists and all required keys are set |
| `psycopg2` connection refused | Check DB_HOST/PORT match your running Postgres instance |
| `vector` type not found | Run `CREATE EXTENSION IF NOT EXISTS vector;` in your database |
| Frontend can't reach API | Confirm backend is running and `BACKEND_URL` matches host/port |
| Gemini `429` quota error | You're hitting rate limits — wait a moment and retry |
| Slow first query | Normal — embedding model loads into memory on first request |

---

*See root `README.md` for full project overview and architecture.*