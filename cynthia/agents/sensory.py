"""Template 1: Sensory Agent."""

from __future__ import annotations

from typing import Any

from cynthia.base import Agent


class SensoryAgent(Agent):
    """Ingest and interpret raw input (camera/vision, file/touch).

    Inputs: image/video frames, file system events
    Outputs: labeled objects, scene descriptions, file interaction events
    Key params: input_source_type, recognition_confidence_threshold
    """

    role = "sensory"

    def __init__(
        self,
        name: str | None = None,
        input_source_type: str = "camera",
        recognition_confidence_threshold: float = 0.5,
        **params: Any,
    ) -> None:
        super().__init__(
            name,
            input_source_type=input_source_type,
            recognition_confidence_threshold=recognition_confidence_threshold,
            **params,
        )

    def process(self, raw_input: Any) -> dict[str, Any]:
        """Label ``raw_input`` (a frame or file event) into a scene description."""
        return {
            "source": self.params["input_source_type"],
            "confidence_threshold": self.params["recognition_confidence_threshold"],
            "labels": [],
            "raw_input": raw_input,
        }
