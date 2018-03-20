import unittest
import os

from programy.context import ClientContext

from programy.config.file.factory import ConfigurationFactory
from programy.clients.events.console.config import ConsoleConfiguration

from programytest.aiml_tests.client import TestClient


class NowAskMeTrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        self._configuration = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(),
                                                                               os.path.dirname(__file__)+ os.sep + "testconfig.yaml",
                                                                               bot_root=os.path.dirname(__file__))

class TrainAIMLTests(unittest.TestCase):

    def setUp(self):
        client = NowAskMeTrainTestClient()
        self._client_context = client.create_client_context("testid")

    def test_now_ask_me(self):
        response = self._client_context.bot.ask_question(self._client_context, "daddy is great")
        self.assertIsNotNone(response)
        self.assertEqual('Now you can ask me: "Who is GREAT?" and "What does my daddy be?"', response)
