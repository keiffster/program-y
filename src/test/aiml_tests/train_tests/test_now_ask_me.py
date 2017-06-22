import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.file.factory import ConfigurationFactory
from programy.config.client.client import ClientConfiguration

class NowAskMeTrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        self.configuration = ClientConfiguration()
        ConfigurationFactory.load_configuration_from_file(self.configuration, os.path.dirname(__file__)+"/testconfig.yaml")

class TrainAIMLTests(unittest.TestCase):

    def setUp(cls):
        TrainAIMLTests.test_client = NowAskMeTrainTestClient()

    def test_now_ask_me(self):
        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "daddy is great")
        self.assertIsNotNone(response)
        self.assertEqual('Now you can ask me: "Who is GREAT?" and "What does my daddy be?"', response)
