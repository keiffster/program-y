import unittest
import os

from programytest.client import TestClient


"""
A set of scratch aiml_tests to provide a unit test framework for testing adhoc grammars
Nothing in here should ever be taken as meaningful aiml_tests, they come and go like the wind
( or my novel deadlines..... lol )
"""

class ScratchTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ScratchTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ScratchAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ScratchTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "ARE YOU FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RESULT 1.')

        response = self._client_context.bot.ask_question(self._client_context, "ARE YOU FRED WEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RESULT 2.')

        response = self._client_context.bot.ask_question(self._client_context, "ARE YOU WRITTEN IN C#")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RESULT 3.')

