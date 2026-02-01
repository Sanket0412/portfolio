# components/config/secrets.py
from __future__ import annotations

import os
from typing import Optional

import streamlit as st


def get_secret(key: str, default: str = "") -> str:
    """
    Reads secrets in a stable order:
    1) Streamlit secrets (st.secrets)
    2) Environment variables (os.getenv)
    """
    value: Optional[str] = None

    # Streamlit secrets
    try:
        if key in st.secrets:
            value = str(st.secrets.get(key, "")).strip()
    except Exception:
        value = None

    # Environment variable fallback
    if not value:
        value = (os.getenv(key) or "").strip()

    return value if value else default


def require_secret(key: str) -> str:
    value = get_secret(key, "")
    if not value:
        raise RuntimeError(
            f"{key} not found. Add it to .streamlit/secrets.toml or set it as an environment variable."
        )
    return value
