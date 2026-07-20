"""Template 2: Motor / Interaction Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class MotorInteractionAgent(Agent):
    """Execute actions and handle user-facing interaction (Jarvis-style).

    Inputs: decision agent output, user messages
    Outputs: natural language responses, system actions, UI events
    Key params: response_tone, action_permissions
    """

    role = "motor_interaction"

    def __init__(
        self,
        name: str | None = None,
        response_tone: str = "neutral",
        action_permissions: tuple[str, ...] = (),
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            response_tone=response_tone,
            action_permissions=action_permissions,
            **params,
        )

    def process(self, decision: Any) -> dict[str, Any]:
        """Turn a chosen action into a user-facing response and/or system action."""
        action = decision.get("action") if isinstance(decision, dict) else decision
        permitted = action in self.params["action_permissions"] if self.params["action_permissions"] else True
        return {
            "tone": self.params["response_tone"],
            "action": action,
            "permitted": permitted,
            "response": None,
        }
