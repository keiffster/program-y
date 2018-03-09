import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class OrderingTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(OrderingTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class OrderingAIMLTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(OrderingTestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain
        self._client_context.brain.sets._sets["COLOR"] = {"RED": [["RED"]]}
        self._client_context.brain.sets._sets["ANIMAL"] = {"DOLPHIN": [["DOLPHIN"]]}

    def test_basic_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS BLUE")
        self.assertEqual(response, "i didn't recognize BLUE AS A COLOR.")

    def test_basic_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "Red IS A NICE COLOR.")

    def test_basic_exact_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "Green IS MY FAVORITE COLOR TOO!")

    def test_hash_v_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS A DOLPHIN")
        self.assertEqual(response, "HASH SELECTED")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE ANIMAL IS AN AARDVARK")
        self.assertEqual(response, "SELECTED ONCE")
