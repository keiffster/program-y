import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class UnderlineStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(UnderlineStarTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class UnderlineStarAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnderlineStarTestClient()
        self._client_context = client.create_client_context("testid")

    def test_underline_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS SAY')

    def test_underline_last(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS THERE')

    def test_underline_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "HI KEIFF MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UNDERLINE IS KEIFF')
