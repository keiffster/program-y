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


class GetAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(GetAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class GetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GetAIMLTestClient()
        self._client_context = client.create_client_context("testid")
        self._client_context.brain.properties.load_from_text("""
             default-get:unknown
         """)
        self._client_context.bot.brain.dynamics.add_dynamic_var('gettime', "programy.dynamic.variables.datetime.GetTime", None)
        self._client_context.bot.brain.dynamics.add_dynamic_var('spelling', "programy.dynamic.variables.system.spelling.Spelling", None)
        self._client_context.bot.brain.dynamics.add_dynamic_var('splitter', "programy.dynamic.variables.system.splitter.SentenceSplitter", None)

        spelling_config = BotSpellingConfiguration()
        spelling_config._classname = "programytest.spelling.test_base.MockSpellingChecker"
        self._client_context.bot._spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, None)

        config = BotSentenceSplitterConfiguration()
        self._client_context.bot._sentence_splitter = SentenceSplitter.initiate_sentence_splitter(config)


    def test_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context,  "UNKNOWN GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    #################################################################################################################
    #

    def test_name_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_name_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Test1.")

    def test_name_get_with_topic(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET WITH TOPIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Test2.")

    def test_name_get_with_topic(self):
        response = self._client_context.bot.ask_question(self._client_context, "NAME GET AFTER TOPIC UNSET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "VAR1 is test3 AND NOW VAR1 is test4 AND FINALLY NOW VAR 1 is test4.")

    #################################################################################################################
    #

    def test_var_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "VAR GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Vtest1.")

    def test_var_unknown_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "VAR UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

