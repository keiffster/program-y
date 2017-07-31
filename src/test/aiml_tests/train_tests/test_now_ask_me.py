import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.file.factory import ConfigurationFactory
from programy.config.programy import ProgramyConfiguration
from programy.config.sections.client.console import ConsoleConfiguration

class NowAskMeTrainTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        self.configuration = ConfigurationFactory.load_configuration_from_file(ConsoleConfiguration(),
                                                                               os.path.dirname(__file__)+ os.sep + "testconfig.yaml",
                                                                               bot_root=os.path.dirname(__file__))

class TrainAIMLTests(unittest.TestCase):

    def setUp(cls):
        TrainAIMLTests.test_client = NowAskMeTrainTestClient()

    def test_now_ask_me(self):
        TrainAIMLTests.test_client.bot.brain.dump_tree()
        response = TrainAIMLTests.test_client.bot.ask_question("test", "daddy is great")
        self.assertIsNotNone(response)
        self.assertEqual('Now you can ask me: "Who is GREAT?" and "What does my daddy be?"', response)
