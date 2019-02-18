import unittest
import os

from programytest.client import TestClient


class SraiSetTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SraiSetTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SraiAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraiSetTestClient()
        self._client_context = client.create_client_context("testid")

    def test_srai__set_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST SRAI SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'BLANK RESPONSE.')
