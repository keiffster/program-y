import unittest
import os

from programytest.client import TestClient


class RandomTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(RandomTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class RandomAIMLTests(unittest.TestCase):

    def setUp(self):
        client = RandomTestClient()
        self._client_context = client.create_client_context("testid")

    def test_random(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertIn(response, ['HI.', 'HELLO.', 'HI THERE.'])