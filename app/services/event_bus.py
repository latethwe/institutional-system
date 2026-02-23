from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventDispatcher:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[dict[str, Any]], None]]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[dict[str, Any]], None]) -> None:
        self._subscribers[event_name].append(handler)

    def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        for handler in self._subscribers[event_name]:
            handler(payload)
