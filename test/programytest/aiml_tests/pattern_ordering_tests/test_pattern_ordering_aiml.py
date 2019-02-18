import unittest
import os

from programytest.client import TestClient


class PatternOrderingTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(PatternOrderingTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class PatternOrderingAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternOrderingTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.sets._sets["COLOR"] = {"RED": [["RED"]]}
        self._client_context.brain.sets._sets["ANIMAL"] = {"DOLPHIN": [["DOLPHIN"]]}

    def test_basic_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS BLUE")
        self.assertEqual(response, "I didn't recognize BLUE AS A COLOR.")

    def test_basic_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "Red IS A NICE COLOR.")

    def test_basic_exact_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "Green IS MY FAVORITE COLOR TOO!")

    def test_hash_v_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS A DOLPHIN")
        self.assertEqual(response, "HASH SELECTED.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS AN AARDVARK")
        self.assertEqual(response, "SELECTED ONCE.")
