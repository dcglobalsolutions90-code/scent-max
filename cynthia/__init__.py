"""Cynthia AI agent architecture.

A small set of agent *type templates* (see docs/AGENT_ARCHITECTURE.md),
each instantiated as many times as a use case requires via
:class:`cynthia.registry.AgentRegistry`, and wired together with
:class:`cynthia.bus.MessageBus`.
"""

from cynthia.base import Agent
from cynthia.bus import MessageBus
from cynthia.registry import AgentRegistry

__all__ = ["Agent", "MessageBus", "AgentRegistry"]
