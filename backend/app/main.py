from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.websockets.manager import websocket_router
from app.api.routes import projects, runs, auth
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.db.database import engine
from sqlalchemy import text
import os

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

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(runs.router, prefix="/api/v1/runs", tags=["Runs"])
app.include_router(websocket_router, prefix="/ws/v1", tags=["WebSockets"])

outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
os.makedirs(outputs_dir, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=outputs_dir), name="outputs")


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
