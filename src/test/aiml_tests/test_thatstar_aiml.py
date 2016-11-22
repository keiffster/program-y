import unittest
import logging

from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class ThatStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatStarTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/thatstar", ".aiml", False)

class ThatStarAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ThatStarAIMLTests.test_client = ThatStarTestClient()

    def test_single_thatstar_word(self):

        response = ThatStarAIMLTests.test_client.bot.ask_question("test", "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO WITH THERE')

