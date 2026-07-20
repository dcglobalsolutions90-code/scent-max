import unittest

from cynthia.agents import AttentionContextAgent, DecisionMakingAgent, MotorInteractionAgent, SensoryAgent
from cynthia.bus import MessageBus
from cynthia.registry import AgentRegistry


class TestPipeline(unittest.TestCase):
    """Wires several agent instances together over a MessageBus, end to end."""

    def test_sensory_to_motor_pipeline(self) -> None:
        registry = AgentRegistry()
        bus = MessageBus()

        (sensory,) = registry.spawn(SensoryAgent, n=1)
        (attention,) = registry.spawn(AttentionContextAgent, n=1, relevance_threshold=0.0)
        (decision,) = registry.spawn(DecisionMakingAgent, n=1, risk_tolerance=1.0)
        (motor,) = registry.spawn(MotorInteractionAgent, n=1)

        responses = []

        bus.subscribe("sensory", lambda frame: bus.publish(
            "attention_context", [{"relevance": 0.9, "urgency": 0.1, "label": sensory.process(frame)}]
        ))
        bus.subscribe("attention_context", lambda signals: bus.publish(
            "decision_making",
            [{"action": s["label"], "score": s["relevance"], "risk": 0.0} for s in attention.process(signals)],
        ))
        bus.subscribe("decision_making", lambda options: bus.publish(
            "motor_interaction", decision.process(options)
        ))
        bus.subscribe("motor_interaction", lambda decision_out: responses.append(motor.process(decision_out)))

        bus.publish("sensory", {"frame": "raw-image-bytes"})

        self.assertEqual(len(responses), 1)
        self.assertTrue(responses[0]["permitted"])
        self.assertIsNotNone(responses[0]["action"])

    def test_registry_scales_templates_independently(self) -> None:
        registry = AgentRegistry()
        registry.spawn(SensoryAgent, n=10)
        registry.spawn(MotorInteractionAgent, n=2)
        self.assertEqual(registry.count(SensoryAgent), 10)
        self.assertEqual(registry.count(MotorInteractionAgent), 2)
        self.assertEqual(registry.count(), 12)


if __name__ == "__main__":
    unittest.main()
