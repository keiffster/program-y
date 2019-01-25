import unittest
import os

from programytest.client import TestClient
from programy.spelling.base import SpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration
from programy.dialog.splitter.splitter import SentenceSplitter
from programy.config.bot.splitter import BotSentenceSplitterConfiguration


class MockSpellingChecker(SpellingChecker):

    def __init__(self, spelling_config=None):
        SpellingChecker.__init__(self, spelling_config)

    def correct(self, phrase):
        return "Hello World"


class SystemSetAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SystemSetAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SystemSetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SystemSetAIMLTestClient()
        self._client_context = client.create_client_context("testid")
        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_var('gettime', "programy.dynamic.variables.datetime.GetTime", None)
        self._client_context.bot.brain.dynamics.add_dynamic_var('spelling', "programy.dynamic.variables.system.spelling.Spelling", None)
        self._client_context.bot.brain.dynamics.add_dynamic_var('splitter', "programy.dynamic.variables.system.splitter.SentenceSplitter", None)

        config = BotSentenceSplitterConfiguration()
        self._client_context.bot._sentence_splitter = SentenceSplitter.initiate_sentence_splitter(config)

    def test_dynamic_splitter_on(self):
        response = self._client_context.bot.ask_question(self._client_context, "START USERNAME WITH SPLITTER ON")
        self.assertIsNotNone(response)
        self.assertEquals("What is your username?", response)

        response = self._client_context.bot.ask_question(self._client_context, "fred.smith")
        self.assertIsNotNone(response)
        self.assertEquals("Thanks, you entered fred. Thanks, you entered smith.", response)

    def test_dynamic_splitter_off(self):
        response = self._client_context.bot.ask_question(self._client_context, "START USERNAME WITH SPLITTER OFF")
        self.assertIsNotNone(response)
        self.assertEquals("What is your username?", response)

        response = self._client_context.bot.ask_question(self._client_context, "fred.smith")
        self.assertIsNotNone(response)
        self.assertEquals("Thanks, you entered fred.smith.", response)
