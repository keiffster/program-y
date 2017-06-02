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

class GetAIMLTests(unittest.TestCase):

    def setUp(self):
        GetAIMLTests.test_client = BasicTestClient()
        GetAIMLTests.test_client.bot.brain.properties.load_from_text("""
             default-get:unknown
         """)

    def test_unknown_get(self):
        response = GetAIMLTests.test_client.bot.ask_question("test",  "UNKNOWN GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    #################################################################################################################
    #

    def test_name_unknown_get(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "NAME UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_name_get(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "NAME GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test1")

    def test_name_get_with_topic(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "NAME GET WITH TOPIC")
        self.assertIsNotNone(response)
        self.assertEqual(response, "test2")

    def test_name_get_with_topic(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "NAME GET AFTER TOPIC UNSET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "VAR1 is test3   AND NOW VAR1 is test4  AND FINALLY NOW VAR 1 is test4")

    #################################################################################################################
    #

    def test_var_get(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "VAR GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "vtest1")

    def test_var_unknown_get(self):
        response = GetAIMLTests.test_client.bot.ask_question("test", "VAR UNKNOWN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

