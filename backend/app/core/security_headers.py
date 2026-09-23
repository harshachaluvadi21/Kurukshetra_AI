"""
Production security headers middleware for Kurukshetra.AI.
Enforces defense-in-depth HTTP response headers.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.settings import settings

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        
        # Prevent MIME-sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Clickjacking defense
        response.headers["X-Frame-Options"] = "DENY"
        
        # Referrer privacy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Hardware access restrictions
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Cross-Site Scripting filter for legacy browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # HSTS (Strict-Transport-Security) in production
        if settings.environment.lower() == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            
        return response
