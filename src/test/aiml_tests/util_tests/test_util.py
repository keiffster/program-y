import unittest
import os

from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class UtiltyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(UtiltyTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class UtiltyAIMLTests(unittest.TestCase):

    def setUp(self):
        UtiltyAIMLTests.test_client = UtiltyTestClient()

    def test_util_function(self):
        response = UtiltyAIMLTests.test_client.bot.ask_question("test", "KEITH IS A PROGRAMMER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Ok, I will remember KEITH is a PROGRAMMER .')
