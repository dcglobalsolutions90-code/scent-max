"""Template 5: Decision-Making Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class DecisionMakingAgent(Agent):
    """Evaluate options against goals and select actions.

    Inputs: memory, context, reward signals
    Outputs: chosen action, confidence score
    Key params: goal_set, risk_tolerance
    """

    role = "decision_making"

    def __init__(
        self,
        name: str | None = None,
        goal_set: tuple[str, ...] = (),
        risk_tolerance: float = 0.5,
        **params: Any,
    ) -> None:
        super().__init__(name, goal_set=goal_set, risk_tolerance=risk_tolerance, **params)

    def process(self, options: list[dict[str, Any]]) -> dict[str, Any]:
        """Pick the option with the highest (goal-weighted) score.

        Each option is a dict like ``{"action": ..., "score": ..., "risk": ...}``.
        Options riskier than ``risk_tolerance`` are excluded before scoring.
        """
        viable = [o for o in options if o.get("risk", 0.0) <= self.params["risk_tolerance"]]
        if not viable:
            return {"action": None, "confidence": 0.0}

        best = max(viable, key=lambda o: o.get("score", 0.0))
        total = sum(max(o.get("score", 0.0), 0.0) for o in viable) or 1.0
        confidence = max(best.get("score", 0.0), 0.0) / total
        return {"action": best["action"], "confidence": confidence}
