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

class ConditionAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        ConditionAIMLTests.test_client = BasicTestClient()

    def test_condition_type1_variant1(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE1 VARIANT1")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant2(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE1 VARIANT2")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant3(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE1 VARIANT3")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant4(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE1 VARIANT4")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type1_variant1_no_match(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE1 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")

    def test_condition_type2_variant1(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE2 VARIANT1 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type2_variant1_default(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE2 VARIANT1 WITH DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "DEF")

    def test_condition_type2_variant1_no_match(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE2 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")

    def test_condition_type2_variant2(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE2 VARIANT2 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "Y")

    def test_condition_type3_variant1(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE3 VARIANT1 NO DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "A")

    def test_condition_type3_variant1_default(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE3 VARIANT1 WITH DEFAULT")
        self.assertIsNotNone(response)
        self.assertEquals(response, "DEF")

    def test_condition_type3_variant1_default(self):
        response = ConditionAIMLTests.test_client.bot.ask_question("test", "TYPE3 VARIANT1 NO MATCH")
        self.assertIsNotNone(response)
        self.assertEquals(response, "")