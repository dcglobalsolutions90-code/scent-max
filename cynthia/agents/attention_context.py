"""Template 9: Attention / Context Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class AttentionContextAgent(Agent):
    """Filter relevance, track cause-effect, maintain situational awareness.

    Inputs: all incoming signals
    Outputs: filtered/prioritized signal stream
    Key params: relevance_threshold, urgency_weighting
    """

    role = "attention_context"

    def __init__(
        self,
        name: str | None = None,
        relevance_threshold: float = 0.4,
        urgency_weighting: float = 1.0,
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            relevance_threshold=relevance_threshold,
            urgency_weighting=urgency_weighting,
            **params,
        )

    def process(self, signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter and rank ``signals`` (each carrying ``relevance``/``urgency``).

        Signals below ``relevance_threshold`` are dropped; the remainder are
        sorted by ``relevance + urgency_weighting * urgency`` descending.
        """
        threshold = self.params["relevance_threshold"]
        weighting = self.params["urgency_weighting"]

        kept = [s for s in signals if s.get("relevance", 0.0) >= threshold]
        kept.sort(key=lambda s: s.get("relevance", 0.0) + weighting * s.get("urgency", 0.0), reverse=True)
        return kept
