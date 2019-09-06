import unittest
import os

from programytest.client import TestClient


class DynamicAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(DynamicAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class DynamicAIMLTests(unittest.TestCase):

    def setUp(self):
        client = DynamicAIMLTestClient()
        self._client_context = client.create_client_context("testid")
        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_var('gettime', "programy.dynamic.variables.datetime.GetTime", None)

    def test_dynamic_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "DYNAMIC GET")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("The time is "))
