# Sanket Shah Portfolio

Personal portfolio with a RAG-powered chatbot ("CloneAMA") that answers questions as
Sanket J Shah using curated portfolio sources.

The project is mid-migration from Streamlit to a production stack:

| Part | Path | Stack |
| --- | --- | --- |
| New frontend | `web/` | Next.js, TypeScript, Tailwind, Framer Motion |
| Agent API | `api/` | FastAPI, LangGraph, Claude, Supabase pgvector |
| Original site | `Home.py`, `pages/` | Streamlit |

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

---

## Original Streamlit app

A Streamlit portfolio with Projects, Publications, Experience, and a Retrieval Augmented Generation (RAG) chatbot that answers questions as Sanket J Shah using curated portfolio sources.

## Pages

- Home: profile and navigation
- Projects: project cards and details
- Publications: publications rendered from JSON
- Experience: experience timeline and impact
- Chat: RAG-based chat interface

## RAG Chatbot

The chat experience is backed by a RAG pipeline that:
- Loads curated sources from the repository
- Chunks and embeds content
- Retrieves the most relevant context for each question
- Produces answers that must stay grounded in the retrieved context
- Applies basic guardrails like rate limiting and prompt injection blocking

## Project Structure

```text
Portfolio/
├── Home.py
├── pages/
│   ├── 1_Projects.py
│   ├── 2_Publications.py
│   ├── 3_Experience.py
│   └── 4_Chat.py
├── components/
│   ├── navbar.py
│   ├── project_cards.py
│   ├── llm/
│   │   ├── chain.py
│   │   └── rag.py
│   └── config/
│       ├── bootstrap.py
│       └── secrets.py
├── content/
│   ├── covers/
│   ├── experience/
│   ├── logos/
│   ├── profile/
│   │   ├── linkedin.pdf
│   │   └── interview_qa.json
|   |   └── summary.txt
│   ├── projects/
│   └── publications/
│       └── publications.json
├── scripts/
│   └── fetch_publications.py
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
└── requirements-dev.txt
```

Notes:
- If resume.pdf is present, it typically lives in content/profile/resume.pdf. If it is not present in the repo, remove references to it from this document.
- If additional project PDFs exist, place them in content/projects/, and the RAG loader can optionally ingest them if configured.

## Run Locally

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure secrets

Recommended: Streamlit secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Set this key in `.streamlit/secrets.toml`:
- OPENAI_API_KEY

Alternative (local only): .env in the repo root
```bash
OPENAI_API_KEY=your_key_here
```

### 3) Start the app
```bash
streamlit run Home.py
```

## Deploy

Streamlit Community Cloud:
- Connect the GitHub repo
- Add OPENAI_API_KEY in the app Secrets settings
- Do not commit `.streamlit/secrets.toml`
