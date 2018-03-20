import unittest
import os

from programy.context import ClientContext
from programy.extensions.newsapi.newsapi import NewsAPIExtension

from programytest.aiml_tests.client import TestClient


# TODO, modify this to return mocked json payload
class MockNewsApiExtension(NewsAPIExtension):

    def execute(self, context, data):
        return "THIS IS NEWS"


class NewsApiTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(NewsApiTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class NewsApiAIMLTests(unittest.TestCase):

    def setUp (self):
        client = NewsApiTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_newsapi(self):
        response = self._client_context.bot.ask_question(self._client_context, "ABC NEWS")
        self.assertIsNotNone(response)
        self.assertEqual(response, "THIS IS NEWS")
