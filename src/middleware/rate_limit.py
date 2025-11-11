"""Rate limiting middleware for EMIS."""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import asyncio

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from src.lib.logging import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using sliding window algorithm."""

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage: {identifier: [(timestamp, count)]}
        self.request_history: Dict[str, list[Tuple[datetime, int]]] = defaultdict(list)
        self._cleanup_task = None

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Get identifier (IP or user ID)
        identifier = self._get_identifier(request)
        
        # Check rate limit
        if not await self._check_rate_limit(identifier):
            logger.warning(f"Rate limit exceeded for {identifier}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Record request
        await self._record_request(identifier)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        minute_count, hour_count = await self._get_request_counts(identifier)
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Minute"] = str(max(0, self.requests_per_minute - minute_count))
        response.headers["X-RateLimit-Remaining-Hour"] = str(max(0, self.requests_per_hour - hour_count))
        
        return response

    def _get_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting."""
        # Try to get user ID from request state
        if hasattr(request.state, "user") and request.state.user:
            return f"user:{request.state.user.id}"
        
        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"
        
        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    async def _check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limits."""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        # Get request history
        history = self.request_history.get(identifier, [])
        
        # Count requests in last minute and hour
        minute_count = sum(count for timestamp, count in history if timestamp > minute_ago)
        hour_count = sum(count for timestamp, count in history if timestamp > hour_ago)
        
        # Check limits
        return minute_count < self.requests_per_minute and hour_count < self.requests_per_hour

    async def _record_request(self, identifier: str):
        """Record a request."""
        now = datetime.utcnow()
        self.request_history[identifier].append((now, 1))
        
        # Cleanup old entries
        hour_ago = now - timedelta(hours=1)
        self.request_history[identifier] = [
            (timestamp, count)
            for timestamp, count in self.request_history[identifier]
            if timestamp > hour_ago
        ]

    async def _get_request_counts(self, identifier: str) -> Tuple[int, int]:
        """Get request counts for last minute and hour."""
        now = datetime.utcnow()
        minute_ago = now - timedelta(minutes=1)
        hour_ago = now - timedelta(hours=1)
        
        history = self.request_history.get(identifier, [])
        
        minute_count = sum(count for timestamp, count in history if timestamp > minute_ago)
        hour_count = sum(count for timestamp, count in history if timestamp > hour_ago)
        
        return minute_count, hour_count

    async def cleanup_old_entries(self):
        """Periodically cleanup old entries."""
        while True:
            await asyncio.sleep(3600)  # Run every hour
            
            now = datetime.utcnow()
            hour_ago = now - timedelta(hours=1)
            
            for identifier in list(self.request_history.keys()):
                self.request_history[identifier] = [
                    (timestamp, count)
                    for timestamp, count in self.request_history[identifier]
                    if timestamp > hour_ago
                ]
                
                # Remove empty entries
                if not self.request_history[identifier]:
                    del self.request_history[identifier]
            
            logger.info(f"Cleaned up rate limit history. Active identifiers: {len(self.request_history)}")
