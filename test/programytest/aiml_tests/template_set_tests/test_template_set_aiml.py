import unittest
import os

from programytest.client import TestClient


class TempleTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TempleTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class TemplateSetAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TempleTestClient()
        self._client_context = client.create_client_context("testid")

    def test_name_set_topic(self):
        response = self._client_context.bot.ask_question(self._client_context,  "NAME SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK test1.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("var1"), "test1")

    def test_multi_word_name_set_topic(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MULTI WORD NAME SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK test1 test2.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("var1 var2"), "test1 test2")

    def test_var_set_topic(self):
        response = self._client_context.bot.ask_question(self._client_context,  "VAR SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK test2.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("var2"), "test2")

    def test_multi_word_var_set_topic(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MULTI WORD VAR SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK test2 test3.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("var2 var3"), "test2 test3")

    def test_topic_set(self):
        response = self._client_context.bot.ask_question(self._client_context, "TOPIC SET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK topic1.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("topic"), "topic1")

        response = self._client_context.bot.ask_question(self._client_context, "TOPIC UNSET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("topic"), "*")

    def test_multi_word_topic_set(self):
        response = self._client_context.bot.ask_question(self._client_context, "SET MULTI WORD TOPIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK topic2 topic3.")
        self.assertEqual(self._client_context.bot.get_conversation(self._client_context).property("topic"), "topic2 topic3")

    def test_var_transience(self):
        response = self._client_context.bot.ask_question(self._client_context, "VAR TEST STEP1")
        self.assertIsNotNone(response)
        self.assertEqual(response, "STEP1 Val1.")
        response = self._client_context.bot.ask_question(self._client_context, "VAR TEST STEP2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "STEP2 unknown.")
