from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.settings import settings
from app.api.websockets.manager import websocket_router
from app.api.routes import projects, runs, auth
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.db.database import engine
from sqlalchemy import text
import os
import logging

logger = logging.getLogger("kurukshetra.app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("\n" + "="*50)
        print("[SUCCESS] DATABASE CONNECTED SUCCESSFULLY!")
        print("="*50 + "\n")
    except Exception as e:
        print("\n" + "="*50)
        print(f"[ERROR] DATABASE CONNECTION FAILED: {e}")
        print("="*50 + "\n")
    yield
    await engine.dispose()

app = FastAPI(title="Kurukshetra AI Backend", version="1.0.0", lifespan=lifespan)

# Attach slowapi limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# Secure CORS configuration
raw_cors = settings.cors_origins or os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000",
)
cors_origins = [origin.strip() for origin in raw_cors.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app" if settings.environment != "test" else None,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
)

# Global Safe Exception Handler (Prevents stack-trace / credential leakage)
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact support if the problem persists."}
    )

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(runs.router, prefix="/api/v1/runs", tags=["Runs"])
app.include_router(websocket_router, prefix="/ws/v1", tags=["WebSockets"])

outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
os.makedirs(outputs_dir, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=outputs_dir, html=False), name="outputs")


@app.get("/")
async def root():
    return {
        "name": "Kurukshetra AI Backend",
        "status": "running",
        "health": "/health",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

