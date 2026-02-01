# # components/rag/chain.py
# # Build the RAG chain used by the chat page

from __future__ import annotations

from typing import List

import streamlit as st
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_classic.chains import create_history_aware_retriever
from components.llm.rag import load_rag_pipeline


def _format_docs(docs: List[Document]) -> str:
    if not docs:
        return "No relevant context found."

    blocks: List[str] = []
    for d in docs:
        src = (d.metadata or {}).get("source", "unknown source")
        text = (d.page_content or "").strip()
        if text:
            blocks.append(f"Source: {src}\n{text}")

    return "\n\n---\n\n".join(blocks).strip()


@st.cache_resource(show_spinner=False)
def _get_cached_retriever(k: int = 3):
    return load_rag_pipeline(k=k)


def _get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    key = f"lc_history::{session_id}"
    if key not in st.session_state:
        st.session_state[key] = InMemoryChatMessageHistory()
    return st.session_state[key]


def build_rag_chain_with_history(system_prompt: str, llm, k: int = 3):
    base_retriever = _get_cached_retriever(k=k)

    # This prompt rewrites the latest user question into a standalone question using chat history.
    # Important: create_history_aware_retriever expects the user input variable to be named "input".
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given the chat history and the latest user question, rewrite the question as a standalone question. "
                "Do not answer the question. Only return the standalone question.",
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=base_retriever,
        prompt=contextualize_q_prompt,
    )

    # Final answer prompt (uses retrieved context)
    answer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "Question:\n{question}\n\nRetrieved context:\n{context}"),
        ]
    )

    # base_chain expects an input dict: {"question": str, "chat_history": List[BaseMessage]}
    base_chain = (
        {
            "question": RunnableLambda(lambda x: x["question"]),
            "chat_history": RunnableLambda(lambda x: x["chat_history"]),
            "context": (
                RunnableLambda(lambda x: {"input": x["question"], "chat_history": x["chat_history"]})
                | history_aware_retriever
                | RunnableLambda(_format_docs)
            ),
        }
        | answer_prompt
        | llm
        | StrOutputParser()
    )

    chain_with_history = RunnableWithMessageHistory(
        base_chain,
        _get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )

    return chain_with_history




#OLD CODE
# from __future__ import annotations

# from typing import List, Optional, Callable, Any

# from langchain_core.documents import Document
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# # IMPORTANT:
# # Adjust this import to match your actual module path
# # If rag.py is at components/rag/rag.py, this import is correct.
# from components.llm.rag import load_rag_pipeline


# def _format_docs(docs: List[Document], max_chars: int = 12000) -> str:
#     """
#     Convert retrieved Documents into a clean text block.
#     Limits total characters to keep prompts stable.
#     """
#     if not docs:
#         return ""

#     chunks: List[str] = []
#     total = 0

#     for i, d in enumerate(docs):
#         src = d.metadata.get("source", "context")
#         text = (d.page_content or "").strip()
#         if not text:
#             continue

#         block = f"[{i + 1}] Source: {src}\n{text}"
#         if total + len(block) > max_chars:
#             remaining = max_chars - total
#             if remaining > 0:
#                 chunks.append(block[:remaining])
#             break

#         chunks.append(block)
#         total += len(block)

#     return "\n\n".join(chunks).strip()


# def _build_rag_prompt(system_prompt: str) -> ChatPromptTemplate:
#     """
#     Prompt that includes:
#     - System rules
#     - Optional chat history (LangChain messages)
#     - User question
#     - Retrieved context
#     """
#     return ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             MessagesPlaceholder(variable_name="chat_history"),
#             (
#                 "human",
#                 "Question:\n{question}\n\n"
#                 "Relevant context:\n{context}\n\n"
#                 "Answer as Sanket in first person. If context is missing, say so.",
#             ),
#         ]
#     )


# def build_rag_chain(system_prompt: str, llm: Any):
#     """
#     Returns a runnable chain that expects input:
#       {
#         "question": <str>,
#         "chat_history": <list[BaseMessage]>
#       }

#     And outputs:
#       <str>
#     """
#     retriever = load_rag_pipeline()
#     prompt = _build_rag_prompt(system_prompt)

#     rag_chain = (
#         {
#             "context": retriever | RunnableLambda(_format_docs),
#             "question": RunnablePassthrough(),
#             "chat_history": RunnablePassthrough(),
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return rag_chain
