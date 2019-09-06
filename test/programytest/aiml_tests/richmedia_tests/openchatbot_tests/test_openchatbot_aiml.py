import unittest
import os

from programytest.client import TestClient


class OpenChatBotTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(OpenChatBotTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class OpenChatBotAIMLTests(unittest.TestCase):

    def setUp(self):
        client = OpenChatBotTestClient()
        self._client_context = client.create_client_context("testid")

    def test_openchatbot(self):
        response = self._client_context.bot.ask_question(self._client_context, "OPENCHATBOT TEST")
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("<tts><type>plainText</type> Je vous envoie+ d&apos;information sur le Strandmon de chez Ikea</tts> <card><image>https://www.ikea.com/fr/fr/images/products/strandmon-fauteuil-enfant-gris__0574584_PE668407_S4.JPG</image>"))
