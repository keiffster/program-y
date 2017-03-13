import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)
        self.configuration.brain_configuration._normal = os.path.dirname(__file__)+"/normal.txt"

class NormalizeAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        NormalizeAIMLTests.test_client = BasicTestClient()

    def test_normalize(self):
        response = NormalizeAIMLTests.test_client.bot.ask_question("test",  "TEST NORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling dot com")
