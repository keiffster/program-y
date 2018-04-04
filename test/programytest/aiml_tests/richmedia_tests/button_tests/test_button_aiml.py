import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class ButtonTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(ButtonTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class ButtonAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ButtonTestClient()
        self._client_context = client.create_client_context("testid")

    def test_text_button(self):
        response = self._client_context.bot.ask_question(self._client_context, "URL BUTTON")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<button><text>Servusai Website</text><url>https://www.servusai.com</url></button>')

    def test_postback_button(self):
        response = self._client_context.bot.ask_question(self._client_context, "POSTBACK BUTTON")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<button><text>Say Hello</text><postback>HELLO</postback></button>')

