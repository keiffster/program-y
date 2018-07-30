import unittest
import os

from programytest.client import TestClient


class TimeoutTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TimeoutTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class TimeoutAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TimeoutTestClient()
        self._client_context = client.create_client_context("testid")

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
