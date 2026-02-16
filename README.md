# Sanket Shah - AI-Powered Portfolio

An interactive portfolio built with Streamlit, featuring Projects, Publications, Experience, and a RAG-based chatbot (CloneAMA) that answers questions in my voice using only curated portfolio sources.

## Features

### Projects
- Modular project cards with rich descriptions, tags, and external links
- Easy to extend by editing the Projects page content

### Publications
- Auto-rendered publication cards
- Structured JSON-backed metadata (venue, authors, abstract, citations)

### Experience
- Timeline-style experience cards
- Focus on impact, scale, and technologies

### AI Chatbot (RAG) - CloneAMA
- Chat interface that answers as Sanket J Shah
- Retrieval over curated documents (resume, LinkedIn, project PDFs, persona summary)
- History-aware question rewriting to reduce drift
- Guardrails to reduce hallucinations and block prompt injection attempts

## System Design and Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the end-to-end RAG pipeline, prompting strategy, security notes, and tradeoffs.

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
│   ├── theme.py
│   ├── llm/
│   │   ├── chain.py
│   │   └── rag.py
│   └── config/
│       ├── bootstrap.py
│       └── secrets.py
├── content/
│   ├── profile/
│   │   ├── linkedin.pdf
│   │   ├── resume.pdf
│   │   └── summary.txt
│   ├── persona/
│   │   └── interview_qa.json (optional)
│   ├── projects/
│   │   ├── WPP_Media_Projects.pdf (optional but supported)
│   │   ├── Third_Estate_Ventures_Projects.pdf (optional but supported)
│   │   └── Cloudserve_Projects.pdf (optional but supported)
│   └── publications/
│       └── publications.json
├── scripts/
│   └── fetch_publications.py
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
└── requirements-dev.txt
```

## Running Locally

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Set API keys

Option A: Streamlit secrets (recommended)

1. Copy the example secrets file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. Edit `.streamlit/secrets.toml` and set:
- OPENAI_API_KEY

Option B: .env (works locally)
Create a `.env` in the repo root and set:
```bash
OPENAI_API_KEY=your_key_here
```

### 3) Run the app
```bash
streamlit run Home.py
```

## Deployment (Streamlit Community Cloud)

- Deploy the repo on Streamlit Community Cloud.
- Add OPENAI_API_KEY under App Settings -> Secrets.
- Do not commit `.streamlit/secrets.toml`.

## Author

Sanket J Shah  
Data Scientist | ML Engineer | GenAI
