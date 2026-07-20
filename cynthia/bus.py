"""In-memory publish/subscribe bus used to wire agent instances together."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

Handler = Callable[[Any], None]


class MessageBus:
    """Routes messages between agents by role.

    Agents don't need direct references to each other: a producer
    ``publish``-es on its role, and any interested consumer
    ``subscribe``-s to that role.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, role: str, handler: Handler) -> None:
        self._subscribers[role].append(handler)

    def publish(self, role: str, message: Any) -> None:
        for handler in self._subscribers[role]:
            handler(message)
