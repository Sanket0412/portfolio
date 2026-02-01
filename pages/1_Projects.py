import streamlit as st
from components.project_cards import render_project_grid

st.set_page_config(page_title="Projects", page_icon="🧩", layout="wide")

from components.navbar import render_sidebar_profile
from components.config.bootstrap import *
with st.sidebar:
    render_sidebar_profile(show_env=True)

# ----------------------------
# Projects data
# ----------------------------
PROJECTS = [
    {   # TODO: Add content
        "title": "Audience Creation Agent",
        "slug": "audience-creation-agent",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=1600&auto=format&fit=crop",
        "summary": "Agentic text to SQL system that generates, validates, and executes audience queries on billions of rows.",
        "description": """
**What it is**  
A multi agent text to SQL workflow that turns natural language audience definitions into executable SQL across Snowflake.  
One model generates candidate SQL, another evaluates for correctness, then an execution agent runs the query and logs lineage.

**Highlights**
- Multi LLM orchestration with evaluation
- Guardrails for schema awareness and safe execution
- Observability with prompt traces and metrics
- Supports NOT logic, nested groups, and multi dataset joins

**Impact**
- Reduced analyst turnaround time
- Scaled to billions of records, with robust caching and retries
        """,
        "tags": ["LLM", "Agentic", "Snowflake", "Text_to_SQL"],
        "links": {"Readme": "https://github.com/", "Slides": ""},
    },
    {   # TODO: Add content
        "title": "Weighted Hybrid RecSys",
        "slug": "weighted-hybrid-recsys",
        "image": "https://images.unsplash.com/photo-1534759846116-5797a4d10a6a?q=80&w=1600&auto=format&fit=crop",
        "summary": "Publication: Weighted hybrid recommendation using SVD and cosine similarity.",
        "description": """
**What it is**  
A weighted hybrid recommendation that combines matrix factorization with content similarity for better coverage and personalization.

**Highlights**
- SVD based latent factors
- Content features with cosine similarity
- Dynamic weighting strategy to mitigate cold start

**Publication**
- Springer, icSoftComp 2021
        """,
        "tags": ["Recommender", "SVD", "Cosine", "Research"],
        "links": {"Paper": "https://link.springer.com/", "Code": ""},
    },
    {   # TODO: Add content
        "title": "LLM RAG Portfolio Chat",
        "slug": "llm-rag-portfolio-chat",
        "image": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1600&auto=format&fit=crop",
        "summary": "Chat that answers as Sanket using retrieval over your portfolio content and PDFs.",
        "description": """
**What it is**  
A Streamlit chat that impersonates the portfolio owner. It retrieves from MDX writeups, PDFs, and GitHub READMEs.

**Highlights**
- OpenAI or Anthropic models
- Embeddings with local Chroma to start
- Citations to source pages
- Configurable persona and guardrails

**Future**
- Add analytics for question categories and click throughs
        """,
        "tags": ["RAG", "LLM", "Streamlit", "Chroma"],
        "links": {"Repo": "https://github.com/"},
    },
]

st.title("Projects")
st.caption("Click any card to read the full description in a modal")

# Render the grid using the reusable component
render_project_grid(
    PROJECTS,
    cols_per_row=2,       # set 1 for very large cards, 3 for denser grid
    summary_width=200,    # characters before truncation
    cover_height=240,     # image height inside cards
    radius=14,            # card image corner radius
    button_label="View details",
)