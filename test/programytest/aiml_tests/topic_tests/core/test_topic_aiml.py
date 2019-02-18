import unittest
import os

from programytest.client import TestClient


class TopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TopicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class TopicAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_topic_single_topic_word(self):

        response = self._client_context.bot.ask_question(self._client_context, "HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'OUTSIDE OF TEST1TOPIC.')

        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'INSIDE OF TEST1TOPIC.')

    def test_topic_multiple_topic_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'OUTSIDE OF TEST2 TOPIC.')

        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'INSIDE OF TEST2 TOPIC.')

    def test_topic_wildcard_topic_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "WILDCARD1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WILDCARD1 TEST OK.')

        response = self._client_context.bot.ask_question(self._client_context, "WILDCARD2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WILDCARD2 TEST OK.')
