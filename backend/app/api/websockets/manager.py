import asyncio
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from typing import Dict, Set, Optional
from jose import JWTError
from sqlalchemy.future import select

from app.events.event_types import AppEvent, EventType
from app.events.event_bus import event_bus
from app.core.auth import decode_access_token
from app.core.security_logging import log_security_event
from app.db.database import AsyncSessionLocal
from app.db.models import Run

websocket_router = APIRouter()

MAX_CONNECTIONS_PER_RUN = 10
MAX_INCOMING_MESSAGE_BYTES = 4096

class ConnectionManager:
    def __init__(self):
        # Maps run_id to a set of active websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, run_id: str) -> bool:
        if run_id in self.active_connections and len(self.active_connections[run_id]) >= MAX_CONNECTIONS_PER_RUN:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Connection limit exceeded")
            return False
            
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = set()
        self.active_connections[run_id].add(websocket)
        return True

    def disconnect(self, websocket: WebSocket, run_id: str):
        if run_id in self.active_connections:
            self.active_connections[run_id].discard(websocket)
            if not self.active_connections[run_id]:
                del self.active_connections[run_id]

    async def broadcast_to_run(self, run_id: str, message: dict):
        if run_id in self.active_connections:
            for connection in list(self.active_connections[run_id]):
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
async def websocket_endpoint(
    websocket: WebSocket,
    run_id: str,
    token: Optional[str] = Query(None),
):
    ip = websocket.client.host if websocket.client else "unknown"

    # 1. Validate run_id UUID format
    try:
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid run_id format")
        return

    # 2. Authenticate token and verify run ownership
    authenticated_user_id = None
    if token:
        try:
            payload = decode_access_token(token)
            authenticated_user_id = payload.get("sub")
        except JWTError:
            log_security_event(
                event_type="WS_UNAUTHORIZED_CONNECT",
                ip=ip,
                details={"run_id": run_id, "reason": "Invalid or expired JWT token"},
                severity="WARNING"
            )
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
            return

    # Verify run exists and belongs to the authenticated user if the run is claimed
    async with AsyncSessionLocal() as session:
        query = select(Run).where(Run.id == run_uuid)
        result = await session.execute(query)
        run = result.scalar_one_or_none()

    if not run:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Run not found")
        return

    if run.user_id:
        if not authenticated_user_id or str(run.user_id) != str(authenticated_user_id):
            log_security_event(
                event_type="AUTHZ_VIOLATION",
                ip=ip,
                user_id=authenticated_user_id,
                details={"action": "websocket_subscribe_blocked", "run_id": run_id, "owner_id": str(run.user_id)},
                severity="WARNING"
            )
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Access denied: unauthorized run")
            return

    connected = await manager.connect(websocket, run_id)
    if not connected:
        return

    try:
        while True:
            # Enforce maximum incoming text payload length to prevent DoS
            data = await websocket.receive_text()
            if len(data) > MAX_INCOMING_MESSAGE_BYTES:
                await websocket.close(code=status.WS_1009_MESSAGE_TOO_BIG, reason="Message too large")
                break
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        manager.disconnect(websocket, run_id)

