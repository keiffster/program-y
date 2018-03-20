import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class HashAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(HashAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class HashAIMLTests(unittest.TestCase):

    def setUp(self):
        client = HashAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_hash_first_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS SAY')

    def test_hash_first_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_first_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS WE SAY')

    def test_hash_last_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU')

    def test_hash_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_no_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS YOU THERE')

    def test_hash_middle_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS HI')

    def test_hash_middle_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS')

    def test_hash_middle_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HASH IS I WAS')

    def test_hash_middle_and_end(self):
        response = self._client_context.bot.ask_question(self._client_context, "ARE YOU FUN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I AM FUNNY')

        response = self._client_context.bot.ask_question(self._client_context, "DO FUN YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'I AM FUNNY')
