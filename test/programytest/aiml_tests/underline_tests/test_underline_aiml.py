import unittest
import os

from programytest.client import TestClient


class UnderlineTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UnderlineTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class UnderlineAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UnderlineTestClient()
        self._client_context = client.create_client_context("testid")

    def test_underline_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS SAY.')

    def test_underline_first_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "THE MAN SAYS HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS THE MAN SAYS.')

    def test_underline_last(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT.')

    def test_underline_last_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT MATE.')

    def test_multi_underline(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL AND THERE.')

    def test_multi_underline_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THEN HI THERE MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL THEN AND THERE MATE.')

    def test_underline_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF.')

    def test_underline_middle_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF MATE SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF MATE.')

    def test_underline_in_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "PLEASE DO _STOP_")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PLEASE DO.')
