import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class UnicodeestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(UnicodeestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class UnicodeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnicodeestClient()
        self._client_context = client.create_client_context("testid")

    def test_cantonese_unicode(self):
        response = self._client_context.bot.ask_question(self._client_context,  u'喂')
        self.assertIsNotNone(response)
        self.assertEqual(response, u'你好')
