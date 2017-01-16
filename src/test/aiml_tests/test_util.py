import unittest
import os

from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class UtiltiyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(UtiltiyTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/util", ".aiml", False)

class UtiltiyAIMLTests(unittest.TestCase):

    def setUp(self):
        UtiltiyAIMLTests.test_client = UtiltiyTestClient()

    def test_util_function(self):
        response = UtiltiyAIMLTests.test_client.bot.ask_question("test", "KEITH IS A PROGRAMMER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Ok, I will remember KEITH is a PROGRAMMER .')
