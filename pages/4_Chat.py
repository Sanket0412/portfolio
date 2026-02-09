# pages/4_Chat.py
# Simple LLM chat interface that answers questions as Sanket using fixed persona context (no RAG)

import streamlit as st
from pathlib import Path
import traceback

from components.config.bootstrap import *  # noqa: F401,F403
from components.config.secrets import require_secret, get_secret
from components.llm import profile_context
from components.navbar import render_sidebar_profile
#from components.llm.profile_context import load_profile_pdfs_context, _load_persona_context
#from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
#from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from components.llm.chain import build_rag_chain_with_history
from datetime import datetime 
import pytz
#from components.llm.chain import build_rag_chain
#User constants
PERSONA_NAME = "Sanket J Shah"
#PROFILE_PDFS_CONTEXT = load_profile_pdfs_context()
#PERSONA_SUMMARY = _load_persona_context()
# First Streamlit call
st.set_page_config(page_title="Chat with Sanket", page_icon="💬", layout="wide")

st.write("OPENAI_API_KEY available (env or secrets):", bool(get_secret("OPENAI_API_KEY")))

with st.sidebar:
    render_sidebar_profile(show_env=True)


# st.write("DEBUG: app started")

# try:
#     from components.llm.rag import load_rag_pipeline
#     st.write("DEBUG: rag imported")
# except Exception:
#     st.error("Failed importing rag")
#     st.text(traceback.format_exc())
#     raise

# try:
#     retriever = load_rag_pipeline(k=3)
#     st.write("DEBUG: retriever built", type(retriever))
# except Exception:
#     st.error("Failed building retriever")
#     st.text(traceback.format_exc())
#     raise
    
# def _load_profile_context() -> str:
#     repo_root = Path(__file__).resolve().parents[1]
#     profile_path = repo_root / "content" / "profile" / "summary.txt"
#     if profile_path.exists():
#         txt = profile_path.read_text(encoding="utf-8", errors="ignore").strip()
#         if txt:
#             return txt
#     return ""


def _build_system_prompt() -> str:
    now_et = datetime.now(pytz.timezone("America/New_York"))
    today_str = now_et.strftime("%B %d, %Y %I:%M %p %Z")

    return f"""
You are acting as {PERSONA_NAME}.

Current date/time: {today_str}

You are impersonating {PERSONA_NAME} on their personal portfolio website.
Your role is to answer questions about {PERSONA_NAME}'s career, background,
skills, experience, and projects in a professional, confident, and engaging manner,
as if speaking directly to a potential employer, client, or collaborator.

You will be provided with retrieved context from a knowledge base built using:
- {PERSONA_NAME}'s LinkedIn profile
- {PERSONA_NAME}'s resume
- A personal background summary
- Detailed project documentation from professional roles, including but not limited to:
  - WPP Media projects (Choreograph is the same as WPP Media)
  - Third Estate Ventures projects
  - CloudServe projects

Treat the retrieved context as ground truth.

Core rules:
- DO NOT GENERATE LARGE RESPONSE FOR GREETINGS
- Choreograph is the same as WPP Media, Always refer to it as "WPP Media"
- Use ONLY the information explicitly present in the retrieved context.
- Speak in the first person, as {PERSONA_NAME}.
- Do not contradict the retrieved context.
- Do not invent employers, titles, dates, metrics, degrees, universities, tools, clients, or claims.
- Do not speculate or generalize beyond what is supported by context.

If multiple retrieved sources conflict:
- Prefer the most detailed and most recent project-specific documentation.
- If the conflict cannot be resolved confidently, state the uncertainty clearly.

If a question cannot be answered using the retrieved context:
- Say so clearly and briefly.
- If appropriate, ask a short follow-up question to clarify what information is needed.

Special handling:
- Education questions: If the retrieved context does not explicitly mention a degree and dates, say that this information is not available in the current context.
- "Current" status questions: Interpret relative to the Current date/time above, but do not contradict retrieved context.
- Contact information: Suggest using the contact links available on the portfolio website or LinkedIn.

Style and safety:
- Be concise, confident, and friendly.
- Do not respond with anything irrelevant to the conversation.
- Do not reveal secrets, internal credentials, API keys, or confidential information.
- Do not use em dashes. Use commas, semicolons, or hyphens instead.

Before finalizing each response:
- Mentally verify that every factual claim is supported by the retrieved context.
- Remove or soften any statement that is not clearly grounded.
""".strip()
    # return f"""
    # You are acting as {PERSONA_NAME}. You are answering questions on {PERSONA_NAME}'s website, \
    # particularly questions related to {PERSONA_NAME}'s career, background, skills and experience. \
    # Your responsibility is to represent {PERSONA_NAME} for interactions on the website as faithfully as possible. \
    # You are given a summary of {PERSONA_NAME}'s background and LinkedIn profile which you can use to answer questions. \
    # Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
    # If you don't know the answer, say so..

    # Persona context (ground truth):
    # {PERSONA_SUMMARY}

    # Profile context (extracted text from LinkedIn and Resume PDFs):
    # {PROFILE_PDFS_CONTEXT}

    # Rules:
    # - Speak in first person as Sanket.
    # - Be concise, confident, and friendly.
    # - If you do not know something, say so and suggest what you can share instead.
    # - Do not invent employers, titles, dates, metrics, or claims not present in the persona context.
    # - If the user asks for contact, suggest they use the contact links on the portfolio or LinkedIn.
    # - Do not use em dashes in your writing. Use commas, semicolons, or hyphens.
    # """.strip()



@st.cache_resource
def _llm() -> ChatOpenAI:
    api_key = require_secret("OPENAI_API_KEY")
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4,
        api_key=api_key,
    )


# def _get_lc_history() -> list:
#     lc_messages = []
#     for m in st.session_state.get("messages", []):
#         role = m.get("role", "")
#         content = m.get("content", "")
#         if role == "user":
#             lc_messages.append(HumanMessage(content=content))
#         elif role == "assistant":
#             lc_messages.append(AIMessage(content=content))
#     return lc_messages


# def _run_chat(user_input: str) -> str:
#     llm = _llm()
#     chat_history = _get_lc_history()
#     system_prompt = _build_system_prompt()

#     rag_chain = build_rag_chain(system_prompt=system_prompt, llm=llm)

#     return rag_chain.invoke(
#         {
#             "question": user_input,
#             "chat_history": chat_history,
#         }
#     )

# RAG Chain with History
def _run_chat(user_input: str) -> str:
    llm = _llm()
    system_prompt = _build_system_prompt()

    chain = build_rag_chain_with_history(
        system_prompt=system_prompt,
        llm=llm,
        k=6,
    )

    session_id = st.session_state.get("session_id", "default")

    answer = chain.invoke(
        {"question": user_input},
        config={"configurable": {"session_id": session_id}},
    )

    return answer


# =========================
# Session state
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# Header
# =========================
st.title("💬 Chat with Sanket")
st.caption(
    "Ask me anything about my background, projects, publications, or experience. "
    "I'll answer as Sanket using a fixed persona context."
)


# =========================
# Chat UI
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about my work, projects, or experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = _run_chat(prompt).strip()
                if not answer:
                    answer = "I am not sure how to answer that. Could you ask in a different way?"
            except Exception as e:
                answer = f"Sorry, I ran into an error while responding: {type(e).__name__}: {e}"

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# =========================
# Sidebar Controls
# =========================
with st.sidebar:
    st.divider()
    st.markdown("### Chat Settings")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
