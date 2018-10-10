import unittest
import os

from programytest.client import TestClient


class UnicodeTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UnicodeTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class UnicodeAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnicodeTestClient()
        self._client_context = client.create_client_context("testid")

    def test_cantonese_unicode(self):
        response = self._client_context.bot.ask_question(self._client_context,  u'喂')
        self.assertIsNotNone(response)
        self.assertEqual(response, u'你好.')
