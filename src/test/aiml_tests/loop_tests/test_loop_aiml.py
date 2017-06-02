import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class ConditionLoopAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ConditionLoopAIMLTests.test_client = BasicTestClient()

    def test_condition_type2_loop(self):
        response = ConditionLoopAIMLTests.test_client.bot.ask_question("test", "TYPE2 LOOP")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y Z")

    def test_condition_type3_loop(self):
        response = ConditionLoopAIMLTests.test_client.bot.ask_question("test", "TYPE3 LOOP")
        self.assertIsNotNone(response)
        self.assertEquals(response, "B D")
