import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class YesNoTopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(YesNoTopicTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._file = os.path.dirname(__file__) + os.sep + "yesno_test.aiml"
        self.configuration.client_configuration.configurations[0].configurations[0].files.set_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files.set_files._extension = ".txt"


class YesNoAIMLTests(unittest.TestCase):

    def setUp(self):
        client = YesNoTopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_yes_no(self):
        response = self._client_context.bot.ask_question(self._client_context, "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes')

        response = self._client_context.bot.ask_question(self._client_context, "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No')

        response = self._client_context.bot.ask_question(self._client_context, "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = self._client_context.bot.ask_question(self._client_context, "yes thanks")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thats great')

        response = self._client_context.bot.ask_question(self._client_context, "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = self._client_context.bot.ask_question(self._client_context, "no not really")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Oh dear')

        response = self._client_context.bot.ask_question(self._client_context, "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes')

        response = self._client_context.bot.ask_question(self._client_context, "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No')

