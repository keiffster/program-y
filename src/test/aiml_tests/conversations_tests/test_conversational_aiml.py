import unittest
import os

from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class ConversationalTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ConversationalTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class ConversationalAIMLTests(unittest.TestCase):

    def setUp(self):
        ConversationalAIMLTests.test_client = ConversationalTestClient()

    def test_basic_conversational(self):
        response = ConversationalAIMLTests.test_client.bot.ask_question("test",  "HELLO")
        self.assertEqual(response, 'HELLO, WORLD')

        response = ConversationalAIMLTests.test_client.bot.ask_question("test", "GOODBYE")
        self.assertEqual(response, 'SEE YA')

