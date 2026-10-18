import sys
import types

from portfolio_api.llm.embeddings import VoyageEmbeddings


class _FakeClient:
    calls: list = []

    def __init__(self, api_key):
        pass

    def embed(self, texts, model, input_type, output_dimension):
        _FakeClient.calls.append((len(texts), model, input_type, output_dimension))
        return types.SimpleNamespace(embeddings=[[0.0] * output_dimension for _ in texts])


def test_voyage_adapter_batches_and_sets_input_type(monkeypatch):
    monkeypatch.setitem(sys.modules, "voyageai", types.SimpleNamespace(Client=_FakeClient, error=types.SimpleNamespace(RateLimitError=RuntimeError)))
    _FakeClient.calls = []
    emb = VoyageEmbeddings("k", "voyage-4-lite", 8)
    docs = emb.embed_documents(["t"] * 130)
    assert len(docs) == 130 and len(docs[0]) == 8
    assert [c[0] for c in _FakeClient.calls] == [64, 64, 2]
    assert all(c[2] == "document" for c in _FakeClient.calls)
    q = emb.embed_query("hello")
    assert len(q) == 8 and _FakeClient.calls[-1][2] == "query"
