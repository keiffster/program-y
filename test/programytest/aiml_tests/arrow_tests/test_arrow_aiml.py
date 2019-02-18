import unittest
import os

from programytest.client import TestClient

class ArrowTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ArrowTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ArrowAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ArrowTestClient()
        self._client_context = client.create_client_context("testid")

    def test_arrow_first_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS SAY.')

    def test_arrow_first_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_first_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS WE SAY.')

    def test_arrow_first_multi_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "WE CHECKING MULTI WORD MATCH")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS NOW WE.')

    def test_arrow_last_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU.')

    def test_arrow_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_no_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU THERE.')

    def test_arrow_middle_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS HI.')

    def test_arrow_middle_no_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS.')

    def test_arrow_middle_multi_word(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS I WAS')

    def test_arrow_specific_case1(self):
        response = self._client_context.bot.ask_question(self._client_context, "aaa bbb ccc ddd")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'passed')
