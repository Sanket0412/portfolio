"""Load portfolio source documents for retrieval.

Ported from the legacy ``components/llm/rag.py``. Builds a list of
``Document`` objects (each tagged with a ``source`` in metadata) from:
  - curated interview Q&A JSON (one Document per item, kept whole)
  - LinkedIn PDF, resume PDF
  - personal background summary
  - experience write-ups (content/experience/*.md), one Document per section
  - personal project write-ups (content/projects/*.md)

Content directories are resolved from ``REPO_ROOT`` in :mod:`portfolio_api.config`.

Two fixes carried over from the legacy code:
  - the resume filename now defaults to the real file (``Sanket_Shah_Resume.pdf``),
    so the resume is actually ingested.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import pdfplumber
from langchain_core.documents import Document

from portfolio_api.config import REPO_ROOT
from portfolio_api.rag.sanitize import sanitize_retrieved_text

PROFILE_DIR = REPO_ROOT / "content" / "profile"
PERSONA_DIR = REPO_ROOT / "content" / "persona"
PROJECTS_DIR = REPO_ROOT / "content" / "projects"
EXPERIENCE_DIR = REPO_ROOT / "content" / "experience"

# Markdown write-ups are curated and sectioned, so they get a much higher cap
# than PDFs (the cap only guards against runaway input, it is not a chunker).
MD_MAX_CHARS = 60_000

INTERVIEW_QA_DEFAULT_FILENAME = "interview_qa.json"


def read_pdf(pdf_path: Path) -> Optional[str]:
    """Extract text from a PDF with pdfplumber, or None if it yields nothing."""
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
    """Locate interview_qa.json across the common repo layouts.

    Priority: content/persona/ -> content/profile/ -> repo root.
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


def load_interview_qa_docs(filename: str, *, max_chars_per_doc: int) -> List[Document]:
    """Load curated interview Q&A as individual Documents.

    Each Q&A becomes one Document (tagged ``interview_qa``) so retrieval can
    return a complete vetted answer rather than forcing the LLM to invent one.
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

        safe = sanitize_retrieved_text(body, max_chars=max_chars_per_doc)
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


def split_markdown_sections(text: str) -> tuple[str, List[tuple[str, str]]]:
    """Split a write-up into ``(title, [(heading, body), ...])``.

    ``title`` is the first ``# `` line. A new section starts at every ``## `` or
    ``### `` heading; headings with an empty body (e.g. a bare "## Projects") are skipped.
    """
    title = ""
    sections: List[tuple[str, str]] = []
    heading: Optional[str] = None
    body: List[str] = []

    def flush() -> None:
        if heading is not None and "\n".join(body).strip():
            sections.append((heading, "\n".join(body).strip()))

    for ln in text.splitlines():
        if ln.startswith("# ") and not title:
            title = ln[2:].strip()
        elif ln.startswith("## ") or ln.startswith("### "):
            flush()
            heading = ln.lstrip("#").strip()
            body = []
        elif heading is not None:
            body.append(ln)
    flush()
    return title, sections


def load_experience_docs(max_chars_per_doc: int = MD_MAX_CHARS) -> List[Document]:
    """One Document per section of each ``content/experience/*.md`` write-up.

    Tagged ``experience_<filename stem>`` with ``title`` and ``section`` metadata; the
    splitter prefixes every chunk with that title and section so it stands alone.
    """
    docs: List[Document] = []
    if not EXPERIENCE_DIR.exists():
        return docs
    for md_path in sorted(EXPERIENCE_DIR.glob("*.md")):
        text = md_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue
        title, sections = split_markdown_sections(text)
        source = f"experience_{md_path.stem.lower()}"
        for heading, body in sections:
            safe = sanitize_retrieved_text(body, max_chars=max_chars_per_doc)
            if safe:
                docs.append(
                    Document(
                        page_content=safe,
                        metadata={"source": source, "title": title, "section": heading},
                    )
                )
    return docs


def load_profile_context(
    linkedin_pdf_name: str = "linkedin.pdf",
    resume_pdf_name: str = "Sanket_Shah_Resume.pdf",
    persona_summary: str = "summary.txt",
    interview_qa_filename: str = INTERVIEW_QA_DEFAULT_FILENAME,
    max_chars_per_doc: int = 20000,
) -> List[Document]:
    """Load portfolio docs and return Documents for retrieval.

    Includes interview Q&A, LinkedIn + resume PDFs, the persona summary, the
    experience write-ups (per section) and personal-project Markdown. Raises
    FileNotFoundError if nothing usable is found.
    """
    linkedin_path = PROFILE_DIR / linkedin_pdf_name
    resume_path = PROFILE_DIR / resume_pdf_name

    # Be robust: summary might be in content/persona in some repo trees
    persona_path_candidates = [
        PERSONA_DIR / persona_summary,
        PROFILE_DIR / persona_summary,
    ]

    docs: List[Document] = []

    # Curated interview Q&A first, so it is easy to retrieve for common interview questions
    docs.extend(
        load_interview_qa_docs(interview_qa_filename, max_chars_per_doc=max_chars_per_doc)
    )

    if linkedin_path.exists():
        linkedin_text = read_pdf(linkedin_path)
        if linkedin_text:
            safe = sanitize_retrieved_text(linkedin_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "linkedin_pdf"}))

    if resume_path.exists():
        resume_text = read_pdf(resume_path)
        if resume_text:
            safe = sanitize_retrieved_text(resume_text, max_chars=max_chars_per_doc)
            if safe:
                docs.append(Document(page_content=safe, metadata={"source": "resume_pdf"}))

    for persona_path in persona_path_candidates:
        if persona_path.exists():
            persona_text = persona_path.read_text(encoding="utf-8", errors="ignore").strip()
            if persona_text:
                safe = sanitize_retrieved_text(persona_text, max_chars=max_chars_per_doc)
                if safe:
                    docs.append(
                        Document(page_content=safe, metadata={"source": "persona_summary"})
                    )
            break

    # Experience write-ups (employer work), split per project section.
    docs.extend(load_experience_docs())

    # Markdown project docs (personal projects only). Any .md in content/projects/ is
    # ingested and tagged by its filename stem, lowercased
    # (TodaySponsor.md -> "todaysponsor"). Drop a new .md here and re-ingest to make
    # the agent aware of another project.
    for md_path in sorted(PROJECTS_DIR.glob("*.md")):
        md_text = md_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not md_text:
            continue
        safe = sanitize_retrieved_text(md_text, max_chars=MD_MAX_CHARS)
        if safe:
            docs.append(
                Document(page_content=safe, metadata={"source": md_path.stem.lower()})
            )

    if not docs:
        raise FileNotFoundError(
            "No usable profile docs found. "
            f"Checked: {PROFILE_DIR}, {PERSONA_DIR}, {EXPERIENCE_DIR}, {PROJECTS_DIR}. "
            f"Expected: {linkedin_pdf_name}, {resume_pdf_name}, {persona_summary}, "
            f"{interview_qa_filename}, experience/*.md"
        )

    return docs
