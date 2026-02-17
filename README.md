# Sanket Shah Portfolio

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
