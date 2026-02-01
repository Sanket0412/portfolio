import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from typing import List, Optional
import pdfplumber

#Changes
from langchain_core.vectorstores import InMemoryVectorStore

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = REPO_ROOT / "content" / "profile"
PERSONA_NAME = "Sanket J Shah"

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
        # If pdfplumber fails for any reason, return None so caller can skip it safely
        return None

    out = "\n\n".join(pages).strip()
    return out if out else None

def load_profile_context(
    linkedin_pdf_name: str = "linkedin.pdf",
    resume_pdf_name: str = "resume.pdf",
    persona_summary: str = "summary.txt",
    max_chars_per_doc: int = 20000
) -> List[Document]:
    """
    Loads LinkedIn PDF and Resume PDF from content/profile and returns docs.
    """
    linkedin_path = PROFILE_DIR / linkedin_pdf_name
    resume_path = PROFILE_DIR / resume_pdf_name
    persona_path = PROFILE_DIR / persona_summary

    docs: List[Document] = []

    if linkedin_path.exists():
        linkedin_text = _read_pdf_with_pdfplumber(linkedin_path)
        if linkedin_text:
            docs.append(
                Document(
                    page_content=linkedin_text[:max_chars_per_doc],
                    metadata={"source": "linkedin_pdf"},
                )
            )

    if resume_path.exists():
        resume_text = _read_pdf_with_pdfplumber(resume_path)
        if resume_text:
            docs.append(
                Document(
                    page_content=resume_text[:max_chars_per_doc],
                    metadata={"source": "resume_pdf"},
                )
            )

    if persona_path.exists():
        persona_txt = persona_path.read_text(encoding="utf-8", errors="ignore").strip()
        if persona_txt:
            docs.append(
                Document(
                    page_content=persona_txt[:max_chars_per_doc],
                    metadata={"source": "persona_summary"},
                )
            )

    if not docs:
        raise FileNotFoundError(
            f"No usable profile docs found in {PROFILE_DIR}. "
            f"Expected one of: {linkedin_pdf_name}, {resume_pdf_name}, {persona_summary}"
        )

    return docs


def _split_docs(docs: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=350,
        chunk_overlap=60
    )
    return text_splitter.split_documents(docs)


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