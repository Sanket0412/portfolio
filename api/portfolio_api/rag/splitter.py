"""Chunk documents for embedding.

Ported from the legacy ``components/llm/rag.py``. Long documents are chunked with
a tiktoken-based splitter (1200 / 200), but curated interview Q&A items are kept
whole so retrieval returns a full vetted answer block.
Sectioned write-ups (metadata ``title`` + ``section``) get that header prepended to
every chunk so each chunk names its employer and project on its own.
"""
from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _section_header(doc: Document) -> str:
    meta = doc.metadata or {}
    title, section = meta.get("title"), meta.get("section")
    return f"{title} | {section}" if title and section else ""


def split_docs(docs: List[Document]) -> List[Document]:
    """Split long documents into chunks, keeping interview Q&A items intact."""
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=100,
    )

    split_out: List[Document] = []
    for d in docs:
        src = (d.metadata or {}).get("source", "")
        if src == "interview_qa":
            split_out.append(d)
        else:
            chunks = text_splitter.split_documents([d])
            header = _section_header(d)
            if header:
                for c in chunks:
                    c.page_content = f"{header}\n\n{c.page_content}"
            split_out.extend(chunks)
    return split_out
