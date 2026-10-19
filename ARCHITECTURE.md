# Architecture

This portfolio is being migrated from a single Streamlit app to a Next.js frontend
backed by a FastAPI + LangGraph agent. Both exist in this repo; the Streamlit app
(`Home.py`, `pages/`) is still the original site and a comparison baseline.

## 1. High-Level Flow

```text
Visitor
  ↓
Next.js site (web/)                    Vercel
  - Home / Projects / Publications / Experience (static)
  - Chat UI: streaming text, citation chips, tool activity, suggestions
  ↓  POST /api/chat  (BFF route handler; forwards client IP)
FastAPI (api/portfolio_api)            Railway
  - rate limiting + input bounds
  - guardrails (injection blocking, secret redaction, em-dash normalization)
  - LangGraph ReAct agent (Claude, provider-configurable)
  ↓
Tools
  - retrieve_portfolio_context   hybrid pgvector search (vetted Q&A + source docs)
  - list_publications            exact venue / date / citation counts
  - lookup_github                live public-repo lookup
  - assess_job_fit               per-requirement evidence for a pasted job description
  ↓
Supabase Postgres + pgvector (embeddings: Voyage AI, 1024-dim)
```

The `/chat` endpoint streams Server-Sent Events: `token`, `tool_call`, `tool_result`,
`citations`, `final`, `suggestions`, `done`, `error`. `final` is the authoritative,
fully guardrailed answer; `token` deltas are best-effort.

## 2. Grounded Sources

The agent answers only from curated content under `content/`: a profile summary,
LinkedIn and resume PDFs, a vetted interview Q&A set, project write-ups, and
`publications.json`. If the retrieved context does not cover a question, the agent
says so instead of guessing. Ingestion is a one-off, idempotent script
(`api/scripts/ingest.py`).

## 3. Retrieval

- Documents are sanitized (control characters, prompt-injection lines, excluded
  topics), split (500/100 tokens), embedded, and upserted into pgvector.
- Retrieval is hybrid: separate searches over the vetted Q&A pool and the source
  document pool are merged so detailed material always surfaces.
- The first retrieval is seeded before the model runs, so common questions need one
  LLM call; tools remain available for compound or specialized questions.

## 4. Prompting and Answer Rules

- First person as Sanket J Shah; no invented employers, titles, dates, or metrics.
- Retrieved text is treated as data, never as instructions.
- A pasted job description triggers a structured fit assessment that states gaps
  honestly.

## 5. Guardrails

- Server-side sliding-window rate limit per client (burst and daily caps).
- Message length and history size bounds; optional shared secret between the BFF and API.
- Prompt-injection blocking, secret redaction, output length cap.
- Citation chips are hidden on refusal replies.

## 6. Tradeoffs

- Client-owned conversation history: the browser resends the transcript each turn. This
  keeps the API stateless and avoids storing anonymous transcripts.
- In-process rate limiting is sufficient for a single API instance; a shared store
  would be needed to scale out.
- Strict grounding trades some coverage for trust.

## 7. Legacy Streamlit App

`pages/4_Chat.py` with `components/llm/` is the original in-memory RAG chatbot
(OpenAI, no tools). `dev/agent_harness.py` (run locally, not part of the deployed Streamlit site) calls the new agent in-process and is
used as a development harness.
