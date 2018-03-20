import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class PriorityTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(PriorityTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class PriorityAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PriorityTestClient()
        self._client_context = client.create_client_context("testid")

    def test_priority_solo(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PRIORITY0")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY0 TEST SUCCESS')

    def test_priority_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PRIORITY1 TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY1 TEST SUCCESS')

    def test_priority_first_multi(self):
        response = self._client_context.bot.ask_question(self._client_context, "PRIORITY2 TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY2 TEST1 SUCCESS')

        response = self._client_context.bot.ask_question(self._client_context, "PRIORITY2 TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY2 TEST2 SUCCESS')

    def test_priority_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS IS PRIORITY3 TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY3 TEST SUCCESS')

    def test_priority_middle_multi(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS IS PRIORITY4 TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY4 TEST1 SUCCESS')

        response = self._client_context.bot.ask_question(self._client_context, "THIS IS PRIORITY4 TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY4 TEST2 SUCCESS')

    def test_priority_last(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS TEST IS PRIORITY5")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY5 TEST SUCCESS')

    def test_priority_last_multi(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS TEST1 IS PRIORITY6")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY6 TEST1 SUCCESS')

        response = self._client_context.bot.ask_question(self._client_context, "THIS TEST2 IS PRIORITY6")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY6 TEST2 SUCCESS')

    def test_priority_catch_all(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS IS NOY A TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'CATCH ALL TEST')

    def test_priority_not_a_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "THIS IS PRIORITY TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'NOT A PRIORITY TEST')

