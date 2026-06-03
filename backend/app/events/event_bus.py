import asyncio
from typing import Callable, Dict, List
from .event_types import AppEvent, EventType

class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {
            event_type: [] for event_type in EventType
        }
        self._queue = asyncio.Queue()

    def subscribe(self, event_type: EventType, callback: Callable):
        self._subscribers[event_type].append(callback)

    async def publish(self, event: AppEvent):
        # We put it in the queue for async processing if needed, 
        # or we can directly notify subscribers here.
        for callback in self._subscribers.get(event.event_type, []):
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)

event_bus = EventBus()
