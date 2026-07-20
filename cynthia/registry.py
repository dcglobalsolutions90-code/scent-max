"""Spawns and tracks N instances of an agent type template.

See the "Scaling note" in docs/AGENT_ARCHITECTURE.md: templates are
replicated at runtime rather than hand-written per instance.
"""

from __future__ import annotations

from typing import Any, TypeVar

from cynthia.base import Agent

AgentT = TypeVar("AgentT", bound=Agent)


class AgentRegistry:
    """Tracks live agent instances, grouped by template class."""

    def __init__(self) -> None:
        self._instances: dict[type[Agent], list[Agent]] = {}

    def spawn(self, agent_cls: type[AgentT], n: int = 1, **params: Any) -> list[AgentT]:
        """Instantiate ``n`` copies of ``agent_cls``, each parameterized with ``params``."""
        instances = [agent_cls(**params) for _ in range(n)]
        self._instances.setdefault(agent_cls, []).extend(instances)
        return instances

    def of_type(self, agent_cls: type[AgentT]) -> list[AgentT]:
        return list(self._instances.get(agent_cls, []))

    def all(self) -> list[Agent]:
        return [agent for group in self._instances.values() for agent in group]

    def count(self, agent_cls: type[Agent] | None = None) -> int:
        if agent_cls is not None:
            return len(self._instances.get(agent_cls, []))
        return sum(len(group) for group in self._instances.values())
