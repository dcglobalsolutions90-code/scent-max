import unittest

from cynthia.agents import SensoryAgent, MemoryAgent
from cynthia.registry import AgentRegistry


class TestAgentRegistry(unittest.TestCase):
    def test_spawn_creates_n_instances(self) -> None:
        registry = AgentRegistry()
        instances = registry.spawn(SensoryAgent, n=5, input_source_type="camera")
        self.assertEqual(len(instances), 5)
        self.assertEqual(registry.count(SensoryAgent), 5)
        self.assertTrue(all(isinstance(i, SensoryAgent) for i in instances))

    def test_spawn_applies_params_per_instance(self) -> None:
        registry = AgentRegistry()
        instances = registry.spawn(SensoryAgent, n=3, recognition_confidence_threshold=0.9)
        self.assertTrue(all(i.params["recognition_confidence_threshold"] == 0.9 for i in instances))

    def test_of_type_isolated_per_class(self) -> None:
        registry = AgentRegistry()
        registry.spawn(SensoryAgent, n=2)
        registry.spawn(MemoryAgent, n=3)
        self.assertEqual(len(registry.of_type(SensoryAgent)), 2)
        self.assertEqual(len(registry.of_type(MemoryAgent)), 3)
        self.assertEqual(registry.count(), 5)

    def test_all_returns_every_instance(self) -> None:
        registry = AgentRegistry()
        registry.spawn(SensoryAgent, n=2)
        registry.spawn(MemoryAgent, n=1)
        self.assertEqual(len(registry.all()), 3)


if __name__ == "__main__":
    unittest.main()
