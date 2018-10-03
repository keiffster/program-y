import unittest
import os

from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.client import TestClient


class TrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(TrainTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_sets_store([os.path.dirname(__file__) + os.sep + "sets"])


class TrainAIMLTests(unittest.TestCase):

    def setUp(self):
        client = TrainTestClient()
        self._client_context = client.create_client_context("testid")

    def test_train_noun(self):
        response = self._client_context.bot.ask_question(self._client_context, "jessica likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Do you smoke cigars too?", response)

        response = self._client_context.bot.ask_question(self._client_context, "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars.", response)

        response = self._client_context.bot.ask_question(self._client_context, "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars.", response)

        response = self._client_context.bot.ask_question(self._client_context, "what does jessica like")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars.", response)

        response = self._client_context.bot.ask_question(self._client_context, "what does jessica smoke")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars.", response)

        response = self._client_context.bot.ask_question(self._client_context, "who smokes")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars.", response)

    def test_train_pronoun(self):
        response = self._client_context.bot.ask_question(self._client_context, "mommy likes to smoke cigars")
        self.assertIsNotNone(response)

        self.assertEqual('Now you can ask me: " Who likes to smoke cigars ?" and " What does my mommy ?".', response)

        response = self._client_context.bot.ask_question(self._client_context, "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Your mommy.", response)

