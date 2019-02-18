import unittest
import os

from programytest.client import TestClient


class JlJobEvalTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(JlJobEvalTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__)+ os.sep + "jljob_eval.aiml")


class JlJobEvalAIMLTests(unittest.TestCase):

    def setUp(self):
        client = JlJobEvalTestClient()
        self._client_context = client.create_client_context("testid")

    def test_eval(self):
        response = self._client_context.bot.ask_question(self._client_context, "WHEN I SAY JUMP YOU SAY HOW HIGH")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Okay. When you say JUMP , I will say HOW HIGH.")

        response = self._client_context.bot.ask_question(self._client_context, "JUMP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HOW HIGH.")
