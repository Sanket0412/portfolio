# 🏛️ Architecture Overview

This document explains the system architecture of the AI-powered portfolio and its RAG-based chatbot.

---

## 1. High-Level System Design

```
User
  ↓
Streamlit UI
  ↓
Chat Controller
  ↓
RAG Pipeline
  ├── Question Rewriter (History Aware)
  ├── Retriever (Vector Store)
  ├── Prompt Composer
  └── LLM
  ↓
Response
```

---

## 2. Data Sources

The chatbot retrieves information strictly from curated sources:

- Resume PDF
- LinkedIn PDF
- Persona summary text

These are treated as ground truth.

---

## 3. Retrieval Pipeline

1. PDFs are parsed using pdfplumber
2. Text is chunked with RecursiveCharacterTextSplitter
3. Embeddings generated via OpenAI
4. Stored in an in-memory vector store
5. Retrieved using semantic similarity

---

## 4. Prompting Strategy

- System prompt enforces first-person responses
- Explicit rules prevent hallucination
- Fallback responses for missing context

---

## 5. Chat History Handling

- Session-based chat history
- Question rewriting for context preservation
- Stateless UI with stateful retrieval

---

## 6. Design Tradeoffs

| Decision | Reason |
|--------|--------|
| In-memory vector store | Simplicity and speed |
| Streamlit | Rapid iteration |
| Strict prompts | Prevent false claims |

---

## 7. Future Enhancements

- Persistent vector databases
- Analytics and monitoring
- Multi-persona routing
- Feedback loops

---

## 8. Security Considerations

- API keys via Streamlit secrets
- No PII exposure beyond uploaded docs
- No hallucinated claims

---

