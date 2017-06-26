import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))
        self.configuration.brain_configuration._normal = os.path.dirname(__file__)+"/normal.txt"

class NormalizeAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        NormalizeAIMLTests.test_client = BasicTestClient()

    def test_normalize(self):
        response = NormalizeAIMLTests.test_client.bot.ask_question("test",  "TEST NORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling dot com")

    def test_normalize_star(self):
        response = NormalizeAIMLTests.test_client.bot.ask_question("test",  "NORMALIZE test.org", srai=True)
        self.assertIsNotNone(response)
        self.assertEqual(response, "test dot org")
