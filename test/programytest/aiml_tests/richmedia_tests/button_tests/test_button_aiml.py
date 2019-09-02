import unittest
import os

from programytest.client import TestClient


class ButtonTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(ButtonTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class ButtonAIMLTests(unittest.TestCase):

    def setUp(self):
        client = ButtonTestClient()
        self._client_context = client.create_client_context("testid")

    def test_text_button(self):
        response = self._client_context.bot.ask_question(self._client_context, "URL BUTTON")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Click this <button><text>Servusai Website</text><url>https://www.servusai.com</url></button>.')

    def test_postback_button(self):
        response = self._client_context.bot.ask_question(self._client_context, "POSTBACK BUTTON")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<button><text>Say Hello</text><postback>HELLO</postback></button>.')

