import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class UtiltyTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(UtiltyTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class UtiltyAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UtiltyTestClient()
        self._client_context = client.create_client_context("testid")

    def test_util_function(self):
        response = self._client_context.bot.ask_question(self._client_context, "KEITH IS A PROGRAMMER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Ok, I will remember KEITH is a PROGRAMMER .')
