"""Template 4: Emotional Regulation Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class EmotionalRegulationAgent(Agent):
    """Assign value (good/bad) to outcomes and experiences.

    Inputs: outcome events, explicit user feedback ("great job", "thank you")
    Outputs: reward/penalty signal
    Key params: reward_weighting, user_feedback_sensitivity
    """

    role = "emotional_regulation"

    POSITIVE_FEEDBACK = {"great job", "thank you", "well done", "nice work"}
    NEGATIVE_FEEDBACK = {"that's wrong", "bad job", "not helpful"}

    def __init__(
        self,
        name: str | None = None,
        reward_weighting: float = 1.0,
        user_feedback_sensitivity: float = 1.0,
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            reward_weighting=reward_weighting,
            user_feedback_sensitivity=user_feedback_sensitivity,
            **params,
        )

    def process(self, outcome: Any, user_feedback: str | None = None) -> float:
        """Combine an outcome event and optional user feedback into a signed reward signal."""
        signal = 0.0
        if isinstance(outcome, dict) and "success" in outcome:
            signal += 1.0 if outcome["success"] else -1.0

        if user_feedback:
            feedback = user_feedback.strip().lower()
            if feedback in self.POSITIVE_FEEDBACK:
                signal += self.params["user_feedback_sensitivity"]
            elif feedback in self.NEGATIVE_FEEDBACK:
                signal -= self.params["user_feedback_sensitivity"]

        return signal * self.params["reward_weighting"]
