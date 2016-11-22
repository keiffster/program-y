import unittest
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration
import logging

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/aiml_tests/test_files/person", ".aiml", False)
        self.configuration.brain_configuration._person = "/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/bots/keiff/config/person.txt"


class PersonAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PersonAIMLTests.test_client = BasicTestClient()

    def test_person(self):
        response = PersonAIMLTests.test_client.bot.ask_question("test",  "TEST PERSON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is your2 cat")
