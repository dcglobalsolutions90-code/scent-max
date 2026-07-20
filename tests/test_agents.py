import unittest

from cynthia.agents import (
    AttentionContextAgent,
    DecisionMakingAgent,
    EmotionalRegulationAgent,
    ExecutiveFunctionAgent,
    LanguageCommunicationAgent,
    MemoryAgent,
    MotorInteractionAgent,
    SensoryAgent,
    SocialCognitionAgent,
)


class TestSensoryAgent(unittest.TestCase):
    def test_process_labels_input(self) -> None:
        agent = SensoryAgent(input_source_type="file", recognition_confidence_threshold=0.7)
        out = agent.process({"event": "created"})
        self.assertEqual(out["source"], "file")
        self.assertEqual(out["confidence_threshold"], 0.7)


class TestMotorInteractionAgent(unittest.TestCase):
    def test_permitted_action_passes(self) -> None:
        agent = MotorInteractionAgent(action_permissions=("greet",))
        out = agent.process({"action": "greet"})
        self.assertTrue(out["permitted"])

    def test_unpermitted_action_blocked(self) -> None:
        agent = MotorInteractionAgent(action_permissions=("greet",))
        out = agent.process({"action": "delete_file"})
        self.assertFalse(out["permitted"])

    def test_no_permission_list_allows_everything(self) -> None:
        agent = MotorInteractionAgent()
        out = agent.process({"action": "anything"})
        self.assertTrue(out["permitted"])


class TestMemoryAgent(unittest.TestCase):
    def test_remember_and_recall_all(self) -> None:
        agent = MemoryAgent()
        agent.remember("user likes coffee")
        agent.remember("user dislikes tea")
        self.assertEqual(len(agent.process(None)), 2)

    def test_recall_filters_by_query(self) -> None:
        agent = MemoryAgent()
        agent.remember("user likes coffee")
        agent.remember("user dislikes tea")
        results = agent.process("coffee")
        self.assertEqual(results, ["user likes coffee"])


class TestEmotionalRegulationAgent(unittest.TestCase):
    def test_positive_feedback_increases_signal(self) -> None:
        agent = EmotionalRegulationAgent()
        signal = agent.process({"success": True}, user_feedback="great job")
        self.assertEqual(signal, 2.0)

    def test_negative_feedback_decreases_signal(self) -> None:
        agent = EmotionalRegulationAgent()
        signal = agent.process({"success": False}, user_feedback="bad job")
        self.assertEqual(signal, -2.0)

    def test_reward_weighting_scales_signal(self) -> None:
        agent = EmotionalRegulationAgent(reward_weighting=2.0)
        signal = agent.process({"success": True})
        self.assertEqual(signal, 2.0)


class TestDecisionMakingAgent(unittest.TestCase):
    def test_picks_highest_scoring_viable_option(self) -> None:
        agent = DecisionMakingAgent(risk_tolerance=0.5)
        options = [
            {"action": "safe", "score": 0.4, "risk": 0.1},
            {"action": "risky", "score": 0.9, "risk": 0.9},
        ]
        out = agent.process(options)
        self.assertEqual(out["action"], "safe")

    def test_no_viable_options_returns_none(self) -> None:
        agent = DecisionMakingAgent(risk_tolerance=0.1)
        options = [{"action": "risky", "score": 0.9, "risk": 0.9}]
        out = agent.process(options)
        self.assertIsNone(out["action"])
        self.assertEqual(out["confidence"], 0.0)


class TestLanguageCommunicationAgent(unittest.TestCase):
    def test_parses_intent_and_slots(self) -> None:
        agent = LanguageCommunicationAgent()
        out = agent.process("greet user_1")
        self.assertEqual(out["intent"], "greet")
        self.assertEqual(out["slots"], ["user_1"])

    def test_generate_applies_tone(self) -> None:
        agent = LanguageCommunicationAgent(tone="cheerful")
        self.assertEqual(agent.generate("hello"), "[cheerful] hello")


class TestSocialCognitionAgent(unittest.TestCase):
    def test_tracks_history_per_user(self) -> None:
        agent = SocialCognitionAgent(social_graph_depth=2)
        agent.observe("u1", "said hi")
        agent.observe("u1", "asked for help")
        agent.observe("u1", "said thanks")
        out = agent.process("u1")
        self.assertEqual(out["recent_history"], ["asked for help", "said thanks"])

    def test_unknown_user_has_empty_history(self) -> None:
        agent = SocialCognitionAgent()
        out = agent.process("unknown")
        self.assertEqual(out["recent_history"], [])


class TestExecutiveFunctionAgent(unittest.TestCase):
    def test_priority_rules_ordered_first(self) -> None:
        agent = ExecutiveFunctionAgent(priority_rules=("sensory", "memory"))
        outputs = {"language": "x", "memory": "y", "sensory": "z"}
        out = agent.process(outputs)
        self.assertEqual(out["schedule"], ["sensory", "memory", "language"])

    def test_oversight_scope_filters_roles(self) -> None:
        agent = ExecutiveFunctionAgent(oversight_scope=("sensory",))
        outputs = {"language": "x", "sensory": "z"}
        out = agent.process(outputs)
        self.assertEqual(out["schedule"], ["sensory"])


class TestAttentionContextAgent(unittest.TestCase):
    def test_filters_below_threshold(self) -> None:
        agent = AttentionContextAgent(relevance_threshold=0.5)
        signals = [{"relevance": 0.2}, {"relevance": 0.8}]
        out = agent.process(signals)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["relevance"], 0.8)

    def test_orders_by_relevance_and_urgency(self) -> None:
        agent = AttentionContextAgent(relevance_threshold=0.0, urgency_weighting=2.0)
        signals = [
            {"relevance": 0.5, "urgency": 0.0, "id": "a"},
            {"relevance": 0.1, "urgency": 0.5, "id": "b"},
        ]
        out = agent.process(signals)
        self.assertEqual([s["id"] for s in out], ["b", "a"])


if __name__ == "__main__":
    unittest.main()
