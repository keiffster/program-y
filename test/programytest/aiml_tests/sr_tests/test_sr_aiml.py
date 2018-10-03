import unittest
import os

from programytest.client import TestClient


class SrTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SrTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SrAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SrTestClient()
        self._client_context = client.create_client_context("testid")

    def test_sr_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

    def test_sr_response_no_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HOWDY")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

    def test_sr_response_two_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "HI FRIEND HOW ARE YOU TODAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HEY FRIEND.')
