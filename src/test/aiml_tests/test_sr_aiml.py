import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class SrTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SrTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/sr", ".aiml", False)

class SrAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SrAIMLTests.test_client = SrTestClient()

    def test_sr_response(self):
        response = SrAIMLTests.test_client.bot.ask_question("test", "WELL HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

    def test_sr_response_no_star(self):
        response = SrAIMLTests.test_client.bot.ask_question("test", "WELL HOWDY")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

    def test_sr_response_two_star(self):
        response = SrAIMLTests.test_client.bot.ask_question("test", "HI FRIEND HOW ARE YOU TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HEY FRIEND')
