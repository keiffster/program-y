import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class SraiSetTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraiSetTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class SraiAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraiSetTestClient()
        self._client_context = client.create_client_context("testid")

    def test_srai__set_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST SRAI SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'BLANK RESPONSE')
