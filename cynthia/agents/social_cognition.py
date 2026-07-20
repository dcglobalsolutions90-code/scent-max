"""Template 7: Social Cognition Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class SocialCognitionAgent(Agent):
    """Track relationships, read context, predict behavior.

    Inputs: interaction history, user profile data
    Outputs: relationship map, predicted response
    Key params: social_graph_depth
    """

    role = "social_cognition"

    def __init__(
        self,
        name: str | None = None,
        social_graph_depth: int = 1,
        **params: Any,
    ) -> None:
        super().__init__(name, social_graph_depth=social_graph_depth, **params)
        self._relationships: dict[str, dict[str, Any]] = {}

    def observe(self, user_id: str, interaction: Any) -> None:
        """Fold a new interaction into the relationship map for ``user_id``."""
        profile = self._relationships.setdefault(user_id, {"history": []})
        profile["history"].append(interaction)

    def process(self, user_id: str) -> dict[str, Any]:
        """Return the tracked relationship map / predicted response for ``user_id``."""
        profile = self._relationships.get(user_id, {"history": []})
        depth = self.params["social_graph_depth"]
        return {
            "user_id": user_id,
            "recent_history": profile["history"][-depth:],
            "predicted_response": None,
        }
