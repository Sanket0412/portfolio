"""
Streamlit app for the portfolio website.
"""
import os
from dotenv import load_dotenv
import streamlit as st
from components.navbar import render_sidebar_profile


# 1) First Streamlit call on the page
st.set_page_config(
    page_title="Sanket Shah's Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    render_sidebar_profile(show_env=True)
# Load environment variables
load_dotenv()

def get_env(key: str, default: str | None = None) -> str | None:
    """Get an environment variable with a default value."""
    # SAFE: secrets access only after set_page_config
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)

APP_ENV = get_env("APP_ENV", "development")
MODEL_NAME = get_env("MODEL_NAME", "gpt-4o-mini")

# ===============================
# Sidebar (default navigation + extras)
# ===============================
# Do NOT hide default nav. This block simply adds extra info below it.
#with st.sidebar:
    # st.divider()
    # st.caption("Environment")
    # st.write(f"Mode: {APP_ENV}")
    # st.write(f"Model: {MODEL_NAME}")

# =========================
# Hero section
# =========================


col1, col2 = st.columns([2, 1])
with col1:
    st.title("Hi, I am Sanket J Shah")
    st.subheader("Data Scientist, MLE and a Gen AI expert")
    st.markdown(
        """
I build end to end data and ML systems that power personalization, audience insights, and agentic AI workflows.
This site showcases selected projects, publications, and a live chat that answers questions as me, backed by retrieval over my work.
        """
    )
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.page_link("pages/1_Projects.py", label="View Projects", icon="🧩")
    with c2:
        st.page_link("pages/4_Chat.py", label="Chat with Sanket", icon="💬")
    with c3:
        st.page_link("pages/2_Publications.py", label="Publications", icon="📄")
    with c4:
        st.page_link("pages/3_Experience.py", label="Experience", icon="💼")

with col2:
    st.markdown("### Education")

    with st.container(border=True):
        st.markdown("**Master of Science in Computer Science**")
        st.caption("Stevens Institute of Technology, Hoboken, NJ")
        st.write("Graduated: January 2024")
        #st.write("Coursework: Machine Learning, Deep Learning, Big Data, Applied AI")

    st.write("")

    with st.container(border=True):
        st.markdown("**B.Tech, Information and Communication Technology**")
        st.caption("Ahmedabad University, India")
        st.write("Graduated: May 2022")
        #st.write("Coursework: Data Structures and Algorithms, Database Management Systems, Operating Systems, Software Engineering, Human Computer Interaction, Cloud Computing")


st.divider()

# =========================
# Highlights section
# =========================
st.markdown("### Highlights")
hcol1, hcol2, hcol3 = st.columns(3)
with hcol1:
    st.markdown("**Audience Creation Agent**")
    st.caption("Agentic text to SQL. Multi LLM evaluation and execution.")
    st.page_link("pages/1_Projects.py", label="Open", icon="➡️")
with hcol2:
    st.markdown("**Weighted Hybrid RecSys**")
    st.caption("SVD plus cosine similarity. Publication in Springer.")
    st.page_link("pages/2_Publications.py", label="Open", icon="➡️")
with hcol3:
    st.markdown("**LLM RAG Portfolio Chat**")
    st.caption("Chat that answers as Sanket using RAG over this site.")
    st.page_link("pages/4_Chat.py", label="Try it", icon="➡️")

#st.divider()

# =========================
# Diagnostics block (dev only)
# =========================
# if (APP_ENV or "").lower() in {"dev", "development"}:
#     with st.expander("Developer diagnostics"):
#         st.write("Loaded configuration:")
#         st.json(
#             {
#                 "APP_ENV": APP_ENV,
#                 "MODEL_NAME": MODEL_NAME,
#                 "OPENAI_API_KEY set": bool(get_env("OPENAI_API_KEY")),
#                 "ANTHROPIC_API_KEY set": bool(get_env("ANTHROPIC_API_KEY")),
#             }
#         )
#         if not get_env("OPENAI_API_KEY") and not get_env("ANTHROPIC_API_KEY"):
#             st.warning(
#                 "No LLM provider key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env for local or in Streamlit secrets when deployed."
#             )

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("© 2025 Sanket J Shah • Built with Streamlit.")
