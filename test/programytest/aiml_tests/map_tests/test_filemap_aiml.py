import os
import unittest

from programytest.client import TestClient


class FileMapAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(FileMapAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_maps_store([os.path.dirname(__file__)])


class FileMapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = FileMapAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.load_from_text("""
             default_get:unknown
         """)

    def test_file_map(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I AM FROM THE UNITED KINGDOM")
        self.assertEqual(response, "Cool, have you been to the capital city London.")
