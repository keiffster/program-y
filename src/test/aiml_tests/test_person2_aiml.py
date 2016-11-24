import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/person2", ".aiml", False)
        self.configuration.brain_configuration._person2 = "/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/bots/rosie/config/person2.txt"

class Person2AIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Person2AIMLTests.test_client = BasicTestClient()

    def test_person2(self):
        response = Person2AIMLTests.test_client.bot.ask_question("test",  "TEST PERSON2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "he or she was going")
