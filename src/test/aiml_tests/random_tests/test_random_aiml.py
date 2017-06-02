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

class RandomAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RandomAIMLTests.test_client = BasicTestClient()

    def test_random(self):
        response = RandomAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertIn(response, ['HI', 'HELLO', 'HI THERE'])