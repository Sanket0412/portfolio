# pages/4_Chat.py
# RAG-based chat interface that answers questions as Sanket using portfolio content

import streamlit as st
import os


# First Streamlit call
st.set_page_config(page_title="Chat with Sanket", page_icon="💬", layout="wide")

from components.navbar import render_sidebar_profile

with st.sidebar:
    render_sidebar_profile(show_env=True)

# =========================
# Session state
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_initialized" not in st.session_state:
    st.session_state.agent_initialized = False

# =========================
# Header Section
# =========================
st.title("💬 Chat with Sanket")
st.caption("Ask me anything about my projects, publications, experience, or work. I'll answer using RAG over my portfolio content.")

st.info("**Note:** This is a placeholder chat interface. The agent implementation will be added later.")

# =========================
# Chat Interface
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(f"- {source}")

if prompt := st.chat_input("Ask me about my work, projects, or experience..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = (
                f"**Placeholder Response**\n\n"
                f"I received your message: \"{prompt}\"\n\n"
                f"The agent implementation will be integrated here to:\n"
                f"- Retrieve relevant content from portfolio\n"
                f"- Generate contextual responses\n"
                f"- Cite sources used in the response"
            )
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# =========================
# Sidebar Controls (Future)
# =========================
with st.sidebar:
    st.divider()
    st.markdown("### Chat Settings")

    # st.caption("Environment")
    # st.write(f"Mode: {os.getenv('APP_ENV', 'development')}")
    # st.write(f"Model: {os.getenv('MODEL_NAME', 'gpt-4o-mini')}")
    # Placeholder for model selection (uncomment when wired)
    # model_option = st.selectbox(
    #     "Model",
    #     ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet"],
    #     help="Select the LLM model for chat responses",
    # )

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent_initialized = False
        st.rerun()

    # Advanced settings placeholders
    # st.markdown("### Advanced")
    # temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    # max_tokens = st.slider("Max Tokens", 100, 4000, 2000, 100)
