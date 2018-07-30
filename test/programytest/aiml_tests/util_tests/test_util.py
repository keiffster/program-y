import unittest
import os

from programytest.client import TestClient


class UtiltyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UtiltyTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class UtiltyAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UtiltyTestClient()
        self._client_context = client.create_client_context("testid")

    def test_util_function(self):
        response = self._client_context.bot.ask_question(self._client_context, "KEITH IS A PROGRAMMER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Ok, I will remember KEITH is a PROGRAMMER .')
