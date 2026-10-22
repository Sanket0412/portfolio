from langchain_core.documents import Document

from portfolio_api.rag import loaders
from portfolio_api.rag.splitter import split_docs

SAMPLE = """# Acme Corp - Data Scientist, 2020 - 2021

## Overview
I worked at Acme.

## Projects

### Project One
- Context: At Acme, I built one.
- Impact: 10% better.

### Project Two
- Context: At Acme, I built two.
"""


def test_split_markdown_sections_skips_empty_headings():
    title, sections = loaders.split_markdown_sections(SAMPLE)
    assert title == "Acme Corp - Data Scientist, 2020 - 2021"
    assert [h for h, _ in sections] == ["Overview", "Project One", "Project Two"]


def test_experience_docs_tagged_and_not_truncated(tmp_path, monkeypatch):
    filler = "\n".join(f"- I did thing number {i} at Acme." for i in range(700))
    text = SAMPLE + "\n### Last Project\n" + filler + "\n- FINAL LINE KEPT\n"
    assert len(text) > 20000
    (tmp_path / "Acme.md").write_text(text, encoding="utf-8")
    monkeypatch.setattr(loaders, "EXPERIENCE_DIR", tmp_path)

    docs = loaders.load_experience_docs()
    assert {d.metadata["source"] for d in docs} == {"experience_acme"}
    last = [d for d in docs if d.metadata["section"] == "Last Project"][0]
    assert "FINAL LINE KEPT" in last.page_content


def test_experience_docs_drop_excluded_lines(tmp_path, monkeypatch):
    (tmp_path / "Acme.md").write_text(
        "# Acme\n\n## Overview\nKept line.\nEngaged through Robert Half.\nBuilt an NL2SQL agent.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(loaders, "EXPERIENCE_DIR", tmp_path)
    body = loaders.load_experience_docs()[0].page_content
    assert "Kept line." in body
    assert "Robert" not in body and "NL2SQL" not in body


def test_missing_experience_dir_is_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(loaders, "EXPERIENCE_DIR", tmp_path / "nope")
    assert loaders.load_experience_docs() == []


def test_split_prefixes_every_chunk_with_title_and_section():
    long_body = " ".join(f"word{i}" for i in range(1500))
    doc = Document(
        page_content=long_body,
        metadata={"source": "experience_acme", "title": "Acme - DS", "section": "Big Project"},
    )
    chunks = split_docs([doc])
    assert len(chunks) > 1
    assert all(c.page_content.startswith("Acme - DS | Big Project\n\n") for c in chunks)
