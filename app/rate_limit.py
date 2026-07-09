from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    def __call__(self, request: Request) -> None:
        client_host = "unknown"

        if request.client is not None:
            client_host = request.client.host

        key = f"{request.url.path}:{client_host}"
        now = monotonic()
        window_start = now - self.window_seconds
        request_times = self._requests[key]

        while request_times and request_times[0] <= window_start:
            request_times.popleft()

        if len(request_times) >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )

        request_times.append(now)

    def reset(self) -> None:
        self._requests.clear()


login_rate_limiter = InMemoryRateLimiter(limit=5, window_seconds=60)
note_create_rate_limiter = InMemoryRateLimiter(limit=5, window_seconds=60)


def reset_rate_limits() -> None:
    login_rate_limiter.reset()
    note_create_rate_limiter.reset()
