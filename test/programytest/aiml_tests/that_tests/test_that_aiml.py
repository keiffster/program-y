import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class ThatTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ThatTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class ThatAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ThatTestClient()
        self._client_context = client.create_client_context("testid")

    def test_that_single_that_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

        response = self._client_context.bot.ask_question(self._client_context, "HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HELLO WITH THAT')

    def test_coffee_yes_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = self._client_context.bot.ask_question(self._client_context, "YES")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I DO TOO.')

    def test_coffee_no_question(self):
        response = self._client_context.bot.ask_question(self._client_context, "I LIKE COFFEE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DO YOU TAKE CREAM OR SUGAR IN YOUR COFFEE?')

        response = self._client_context.bot.ask_question(self._client_context, "NO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'REALLY? I HAVE A HARD TIME DRINKING BLACK COFFEE.')

    def test_that_case(self):
        response = self._client_context.bot.ask_question(self._client_context, "CASE HELLO1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HI THERE')

        response = self._client_context.bot.ask_question(self._client_context, "CASE HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HELLO RESPONSE')

        response = self._client_context.bot.ask_question(self._client_context, "CASE HELLO2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Case Hi There')

        response = self._client_context.bot.ask_question(self._client_context, "CASE HELLO AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CASE HELLO RESPONSE')

    def test_multiple_sentenes(self):
        response = self._client_context.bot.ask_question(self._client_context, "START")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'This is sentence 1. This is sentence two.')

        response = self._client_context.bot.ask_question(self._client_context, "CONTINUE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'TEST PASS')

    def test_wildcard_matching(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELCOME")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'aaa bbb ccc ddd')

        response = self._client_context.bot.ask_question(self._client_context, "AND AGAIN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'matched')

