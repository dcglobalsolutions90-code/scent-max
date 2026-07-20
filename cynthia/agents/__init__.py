"""The 9 Cynthia AI agent type templates.

See docs/AGENT_ARCHITECTURE.md for the full spec each class implements.
"""

from cynthia.agents.attention_context import AttentionContextAgent
from cynthia.agents.decision_making import DecisionMakingAgent
from cynthia.agents.emotional_regulation import EmotionalRegulationAgent
from cynthia.agents.executive_function import ExecutiveFunctionAgent
from cynthia.agents.language import LanguageCommunicationAgent
from cynthia.agents.memory import MemoryAgent
from cynthia.agents.motor import MotorInteractionAgent
from cynthia.agents.sensory import SensoryAgent
from cynthia.agents.social_cognition import SocialCognitionAgent

__all__ = [
    "SensoryAgent",
    "MotorInteractionAgent",
    "MemoryAgent",
    "EmotionalRegulationAgent",
    "DecisionMakingAgent",
    "LanguageCommunicationAgent",
    "SocialCognitionAgent",
    "ExecutiveFunctionAgent",
    "AttentionContextAgent",
]
