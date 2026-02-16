# components/theme.py
import streamlit as st

def apply_dark_theme(
    page_bg: str = "#000000",
    sidebar_bg: str = "#0b1220",
    sidebar_border: str = "rgba(255, 255, 255, 0.10)",
    card_bg: str = "#111827",
    input_bg: str = "#1f2937",
    button_bg: str = "#00357a",
    button_bg_hover: str = "#06408e",
    button_text: str = "#ffffff",
) -> None:
    st.markdown(
        f"""
        <style>
          /* Page backgrounds */
          html, body, [data-testid="stAppViewContainer"], .stApp {{
            background-color: {page_bg} !important;
          }}
          [data-testid="stMain"] {{
            background-color: {page_bg} !important;
          }}

          /* Sidebar */
          [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {sidebar_border} !important;
          }}
          [data-testid="stSidebar"] > div {{
            background-color: {sidebar_bg} !important;
          }}

          /* Header */
          header[data-testid="stHeader"] {{
            background: transparent !important;
          }}

          /* Reduce outer padding if desired */
          .block-container {{
            padding-top: 1.25rem !important;
            padding-bottom: 1.25rem !important;
          }}

          /* Global text */
          .stMarkdown, .stMarkdown p, .stText, label, textarea, input {{
            color: rgba(255, 255, 255, 0.92) !important;
          }}


          /* ---------- Chat message cards (optional) ---------- */
          div[data-testid="stChatMessage"] {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 10px 12px;
            margin-bottom: 10px;
          }}

          /* ---------- All Streamlit buttons (like "Read paper") ---------- */
          div.stButton > button {{
            background-color: {button_bg} !important;
            color: {button_text} !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            border-radius: 12px !important;
            padding: 0.6rem 1rem !important;
          }}
          div.stButton > button:hover {{
            background-color: {button_bg_hover} !important;
          }}

          /* If you used st.link_button anywhere */
          a[data-testid="stLinkButton"] {{
            background-color: {button_bg} !important;
            color: {button_text} !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
          }}
          a[data-testid="stLinkButton"]:hover {{
            background-color: {button_bg_hover} !important;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
