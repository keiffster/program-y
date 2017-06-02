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
        self.configuration.brain_configuration._gender = os.path.dirname(__file__)+"/gender.txt"

class GenderAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GenderAIMLTests.test_client = BasicTestClient()

    def test_gender(self):
        response = GenderAIMLTests.test_client.bot.ask_question("test",  "TEST GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This goes to her")
