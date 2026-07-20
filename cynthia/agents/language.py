"""Template 6: Language & Communication Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class LanguageCommunicationAgent(Agent):
    """Parse input language, generate expressive output.

    Inputs: raw text/speech
    Outputs: structured intent, generated language
    Key params: language_model_config, tone
    """

    role = "language"

    def __init__(
        self,
        name: str | None = None,
        language_model_config: dict[str, Any] | None = None,
        tone: str = "neutral",
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            language_model_config=language_model_config or {},
            tone=tone,
            **params,
        )

    def process(self, raw_text: str) -> dict[str, Any]:
        """Parse ``raw_text`` into a structured intent."""
        tokens = raw_text.strip().split()
        return {
            "intent": tokens[0].lower() if tokens else None,
            "slots": tokens[1:],
            "tone": self.params["tone"],
        }

    def generate(self, content: Any) -> str:
        """Render ``content`` back out as natural language in the configured tone."""
        return f"[{self.params['tone']}] {content}"
