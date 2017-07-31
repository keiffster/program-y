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
        self.configuration.brain_configuration.files._person2 = os.path.dirname(__file__)+ os.sep + "person2.txt"

class Person2AIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Person2AIMLTests.test_client = BasicTestClient()

    def test_person2(self):
        response = Person2AIMLTests.test_client.bot.ask_question("test",  "TEST PERSON2")
        self.assertIsNotNone(response)
        self.assertEqual(response, "he or she was going")
