# 🧠 Sanket Shah – AI-Powered Portfolio

An interactive, AI-powered personal portfolio built with Streamlit, featuring projects, publications, experience, and a RAG-based chatbot that answers questions as Sanket Shah using curated portfolio content, resume, and LinkedIn PDFs.

---

## ✨ Features

### 🧩 Projects
- Modular project cards with modal dialogs
- Rich descriptions, tags, and external links
- Easily extensible via Python dictionaries

### 📄 Publications
- Auto-rendered publication cards
- Metadata support: venue, authors, abstract, citations
- Backed by a structured JSON source

### 💼 Experience
- Timeline-style professional experience cards
- Emphasis on impact, scale, and technologies

### 💬 AI Chatbot (RAG)
- Chat interface that impersonates Sanket Shah
- Retrieval over resume, LinkedIn, and persona summary
- Chat-history aware
- Guardrails to prevent hallucinations

---
📐 **System Design & Architecture**  
See [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed breakdown of the RAG pipeline, chatbot design, and system tradeoffs.

## 🏗️ Project Structure

```
Portfolio/
├── app.py
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
│   ├── profile/
│   │   ├── linkedin.pdf
│   │   ├── resume.pdf
│   │   └── summary.txt
│   ├── publications/
│   │   └── publications.json
├── scripts/
│   └── fetch_publications.py
└── README.md
```

---

## 🚀 Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 👤 Author 
**Sanket J Shah**  
Data Scientist | ML Engineer | GenAI 
