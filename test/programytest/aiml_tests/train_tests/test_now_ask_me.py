import unittest
import os

from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.client import TestClient


class NowAskMeTrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(NowAskMeTrainTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_sets_store([os.path.dirname(__file__) + os.sep + "sets"])


class TrainAIMLTests(unittest.TestCase):

    def setUp(self):
        client = NowAskMeTrainTestClient()
        self._client_context = client.create_client_context("testid")

    def test_now_ask_me(self):
        response = self._client_context.bot.ask_question(self._client_context, "daddy is great")
        self.assertIsNotNone(response)
        
        self.assertEqual('Now you can ask me: " Who is great ?" and " What does my daddy ?".', response)
