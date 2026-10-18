"""Embeddings factory (Voyage AI by default, OpenAI optional).

Anthropic has no embeddings API; Voyage is its recommended partner. The pgvector
dimension is fixed by the provider/model, so changing either requires re-ingesting
(``python api/scripts/ingest.py --reset``).
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from langchain_core.embeddings import Embeddings

from portfolio_api.config import get_settings

_VOYAGE_BATCH = 64


class VoyageEmbeddings(Embeddings):
    """Thin LangChain adapter over the ``voyageai`` client.

    Uses ``input_type`` ``document`` for ingestion and ``query`` for searches, which
    Voyage's retrieval models are trained for.
    """

    def __init__(self, api_key: str, model: str, dimension: int) -> None:
        import voyageai

        self._client = voyageai.Client(api_key=api_key)
        self._model = model
        self._dim = dimension

    def _embed(self, texts: List[str], input_type: str) -> List[List[float]]:
        out: List[List[float]] = []
        for i in range(0, len(texts), _VOYAGE_BATCH):
            res = self._client.embed(
                texts[i : i + _VOYAGE_BATCH],
                model=self._model,
                input_type=input_type,
                output_dimension=self._dim,
            )
            out.extend(res.embeddings)
        return out

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts, "document")

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text], "query")[0]


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    settings = get_settings()
    if settings.embedding_provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        settings.require("openai_api_key")
        return OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)
    if settings.embedding_provider == "voyage":
        settings.require("voyage_api_key")
        return VoyageEmbeddings(
            settings.voyage_api_key, settings.embedding_model, settings.embedding_dim
        )
    raise ValueError(
        f"Unknown EMBEDDING_PROVIDER: {settings.embedding_provider!r}. Expected 'voyage' or 'openai'."
    )
