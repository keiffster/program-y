import unittest
import os
from programytest.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = [os.path.dirname(__file__)]

class RequestAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        RequestAIMLTests.test_client = BasicTestClient()

    def test_request(self):
        Request = RequestAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(Request)
        self.assertEquals(Request, "Hi! It's delightful to see you.")

        Request = RequestAIMLTests.test_client.bot.ask_question("test", "WHAT DID I SAY")
        self.assertIsNotNone(Request)
        self.assertEquals(Request, "You said, HELLO")
