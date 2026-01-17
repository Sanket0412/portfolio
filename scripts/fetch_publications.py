# scripts/fetch_publications.py
"""
Refresh publication metadata and citation counts, then write
content/publications/publications.json

Sources
- Crossref for authoritative metadata by DOI
- OpenAlex for up-to-date citation counts

Run:
  .venv\Scripts\activate
  python scripts/fetch_publications.py
"""

from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests

# -----------------------------
# Configure your publications
# -----------------------------
# Map each paper to its DOI and preferred cover image
PUBLICATIONS_INPUT = [
    {
        "doi": "10.1109/M2VIP55626.2022.10041089",
        "cover_image": "content/covers/coin-vision.png",  # put your image here
        "publisher_logo": "content/logos/ieee.png",       # put your logo here
    },
    {
        "doi": "10.1007/978-3-031-05767-0_29",
        "cover_image": "content/covers/recsys.png",
        "publisher_logo": "content/logos/springer.png",
    },
]

OUT_PATH = Path("content/publications/publications.json")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def fetch_crossref(doi: str) -> Dict[str, Any]:
    url = f"https://api.crossref.org/works/{doi}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()["message"]


def fetch_openalex_citations(doi: str) -> Optional[int]:
    # DOI must be normalized with "https://doi.org/..." for OpenAlex lookup
    url = "https://api.openalex.org/works/https://doi.org/" + doi
    r = requests.get(url, timeout=20)
    if r.status_code != 200:
        return None
    data = r.json()
    return data.get("cited_by_count")


def first_str(x):
    if isinstance(x, list) and x:
        return x[0]
    return x


def fmt_date(msg: Dict[str, Any]) -> str:
    # Prefer published-online, fall back to issued
    for key in ["published-online", "published-print", "issued"]:
        part = msg.get(key, {})
        date_parts = part.get("date-parts") or []
        if date_parts and date_parts[0]:
            dp = date_parts[0]
            yyyy = str(dp[0])
            mm = f"{dp[1]:02d}" if len(dp) > 1 else "01"
            dd = f"{dp[2]:02d}" if len(dp) > 2 else "01"
            return f"{yyyy}-{mm}-{dd}"
    return ""


def normalize_record(doi: str, msg: Dict[str, Any], citations: Optional[int], cover_image: str, publisher_logo: str) -> Dict[str, Any]:
    title = first_str(msg.get("title", "")) or ""
    publisher = msg.get("publisher", "") or ""
    container = first_str(msg.get("container-title", "")) or ""
    url = msg.get("URL", f"https://doi.org/{doi}")
    date = fmt_date(msg)
    authors = []
    for a in msg.get("author", []) or []:
        given = a.get("given", "")
        family = a.get("family", "")
        name = (given + " " + family).strip() or a.get("name", "")
        if name:
            authors.append(name)

    rec = {
        "title": title,
        "publisher": publisher,
        "venue_name": container,
        "venue_logo": publisher_logo,
        "authors": authors,
        "date": date,
        "abstract": "",  # Crossref sometimes has 'abstract' in JATS, often empty
        "doi": doi,
        "url": url,
        "citations": citations or 0,
        "cover_image": cover_image,
    }
    return rec


def main():
    out: List[Dict[str, Any]] = []

    for item in PUBLICATIONS_INPUT:
        doi = item["doi"]
        cover = item["cover_image"]
        logo = item["publisher_logo"]
        try:
            cr = fetch_crossref(doi)
            # Be polite between requests
            time.sleep(0.3)
            cites = fetch_openalex_citations(doi)
            rec = normalize_record(doi, cr, cites, cover, logo)
            out.append(rec)
        except Exception as e:
            print(f"Failed to fetch for DOI {doi}: {e}")

    # deterministic order by date desc then title
    out.sort(key=lambda r: (r.get("date", ""), r.get("title", "")), reverse=True)

    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_PATH} with {len(out)} records.")


if __name__ == "__main__":
    main()
