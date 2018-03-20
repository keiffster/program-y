import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class PatternBotTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(PatternBotTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]

class PatternBotAIMLTests(unittest.TestCase):

    def setUp(self):
        client = PatternBotTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.properties.pairs.append(("favouritecolor", "RED"))

    def test_pattern_bot_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "RED IS A NICE COLOR.")

    def test_pattern_bot_match_name_variant(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY OTHER FAVORITE COLOR USED TO BE RED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YES RED WAS A NICE COLOR.")
