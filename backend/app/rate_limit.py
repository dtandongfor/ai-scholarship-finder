"""Small dependency-free rate limiter for public write endpoints.

Use a managed gateway or Redis-backed limiter before multi-instance production
deployment; this keeps the local/early-launch API from accepting rapid abuse.
"""

from collections import defaultdict, deque
from time import monotonic

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class WriteRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 30, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.method not in {"POST", "PUT", "DELETE"}:
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        key = f"{client}:{request.method}:{request.url.path.split('/', 3)[1:3]}"
        now = monotonic()
        timestamps = self.requests[key]
        while timestamps and timestamps[0] <= now - self.window_seconds:
            timestamps.popleft()
        if len(timestamps) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please wait a minute and try again."},
            )
        timestamps.append(now)
        return await call_next(request)
