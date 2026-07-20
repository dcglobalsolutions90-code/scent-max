import unittest

from cynthia.base import Agent


class TestAgentBase(unittest.TestCase):
    def test_process_not_implemented(self) -> None:
        agent = Agent()
        with self.assertRaises(NotImplementedError):
            agent.process()

    def test_ids_are_unique(self) -> None:
        a1, a2 = Agent(), Agent()
        self.assertNotEqual(a1.id, a2.id)

    def test_name_defaults_to_id(self) -> None:
        agent = Agent()
        self.assertEqual(agent.name, agent.id)

    def test_params_stored(self) -> None:
        agent = Agent(threshold=0.9)
        self.assertEqual(agent.params, {"threshold": 0.9})


if __name__ == "__main__":
    unittest.main()
