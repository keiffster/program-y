import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)
        self.configuration.brain_configuration.files._person = os.path.dirname(__file__)+ os.sep + "person.txt"

class PersonAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PersonAIMLTests.test_client = BasicTestClient()

    def test_person(self):
        response = PersonAIMLTests.test_client.bot.ask_question("test",  "TEST PERSON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "This is your2 cat")
