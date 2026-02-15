# components/llm/rag.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from typing import List, Optional
import pdfplumber
import re
import json

from langchain_core.vectorstores import InMemoryVectorStore

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = REPO_ROOT / "content" / "profile"
PERSONA_DIR = REPO_ROOT / "content" / "persona"
PROJECTS_DIR = REPO_ROOT / "content" / "projects"
PERSONA_NAME = "Sanket J Shah"

INTERVIEW_QA_DEFAULT_FILENAME = "interview_qa.json"


# =========================
# Guardrail helpers
# =========================
_INJECTION_PATTERNS = [
    r"ignore (all|any|previous) instructions",
    r"system prompt",
    r"developer message",
    r"reveal (the )?hidden",
    r"you are chatgpt",
    r"do anything now",
    r"jailbreak",
    r"bypass",
]


def _sanitize_retrieved_text(text: str, *, max_chars: int) -> str:
    """
    Sanitize retrieved text to reduce prompt injection risk while preserving facts.
    This is intentionally light-touch: removes control chars and obvious injection lines.
    """
    if not text:
        return ""

    # Normalize whitespace and remove non-printable control characters
    text = text.replace("\x00", " ")
    text = re.sub(r"[\x01-\x08\x0B-\x1F\x7F]", " ", text)
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Remove lines that look like instruction hijacks
    lines = text.splitlines()
    kept: List[str] = []
    for ln in lines:
        low = ln.strip().lower()
        if any(re.search(p, low) for p in _INJECTION_PATTERNS):
            continue
        kept.append(ln)

    out = "\n".join(kept).strip()
    return out[:max_chars]


def _read_pdf_with_pdfplumber(pdf_path: Path) -> Optional[str]:
    pages: List[str] = []
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                txt = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
                txt = txt.strip()
                if txt:
                    pages.append(txt)
    except Exception:
        return None

    out = "\n\n".join(pages).strip()
    return out if out else None


