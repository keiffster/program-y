import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class TimeoutAIMLTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(BasicTestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_max_question_recursion_timeout(self):

        self._client_context.client.configuration.client_configuration.configurations[0]._max_question_recursion = 10
        self._client_context.client.configuration.client_configuration.configurations[0]._max_question_timeout = -1
        self._client_context.client.configuration.client_configuration.configurations[0]._max_search_depth = -1
        self._client_context.client.configuration.client_configuration.configurations[0]._max_search_timeout = -1

        response = self._client_context.bot.ask_question(self._client_context,  "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

    def test_max_question_timeout_timeout(self):

        self._client_context.client.configuration.client_configuration.configurations[0]._max_question_recursion = -1
        self._client_context.client.configuration.client_configuration.configurations[0]._max_question_timeout = 0.1
        self._client_context.client.configuration.client_configuration.configurations[0]._max_search_depth = -1
        self._client_context.client.configuration.client_configuration.configurations[0]._max_search_timeout = -1

        response = self._client_context.bot.ask_question(self._client_context,  "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')
