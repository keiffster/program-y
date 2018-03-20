import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class TemplateMapTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TemplateMapTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files.map_files._files=[os.path.dirname(__file__)+ os.sep + "maps"]
        self.configuration.client_configuration.configurations[0].configurations[0].files.map_files._extension=".txt"


class TemplateMapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TemplateMapTestClient()
        self._client_context = client.create_client_context("testid")

    def test_name_map_topic(self):
        response =self._client_context.bot.ask_question(self._client_context,  "NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")

    def test_multi_word_name_map_topic(self):
        response =self._client_context.bot.ask_question(self._client_context,  "MULTI WORD NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1")
