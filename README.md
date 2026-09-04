## GovroPK – Pakistan Citizen Services Assistant

Production-ready, multi-agent AI platform that helps Pakistani citizens get accurate,
up-to-date information on government services (passport, NADRA, driving license,
taxes, scholarships, health, legal aid, utility complaints) by retrieving answers
from official sources via RAG + web search, instead of relying purely on LLM memory.

## Stack
FastAPI · LangChain · LangGraph · MCP (server + client) · OpenAI · Tavily · ChromaDB ·
PostgreSQL · BeautifulSoup + Playwright · LangSmith · React + TypeScript · Docker.

## Quick start

By default this project uses **Groq** (free tier) for chat/reasoning and **FastEmbed**
(a lightweight, ONNX-based, no-API-key embedding library — no torch/CUDA download
required) for RAG embeddings — so you can run the whole thing without any paid API.

The configured chat model is Groq-hosted `openai/gpt-oss-120b`. Keep
`LLM_PROVIDER=groq`; the `openai/` prefix is part of the model identifier and does
not mean that the OpenAI provider should be selected.

```bash
cp .env.example .env
```

Then edit `.env` and set at minimum:
```
GROQ_API_KEY=gsk-your-key       # free at https://console.groq.com/keys
TAVILY_API_KEY=tvly-your-key    # free tier at https://tavily.com
JWT_SECRET_KEY=<a random 32+ byte hex string>
```

`LANGCHAIN_API_KEY` (LangSmith tracing) is optional — leave `LANGCHAIN_TRACING_V2=false`
if you don't want to set it up.

To use OpenAI instead of Groq, set `LLM_PROVIDER=openai`, `OPENAI_API_KEY=...`, and
optionally `EMBEDDING_PROVIDER=openai` if you also want OpenAI embeddings instead of
the local model.

```bash
docker compose up --build
```

### System requirements
- **At least 10 GB free disk space** before building (much less than before —
  the backend no longer needs a torch/CUDA-capable environment at all).
- All Python dependencies in `backend/requirements.txt` are **exactly pinned**
  to a resolver-verified, mutually compatible set (no `==` conflicts, no slow
  pip backtracking) — resolves in ~15 seconds.
- **Local embeddings use [FastEmbed](https://github.com/qdrant/fastembed)**
  (ONNX Runtime), not `sentence-transformers`/PyTorch. This avoids the ~190MB
  torch download entirely, which was previously the most common cause of
  build timeouts on slow/unstable connections.
- The Dockerfile sets generous pip timeouts/retries (`PIP_DEFAULT_TIMEOUT=600`,
  `--retries 10`) and retries the Playwright Chromium install automatically,
  so a single slow moment on your connection won't fail the whole build.

### If you still hit timeouts on a very slow/unstable connection
`backend` and `mcp-server` share this Dockerfile and both need the same
dependencies. Docker Compose builds services **in parallel** by default, so
on a slow connection both can end up downloading at once and compete for
bandwidth. Force sequential builds instead — the second image will reuse the
first's cached layers almost instantly:

```bash
# PowerShell
$env:COMPOSE_PARALLEL_LIMIT=1
docker compose build
docker compose up -d
```
```bash
# macOS/Linux
COMPOSE_PARALLEL_LIMIT=1 docker compose build
docker compose up -d
```

- Backend API: http://localhost:8000/docs
- Frontend:    http://localhost:5173
- ChromaDB:    http://localhost:8001
- Postgres:    localhost:5432

### Render deployment

Set these environment variables on the backend service:

```
CORS_ORIGINS=https://govro-pk-4ipj-git-main-abeera-amir-s-projects.vercel.app
```

Use the exact frontend origin, without a trailing slash. Also set the frontend
build variable to the deployed API URL, for example:

```
VITE_API_BASE_URL=https://govropk.onrender.com/api
```

Seed Qdrant with the included scraped government content:

```bash
docker compose exec backend python scripts/run_scraper.py
docker compose exec backend python scripts/ingest_to_qdrant.py
```

## Architecture

```
frontend (React/TS)  ->  FastAPI (JWT auth, REST)  ->  LangGraph multi-agent graph
                                                          |-- Supervisor
                                                          |-- Router
                                                          |-- Retrieval Agent (RAG via ChromaDB)
                                                          |-- Clarification Agent (human-in-the-loop)
                                                          |-- Citation Agent
                                                          |-- Fallback Agent (Tavily web search)
                                             MCP Server exposes: web_search, gov_lookup, rag_search tools
                                             Scraper pipeline (Playwright + BS4) -> Chroma ingestion
```
