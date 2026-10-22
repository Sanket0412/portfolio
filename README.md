# Sanket Shah Portfolio

Personal portfolio with a RAG-powered chatbot ("CloneAMA") that answers questions as
Sanket Shah using curated portfolio sources.

Production stack:

| Part | Path | Stack |
| --- | --- | --- |
| New frontend | `web/` | Next.js, TypeScript, Tailwind, Framer Motion |
| Agent API | `api/` | FastAPI, LangGraph, Claude, Supabase pgvector |

See [ARCHITECTURE.md](ARCHITECTURE.md) for how the pieces fit together.

## Run the new stack locally

```bash
# API (needs api/.env, see api/.env.example)
pip install -e ./api
python api/scripts/ingest.py        # one-off: embed content/ into pgvector
uvicorn portfolio_api.main:app --port 8000

# Frontend (needs web/.env.local, see web/.env.local.example)
cd web && npm install && npm run dev
```

Tests: `pip install -e "./api[dev]" && pytest api/tests`.

The API ships as a container (`Dockerfile`, `railway.json`; build context is the repo
root). The frontend deploys from `web/` (e.g. Vercel) with `PORTFOLIO_API_URL` set.

## Layout

```text
Portfolio/
├── web/        # Next.js frontend + BFF chat route (Vercel)
├── api/        # FastAPI + LangGraph agent, ingest/eval scripts, tests (Railway)
├── content/    # publications.json plus site assets; private RAG sources are local-only
├── scripts/    # fetch_publications.py (Crossref + OpenAlex)
├── Dockerfile / railway.json
├── README.md
└── ARCHITECTURE.md
```
