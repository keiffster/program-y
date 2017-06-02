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

class ArrowAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ArrowAIMLTests.test_client = BasicTestClient()

    def test_arrow_first_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test",  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS SAY')

    def test_arrow_first_no_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS')

    def test_arrow_first_multi_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "WE SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS WE SAY')

    def test_arrow_last_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "HELLO YOU")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU')

    def test_arrow_no_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS')

    def test_arrow_no_multi_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "HELLO YOU THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS YOU THERE')

    def test_arrow_middle_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS HI')

    def test_arrow_middle_no_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "WELL THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS')

    def test_arrow_middle_multi_word(self):
        response = ArrowAIMLTests.test_client.bot.ask_question("test", "WELL I WAS THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ARROW IS I WAS')
