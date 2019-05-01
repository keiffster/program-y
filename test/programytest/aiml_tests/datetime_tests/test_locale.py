import unittest
import os

from programy.utils.text.dateformat import DateFormatter

from programytest.client import TestClient

class LocaleAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(LocaleAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "locale.aiml")


class LocaleAIMLTests(unittest.TestCase):

    DEFAULT_DATETIME_REGEX = "^.*.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def setUp(self):
        client = LocaleAIMLTestClient()
        self._client_context = client.create_client_context("testid")
        self.date = DateFormatter()

    def test_locale(self):
        response = self._client_context.bot.ask_question(self._client_context, "TESTDATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, "Nous sommes le \d*\s*\d*")
