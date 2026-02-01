# pages/2_Publications.py
# Renders large publication cards from content/publications/publications.json

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st

# First Streamlit call
st.set_page_config(page_title="Publications", page_icon="📄", layout="wide")

from components.navbar import render_sidebar_profile
from components.config.bootstrap import *
with st.sidebar:
    render_sidebar_profile(show_env=True)
DATA_PATH = Path("content/publications/publications.json")

@st.cache_data(ttl=86400)  # cache for 1 day
def load_publications() -> List[Dict[str, Any]]:
    if DATA_PATH.exists():
        try:
            return json.loads(DATA_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []  # fall back to empty

def author_line(authors: List[str]) -> str:
    return ", ".join(authors)

def badge(text: str):
    st.markdown(
        f"<span style='display:inline-block;padding:2px 8px;border-radius:999px;"
        f"border:1px solid #374151;background:#111827;color:#e5e7eb;font-size:12px;'>{text}</span>",
        unsafe_allow_html=True,
    )

def pub_card(pub: Dict[str, Any]):
    # Big single column card
    with st.container(border=True):
        # Cover image (uncomment if you want the hero image back)
        # img = pub.get("cover_image")
        # if img:
        #     st.markdown(
        #         f"""
        #         <div style="height:320px;overflow:hidden;border-radius:16px;border:1px solid #2a2a2a;">
        #             <img src="{img}" style="width:100%;height:100%;object-fit:cover;display:block;" />
        #         </div>
        #         """,
        #         unsafe_allow_html=True,
        #     )

        # Title
        st.markdown(f"## {pub.get('title', '')}")

        # Venue row: logo + name/publisher + citations
        cols = st.columns([0.12, 0.88])
        with cols[0]:
            vlogo = pub.get("venue_logo")
            if vlogo:
                st.image(vlogo, use_container_width=True)
        with cols[1]:
            venue = pub.get("venue_name") or ""
            publisher = pub.get("publisher") or ""
            row_bits = []
            if venue:
                row_bits.append(venue)
            if publisher and publisher not in venue:
                row_bits.append(publisher)
            row_text = " • ".join(row_bits) if row_bits else ""
            meta_cols = st.columns([0.7, 0.3])
            with meta_cols[0]:
                st.caption(row_text)
            with meta_cols[1]:
                c = pub.get("citations")
                if isinstance(c, int):
                    badge(f"Citations: {c}")

        # Authors and date
        authors = pub.get("authors") or []
        date = pub.get("date") or ""
        st.caption(author_line(authors))
        if date:
            st.caption(f"Published: {date}")

        # Abstract
        abstract = pub.get("abstract") or ""
        if abstract:
            st.markdown("**Abstract**")
            st.write(abstract.strip())

        # Actions
        st.write("")
        bcols = st.columns([0.2, 0.2, 0.6])
        with bcols[0]:
            if pub.get("url"):
                st.link_button("Read paper", pub["url"], use_container_width=True)
        with bcols[1]:
            doi = pub.get("doi")
            if doi:
                st.link_button("Cite (DOI)", f"https://doi.org/{doi}", use_container_width=True)

st.title("Publications")
st.caption("Auto populated from Crossref and OpenAlex. Cards show title, venue, authors, date, abstract, and links.")

pubs = load_publications()

# Show 2 rows, 1 column
if not pubs:
    st.info("No publications found yet. Run:  python scripts/fetch_publications.py")
else:
    for p in pubs:
        pub_card(p)
        st.write("")  # spacing between cards
