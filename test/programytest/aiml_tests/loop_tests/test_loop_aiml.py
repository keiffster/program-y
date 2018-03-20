import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class ConditionalLoopAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ConditionalLoopAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class ConditionLoopAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ConditionalLoopAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_condition_type2_loop(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE2 LOOP")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y Z")

    def test_condition_type3_loop(self):
        response = self._client_context.bot.ask_question(self._client_context, "TYPE3 LOOP")
        self.assertIsNotNone(response)
        self.assertEquals(response, "B D")
