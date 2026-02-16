# pages/3_Experience.py
# Renders experience/work history timeline

import streamlit as st
from components.theme import apply_dark_theme

# First Streamlit call
st.set_page_config(page_title="Experience", page_icon="💼", layout="wide")
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
# Experience data
# ----------------------------
EXPERIENCES = [
    {
        "title": "Data Scientist",
        "company": "WPP Media (Choreograph)",
        "logo": "https://media.licdn.com/dms/image/v2/D4E0BAQEg1Ox7FAhShg/company-logo_200_200/B4EZoBzd05GoAI-/0/1760966860672/wpp_media_logo?e=1772668800&v=beta&t=l7FUT9X3_la3oWQMM3l8LHkvzEcSzdpIw2mlX0Q_lw0",
        "website": "https://www.choreograph.com/",
        "location": "New York City, USA",
        "period": "March 2025 - Present",
        "description": """
**Role Overview**  
Working as a Data Scientist in WPP’s advanced analytics and media intelligence arm, focusing on large-scale audience intelligence, ML-powered decision systems, and LLM-driven analytics workflows.

**Key Responsibilities**
- Architected the **Audience Creation module** of the Audience Insights App using Python Dash, enabling audience generation across **4.5B+ demographic, financial, and transactional records**
- Optimized Snowflake SQL pipelines for audience creation, feature engineering, and profiling workflows at scale
- Trained and deployed ML models to score audience propensities for global brands
- Delivered **Fusion-as-a-Service** pipelines that map survey data onto national populations using donor-recipient feature fusion
- Collaborated closely with product, engineering, and analytics stakeholders to productionize ML systems with real business impact

**Technologies**
- Python, SQL, Snowflake
- Machine Learning, Feature Engineering, Propensity Modeling
- LLMs, RAG, LangChain
- Dash, FastAPI
        """,
        "tags": ["Data Science", "Machine Learning", "LLMs", "Audience Intelligence", "Production ML", "RAG", "Ads", "Text-to-SQL", "Agentic", "Propensity Modeling"],
    },
    {
        "title": "Data Scientist",
        "company": "Third Estate Ventures",
        "logo": "https://media.licdn.com/dms/image/v2/C4E0BAQGgwlNdQ7FEBA/company-logo_200_200/company-logo_200_200/0/1630601974607/thirdestateventures_logo?e=1772668800&v=beta&t=5t8FBHUcd7Ej3v1h61jGe2Qjonxf9xGHRkghDwAn7QM",
        "website": "",
        "location": "Jersey City, USA",
        "period": "January 2024 - February 2025",
        "description": """
**Role Overview**  
Led end-to-end data science and ML initiatives in the real estate and preservation domain, spanning computer vision, optimization, and LLM-based insight extraction.

**Key Responsibilities**
- Built an automated **property image annotation system** processing **10,000+ images**, improving preservation fund allocation efficiency by **20%**
- Designed and trained **CNN-based image classification models** and clustering pipelines to categorize properties by condition and architectural features
- Developed an **optimization algorithm** using linear programming to allocate a **$1M preservation fund**, maximizing impact under cost constraints
- Built **LLM-powered insight extraction pipelines** to summarize unstructured real estate documents, improving reporting quality by **35%**
- Implemented **RAG-based systems** combining structured market data with unstructured property descriptions for trend analysis
- Developed interactive dashboards and mobile interfaces to surface insights to non-technical stakeholders

**Technologies**
- Python, NumPy, SciPy
- TensorFlow, OpenCV, CNNs
- LLMs, LangChain, Hugging Face
- Flask, React.js, React Native
- PostgreSQL, Elasticsearch, AWS
        """,
        "tags": ["Data Science", "Computer Vision", "Optimization", "LLMs", "RAG"],
    },
    {
        "title": "Software Engineer",
        "company": "Cloudserve Systems",
        "logo": "https://media.licdn.com/dms/image/v2/C4E0BAQEEm3-PUGLV0Q/company-logo_200_200/company-logo_200_200/0/1630633920850?e=1772668800&v=beta&t=qaAKwoeFuziBJppVbIlHzxxaxtAnTu5lCbhQ3PWe-mk",
        "website": "https://cloudservesystems.com/home",
        "location": "India",
        "period": "May 2021 - August 2022",
        "description": """
**Role Overview**  
Worked as a Software Engineer at the intersection of ML, full-stack systems, and cloud infrastructure, contributing to healthcare AI, recommendation systems, and large-scale web platforms.

**Key Responsibilities**
- Fine-tuned **BERT-based models** for medical document summarization, reducing processing time by **80%** across large healthcare datasets
- Built **NER pipelines** to extract clinical entities from unstructured medical documents, enabling faster decision-making
- Developed a **hybrid recommendation system** (collaborative + content-based filtering) serving **50K+ users**, improving recommendation accuracy by **30%**
- Built and deployed full-stack applications using Flask, React.js, and cloud services on AWS and Azure
- Engineered data pipelines for large-scale processing and optimized backend performance
- Led website migration initiatives using modern web frameworks, cutting page load times by **50%**

**Technologies**
- Python, C++, JavaScript
- BERT, NER, Recommendation Systems
- Flask, React.js
- AWS, Azure
- SQL, Data Pipelines
        """,
        "tags": ["Software Engineering", "Machine Learning", "NLP", "Recommender Systems", "Cloud"],
    },
]

def experience_card(exp: dict):
    """Render a single experience entry as a card."""
    with st.container(border=True):
        # Header row: Title and Period
        cols = st.columns([0.7, 0.3])
        with cols[0]:
            # Title row: Logo (optional) + Role title
            logo = exp.get("logo", "")  # URL or local path
            title = exp.get("title", "")

            if logo:
                # Bigger logo and vertically centered with the title
                title_cols = st.columns([0.13, 0.87], vertical_alignment="center")
                with title_cols[0]:
                    st.image(logo, width=64)  # increase size here (60-72 is a good range)
                with title_cols[1]:
                    st.markdown(
                        f"<div style='display:flex;align-items:center;height:64px;'>"
                        f"<span style='font-size:44px;font-weight:800;line-height:1;'>{title}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(f"## {title}")

            # Company + location row (this was missing)
            company = exp.get("company", "")
            website = exp.get("website") or exp.get("url")
            location = exp.get("location", "")
            if company or location:
                company_md = f"**[{company}]({website})**" if (company and website) else (f"**{company}**" if company else "")
                sep = " • " if (company_md and location) else ""
                st.markdown(f"{company_md}{sep}{location}")

        with cols[1]:
            st.markdown(
                f"<div style='text-align:right;color:#9ca3af;margin-top:0.5rem;'>{exp.get('period', '')}</div>",
                unsafe_allow_html=True,
            )

        # Description
        description = exp.get("description", "")
        if description:
            st.markdown(description.strip())

        # Tags
        tags = exp.get("tags", [])
        if tags:
            tag_html = " ".join([
                f"<span style='display:inline-block;padding:2px 8px;border-radius:999px;"
                f"border:1px solid #374151;background:#111827;color:#e5e7eb;font-size:12px;margin:4px 4px 4px 0;'>{tag}</span>"
                for tag in tags
            ])
            st.markdown(f"<div>{tag_html}</div>", unsafe_allow_html=True)



st.title("Experience")
st.caption("Professional work history and career highlights")

if not EXPERIENCES:
    st.info("Experience entries will be displayed here.")
else:
    for exp in EXPERIENCES:
        experience_card(exp)
        st.write("")  # spacing between cards
