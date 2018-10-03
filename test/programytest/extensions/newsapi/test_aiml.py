import unittest
import os

from programy.extensions.newsapi.newsapi import NewsAPIExtension

from programytest.client import TestClient


class MockNewsApiExtension(NewsAPIExtension):

    def execute(self, context, data):
        return "THIS IS NEWS"


class NewsApiTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(NewsApiTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class NewsApiAIMLTests(unittest.TestCase):

    def setUp (self):
        client = NewsApiTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_newsapi(self):
        response = self._client_context.bot.ask_question(self._client_context, "ABC NEWS")
        self.assertIsNotNone(response)
        self.assertEqual(response, "THIS IS NEWS.")
