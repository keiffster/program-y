import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration
import logging

class SraiSetTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraiSetTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class SraiAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SraiAIMLTests.test_client = SraiSetTestClient()

    def test_srai__set_response(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "TEST SRAI SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'BLANK RESPONSE')
