"""Base class shared by every agent type template."""

from __future__ import annotations

import itertools
from typing import Any


class Agent:
    """Base class for a single instance of an agent type template.

    Subclasses represent a *template* (e.g. ``SensoryAgent``); each
    instantiation is one runtime agent. Behavior lives in :meth:`process`,
    which subclasses override to implement their inputs -> outputs contract.
    """

    #: Short machine-readable name for the template, used as the default
    #: routing key on a :class:`cynthia.bus.MessageBus`.
    role: str = "agent"

    _id_counter = itertools.count(1)

    def __init__(self, name: str | None = None, **params: Any) -> None:
        self.id = f"{self.__class__.__name__.lower()}-{next(Agent._id_counter)}"
        self.name = name or self.id
        self.params: dict[str, Any] = params

    def process(self, *inputs: Any) -> Any:
        """Consume this agent's inputs and produce its output.

        Must be overridden by every template subclass.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement process()")

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"<{self.__class__.__name__} id={self.id!r} params={self.params!r}>"
