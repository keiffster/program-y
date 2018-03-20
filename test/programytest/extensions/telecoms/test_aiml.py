import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class TelecomsMinutesTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(TelecomsMinutesTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class TelecomsMinutesAIMLTests(unittest.TestCase):

    def setUp (self):
        client = TelecomsMinutesTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_balance(self):
        response = self._client_context.bot.ask_question(self._client_context, "HOW MANY MINUTES DO I HAVE LEFT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'This month you have 0 minutes available and have consumed 0 minutes.')

