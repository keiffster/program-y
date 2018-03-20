import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class GimisaTopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(GimisaTopicTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._file = os.path.dirname(__file__) + os.sep + "gimisa_test.aiml"
        self.configuration.client_configuration.configurations[0].configurations[0].files.set_files._files = [os.path.dirname(__file__)]
        self.configuration.client_configuration.configurations[0].configurations[0].files.set_files._extension = ".txt"

class GimisaAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GimisaTopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_blender_twice(self):
        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'some definition of render as per professor ....')

        response = self._client_context.bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'hi .. setting topic to blender....')

        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'the definition of render in blender is')

