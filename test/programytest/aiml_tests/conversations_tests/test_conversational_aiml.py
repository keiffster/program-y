import unittest
import os

from programytest.client import TestClient

class ConversationalTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ConversationalTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ConversationalAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ConversationalTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_conversational(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO")
        self.assertEqual(response, 'HELLO, WORLD.')

        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE")
        self.assertEqual(response, 'SEE YA.')

