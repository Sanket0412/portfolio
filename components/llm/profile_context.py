# components/llm/profile_context.py
from __future__ import annotations

from pathlib import Path
from typing import List, Optional
from PyPDF2 import PdfReader
import pdfplumber

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = REPO_ROOT / "content" / "profile"
PERSONA_NAME = "Sanket J Shah"

def _read_pdf_with_pdfplumber(pdf_path: Path) -> Optional[str]:
    pages: List[str] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            txt = txt.strip()
            if txt:
                pages.append(txt)

    out = "\n\n".join(pages).strip()
    return out if out else None


def _read_pdf_text(pdf_path: Path) -> str:
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text = _read_pdf_with_pdfplumber(pdf_path)
    if text:
        return text

    raise RuntimeError(
        "Could not parse PDF. Install one of these options:\n"
        "1) pip install pypdf\n"
        f"File: {pdf_path}"
    )


def load_profile_pdfs_context(
    linkedin_pdf_name: str = "linkedin.pdf",
    resume_pdf_name: str = "resume.pdf",
    max_chars_per_doc: int = 20000
) -> str:
    """
    Loads LinkedIn PDF and Resume PDF from content/profile and returns a single context string.

    Args:
      linkedin_pdf_name: file name in content/profile
      resume_pdf_name: file name in content/profile
      max_chars_per_doc: trims each extracted text block to avoid overlong prompts

    Returns:
      A formatted string suitable to include in an LLM system prompt.
    """
    linkedin_path = PROFILE_DIR / linkedin_pdf_name
    resume_path = PROFILE_DIR / resume_pdf_name

    blocks: List[str] = []

    if linkedin_path.exists():
        linkedin_text = _read_pdf_text(linkedin_path)
        blocks.append(
            "LinkedIn Profile PDF (extracted text):\n"
            + linkedin_text[:max_chars_per_doc].strip()
        )

    if resume_path.exists():
        resume_text = _read_pdf_text(resume_path)
        blocks.append(
            "Resume PDF (extracted text):\n"
            + resume_text[:max_chars_per_doc].strip()
        )

    if not blocks:
        raise FileNotFoundError(
            f"No profile PDFs found in {PROFILE_DIR}. "
            f"Expected: {linkedin_pdf_name} and or {resume_pdf_name}"
        )

    return "\n\n".join(blocks).strip()



def _load_persona_context(
    persona_summary: str = "summary.txt"
) -> str:

    persona_path = PROFILE_DIR / persona_summary

    if persona_path.exists():
        txt = persona_path.read_text(encoding="utf-8", errors="ignore").strip()
        if txt:
            return txt

    return (
        f"You are {PERSONA_NAME}, a Data Scientist and ML Engineer based in Jersey City, NJ. "
        "You work on audience profiling, recommendations, and agentic AI workflows. "
        "You have experience with Python, SQL, Snowflake, and building ML systems."
    )