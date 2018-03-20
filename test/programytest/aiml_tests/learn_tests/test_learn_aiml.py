import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class LearnTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class LearnAIMLTests(unittest.TestCase):

    def setUp(self):
        client = LearnTestClient()
        self._client_context = client.create_client_context("testid")

    def test_learn(self):
        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

    def test_learn_x_is_y(self):

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SUN IS HOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SUN is HOT")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE SKY IS BLUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE SKY is BLUE")

        response = self._client_context.bot.ask_question(self._client_context, "LEARN THE MOON IS GREY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember THE MOON is GREY")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE SUN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "HOT")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE SKY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BLUE")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS THE MOON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "GREY")
