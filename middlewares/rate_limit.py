from fastapi import Request, HTTPException
from collections import defaultdict
import time

request_history: dict = defaultdict(list)


class RateLimiter:
    # FIX: was _init_ (single underscore), __call__ was outside the class body
    def __init__(self, requests: int = 100, seconds: int = 60):
        self.requests = requests
        self.seconds = seconds

    async def __call__(self, request: Request):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        request_history[ip] = [
            t for t in request_history[ip] if now - t < self.seconds
        ]
        if len(request_history[ip]) >= self.requests:
            raise HTTPException(status_code=429, detail="Too many requests")
        request_history[ip].append(now)