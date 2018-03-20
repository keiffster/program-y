import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class MultiplesTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(MultiplesTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class MultiplesAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MultiplesTestClient()
        self._client_context = client.create_client_context("testid")

    def test_multiple_questionsn(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO. HOW ARE YOU")
        self.assertIsNotNone(response)
        self.assertEqual("HI THERE. I AM WELL THANKS", response)
