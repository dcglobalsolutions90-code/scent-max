"""Template 3: Memory Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class MemoryAgent(Agent):
    """Store, organize, and retrieve information (short + long term).

    Inputs: learning agent output, context queries
    Outputs: retrieved facts/events, updated memory store
    Key params: retention_policy, indexing_method, recall_relevance_threshold
    """

    role = "memory"

    def __init__(
        self,
        name: str | None = None,
        retention_policy: str = "long_term",
        indexing_method: str = "keyword",
        recall_relevance_threshold: float = 0.3,
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            retention_policy=retention_policy,
            indexing_method=indexing_method,
            recall_relevance_threshold=recall_relevance_threshold,
            **params,
        )
        self._store: list[dict[str, Any]] = []

    def remember(self, item: Any) -> None:
        """Write a new fact/event to the store (called with learning agent output)."""
        self._store.append({"item": item})

    def process(self, query: Any) -> list[Any]:
        """Retrieve stored items relevant to ``query``."""
        if query is None:
            return [entry["item"] for entry in self._store]
        return [entry["item"] for entry in self._store if str(query) in str(entry["item"])]
