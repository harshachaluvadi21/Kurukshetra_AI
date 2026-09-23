"""
Rate limiting module for Kurukshetra.AI using slowapi.
Protects authentication, AI execution, reports, and public APIs.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from app.core.settings import settings
from app.core.security_logging import log_security_event

def get_identifier(request: Request) -> str:
    """
    Derives identity for rate limiting:
    If Authorization header is present, extracts token hash / prefix.
    Otherwise uses client remote IP.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        # Use last 16 chars of token as unique user bucket identifier
        return f"user:{token[-16:]}"
    return get_remote_address(request) or "127.0.0.1"

# Initialize slowapi limiter
limiter = Limiter(
    key_func=get_identifier,
    default_limits=[f"{settings.auth_rate_limit * 12}/minute"]
)

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Custom 429 handler returning clean JSON error with Retry-After header and security logging.
    """
    ip = get_remote_address(request) or "unknown"
    path = request.url.path
    
    log_security_event(
        event_type="RATE_LIMIT_EXCEEDED",
        ip=ip,
        details={"path": path, "limit": str(exc.detail)},
        severity="WARNING"
    )
    
    response = JSONResponse(
        status_code=429,
        content={
            "detail": f"Rate limit exceeded: {exc.detail}. Please slow down your requests."
        }
    )
    response.headers["Retry-After"] = "60"
    return response
