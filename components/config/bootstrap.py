# components/config/bootstrap.py
from __future__ import annotations

from dotenv import load_dotenv

# Load .env for local development (safe no-op if missing)
load_dotenv()
