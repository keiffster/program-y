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

class ResponseAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ResponseAIMLTests.test_client = BasicTestClient()

    def test_Response(self):
        response = ResponseAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Hi! It's delightful to see you.")

        response = ResponseAIMLTests.test_client.bot.ask_question("test", "CAN YOU REPEAT THAT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "I said, Hi! It's delightful to see you.")
