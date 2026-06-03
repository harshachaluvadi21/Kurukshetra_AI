import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime

from app.graph.state import GraphState
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def validate_input(self, state: GraphState) -> bool:
        """Validates if the required state exists before execution."""
        pass

    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validates the generated output structure before returning."""
        pass

    async def emit_event(self, event_type: EventType, run_id: str, message: str, payload: dict = None):
        """Emits standard lifecycle events."""
        event = AppEvent(
            event_type=event_type,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={
                "agent_name": self.name,
                "message": message,
                "payload": payload or {}
            }
        )
        await event_bus.publish(event)

    async def invoke(self, state: GraphState) -> Dict[str, Any]:
        """Core execution loop with guaranteed events."""
        run_id = state.get("run_id", "unknown")
        
        await self.emit_event(EventType.AGENT_STARTED, run_id, f"{self.name} started.")
        
        if not self.validate_input(state):
            error_msg = f"{self.name} failed input validation."
            await self.emit_event(EventType.AGENT_COMPLETED, run_id, error_msg, {"status": "error"})
            return {"errors": [error_msg]}

        await self.emit_event(EventType.AGENT_THINKING, run_id, f"{self.name} is processing.")
        
        # Execute specific logic (implemented by child class)
        try:
            output = await self._execute(state)
        except Exception as e:
            error_msg = f"{self.name} execution error: {str(e)}"
            await self.emit_event(EventType.AGENT_COMPLETED, run_id, error_msg, {"status": "error"})
            return {"errors": [error_msg]}

        if not self.validate_output(output):
            error_msg = f"{self.name} failed output validation."
            await self.emit_event(EventType.AGENT_COMPLETED, run_id, error_msg, {"status": "error"})
            return {"errors": [error_msg]}

        await self.emit_event(EventType.AGENT_COMPLETED, run_id, f"{self.name} completed successfully.", {"status": "success"})
        
        # Append execution log to the state
        output["execution_logs"] = [f"{self.name} executed successfully."]
        return output

    @abstractmethod
    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        """Internal execution method. Must return a dict to merge into GraphState."""
        pass