def _find_interview_qa_path(filename: str) -> Optional[Path]:
    """
    Look for interview_qa.json in common locations to be robust across repo layouts.
    Priority:
      1) content/persona/<filename>
      2) content/profile/<filename>
      3) repo root/<filename>
    """
    candidates = [
        PERSONA_DIR / filename,
        PROFILE_DIR / filename,
        REPO_ROOT / filename,
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def _load_interview_qa_docs(filename: str, *, max_chars_per_doc: int) -> List[Document]:
    """
    Load curated interview Q&A as individual Documents so retrieval can return
    a complete vetted answer rather than forcing the LLM to invent content.

    Each Q&A becomes one Document with metadata:
      - source: interview_qa
      - qa_id
      - tags
    """
    path = _find_interview_qa_path(filename)
    if not path:
        return []

    try:
        raw = path.read_text(encoding="utf-8", errors="ignore").strip()
        if not raw:
            return []
        payload = json.loads(raw)
    except Exception:
        return []

    items = payload.get("items", [])
    docs: List[Document] = []

    for it in items:
        qid = str(it.get("id", "")).strip()
        question = str(it.get("question", "")).strip()
        answer_short = str(it.get("answer_short", "")).strip()
        answer_long = str(it.get("answer_long", "")).strip()
        tags = it.get("tags", []) or []
        sources = it.get("sources", []) or []

        if not question:
            continue

        body = (
            "INTERVIEW_QA\n"
            f"QA_ID: {qid}\n"
            f"Question: {question}\n\n"
            "Vetted answer (short):\n"
            f"{answer_short}\n\n"
            "Vetted answer (long):\n"
            f"{answer_long}\n\n"
            f"Tags: {', '.join([str(t) for t in tags])}\n"
            f"Origin sources: {', '.join([str(s) for s in sources])}\n"
        )

        safe = _sanitize_retrieved_text(body, max_chars=max_chars_per_doc)
        if not safe:
            continue

        docs.append(
            Document(
                page_content=safe,
                metadata={
                    "source": "interview_qa",
                    "qa_id": qid,
                    "tags": tags,
                },
            )
        )

    return docs


def load_profile_context(
    linkedin_pdf_name: str = "linkedin.pdf",
    resume_pdf_name: str = "resume.pdf",
    persona_summary: str = "summary.txt",
    interview_qa_filename: str = INTERVIEW_QA_DEFAULT_FILENAME,
    wpp_media_projects: str = "WPP_Media_Projects.pdf",
    third_estate_ventures_projects: str = "Third_Estate_Ventures_Projects.pdf",
    cloudserve_projects: str = "Cloudserve_Projects.pdf",
    max_chars_per_doc: int = 20000,
) -> List[Document]:
    """
    Loads portfolio docs and returns Documents for retrieval.

    Includes:
    - LinkedIn PDF (content/profile)
    - Resume PDF (content/profile)
    - Persona summary (content/persona preferred, fallback to content/profile)
    - Interview Q&A JSON (content/persona preferred, fallback to content/profile)
    - Project PDFs (content/projects)
    """
    linkedin_path = PROFILE_DIR / linkedin_pdf_name
    resume_path = PROFILE_DIR / resume_pdf_name

    # Be robust: summary might be in content/persona in your repo tree
    persona_path_candidates = [
        PERSONA_DIR / persona_summary,
        PROFILE_DIR / persona_summary,
    ]

    wpp_media_projects_path = PROJECTS_DIR / wpp_media_projects
    third_estate_ventures_projects_path = PROJECTS_DIR / third_estate_ventures_projects
    cloudserve_projects_path = PROJECTS_DIR / cloudserve_projects

    docs: List[Document] = []

    # Curated interview Q&A first, so it is easy to retrieve for common interview questions
    docs.extend(_load_interview_qa_docs(interview_qa_filename, max_chars_per_doc=max_chars_per_doc))

    if linkedin_path.exists():
        linkedin_text = _read_pdf_with_pdfplumber(linkedin_path)
        if linkedin_text:
            safe = _sanitize_retrieved_text(linkedin_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "linkedin_pdf"}))

    if resume_path.exists():
        resume_text = _read_pdf_with_pdfplumber(resume_path)
        if resume_text:
            safe = _sanitize_retrieved_text(resume_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "resume_pdf"}))

    for persona_path in persona_path_candidates:
        if persona_path.exists():
            persona_text = persona_path.read_text(encoding="utf-8", errors="ignore").strip()
            if persona_text:
                safe = _sanitize_retrieved_text(persona_text, max_chars=max_chars_per_doc)
                if safe:
                    docs.append(Document(page_content=safe, metadata={"source": "persona_summary"}))
            break

    if wpp_media_projects_path.exists():
        wpp_text = _read_pdf_with_pdfplumber(wpp_media_projects_path)
        if wpp_text:
            safe = _sanitize_retrieved_text(wpp_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "wpp_media_projects"}))

    if third_estate_ventures_projects_path.exists():
        tev_text = _read_pdf_with_pdfplumber(third_estate_ventures_projects_path)
        if tev_text:
            safe = _sanitize_retrieved_text(tev_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "third_estate_ventures_projects"}))

    if cloudserve_projects_path.exists():
        cloudserve_text = _read_pdf_with_pdfplumber(cloudserve_projects_path)
        if cloudserve_text:
            safe = _sanitize_retrieved_text(cloudserve_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "cloudserve_projects"}))

    if not docs:
        raise FileNotFoundError(
            f"No usable profile docs found. "
            f"Checked: {PROFILE_DIR}, {PERSONA_DIR}, {PROJECTS_DIR}. "
            f"Expected: {linkedin_pdf_name}, {resume_pdf_name}, {persona_summary}, {interview_qa_filename}, "
            f"{wpp_media_projects}, {third_estate_ventures_projects}, {cloudserve_projects}"
        )

    return docs


def _split_docs(docs: List[Document]) -> List[Document]:
    """
    Split long documents into chunks, but keep interview Q&A items intact
    so retrieval returns a full vetted answer block.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1200,
        chunk_overlap=200,
    )

    split_out: List[Document] = []
    for d in docs:
        src = (d.metadata or {}).get("source", "")
        if src == "interview_qa":
            split_out.append(d)
        else:
            split_out.extend(text_splitter.split_documents([d]))
    return split_out


def _load_vectorstore(docs: List[Document]) -> InMemoryVectorStore:
    embeddings = OpenAIEmbeddings()
    vectorstore = InMemoryVectorStore.from_documents(docs, embedding=embeddings)
    return vectorstore


def _get_retriever(vectorstore: InMemoryVectorStore, k: int = 3):
    return vectorstore.as_retriever(search_kwargs={"k": k})


def load_rag_pipeline(k: int = 3):
    docs = load_profile_context()
    split_docs = _split_docs(docs)
    vectorstore = _load_vectorstore(split_docs)
    retriever = _get_retriever(vectorstore, k=k)
    return retriever
