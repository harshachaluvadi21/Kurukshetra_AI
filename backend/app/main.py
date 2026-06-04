from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.websockets.manager import websocket_router
from app.api.routes import projects, runs, auth
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Kurukshetra AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"],
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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
