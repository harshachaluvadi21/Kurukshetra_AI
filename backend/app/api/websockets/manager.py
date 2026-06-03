import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from app.events.event_types import AppEvent, EventType
from app.events.event_bus import event_bus

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Maps run_id to a set of active websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = set()
        self.active_connections[run_id].add(websocket)

    def disconnect(self, websocket: WebSocket, run_id: str):
        if run_id in self.active_connections:
            self.active_connections[run_id].discard(websocket)
            if not self.active_connections[run_id]:
                del self.active_connections[run_id]

    async def broadcast_to_run(self, run_id: str, message: dict):
        if run_id in self.active_connections:
            for connection in self.active_connections[run_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

manager = ConnectionManager()

# Subscribe the WebSocket manager to all event types on the Event Bus
async def websocket_event_subscriber(event: AppEvent):
    await manager.broadcast_to_run(event.run_id, event.model_dump(mode="json"))

for ev_type in EventType:
    event_bus.subscribe(ev_type, websocket_event_subscriber)

@websocket_router.websocket("/runs/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await manager.connect(websocket, run_id)
    try:
        while True:
            # We don't expect client to send messages, but keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, run_id)
