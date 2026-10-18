"""Centralized configuration loaded from environment / api/.env.

Secrets are never hardcoded. Populate `api/.env` (gitignored) from `.env.example`.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# api/ directory (parent of this package). api/.env lives here.
API_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = API_ROOT.parent

# Load api/.env if present (does not override already-set process env vars).
load_dotenv(API_ROOT / ".env", override=False)


def _split_csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


@dataclass(frozen=True)
class Settings:
    # Environment
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "development"))

    # LLM provider selection + keys
    llm_provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai").lower())
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    anthropic_model: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
    )
    llm_temperature: float = field(
        default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.4"))
    )

    # Embeddings: "voyage" (default; Anthropic's recommended partner) or "openai".
    # Dimension depends on provider/model; changing either requires `ingest.py --reset`.
    embedding_provider: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_PROVIDER", "voyage").lower()
    )
    voyage_api_key: str = field(default_factory=lambda: os.getenv("VOYAGE_API_KEY", ""))
    embedding_model: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL")
        or (
            "text-embedding-3-small"
            if os.getenv("EMBEDDING_PROVIDER", "voyage").lower() == "openai"
            else "voyage-3.5-lite"
        )
    )
    embedding_dim: int = field(
        default_factory=lambda: int(
            os.getenv("EMBEDDING_DIM")
            or (1536 if os.getenv("EMBEDDING_PROVIDER", "voyage").lower() == "openai" else 1024)
        )
    )

    # Vector store (Supabase Postgres + pgvector)
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    pgvector_collection: str = field(
        default_factory=lambda: os.getenv("PGVECTOR_COLLECTION", "portfolio")
    )

    # Optional integrations (Phase 2 tools)
    github_token: str = field(default_factory=lambda: os.getenv("GITHUB_TOKEN", ""))
    github_username: str = field(
        default_factory=lambda: os.getenv("GITHUB_USERNAME", "Sanket0412")
    )

    # Abuse protection (Phase 5). A limit <= 0 disables that window.
    rate_limit_per_minute: int = field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_MINUTE", "8"))
    )
    rate_limit_per_day: int = field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_DAY", "150"))
    )
    # Optional shared secret the BFF sends in X-Internal-Key; empty disables the check.
    internal_api_key: str = field(default_factory=lambda: os.getenv("INTERNAL_API_KEY", ""))

    # FastAPI
    cors_origins: list[str] = field(
        default_factory=lambda: _split_csv(os.getenv("CORS_ORIGINS", "*"))
    )

    def require(self, *keys: str) -> None:
        """Raise a clear error if any required setting is empty."""
        missing = [k for k in keys if not getattr(self, k, "")]
        if missing:
            raise RuntimeError(
                "Missing required configuration: "
                + ", ".join(missing)
                + f". Set them in {API_ROOT / '.env'} or the process environment."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
