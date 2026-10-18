"""Server-side rate limiting for ``/chat`` (Phase 5).

A small in-process sliding-window limiter keyed by client id (IP). It is deliberately
dependency-free: the API runs as a single process on Railway, so per-process state is
sufficient. If the API is ever scaled horizontally, swap :class:`SlidingWindowLimiter`
for a shared store (Upstash/Redis) behind the same ``check`` interface.
"""
from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Optional


@dataclass(frozen=True)
class LimitResult:
    allowed: bool
    retry_after: int = 0  # seconds until a request would be allowed again


class SlidingWindowLimiter:
    """Allow at most ``limit`` hits per ``window`` seconds per key."""

    def __init__(
        self, limit: int, window: float, clock: Callable[[], float] = time.monotonic
    ) -> None:
        self.limit = limit
        self.window = window
        self._clock = clock
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> LimitResult:
        now = self._clock()
        cutoff = now - self.window
        with self._lock:
            hits = self._hits[key]
            while hits and hits[0] <= cutoff:
                hits.popleft()
            if len(hits) >= self.limit:
                retry = int(hits[0] + self.window - now) + 1
                return LimitResult(False, max(retry, 1))
            hits.append(now)
            if len(self._hits) > 10_000:  # bound memory under key churn
                self._evict(cutoff)
            return LimitResult(True)

    def _evict(self, cutoff: float) -> None:
        for k in [k for k, h in self._hits.items() if not h or h[-1] <= cutoff]:
            del self._hits[k]


class ChatRateLimiter:
    """Burst (per-minute) plus daily cap. ``limit <= 0`` disables a window."""

    def __init__(
        self,
        per_minute: int,
        per_day: int,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._windows = []
        if per_minute > 0:
            self._windows.append(SlidingWindowLimiter(per_minute, 60.0, clock))
        if per_day > 0:
            self._windows.append(SlidingWindowLimiter(per_day, 86_400.0, clock))

    def check(self, key: str) -> LimitResult:
        worst: Optional[LimitResult] = None
        for w in self._windows:
            res = w.check(key)
            if not res.allowed and (worst is None or res.retry_after > worst.retry_after):
                worst = res
        return worst or LimitResult(True)
