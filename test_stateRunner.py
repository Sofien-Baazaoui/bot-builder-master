from unittest import TestCase
from core.state_runner.state_runner import StateRunner


class TestStateRunner(TestCase):
    def test_get_state_graph(self):
        output = StateRunner().create_instance()
        expectedOutput = None

        self.assertIsNot(output, expectedOutput)
