import unittest
import os

from programy.context import ClientContext
from programytest.aiml_tests.client import TestClient

class ConditionTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ConditionTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class ConditionAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ConditionTestClient()
        self._client_context = client.create_client_context("testid")

    def test_condition_type1_variant1(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE1 VARIANT1")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant2(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE1 VARIANT2")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant3(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE1 VARIANT3")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant4(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE1 VARIANT4")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant1_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE1 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")

    def test_condition_type2_variant1(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 VARIANT1 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type2_variant1_default(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 VARIANT1 WITH DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "DEF")

    def test_condition_type2_variant1_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")

    def test_condition_type2_variant2(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 VARIANT2 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type3_variant1(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE3 VARIANT1 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "A")

    def test_condition_type3_variant1_default(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE3 VARIANT1 WITH DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "DEF")

    def test_condition_type3_variant1_default(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE3 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")