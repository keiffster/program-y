import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class GetAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(GetAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class GetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GetAIMLTestClient()
        self._client_context = client.create_client_context("testid")
        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_var('gettime', "programy.dynamic.variables.datetime.GetTime", None)

    def test_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context,  "UNKNOWN GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    #################################################################################################################
    #

    def test_name_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_name_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test1")

    def test_name_get_with_topic(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET WITH TOPIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test2")

    def test_name_get_with_topic(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET AFTER TOPIC UNSET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "VAR1 is test3 AND NOW VAR1 is test4 AND FINALLY NOW VAR 1 is test4")

    #################################################################################################################
    #

    def test_var_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "VAR GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "vtest1")

    def test_var_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "VAR UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    #################################################################################################################
    #

    def test_dynamic_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "DYNAMIC GET")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("The time is "))


