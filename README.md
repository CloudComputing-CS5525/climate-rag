# Climate Research Intelligence System

> A cloud-native RAG system that answers natural language questions about
> climate and environmental science papers using pgvector similarity search,
> knowledge graph traversal, and Gemini 2.5 Flash — deployed on AWS.

---

## Live Demo

| Service | URL |
|---|---|
| **Frontend (Streamlit)** | TBD after AWS deployment |
| **Backend API** | TBD after AWS deployment |
| **Health Check** | TBD after AWS deployment |

---

## Team

| Name | GitHub |
|---|---|
| Rohan Hashmi | @rohanhashmi2 |
| [Teammate 2] | |
| [Teammate 3] | |
| [Teammate 4] | |

---

## What It Does

You ask a natural language question like *"What are the effects of ocean
warming on precipitation patterns?"* The system searches 2,000 climate
papers using vector similarity and knowledge graph traversal, then
synthesizes a cited answer using Gemini 2.5 Flash. Every query is logged
to Postgres for monitoring via a real-time metrics dashboard.

---

## System Architecture

```mermaid
flowchart LR
    A([HuggingFace Dataset\nccdv/arxiv-summarization\nclimate filter]) --> B

    subgraph B[" data/ingestion.py — 6-Stage Pipeline "]
        direction TB
        B1[1 Load] --> B2[2 Chunk\n~80k chunks] --> B3[3 Embed\n768-dim vectors] --> B4[4 KG Extract\nCO_OCCURS edges] --> B5[5 Upload] --> B6[6 Verify]
    end

    B --> C

    subgraph C[" PostgreSQL + pgvector (AWS RDS) "]
        direction TB
        C1[raw.papers\n2,000 papers]
        C2[raw.chunks\n~80k chunks + embeddings]
        C3[graph.knowledge_edges\nCO_OCCURS relationships]
        C4[app.eval_metrics\nquery logs]
    end

    C --> D

    subgraph D[" FastAPI Backend — backend/app.py "]
        direction TB
        D1[1 pgvector cosine search]
        D2[2 KG entity lookup]
        D3[3 Gemini 2.5 Flash\nsingle cited answer]
        D1 --> D2 --> D3
    end

    D --> E

    subgraph E[" Streamlit Frontend — frontend/app.py "]
        E1[Chat Tab\ncitations + history]
        E2[Dashboard Tab\nlatency · confidence · tools]
    end

    D -->|log metrics| C
    E -.->|deployed on| F([AWS ECS Fargate\nDocker · GitHub Actions CI/CD])
    D -.->|deployed on| F
```

---

## Quickstart

> **For full step-by-step instructions see [RUN.md](RUN.md)**

### Option A — Single command (recommended)

```bash
bash reproduce.sh
```

Validates Python 3.12+, creates venv, installs dependencies, tests DB
connection, starts the FastAPI backend, runs smoke tests, and launches
the Streamlit frontend.

### Option B — Manual

```bash
# 1. Clone and set up
git clone <repo-url>
cd climate-rag
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Fill in your credentials

# 3. Create schema
# Run sql/01_create_schema.sql in pgAdmin4

# 4. Run ingestion (one-time, ~2 hours)
python3 data/ingestion.py --n 2000

# 5. Start backend
uvicorn backend.app:app --reload --port 3001

# 6. Start frontend
streamlit run frontend/app.py --server.port 3000
```

---

## Environment Variables

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password

# LLM
GEMINI_API_KEY=your_gemini_key   # https://aistudio.google.com/app/apikey

# Deployment
BACKEND_URL=http://localhost:3001  # set to AWS URL after deployment
```

---

## Dataset

**Source:** [`ccdv/arxiv-summarization`](https://huggingface.co/datasets/ccdv/arxiv-summarization) on HuggingFace  
**Domain:** Climate and environmental science arXiv papers  
**Filter:** Keyword match on abstract (climate, environment, carbon, emission, atmospheric, ocean, renewable, fossil fuel, greenhouse, temperature, precipitation, drought)  
**Size:** 2,000 papers streamed — no full dataset download required  
**Preprocessing:** LaTeX removed, URLs stripped, whitespace normalized

**Corpus statistics after ingestion:**

| Table | Rows | Description |
|---|---|---|
| raw.papers | 2,000 | Climate/environment arXiv papers |
| raw.chunks | 71,661 | Text segments (200 words, 30-word overlap) |
| graph.knowledge_nodes | 320,904 | Scientific entities (scispaCy NER) |
| graph.knowledge_edges | 5,459,043 | CO_OCCURS relationships (weight ≥ 2) |
| graph.chunk_entity_map | 3,317,667 | Chunk-to-entity links |

---

## Project Structure

```
climate-rag/
├── backend/
│   ├── app.py              # FastAPI — all API endpoints + query logic
│   ├── retrieval.py        # pgvector search + knowledge graph retrieval
│   ├── logger.py           # Structured logging with request tracing
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py              # Streamlit — chat UI + metrics dashboard
│   ├── Dockerfile
│   └── requirements.txt
├── data/
│   ├── ingestion.py        # 6-stage ingestion pipeline
│   └── config.py           # Centralized configuration
├── scripts/
│   └── db_connect.py       # Postgres connection helper
├── evaluation/
│   └── evaluate.py         # Metrics logging to app.eval_metrics
├── sql/
│   └── 01_create_schema.sql  # Full schema (raw, graph, app + pgvector)
├── tests/
│   └── smoke_test.py       # Pytest smoke tests (no DB required)
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml   # CI/CD → AWS ECS
│       └── deploy-frontend.yml
├── artifacts/              # Run summaries and frozen requirements
├── reproduce.sh            # Single-command local runner
├── RUN.md                  # Full setup guide
├── requirements.txt
├── .env.example
└── .python-version         # 3.12
```

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Backend liveness check |
| `/health/db` | GET | Postgres connectivity + table row counts |
| `/query` | POST | Run RAG query — returns answer + citations |
| `/history` | GET | Retrieve chat history |
| `/metrics` | GET | Aggregated performance stats |
| `/metrics/history` | GET | Per-query metrics for dashboard charts |
| `/papers` | GET | List all papers in corpus |

---

## Reproducibility

- **Single command:** `bash reproduce.sh` validates environment, installs deps, starts services, runs smoke tests
- **Checkpointing:** Ingestion saves Parquet checkpoints after each stage — use `--resume` to skip completed stages
- **Determinism:** Random seeds fixed (`random.seed(100)`, `np.random.seed(100)`)
- **Pinned deps:** `artifacts/requirements_frozen.txt` contains pinned packages from a working environment
- **Smoke tests:** `pytest tests/smoke_test.py` validates the backend without requiring a live DB

---

## Tech Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 17 + pgvector (AWS RDS) |
| Embeddings | sentence-transformers/all-mpnet-base-v2 (768-dim) |
| NLP / KG | scispaCy en_core_sci_sm |
| LLM | Gemini 2.5 Flash (Google GenAI) |
| Backend | FastAPI + uvicorn |
| Frontend | Streamlit |
| Deployment | AWS ECS Fargate (Docker) |
| CI/CD | GitHub Actions |