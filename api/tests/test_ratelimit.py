from portfolio_api.ratelimit import ChatRateLimiter, SlidingWindowLimiter


class Clock:
    def __init__(self) -> None:
        self.t = 1000.0

    def __call__(self) -> float:
        return self.t


def test_allows_up_to_limit_then_blocks():
    clock = Clock()
    lim = SlidingWindowLimiter(3, 60, clock)
    assert all(lim.check("a").allowed for _ in range(3))
    res = lim.check("a")
    assert not res.allowed and res.retry_after >= 1


def test_window_slides():
    clock = Clock()
    lim = SlidingWindowLimiter(1, 60, clock)
    assert lim.check("a").allowed
    assert not lim.check("a").allowed
    clock.t += 61
    assert lim.check("a").allowed


def test_keys_are_independent():
    lim = SlidingWindowLimiter(1, 60, Clock())
    assert lim.check("a").allowed
    assert lim.check("b").allowed


def test_chat_limiter_burst_and_disabled_windows():
    clock = Clock()
    lim = ChatRateLimiter(per_minute=2, per_day=0, clock=clock)
    assert lim.check("a").allowed and lim.check("a").allowed
    assert not lim.check("a").allowed
    off = ChatRateLimiter(per_minute=0, per_day=0)
    assert all(off.check("a").allowed for _ in range(100))
