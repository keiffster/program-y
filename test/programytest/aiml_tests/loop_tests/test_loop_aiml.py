import unittest
import os

from programytest.client import TestClient


class ConditionalLoopAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ConditionalLoopAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ConditionLoopAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ConditionalLoopAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_condition_type2_loop(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 LOOP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Y Z.")

    def test_condition_type3_loop(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE3 LOOP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "B D.")
