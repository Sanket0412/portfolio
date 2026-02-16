import streamlit as st
from components.project_cards import render_project_grid
from components.theme import apply_dark_theme

st.set_page_config(page_title="Projects", page_icon="🧩", layout="wide")
# apply_dark_theme(
#     page_bg="#000000",
#     sidebar_bg="#000724",  # pick your sidebar color here
#     input_bg="#000724",
#     button_bg="#000724",
#     button_bg_hover="#06408e"
# )
from components.navbar import render_sidebar_profile
from components.config.bootstrap import *
with st.sidebar:
    render_sidebar_profile(show_env=True)


# ----------------------------
# Projects data
# ----------------------------
PROJECTS = [
        {
        "title": "Echos: Learn and Translate ASL",
        "slug": "echos-asl",
        "image": "content/covers/ECHOS2.png",
        "summary": "Flutter + Firebase full stack app to learn ASL via interactive tutorials, with an ML module for translation.",
        "description": """
**What it is**  
Echos is a mobile application designed as one place to learn and translate ASL through interactive tutorials.

**How it works**  
- Flutter frontend for a smooth mobile UX  
- Firebase backend for auth, storage, and app data  
- Machine learning module for ASL related translation capabilities

**Highlights**  
- Full stack mobile app architecture (Flutter + Firebase)  
- Learning oriented UX built around interactive tutorials  
- ML module integrated into the product experience

**Links**  
- GitHub repo: https://github.com/Sanket0412/Echos
        """,
        "tags": ["Flutter", "Firebase", "Mobile_App", "ASL", "Machine_Learning"],
        "tech": ["Flutter", "Firebase", "Dart", "ML module"],
        "links": {
            "Repo": "https://github.com/Sanket0412/Echos",
        },
    },
    {
        "title": "Video Summarization (Key Frames + Captions)",
        "slug": "video-summarization-keyframes-captions",
        "image": "https://github.com/Sanket0412/Video-Summarization/raw/master/images/default.png",
        "summary": "Upload a video and get a compact visual summary, unique key frames, and captions generated via a TensorFlow captioning model.",
        "description": """
**What it is**  
A video summarization pipeline that takes a user uploaded video and returns a curated set of unique frames along with natural language captions for each selected frame.

**How it works**  
- Frontend (React) uploads a video and renders the returned frames + captions  
- Backend (Flask) runs the inference pipeline and serves image outputs  
- Captioning uses Beam Search by default (width 3), configurable from the frontend

**Highlights**  
- End to end flow from upload to summarized outputs  
- Key frame selection and caption generation packaged behind a simple UI  
- Clear separation of concerns between UI and model serving

**Notes**  
- The project is work in progress and relies on pretrained checkpoints for inference
        """,
        "tags": ["Computer_Vision", "Video", "TensorFlow", "Flask", "React", "Beam_Search"],
        "tech": ["TensorFlow", "Flask", "React", "OpenCV", "CNN features", "Beam Search"],
        "links": {
            "Repo": "https://github.com/Sanket0412/Video-Summarization",
        },
    },
    {   # TODO: Add content
        "title": "CloneAMA - LLM RAG Portfolio Chat",
        "slug": "llm-rag-portfolio-chat",
        "image": "content/covers/CloneAMA.png",
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
        "links": {"Repo": "https://github.com/Sanket0412/Portfolio"},
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