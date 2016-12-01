import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class ThatTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/that", ".aiml", False)

class ThatAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ThatAIMLTests.test_client = ThatTestClient()

    def test_that_single_that_word(self):
        response = ThatAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO WITH THAT')

