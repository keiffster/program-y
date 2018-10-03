import unittest
import os

from programytest.client import TestClient


class YesNoTopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(YesNoTopicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "yesno_test.aiml")


class YesNoAIMLTests(unittest.TestCase):

    def setUp(self):
        client = YesNoTopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_yes_no(self):
        response = self._client_context.bot.ask_question(self._client_context, "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes.')

        response = self._client_context.bot.ask_question(self._client_context, "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No.')

        response = self._client_context.bot.ask_question(self._client_context, "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = self._client_context.bot.ask_question(self._client_context, "yes thanks")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thats great.')

        response = self._client_context.bot.ask_question(self._client_context, "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = self._client_context.bot.ask_question(self._client_context, "no not really")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Oh dear.')

        response = self._client_context.bot.ask_question(self._client_context, "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes.')

        response = self._client_context.bot.ask_question(self._client_context, "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No.')

