import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class NormalizeTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(NormalizeTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files._normal = os.path.dirname(__file__)+ os.sep + "normal.txt"


class NormalizeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = NormalizeTestClient()
        self._client_context = client.create_client_context("testid")

    def test_normalize(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST NORMALIZE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling dot com")

    def test_normalize_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "NORMALIZE test.org", srai=True)
        self.assertIsNotNone(response)
        self.assertEqual(response, "test dot org")
