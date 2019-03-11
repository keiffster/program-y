import unittest
import os

from programytest.client import TestClient


class RegexTemplatesTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(RegexTemplatesTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_regex_templates_store(os.path.dirname(__file__) + os.sep + "regex-templates.txt")


class RegexTemplatesAIMLTests(unittest.TestCase):

    def setUp(self):
        client = RegexTemplatesTestClient()
        self._client_context = client.create_client_context("testid")

    def test_regex_template(self):
        response = self._client_context.bot.ask_question(self._client_context, "I AM 27 YEARS OLD")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Thats Great! You are 27.")