# pages/3_Experience.py
# Renders experience/work history timeline

import streamlit as st

# First Streamlit call
st.set_page_config(page_title="Experience", page_icon="💼", layout="wide")

from components.navbar import render_sidebar_profile

with st.sidebar:
    render_sidebar_profile(show_env=True)
# ----------------------------
# Experience data
# ----------------------------
EXPERIENCES = [
    {
        "title": "Data Scientist",
        "company": "Choreograph (WPP Media)",
        "website": "https://www.choreograph.com/",
        "location": "New York City, USA",
        "period": "March 2025 - Present",
        "description": """
**Role Overview**  
Working as a Data Scientist in WPP’s advanced analytics and media intelligence arm, focusing on large-scale audience intelligence, ML-powered decision systems, and LLM-driven analytics workflows.

**Key Responsibilities**
- Architected the **Audience Creation module** of the Audience Insights App using Python Dash, enabling audience generation across **4.5B+ demographic, financial, and transactional records**
- Designed and integrated a **text-to-SQL LLM agent** for Snowflake, reducing ad-hoc query turnaround time by **90%** and significantly improving analyst productivity
- Optimized Snowflake SQL pipelines for audience creation, feature engineering, and profiling workflows at scale
- Trained and deployed ML models to score audience propensities for global brands including **Unilever, Nestlé, Coca-Cola, and Audible**
- Delivered **Fusion-as-a-Service** pipelines that map survey data onto national populations using donor-recipient feature fusion
- Collaborated closely with product, engineering, and analytics stakeholders to productionize ML systems with real business impact

**Technologies**
- Python, SQL, Snowflake
- Machine Learning, Feature Engineering, Propensity Modeling
- LLMs, Text-to-SQL, RAG, LangChain
- Dash, FastAPI
        """,
        "tags": ["Data Science", "Machine Learning", "LLMs", "Audience Intelligence", "Production ML", "RAG", "Ads", "Text-to-SQL", "Agentic", "Propensity Modeling"],
    },
    {
        "title": "Data Scientist",
        "company": "Third Estate Ventures",
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
            st.markdown(f"## {exp.get('title', '')}")
            company = exp.get('company', '')
            website = exp.get('website') or exp.get('url')
            location = exp.get('location', '')
            company_md = f"**[{company}]({website})**" if website else f"**{company}**"
            st.markdown(f"{company_md} • {location}")
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
