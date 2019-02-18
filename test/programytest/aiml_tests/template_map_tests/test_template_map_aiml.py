import unittest
import os

from programytest.client import TestClient


class TemplateMapTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TemplateMapTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_maps_store([os.path.dirname(__file__)+ os.sep + "maps"])


class TemplateMapAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TemplateMapTestClient()
        self._client_context = client.create_client_context("testid")

    def test_name_map_topic(self):
        response =self._client_context.bot.ask_question(self._client_context,  "NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1.")

    def test_multi_word_name_map_topic(self):
        response =self._client_context.bot.ask_question(self._client_context,  "MULTI WORD NAME MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK VAL1.")
