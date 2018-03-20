import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class TopicStarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicStarTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class TopicStarAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TopicStarTestClient()
        self._client_context = client.create_client_context("testid")

    def test_single_topicstar_word(self):

        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO STAR TOPIC')

