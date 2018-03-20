import unittest
import os

from programy.context import ClientContext
from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.aiml_tests.client import TestClient


class TrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        self._configuration = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(),
                                                                               os.path.dirname(__file__)+ os.sep + "testconfig.yaml",
                                                                               bot_root=os.path.dirname(__file__))

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
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = self._client_context.bot.ask_question(self._client_context, "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = self._client_context.bot.ask_question(self._client_context, "what does jessica like")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = self._client_context.bot.ask_question(self._client_context, "what does jessica smoke")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

        response = self._client_context.bot.ask_question(self._client_context, "who smokes")
        self.assertIsNotNone(response)
        self.assertEqual("Jessica likes to smoke cigars", response)

    def test_train_pronoun(self):
        response = self._client_context.bot.ask_question(self._client_context, "mommy likes to smoke cigars")
        self.assertIsNotNone(response)

        self.assertEqual('Now you can ask me: "Who likes TO SMOKE CIGARS?" and "What does my mommy like?"', response)

        response = self._client_context.bot.ask_question(self._client_context, "who likes to smoke cigars")
        self.assertIsNotNone(response)
        self.assertEqual("Your mommy", response)

