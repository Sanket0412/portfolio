"""HTTP-level checks for /chat that never reach the model (fast paths and 4xx)."""
import pytest
from fastapi.testclient import TestClient

from portfolio_api.api import chat as chat_mod
from portfolio_api.main import app
from portfolio_api.ratelimit import ChatRateLimiter


@pytest.fixture(autouse=True)
def _fresh_limiter(monkeypatch):
    monkeypatch.setattr(chat_mod, "_limiter", ChatRateLimiter(per_minute=3, per_day=0))


client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_greeting_fast_path_streams_final_and_done():
    r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 200
    assert "event: final" in r.text and "event: done" in r.text


def test_rate_limit_returns_429_with_retry_after():
    for _ in range(3):
        assert client.post("/chat", json={"message": "hi"}).status_code == 200
    r = client.post("/chat", json={"message": "hi"})
    assert r.status_code == 429
    assert int(r.headers["retry-after"]) >= 1


def test_rate_limit_is_per_forwarded_client():
    for _ in range(3):
        client.post("/chat", json={"message": "hi"}, headers={"X-Forwarded-For": "1.1.1.1"})
    r = client.post("/chat", json={"message": "hi"}, headers={"X-Forwarded-For": "2.2.2.2"})
    assert r.status_code == 200


def test_oversized_message_rejected():
    r = client.post("/chat", json={"message": "x" * (chat_mod.MAX_MESSAGE_CHARS + 1)})
    assert r.status_code == 422


def test_too_much_history_rejected():
    hist = [{"role": "user", "content": "q"}] * (chat_mod.MAX_HISTORY_MESSAGES + 1)
    r = client.post("/chat", json={"message": "hi", "history": hist})
    assert r.status_code == 422


def test_internal_key_enforced(monkeypatch):
    monkeypatch.setattr(chat_mod._settings.__class__, "internal_api_key", "s3cret", raising=False)
    object.__setattr__(chat_mod._settings, "internal_api_key", "s3cret")
    try:
        assert client.post("/chat", json={"message": "hi"}).status_code == 401
        ok = client.post("/chat", json={"message": "hi"}, headers={"X-Internal-Key": "s3cret"})
        assert ok.status_code == 200
    finally:
        object.__setattr__(chat_mod._settings, "internal_api_key", "")
